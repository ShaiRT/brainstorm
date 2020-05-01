#!/bin/bash

docker run --rm -d -p 9867:27017 --name test_mongo mongo
docker run --rm -d -p 9877:5672 --name test_rabbitmq rabbitmq
./scripts/wait-for-it.sh 0.0.0.0:9877
pytest --cov-report term --cov=brainstorm ./tests
docker stop test_mongo
docker stop test_rabbitmq