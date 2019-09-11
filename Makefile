package:
	python3 setup.py sdist bdist_wheel

parse:
	python3 confusables/parse.py

update:
	wget -O confusables/assets/confusables.txt https://www.unicode.org/Public/security/12.1.0/confusables.txt

test:
	python3 -m unittest discover

release:
	python3 -m twine upload dist/*

