import json
from unicodedata import normalize
import string
import os
from config import CUSTOM_CONFUSABLE_PATH, CONFUSABLES_PATH, CONFUSABLE_MAPPING_PATH

def _asciify(char):
    return normalize('NFD',char).encode('ascii', 'ignore').decode('ascii')

def _get_accented_characters(char):
    return [u for u in (chr(i) for i in range(65536)) if u != char and _asciify(u) == char]

def _get_confusable_chars(character, unicode_confusable_map, remaining_chars):
    mapped_chars = unicode_confusable_map[character]
    remaining_chars.remove(character)

    group = [character]
    for mapped_char in mapped_chars:
        if mapped_char in remaining_chars:
            group.extend(_get_confusable_chars(mapped_char, unicode_confusable_map, remaining_chars))
    return group

def parse_new_mapping_file():
    unicode_confusable_map = {}

    with open(os.path.join(os.path.dirname(__file__), CONFUSABLES_PATH), "r") as unicode_mappings:
        with open(os.path.join(os.path.dirname(__file__), CUSTOM_CONFUSABLE_PATH), "r") as custom_mappings:
            mappings = unicode_mappings.readlines()
            mappings.extend(custom_mappings)

            for mapping_line in mappings:
                if not mapping_line.strip():
                    continue

                mapping = mapping_line.split(";")[:2]
                str1 = chr(int(mapping[0].strip(), 16))
                mapping[1] = mapping[1].strip().split(" ")
                mapping[1] = [chr(int(x, 16)) for x in mapping[1]]
                str2 = "".join(mapping[1])

                if unicode_confusable_map.get(str1):
                    unicode_confusable_map[str1].append(str2)
                else:
                    unicode_confusable_map[str1] = [str2]

                if unicode_confusable_map.get(str2):
                    unicode_confusable_map[str2].append(str1)
                else:
                    unicode_confusable_map[str2] = [str1]

                if len(str1) == 1:
                    case_change = str1.lower() if str1.isupper() else str1.upper()
                    if case_change != str1:
                        unicode_confusable_map[str1].append(case_change)

                if len(str2) == 1:
                    case_change = str2.lower() if str2.isupper() else str2.upper()
                    if case_change != str2:
                        unicode_confusable_map[str2].append(case_change)

    for char in string.ascii_lowercase:
        accented = _get_accented_characters(char)
        unicode_confusable_map[char].extend(accented)
        for accent in accented:
            unicode_confusable_map[accent] = char

    for char in string.ascii_uppercase:
        accented = _get_accented_characters(char)
        unicode_confusable_map[char].extend(accented)
        for accent in accented:
            unicode_confusable_map[accent] = char

    CONFUSABLE_MAP = {}
    characters_to_map = list(unicode_confusable_map.keys())
    while 0 != len(characters_to_map):
        character = characters_to_map[0]
        char_group = _get_confusable_chars(character, unicode_confusable_map, characters_to_map)

        for i in range(len(char_group)):
            CONFUSABLE_MAP[char_group[i]] = char_group[:i] + char_group[i+1:]

    mapping_file = open(os.path.join(os.path.dirname(__file__), CONFUSABLE_MAPPING_PATH), "w")
    mapping_file.write(json.dumps(CONFUSABLE_MAP))
    mapping_file.close()

parse_new_mapping_file()