#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."

GREEN="\e[32m"
BLUE="\e[34m"
PINK="\e[38;5;206m"
BOLD="\e[1m"
NC="\e[0m"

function main {
	echo -e "\n${GREEN}${BOLD}Starting build, this might take a while...${NC}"
	curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
	sudo apt install -y nodejs 
	cd ./brainstorm/gui/gui-app
    sudo npm install
    sudo npm run build
    cd ../../..
    echo -e "${GREEN}${BOLD}Done!${NC}\n"
    echo -e "Try running ${BLUE}$ python -m brainstorm.gui run-server${NC}"
    echo -e "**for more information run ${BLUE}$ python -m brainstorm.gui run-server --help${NC}\n"
    echo -e "${PINK}${BOLD}Happy BrainStorming!${NC}"
}


main "$@"
