import unittest
import datetime
from unittest.mock import Mock
import re

from confusables import is_confusable, confusable_characters, confusable_regex, normalize

class TestConfusables(unittest.TestCase):

    def test_is_confusable__unicode_mapping_only(self):
        self.assertTrue(is_confusable('rover', 'Ʀỏ𝕍3ℛ'))

    def test_is_confusable__multi_character_mapping(self):
        self.assertTrue(is_confusable('Ʀỏ𝕍3ℛ', 'ro\'ver'))
        self.assertTrue(is_confusable('ro\'ver', 'Ʀỏ𝕍3ℛ'))

    def test_is_confusable__not_remotely_similar_words(self):
        self.assertFalse(is_confusable('Ʀỏ𝕍3ℛ', 'salmon'))
        self.assertFalse(is_confusable('salmon', 'Ʀỏ𝕍3ℛ'))

    def test_is_confusable__prefix_does_not_give_false_positive(self):
        self.assertFalse(is_confusable('Ʀỏ𝕍3ℛ', 'rover is my favourite dog'))
        self.assertFalse(is_confusable('rover is my favourite dog', 'Ʀỏ𝕍3ℛ'))

    def test_is_confusable__None_input(self):
        self.assertTrue(is_confusable(None, None))
        self.assertFalse(is_confusable('rover is my favourite dog', None))
        self.assertFalse(is_confusable(None, 'rover is my favourite dog'))

    def test_is_confusable__empty_input(self):
        self.assertTrue(is_confusable('', ''))
        self.assertFalse(is_confusable('rover is my favourite dog', ''))
        self.assertFalse(is_confusable('', 'rover is my favourite dog'))

    def test_confusable_characters__is_two_way(self):
        for u in [chr(i) for i in range(137928)]:
            mapped_chars = confusable_characters(u)
            if mapped_chars:
                for mapped_char in mapped_chars:
                    self.assertTrue(u in confusable_characters(mapped_char))

    def test_confusable_characters__no_confusables_returns_input_character_if_length_is_zero(self):
        self.assertEqual(confusable_characters(''), [''])

    def test_confusable_characters__no_confusables_returns_input_character_if_length_is_one(self):
        self.assertEqual(confusable_characters('#'), ['#'])

    def test_confusable_characters__no_confusables_returns_none_if_length_is_not_one(self):
        self.assertEqual(confusable_characters('This is a long string that has no chance being confusable with a single character'), None)

    def test_confusable_regex__basic_ascii_regex_with_padding(self):
        regex = confusable_regex('bore', include_character_padding=True)
        reg = re.compile(regex)
        self.assertTrue(reg.search('Sometimes people say that life can be a ь.𝞂.ř.ɜ, but I don\'t agree'))

    def test_confusable_regex__basic_ascii_regex_without_padding(self):
        regex = confusable_regex('bore')
        reg = re.compile(regex)
        self.assertFalse(reg.search('Sometimes people say that life can be a ь.𝞂.ř.ɜ, but I don\'t agree'))
        self.assertTrue(reg.search('Sometimes people say that life can be a ь𝞂řɜ, but I don\'t agree'))

    def test_confusable_regex__match_subwords(self):
        regex = confusable_regex('bore')
        reg = re.compile(regex)
        self.assertTrue(reg.search('Sometimes people say that life can be a ь𝞂řɜd, but I don\'t agree'))
        self.assertTrue(reg.search('Sometimes people say that life can be a ь𝞂řɜ, but I don\'t agree'))

    def test_confusable_regex__match_multi_character_confusion(self):
        regex = confusable_regex('‷')
        reg = re.compile(regex)
        self.assertFalse(reg.search('Sometimes people say that life can be \' , but I don\'t agree'))
        self.assertTrue(reg.search('Sometimes people say that life can be \'\'\' , but I don\'t agree'))

    def test_confusable_regex__dont_treat_pipe_as_wildcard(self):
        regex = confusable_regex('bore')
        reg = re.compile(regex)
        self.assertFalse(reg.search('Sometimes people say that life can be a ||||, but I don\'t agree'))

    def test_normalize__prioritize_alpha_True_and_False(self):
        self.assertEqual(normalize('Ʀỏ𝕍3ℛ', prioritize_alpha=True), ['rov3r', 'rover'])
        self.assertEqual(normalize('Ʀỏ𝕍3ℛ'), normalize('Ʀỏ𝕍3ℛ', prioritize_alpha=False), ['r0v3r', 'r0ver', 'ro\'v3r', 'ro\'ver', 'rov3r', 'rover'])

    def test_normalize__at_character_gets_normalized(self):
        self.assertEqual(normalize('te@time'), ['teatime'])
