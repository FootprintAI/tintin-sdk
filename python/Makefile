install-dependency:
	pip3 install bumpversion=1.0.1 twine=0.6.0
build:
	python3 setup.py sdist bdist_wheel
check:
	twine check dist/*
publish:
	twine upload dist/*
clean:
	rm -rf dist build tintin_sdk.egg-info/
