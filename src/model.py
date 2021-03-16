from datetime import datetime

import numpy as np
import sqlalchemy as db
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import DATABASE_URL


metadata = db.MetaData()
Base = declarative_base(metadata=metadata)
engine = db.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
