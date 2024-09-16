You must make a copy of creds.example.creds as creds.env.
Do not make any changes to docker-compose, just change the secrets in creds.env.
You also need to make a copy of docker-compose.example.txt and make it ad docker-compose.yml.
Once this is done, you can set this all together by running ./start_up.sh

When creating your creds.env file, here are some examples

# PGADMIN
PGADMIN_DEFAULT_EMAIL=user@email.com
PGADMIN_DEFAULT_PASSWORD=password
PGADMIN_ADDRESS=localhost:5050

# POSTGRES
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=postgres
POSTGRES_ADDRESS=localhost:5432

We set pgadmin to 5050 because that is what is mapped in docker compose file.
we are using localhost because postgres and pgadmin are both containers.

You may need to change the start_up.sh file to python if python3 doesn't work.

If the file permissions are not set, you may need to change the file permissions for both clean_up and start_up scripts.

You can do so by using the command `a+x chmod clean_up.sh` or `a+x chmod start_up.sh`.
