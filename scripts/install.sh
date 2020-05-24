#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    python -m virtualenv .env --prompt "[brainstorm] "
    find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    .env/bin/pip install -U pip
    .env/bin/pip install -r requirements.txt

    sudo sh get-docker.sh
    # TODO: pull images for mongo and rabbitmq and build bs image

    # TODO: install npm and build gui?
    # apt-get update -y
	# apt-get install -y npm
	# npm install -g npm@latest
	# sudo npm install ./brainstorm/gui/gui-app
    # npm run --prefix ./brainstorm/gui/gui-app build
}


main "$@"