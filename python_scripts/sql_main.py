"""Main module"""

from typing import List
from logging import Logger
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy.dialects.postgresql.base import PGInspector
from sql_mixin import SQLMixin
from utils import get_secret, load_secrets_from_file, configure_logger


load_secrets_from_file("creds.env", __file__)


class SQLMain(SQLMixin):
    """SQLMain class"""

    def __init__(self):
        """Initialize SQLMain"""
        self.logger: Logger = configure_logger(__name__, "INFO")

        self.db_username: str = get_secret("POSTGRES_USERNAME")
        self.db_password: str = get_secret("POSTGRES_PASSWORD")
        db_url: List[str] = get_secret("POSTGRES_ADDRESS").split(":")
        self.db_host: str = db_url[0]
        self.db_port: str = db_url[1]
        self.db_name: str = "dvd"

        self.configure_engine(
            "postgresql",
            self.db_username,
            self.db_password,
            self.db_host,
            self.db_port,
            self.db_name,
            False,
        )

        self.engine: Engine
        self.session: Session
        self.metadata: MetaData
        self.postgres_inspector: PGInspector


if __name__ == "__main__":

    sql_main: SQLMain = SQLMain()

    # sql_main.create_table(
    #     Rating, sql_main.logger.info,
    # )

    table_name: str = "customer"
    limit: int = 10

    query: str = f"""
    SELECT DISTINCT payment_id,customer.customer_id,first_name
    FROM customer
    INNER JOIN payment
    ON customer.customer_id = payment.customer_id
    ORDER BY customer.customer_id DESC
    LIMIT {limit};
    """
    sql_main.raw_query(query, sql_main.session, sql_main.logger.info)
    print("\n")

    sql_main.get_table_column_names(table_name, sql_main.logger.info)
    print("\n")

    sql_main.get_tables(sql_main.logger.info)

    sql_main.close_session()
