[![Build Status](https://travis-ci.org/woodgern/confusables.svg?branch=master)](https://travis-ci.org/woodgern/confusables) [![PyPI version](https://badge.fury.io/py/confusables.svg)](https://badge.fury.io/py/confusables)


# Confusables

Confusables is a python package that provides functionality for analyzing and matching words that "appear"
to be the same or similar, but use different characters.

Confusables uses the unicode confusable characters list (https://www.unicode.org/Public/security/8.0.0/confusables.txt)
along with other methods of matching characters.

This package can be used for any application where detecting words using any unexpected characters to pass filters
is required. This could include finding malicious fake website names, analyzing or normalizing text data, or even detecting
attempts to get past a profanity filter.


## Installation

Confusables can be installed through pip using
`pip3 install confusables`


## Usage

The functions in the confusables module focus around comparing and finding strings that can be considered "confusable". This means that they can be humanly interpretable as the same string. Since this deals with human interpretation, the "confusable" definition is loose, and in later versions may be more or less strict.

Currently, confusables provides: `is_confusable`, `confusable_characters`, and `confusable_regex`


`is_confusable(string1, string2)` takes in 2 strings and outputs whether or not the two are "confusable". Keep in mind that in some cases, a single character can be confusable with 2 characters combined (eg. ‼ is a single character, !! is two)
```
from confusables import is_confusable

print(is_confusable('rover', 'Ʀỏ𝕍3ℛ'))
# prints True
```



`confusable_characters(char)` takes in a character and outputs a list of characters that are confusable with it. In some cases, as mentioned above, a single characters can be confusables with multiple characters, in which case those characters will be inluded in the list in the form of a string.
```
from confusables import confusables_characters

print(confusable_characters('c'))
# prints ['ċ', 'ᴄ', '𝔠', '𝒄', '𝗰', '𝗖', 'ḉ', 'ℂ', 'Ꮯ', 'ć', 'c̦', '𝑐', '𝓬', '𝚌', '𐌂', 'Ⅽ', 'С', '𝘤', 'ｃ', 'ҫ', '𝖈', '🝌', '𝖢', '𝐂', 'C', '𝓒', 'Ç', '𝘾', 'ç', 'Ⲥ', 'с', 'ⅽ', 'ĉ', '𐔜', 'c', 'ℭ', 'ϲ', '𑣩', 'Ϲ', '𝕮', 'č', '𐊢', 'Ĉ', '𝑪', 'Ｃ', '𑣲', '𐐕', '𐐽', 'ⲥ', '𝐶', 'Ċ', 'C̦', 'ꮯ', '𝒞', '𝕔', '𝘊', 'Č', 'ꓚ', '𝒸', '𝐜', '𝙲', '𝖼', 'Ć', '𝙘', 'Ḉ']
```


`confusable_regex(string, include_character_padding=False)` takes a string and outputs a regex string that matches words that are confusable with the input string.
```
from confusables import confusable_regex
import re

regex_string = confusable_regex('bore', include_character_padding=True)
regex = re.compile(regex_string)

print(regex.search('Sometimes people say that life can be a ь.𝞂.ř.ɜ, but I don\'t agree'))
# prints <_sre.SRE_Match object; span=(40, 47), match='ь.𝞂.ř.ɜ'>
```



`normalize(string, prioritize_alpha=False)` takes a string and outputs a list of possible "normal forms". This means that characters in the string get converted to their confusable ascii counterparts. The `prioritize_alpha` option means the outputted options will prioritize converting characters to characters of the latin alphabet over any others. This option is recommended when natural language is expected.
```
from confusables import normalize

print(normalize('Ʀỏ𝕍3ℛ', prioritize_alpha=True))
# prints ['rov3r', 'rover']

print(normalize('Ʀỏ𝕍3ℛ', prioritize_alpha=False))
# prints ['r0v3r', 'r0ver', 'ro\'v3r', 'ro\'ver', 'rov3r', 'rover']
```

## About confusables

This module is something I put together because I'm interested in the field of language processing. I'm hoping to build out it's functionality, and I'm more than happy to take suggestions!

Additionally, I think the effectiveness of the module could be greatly improved using some machine learning models, and I'm currently on the hunt for some useful data sets. Please let me know if you know of any!

You can contact me through any normal Github means, or using my email, `woodgern@gmail.com`
