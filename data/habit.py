from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class Habit(SqlAlchemyBase):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")

    days_of_week = Column(String)
