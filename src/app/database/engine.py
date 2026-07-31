import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from .models.base_model import BaseModel

engine = sa.create_engine("sqlite:///app.db")
SessionLocal = sessionmaker(bind=engine)
BaseModel.metadata.create_all(engine)