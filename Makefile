package:
	python3 setup.py sdist bdist_wheel

parse:
	python3 confusables/parse.py

update:
	if [ -z "$(VERSION)" ]; then \
		echo "Please specify the VERSION argument with a valid version of unicode confusables"; \
	else \
		wget -O confusables/assets/confusables.txt https://www.unicode.org/Public/security/${VERSION}/confusables.txt; \
	fi
test:
	python3 -m unittest discover

release:
	python3 -m twine upload dist/*

