"""Mixin module"""

from typing import List, Union
from logging import Logger
from sqlalchemy import create_engine, inspect, text, MetaData, Table
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.dialects.postgresql.base import PGInspector
from sql_models import Rating


class SQLMixin:
    """SQLMixin class"""

    def configure_engine(
        self,
        driver: str,
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
        debug: bool = False,
    ) -> None:
        """
        Configure engine. If you have both postgres and pgadmin
        running, you have to pass the postgres credentials.

        Args:
            driver (str): Driver to use to connect, for example, 'postgresql'
            username (str): username to use
            password (str): password to use
            host (str): host address
            port (int): port number
            database (str): database name
        """
        url: URL = URL.create(
            drivername=driver,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )

        self.engine: Engine = create_engine(url, echo=debug)
        self.session: Session = sessionmaker(bind=self.engine)()
        self.metadata: MetaData = MetaData()

        # reflect will load the existing table into the metadata, given an Engine or Connection object
        self.metadata.reflect(bind=self.engine)

        # inspect will load the existing table into the metadata, given an Engine or Connection object
        self.postgres_inspector: PGInspector = inspect(self.engine)

    def get_tables(self, logger: Logger) -> List[str]:
        """Get table names

        Returns:
            List[str]: table names
        """
        logger("Table names: %s", self.postgres_inspector.get_table_names())

    def create_table(
        self,
        table: Union[Rating, DeclarativeMeta],
        logger: Logger,
    ) -> None:
        """Create table

        Args:
            table (Union[Rating, DeclarativeMeta]): Table object to create
            logger (Logger): Logger object

        Raises:
            ValueError: Table must be a subclass of DeclarativeMeta
        """
        if not isinstance(table, DeclarativeMeta):
            logger(table.__class__)
            raise ValueError("Table must be a subclass of DeclarativeMeta")

        tables: List[str] = self.get_tables()

        if str(table.__tablename__) in tables:
            logger("table %s already exists", table.__tablename__)
            return

        table.metadata.create_all(bind=self.engine)
        self.session.add(table)
        self.session.commit()

    def get_table_columns_data(self, table_name: str, logger: Logger) -> List[str]:
        """Get table columns

        Args:
            table_name (str): table name

        Returns:
            List[str]: table columns
        """
        logger(self.postgres_inspector.get_columns(table_name))

    def get_table_column_names(self, table_name: str, logger: Logger) -> List[str]:
        """Get table column names

        Args:
            table_name (str): Name of the table
            logger (Logger): Logger object

        Returns:
            List[str]: List of column names
        """
        my_table: Table = self.metadata.tables[table_name]

        inspector: Table = inspect(my_table)
        column_names: List[str] = inspector._columns.keys()
        logger("Column names: %s", column_names)

    def raw_query(self, query: str, session: Session, logger: Logger):
        """Raw query

        Args:
            query (str): Query string to execute.
            session (Session): sqlalchemy Session object
            logger (Logger): Logger object
        """

        results: CursorResult = session.execute(text(query))

        for result in results:
            logger(result)

    def close_session(self) -> None:
        """Close session"""
        self.session.close_all()
