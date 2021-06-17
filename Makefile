
init:
	pip install -r requirements.txt
	python setup.py install
	
clean:
	rm -rf ARgorithmToolkit.egg-info/ build/ dist/

lint:
	pylint ARgorithmToolkit
	pylint tests/

test:
	pytest tests

server:
	docker build . -t argorithm-server:local
	docker run --rm -p 80:80 argorithm-server:local

verify:
	python schema.py

dist:
	python setup.py sdist
	python setup.py bdist_wheel

deploy:
	python3 -m pip install --user --upgrade twine && python3 -m twine upload dist/*

testdeploy:
	python3 -m pip install --user --upgrade twine && python3 -m twine upload --repository testpypi dist/*
