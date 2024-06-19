from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Shoes(Base):
  __tablename__ = 'shoes'

  id = Column(Integer, primary_key=True, index=True)
  type = Column(String, index=True)
  name = Column(String, index=True)
  is_expensive = Column(Boolean, index=True)

