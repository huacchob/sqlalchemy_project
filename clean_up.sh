# bin/bash

docker rm -f $(docker ps -a -f name=sql-training-pgadmin-1 -q && docker ps -a -f name=sql-training-db-1 -q)
rm -rf database_volume/* && rm -rf pgadmin_volume/*