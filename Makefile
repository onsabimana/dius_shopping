
lint:
	docker run --rm -v $(PWD):/app -w /app --entrypoint /bin/bash \
		python:3.7 -c "pip install pylint && pylint shopping"

test: lint
	docker run --rm -v $(PWD):/app -w /app --entrypoint /bin/bash \
		python:3.7 -c "python -m unittest discover -s tests/ -v -p 'test_*.py'"
