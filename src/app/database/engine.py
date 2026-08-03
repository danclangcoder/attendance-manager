import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from app.config.app_settings import Settings

from .models.base_model import BaseModel

engine = sa.create_engine(Settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
BaseModel.metadata.create_all(engine)
