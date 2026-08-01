import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from .models.base_model import BaseModel
from app.config.app_settings import Settings

engine = sa.create_engine(Settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
BaseModel.metadata.create_all(engine)