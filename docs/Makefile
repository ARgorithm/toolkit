doc:
	rm -rf docs/api/
	pdoc3 --html ../ARgorithmToolkit --template-dir=docs/templates --output-dir docs
	mv docs/ARgorithmToolkit docs/api
	
serve:
	rm -rf docs/api/
	pdoc3 --html ../ARgorithmToolkit --template-dir=docs/templates --output-dir docs
	mv docs/ARgorithmToolkit docs/api
	mkdocs serve
	rm -rf docs/api/

deploy:
	rm -rf docs/api/
	pdoc3 --html ../ARgorithmToolkit --template-dir=docs/templates --output-dir docs
	mv docs/ARgorithmToolkit docs/api
	mkdocs gh-deploy
	rm -rf site/
	rm -rf docs/api/

clean:
	rm -rf docs/api/