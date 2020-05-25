#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    sudo docker-compose up -d
}


main "$@"