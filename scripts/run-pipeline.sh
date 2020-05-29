#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."

GREEN="\e[32m"
BLUE="\e[34m"
PINK="\e[38;5;206m"
BOLD="\e[1m"
NC="\e[0m"

function main {
	echo -e "\n${GREEN}${BOLD}Starting pipeline...${NC}\n"
    sudo docker-compose up -d
    echo -e "\n${GREEN}${BOLD}Pipeline is now running!${NC}\n"
    echo -e "Run a client to upload a sample."
   	echo -e "Also check out ${BLUE}http://localhost:8080/${NC} to see the data.\n"
   	echo -e "${PINK}${BOLD}Happy BrainStorming!${NC}"
}


main "$@"