from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class Habit(SqlAlchemyBase):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    days_of_week = Column(String)
    completion_count = Column(Integer, default=0)
    last_reset_date = Column(Date)

    user = relationship("User")

