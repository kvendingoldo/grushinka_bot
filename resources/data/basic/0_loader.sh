#!/bin/bash

CONTAINER_NAME='grushinka-mongodb'
DATABASE='grushinka'

function main() {
    docker cp days.json ${CONTAINER_NAME}:/tmp
    docker exec -it ${CONTAINER_NAME} mongoimport --db "${DATABASE}" --collection 'days' --jsonArray /tmp/days.json
}

main "${@}"