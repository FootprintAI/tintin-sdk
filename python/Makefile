install:
	pip3 install -r requirements.txt
build:
	python3 setup.py sdist bdist_wheel
check:
	twine check dist/*
publish:
	twine upload dist/*
clean:
	rm -rf dist build tintin_sdk.egg-info/
