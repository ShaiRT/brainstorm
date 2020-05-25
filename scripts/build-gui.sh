#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
	curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
	sudo apt install -y nodejs
    npm run --prefix ./brainstorm/gui/gui-app build
    sudo npm install ./brainstorm/gui/gui-app
}


main "$@"
