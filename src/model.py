import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from src.config import DATABASE_URL


metadata = db.MetaData()
Base = declarative_base(metadata=metadata)
engine = db.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


BusinessToCategory = db.Table(
    "business_to_category",
    Base.metadata,
    db.Column(
        "business_id",
        db.String(64),
        db.ForeignKey("business.business_id")
    ),
    db.Column(
        "category_id",
        db.Integer(),
        db.ForeignKey("business_categories.category_id")
    )
)


class User(Base):
    __tablename__ = "users"

    user_id = db.Column(db.String(64), primary_key=True)
    review_count = db.Column(db.Integer())
    yelping_since = db.Column(db.String(64))  # TODO: check why DateTime fails
    useful = db.Column(db.Integer())
    funny = db.Column(db.Integer())
    cool = db.Column(db.Integer())
    # TODO: add friends
    fans = db.Column(db.Integer())
    average_stars = db.Column(db.Float())
    compliment_hot = db.Column(db.Integer())
    compliment_more = db.Column(db.Integer())
    compliment_profile = db.Column(db.Integer())
    compliment_cute = db.Column(db.Integer())
    compliment_list = db.Column(db.Integer())
    compliment_note = db.Column(db.Integer())
    compliment_plain = db.Column(db.Integer())
    compliment_cool = db.Column(db.Integer())
    compliment_funny = db.Column(db.Integer())
    compliment_writer = db.Column(db.Integer())
    compliment_photos = db.Column(db.Integer())

class Business(Base):
    __tablename__ = "business"

    business_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.Text())
    address = db.Column(db.Text())
    city = db.Column(db.Text())
    state = db.Column(db.String(2))
    postal_code = db.Column(db.String(5))
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    stars = db.Column(db.Float())
    review_count = db.Column(db.Integer())
    is_open = db.Column(db.Integer())

    categories = relationship(
        "BusinessCategory",
        secondary=BusinessToCategory,
        back_populates="businesses"
    )


class BusinessCategory(Base):
    __tablename__ = "business_categories"

    category_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text())

    businesses = relationship(
        "Business",
        secondary=BusinessToCategory,
        back_populates="categories"
    )

class Review(Base):
    __tablename__ = "reviews"

    review_id = db.Column(db.String(64), primary_key=True)
    date = db.Column(db.DateTime())
    user_id = db.Column(
        db.String(64),
        db.ForeignKey(User.user_id)
    )
    business_id = db.Column(
        db.String(64),
        db.ForeignKey(Business.business_id)
    )
    stars = db.Column(db.Integer())
    useful = db.Column(db.Integer())
    funny = db.Column(db.Integer())
    cool = db.Column(db.Integer())
    text = db.Column(db.Text())


class Tip(Base):
    __tablename__ = "tips"

    tip_id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    user_id = db.Column(
        db.String(64),
        db.ForeignKey(User.user_id)
    )
    business_id = db.Column(
        db.String(64),
        db.ForeignKey(Business.business_id)
    )
    text = db.Column(db.Text())
    compliment_count = db.Column(db.Integer())
