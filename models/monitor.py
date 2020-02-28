# coding: utf-8
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Monitor(Base):
    __tablename__ = 'monitor'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    item = Column(String)
    pre_offset = Column(Integer)
    post_offset = Column(Integer)
    size = Column(Integer)
    success = Column(Boolean)
