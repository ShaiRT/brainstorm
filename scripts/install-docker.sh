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
	curl -fsSL https://get.docker.com -o scripts/get-docker.sh
	chmod 755 scripts/get-docker.sh
	sudo sh scripts/get-docker.sh
	sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod 755 /usr/local/bin/docker-compose
	echo -e "\n${GREEN}${BOLD}Done!${NC}\n"
	echo -e "Ready to install ${PINK}${BOLD}BrainStorm${NC}:"
	echo -e "Run ${BLUE}$ ./scripts/install.sh${NC}"
	echo -e "and then run ${BLUE}$ source .env/bin/activate${NC} and you're good to go!\n"
	echo -e "${PINK}${BOLD}Happy BrainStorming!${NC}"
}


main "$@"
