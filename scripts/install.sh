#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    python -m virtualenv .env --prompt "[brainstorm] "
    find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    .env/bin/pip install -U pip
    .env/bin/pip install -r requirements.txt

    sudo docker pull rabbitmq:management
    sudo docker pull mongo
    sudo docker build -t brainstorm .
    sudo docker build -f Dockerfile.gui -t brainstorm-gui .
}


main "$@"