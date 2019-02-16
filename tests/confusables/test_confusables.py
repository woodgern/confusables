import unittest
import datetime
from unittest.mock import Mock
import re

from confusables import is_confusable, confusable_characters, confusable_regex

class TestConfusables(unittest.TestCase):

    def test_is_confusable__unicode_mapping_only(self):
        self.assertTrue(is_confusable('rover', 'Ʀỏ𝕍3ℛ'))

    def test_confusable_characters__is_two_way(self):
        for u in [chr(i) for i in range(65536)]:
            mapped_chars = confusable_characters(u)
            if mapped_chars:
                for mapped_char in mapped_chars:
                    self.assertTrue(u in confusable_characters(mapped_char))

    def test_confusable_regex__basic_ascii_regex(self):
        regex = confusable_regex('bore', include_character_padding=True)
        reg = re.compile(regex)
        print(reg.search('Sometimes people say that life can be a ь.𝞂.ř.ɜ, but I don\'t agree'))
        self.assertTrue(reg.search('Sometimes people say that life can be a ь.𝞂.ř.ɜ, but I don\'t agree'))
        self.assertFalse(reg.search('Hopefully you don\'t get bored easily'))
