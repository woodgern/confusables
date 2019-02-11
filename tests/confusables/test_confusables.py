import unittest
import datetime
from unittest.mock import Mock

import confusables

class TestConfusables(unittest.TestCase):

    def test_is_confusable__unicode_mapping_only(self):
        self.assertTrue(confusables.is_confusable('rover', '𝜰ỏ𝕍3ℛ'))