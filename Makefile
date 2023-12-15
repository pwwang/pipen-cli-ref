example:
	pipen ref \
		-p "example/pipeline.py:Pipeline" \
		-d example/docs/ \
		-i Input \
		-i Output \
		-r "Envs=Environment Variables" \
		--replace "<url1>=https://google.com" \
		--replace "<url2>=https://github.com"

.PHONY: example
