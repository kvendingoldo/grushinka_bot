#!/bin/bash

CONTAINER_NAME='grushinka-mongodb'
DATABASE='grushinka'

function main() {
    for FILE in *; do
        LETTER=${FILE%%.json}
        docker cp ${FILE} ${CONTAINER_NAME}:/tmp
        docker exec -it ${CONTAINER_NAME} mongoimport --db "${DATABASE}" --collection "${LETTER}" --jsonArray /tmp/${FILE}
    done
}

main "${@}"