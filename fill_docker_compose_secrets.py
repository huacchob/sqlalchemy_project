import os
import typing as t

from yaml import safe_load, dump

from python_scripts.utils import find_file_path, load_secrets_from_file, get_secret

creds_env_file: t.Optional[str | None] = find_file_path("creds.env", __file__)
docker_compose_file: t.Optional[str | None] = find_file_path(
    "docker-compose.yml", __file__
)

load_secrets_from_file("creds.env", __file__)

with open(creds_env_file, "r", encoding="utf-8") as creds_file:
    creds_file: t.TextIO
    secrets_values: str = creds_file.read()
    secrets_values_list: t.List[str] = secrets_values.split("\n")

secrets = []

for secret_pair in secrets_values_list:
    if secret_pair.startswith("#"):
        continue
    split_secret: t.List[str] = secret_pair.split("=")
    if os.environ.get(split_secret[0], None):
        secrets.append(split_secret[0])

with open(docker_compose_file, "r", encoding="utf-8") as docker_compose_file_read:
    docker_compose_config: t.Dict[
        str, t.Dict[str, t.Dict[str, t.Union[str, t.List[str]]]]
    ] = safe_load(docker_compose_file_read)

db_secrets_path: t.List[str] = (
    docker_compose_config.get("services", {}).get("db", {}).get("environment", [])
)
pgadmin_secrets_path: t.List[str] = (
    docker_compose_config.get("services", {}).get("pgadmin", {}).get("environment", [])
)

total_secrets: t.List[str] = db_secrets_path + pgadmin_secrets_path

postgres_secrets: t.List[str | None] = []
pgadmin_secrets: t.List[str | None] = []

for secret in total_secrets:
    docker_secret_value: t.List[str] = secret.split("=")
    secret_name: str = docker_secret_value[0]
    if secret_name not in secrets:
        raise ValueError(f"Secret {secret_name} not found in creds.env file")
    secret_value: str = get_secret(secret_name)
    if "POSTGRES" in secret_name:
        postgres_secrets.append(f"{secret_name}={secret_value}")
    if "PGADMIN" in secret_name:
        pgadmin_secrets.append(f"{secret_name}={secret_value}")

docker_compose_config.get("services").get("db")["environment"] = postgres_secrets
docker_compose_config.get("services").get("pgadmin")["environment"] = pgadmin_secrets

with open(docker_compose_file, "w", encoding="utf-8") as docker_compose_file_write:
    docker_compose_file_write: t.TextIO
    dump(docker_compose_config, docker_compose_file_write)
