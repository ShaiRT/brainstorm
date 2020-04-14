#!/bin/bash

cleanup() {
	python -m brainstorm.cleanup cleanup-server -h 'localhost' -p 8000
	python -m brainstorm.cleanup cleanup-server -h 'localhost' -p 5000
	exit
}
trap cleanup INT

docker run -d -p 27017:27017 mongo > /dev/null 2>&1 &
docker run -d -p 5672:5672 rabbitmq > /dev/null 2>&1 &
python -m brainstorm.server run-server -h 'localhost' -p 8000 'rabbitmq://localhost:5672/' &
python -m brainstorm.parsers run-parser 'pose' 'rabbitmq://localhost:5672/' &
python -m brainstorm.parsers run-parser 'feelings' 'rabbitmq://localhost:5672/' &
python -m brainstorm.parsers run-parser 'color_image' 'rabbitmq://localhost:5672/' &
python -m brainstorm.parsers run-parser 'depth_image' 'rabbitmq://localhost:5672/' &
python -m brainstorm.saver.saver run-saver 'mongodb://localhost:27017' 'rabbitmq://localhost:5672/' &
python -m brainstorm.api.api run-server -h 'localhost' -p 5000 -d 'mongodb://localhost:27017/' &
read -r -d '' _	