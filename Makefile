
init:
	python setup.py install
	pip install -r requirements.txt
	
test:
	pytest tests

verify:
	python schema.py

dist:
	python setup.py sdist bdist_wheel

deploy:
	python3 -m pip install --user --upgrade twine && python3 -m twine upload dist/*

testdeploy:
	python3 -m pip install --user --upgrade twine && python3 -m twine upload --repository testpypi dist/*
