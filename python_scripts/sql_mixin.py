"""Mixin module"""

from typing import Any, List, Union, Callable, Optional
import logging

from sqlalchemy import (
    Inspector,
    Result,
    create_engine,
    inspect,
    text,
    MetaData,
    Table,
)
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta

from sql_models import Rating


class SQLMixin:
    """SQLMixin class"""

    def configure_engine(  # pylint: disable=too-many-arguments
        self,
        driver: str,
        username: str,
        password: str,
        host: str,
        port: Optional[int],
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

        # reflect will load the existing table into the metadata
        # given an Engine or Connection object
        self.metadata.reflect(bind=self.engine)

        # inspect will load the existing table into the metadata
        # given an Engine or Connection object
        self.postgres_inspector: Inspector = inspect(self.engine)

    def get_tables(self, logger: Callable[[str], None]) -> List[str]:
        """Get table names

        Args:
            logger (Callable[[str], None]): Logger object
        """
        table_names = self.postgres_inspector.get_table_names()
        logger(f"Table names: {table_names}")
        return table_names

    def create_table(
        self,
        table_obj: Union[Rating, DeclarativeMeta],
        logger: Callable[[str], None],
    ) -> None:
        """Create table

        Args:
            table (Union[T, Table],): Table object to create
            logger (Callable): Logger object

        Raises:
            ValueError: Table must be a subclass of DeclarativeMeta
        """
        if not isinstance(table_obj, DeclarativeMeta):
            logger(str(table_obj.__class__))
            raise ValueError("Table must be a subclass of DeclarativeMeta")

        tables: List[str] = self.get_tables(logging.getLogger(__name__).info)
        tablename: str = table_obj.__tablename__  # type: ignore

        if str(tablename) in tables:  # type: ignore
            logger(f"table {tablename} already exists")
            return

        table_obj.metadata.create_all(bind=self.engine)  # type: ignore
        self.session.add(table_obj)
        self.session.commit()

    def get_table_columns_data(
        self, table_name: str, logger: Callable[[str], None]
    ) -> None:
        """Get table columns data

        Args:
            table_name (str): Name of the table
            logger (Callable[[str], None]): Logger object
        """
        logger(str(self.postgres_inspector.get_columns(table_name)))

    def get_table_column_names(
        self, table_name: str, logger: Callable[[str], None]
    ) -> None:
        """Get table column names

        Args:
            table_name (str): Name of the table
            logger (Logger): Logger object

        Returns:
            List[str]: List of column names
        """
        my_table: Table = self.metadata.tables[table_name]

        inspector: Table = inspect(my_table)
        column_names: List[str] = inspector._columns.keys()  # type: ignore
        logger(f"Column names: {column_names}")

    def raw_query(
        self, query: str, session: Session, logger: Callable[[str], None]
    ) -> None:
        """Raw query

        Args:
            query (str): Query string to execute.
            session (Session): sqlalchemy Session object
            logger (Logger): Logger object
        """

        results: Result[Any] = session.execute(text(query))

        for result in results:
            logger(str(result))

    def close_session(self) -> None:
        """Close session"""
        self.session.close_all()
