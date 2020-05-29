#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."

GREEN="\e[32m"
BLUE="\e[34m"
PINK="\e[38;5;206m"
BOLD="\e[1m"
NC="\e[0m"

function main {
	echo -e "\n${GREEN}${BOLD}Stopping pipeline...${NC}\n"
    sudo docker-compose down
    echo -e "\n${GREEN}${BOLD}Pipeline stopped.${NC}"
    echo -e "${PINK}${BOLD}Hope you enjoyed your BrainStorming!${NC}"
}


main "$@"
