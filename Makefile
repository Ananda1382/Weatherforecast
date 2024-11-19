all:
	docker build -f Producer_Dockerfile --no-cache -t weatherproducer:v2.0 .
	docker build -f Consumer_Dockerfile --no-cache -t weatherconsumer:v2.0 .
