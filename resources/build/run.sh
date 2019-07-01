#!/bin/bash

########################################################
#
# Name: run.sh
#
# Launches grushinka bot
#
##########################################################

SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
CONTAINER_NAME='grushinka:1.0'

function main() {
    cd "${SCRIPT_DIR}/../.." || exit
    docker build -t "${CONTAINER_NAME}" .

    cd "${SCRIPT_DIR}/../compose" || exit
    docker-compose up -d

    sleep 5
    cd "${SCRIPT_DIR}/../data" || exit
    bash 0_loader.sh
}

main "${@}"