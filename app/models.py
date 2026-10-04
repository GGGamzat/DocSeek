from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_date = Column(DateTime, nullable=False)
    rubrics = Column(ARRAY(String), nullable=False)