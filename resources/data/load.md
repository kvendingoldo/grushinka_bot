mongoimport --db grushinka --collection l21 --jsonArray /tmp/21.json
mongoimport --db grushinka --collection l5 --jsonArray /tmp/5.json

mongoimport --db grushinka --collection letters --jsonArray /tmp/letters.json


db.authors.deleteMany({})