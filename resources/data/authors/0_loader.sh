#!/bin/bash

CONTAINER_NAME='grushinka-mongodb'
DATABASE='grushinka'

function main() {
    for FILE in *.json; do
        docker cp ${FILE} ${CONTAINER_NAME}:/tmp
        docker exec -it ${CONTAINER_NAME} mongo "${DATABASE}" --eval "db.${FILE%%.json}.drop()"
        docker exec -it ${CONTAINER_NAME} mongoimport --db "${DATABASE}" --collection ${FILE%%.json} --jsonArray /tmp/${FILE}
    done
}

main "${@}"