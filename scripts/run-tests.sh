#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
	sudo docker run --rm -d -p 9867:27017 --name test_mongo mongo > /dev/null
	sudo docker run --rm -d -p 9877:5672 --name test_rabbitmq rabbitmq > /dev/null
	pytest --cov-report term --cov=brainstorm ./tests
	sudo docker stop test_mongo > /dev/null
	sudo docker stop test_rabbitmq > /dev/null
}


main "$@"