"""DB Models"""

from sqlalchemy import Column, Integer, Sequence
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()

user_id_seq: Sequence = Sequence("user_id_seq")


class Rating(Base):
    """User model"""

    __tablename__ = "ratings"

    id = Column(Integer, user_id_seq, primary_key=True)
    stars = Column(Integer)

    def __init__(self, stars: int):
        """Initialize User

        Args:
            stars (int): number of stars
        """
        self.stars: int = stars

    def __repr__(self):
        """
        String representation of User

        Returns:
            str: user name
        """
        return f"<stars {self.stars}>"
