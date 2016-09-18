#!/bin/zsh

set -ex

docker exec -it roach1 ./cockroach sql -e 'DROP DATABASE IF EXISTS shoppr_db'
docker exec -it roach1 ./cockroach sql -e 'CREATE DATABASE shoppr_db'
docker exec -it roach1 ./cockroach sql -e 'GRANT ALL ON DATABASE shoppr_db TO dave'

~/venvs/htntest/bin/python -c 'import main; main.create_db()'
