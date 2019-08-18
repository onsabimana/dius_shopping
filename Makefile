test:
	docker run --rm \
		-v $(PWD):/var/task \
		-w /var/task --entrypoint /bin/bash \
		lambci/lambda:build-python3.7 -c \
		"python -m unittest discover -s tests/ -v -p 'test_*.py'"
