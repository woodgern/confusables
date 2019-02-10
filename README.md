# Confusables

Confusables is a python package that provides functionality for analyzing and matching words that "appear"
to be the same or similar, but use differnt characters.

Confusables uses the unicode confusable characters list (https://www.unicode.org/Public/security/8.0.0/confusables.txt)
along with other methods of matching characters.

This package can be used for any application where detecting words using any unexpected characters to pass filters
is required. This could include be finding fake website names, analyzing or normalizing text data, or even detecting
attempts to get past a profanity filter.
