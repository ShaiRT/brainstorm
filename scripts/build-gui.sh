#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
	curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
	sudo apt install -y nodejs
	cd ./brainstorm/gui/gui-app
    sudo npm install
    npm run build
    cd ../../..
}


main "$@"
