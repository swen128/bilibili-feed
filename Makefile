deps:
	pip3 install -r requirements_to_freeze.txt
	pip3 install -r requirements_dev.txt
	pip3 freeze > requirements.txt

release:
	serverless deploy -v --stage prod

deploy:
	serverless deploy function -f Feed
