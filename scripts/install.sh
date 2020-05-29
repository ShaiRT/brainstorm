#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."

GREEN="\e[32m"
BLUE="\e[34m"
PINK="\e[38;5;206m"
BOLD="\e[1m"
NC="\e[0m"

function main {
	echo -e "\n${GREEN}${BOLD}Starting installation...${NC}\n"

    python -m virtualenv .env --prompt "[brainstorm] "
    find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    .env/bin/pip install -U pip
    .env/bin/pip install -r requirements.txt

    sudo docker pull rabbitmq
    sudo docker pull mongo
    sudo docker build -t brainstorm .
    sudo docker build -f Dockerfile.gui -t brainstorm-gui .

    echo -e "\n${GREEN}${BOLD}Done!${NC}\n"
	echo -e "run ${BLUE}$ source .env/bin/activate${NC} to start\n"
	echo -e "${PINK}${BOLD}Happy BrainStorming!${NC}"
}


main "$@"