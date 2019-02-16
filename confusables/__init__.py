import json
import re
import os
from .config import CONFUSABLE_MAPPING_PATH


# read confusable mappings from file, build 2-way map of the pairs
with open(os.path.join(os.path.dirname(__file__), CONFUSABLE_MAPPING_PATH), "r") as mappings:
    CONFUSABLE_MAP = json.loads(mappings.readline())


def is_confusable(str1, str2):
    while str1 + str2:
        if bool(str1) != bool(str2):
            return False

        if str1[0] == str2[0]:
            str1 = str1[1:]
            str2 = str2[1:]
        elif str2[0] in CONFUSABLE_MAP.get(str1[0]):
            str1 = str1[1:]
            str2 = str2[1:]
        else:
            next = False
            for index in range(1, len(str1) + 1):
                if str1[:index] == CONFUSABLE_MAP.get(str2[0]):
                    str1 = str1[index:]
                    str2 = str2[1:]
                    next = True
                    break
            if next:
                continue

            for index in range(1, len(str2) + 1):
                if str2[:index] == CONFUSABLE_MAP.get(str1[0]):
                    str2 = str2[index:]
                    str1 = str1[1:]
                    next = True
                    break
            if next:
                continue
            return False
    return True

def confusable_characters(char):
    return CONFUSABLE_MAP.get(char)

def confusable_regex(string, include_character_padding=False):
    space_regex = "[\*|_|~|`|-|\.]*" if include_character_padding else ''
    regex = "\\b" + space_regex
    for char in string:
        regex += "[" + "|".join(CONFUSABLE_MAP[char]) + "|" + char + "]" + space_regex
    regex += "\\b"

    return regex
