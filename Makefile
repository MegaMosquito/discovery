all: build run

build:
	docker build -t discovery .

dev: build
	-docker rm -f discovery 2> /dev/null || :
	docker run -it --name discovery --net=host --volume `pwd`:/outside discovery /bin/sh

run:
	-docker rm -f discovery 2>/dev/null || :
	docker run -d --name discovery --net=host --volume `pwd`:/outside discovery

exec:
	docker exec -it discovery /bin/sh

stop:
	-docker rm -f discovery 2>/dev/null || :

clean: stop
	-docker rmi discovery 2>/dev/null || :

.PHONY: all build dev run exec stop clean

