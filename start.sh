#!/bin/bash
#app="docker.test"
#docker build -t ${app} .
#docker run -d -p 56733:80 \
#  --name=${app} \
#  -v $PWD:/app ${app}


app="mydockerapp"
db="flask_db"
docker build -t ${app} .
docker run -d -p 5432:5432 \
  --name=${db} \
  -v $PWD:/app \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=${db} \
  -e DATABASE_URL=postgresql://postgres:postgres@localhost:5432/${db} \
  postgres:13-alpine
docker run -d -p 56733:80 \
  --name=${app} \
  --link ${db}:${db} \
  -v $PWD:/app \
  -e DATABASE_URL=postgresql://${db}:5432/${db} \
  ${app}
