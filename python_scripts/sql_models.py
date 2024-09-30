"""DB Models"""

from sqlalchemy import Column, Integer, Sequence
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()

user_id_seq: Sequence = Sequence(name="user_id_seq")


class Rating(Base):  # type: ignore # pylint: disable=too-few-public-methods
    """User model"""

    __tablename__: str = "ratings"

    id: Column[int] = Column(
        __name_pos=Integer, __type_pos=user_id_seq, primary_key=True
    )
    stars: Column[int] = Column(__name_pos=Integer)

    def __init__(self, stars: Column[int]) -> None:
        """Initialize User

        Args:
            stars (int): number of stars
        """
        self.stars: Column[int] = stars

    def __repr__(self) -> str:
        """
        String representation of User

        Returns:
            str: user name
        """
        return f"<stars {self.stars}>"
