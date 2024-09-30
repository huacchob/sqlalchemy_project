"""Main module"""

from dataclasses import dataclass
from logging import Logger
from typing import List

from sql_mixin import SQLMixin
from sqlalchemy import Inspector, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from utils import configure_logger, get_secret, load_secrets_from_file

load_secrets_from_file(target_file_name="creds.env", source_file_name=__file__)


@dataclass
class SQLMain(SQLMixin):  # pylint: disable=R0902, R0903
    """SQLMain class"""

    def __init__(self) -> None:
        """Initialize SQLMain"""
        self.logger: Logger = configure_logger(
            name=__name__,
            logger_level_str="INFO",
        )

        self.db_username: str = get_secret(secret_name="POSTGRES_USER")
        self.db_password: str = get_secret(secret_name="POSTGRES_PASSWORD")
        db_url: List[str] = get_secret(
            secret_name="POSTGRES_ADDRESS",
        ).split(sep=":")
        self.db_host: str = db_url[0]
        self.db_port: int = int(db_url[1])
        self.db_name: str = "dvd"

        self.configure_engine(
            driver="postgresql",
            username=self.db_username,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            debug=False,
        )

        self.engine: Engine
        self.session: Session
        self.metadata: MetaData
        self.postgres_inspector: Inspector


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
    sql_main.raw_query(
        query=query, session=sql_main.session, logger=sql_main.logger.info
    )
    print("\n")

    sql_main.get_table_column_names(
        table_name=table_name,
        logger=sql_main.logger.info,
    )
    print("\n")

    sql_main.get_tables(logger=sql_main.logger.info)

    sql_main.close_session()
