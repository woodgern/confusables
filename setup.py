import setuptools
import os

long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setuptools.setup(
    name="confusables",
    version="0.0.1",
    author="Nathan Woodger",
    author_email="woodgern@gmail.com",
    description="A python package providing functionality for matching words using different characters but appearing to be similar/the same word.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/woodgern/confusables",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

