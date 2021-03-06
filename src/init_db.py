import os
import logging
from datetime import datetime
from collections import defaultdict

import pandas as pd
from sqlalchemy_utils import create_database, database_exists

from src.config import DATABASE_URL, DATASET_PATH
from src.model import (
    metadata, engine, Session,
    User, Business, BusinessCategory,
    Review, Tip, Checkin
)


def create_db(database_url):
    if not database_exists(database_url):
        create_database(database_url)

    metadata.drop_all(engine)
    metadata.create_all(engine)


def insert_users(dataset_path):
    session = Session()

    dfs = pd.read_json(
        os.path.join(dataset_path, "yelp_academic_dataset_user.json"),
        lines=True,
        chunksize=10000
    )

    for df_chunk in dfs:
        for i, row in df_chunk.iterrows():
            yelping_since = datetime.strptime(
                row["yelping_since"],
                "%Y-%m-%d %H:%M:%S"
            )

            user = User(
                user_id=row["user_id"],
                review_count=row["review_count"],
                yelping_since=yelping_since,
                useful=row["useful"],
                funny=row["funny"],
                cool=row["cool"],
                fans=row["fans"],
                average_stars=row["average_stars"],
                compliment_hot=row["compliment_hot"],
                compliment_more=row["compliment_more"],
                compliment_profile=row["compliment_profile"],
                compliment_cute=row["compliment_cute"],
                compliment_list=row["compliment_list"],
                compliment_note=row["compliment_note"],
                compliment_plain=row["compliment_plain"],
                compliment_cool=row["compliment_cool"],
                compliment_funny=row["compliment_funny"],
                compliment_writer=row["compliment_writer"],
                compliment_photos=row["compliment_photos"]
            )
            session.add(user)
        session.commit()
    session.close()


def insert_businesses(dataset_path):
    session = Session()

    dfs = pd.read_json(
        os.path.join(dataset_path, "yelp_academic_dataset_business.json"),
        lines=True,
        chunksize=10000
    )

    business_category_id = defaultdict(int)

    for df_chunk in dfs:
        for i, row in df_chunk.iterrows():
            business = Business(
                business_id=row["business_id"],
                name=row["name"],
                address=row["address"],
                city=row["city"],
                state=row["state"],
                postal_code=row["postal_code"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                stars=row["stars"],
                review_count=row["review_count"],
                is_open=row["is_open"],
            )

            if row["categories"]:
                for category_name in row["categories"].split(","):
                    category_name = category_name.strip()

                    if category_name not in business_category_id:
                        business_category_id[category_name] = len(business_category_id) + 1

                        category = BusinessCategory(
                            category_id=business_category_id[category_name],
                            name=category_name
                        )
                        session.add(category)
                        session.commit()
                    else:
                        category = session\
                            .query(BusinessCategory)\
                            .filter_by(category_id=business_category_id[category_name])\
                            .first()
            business.categories.append(category)
            session.add(business)
        session.commit()
    session.close()


def insert_reviews(dataset_path):
    session = Session()

    dfs = pd.read_json(
        os.path.join(dataset_path, "yelp_academic_dataset_review.json"),
        lines=True,
        chunksize=10000
    )

    for df_chunk in dfs:
        for i, row in df_chunk.iterrows():
            review = Review(
                review_id=row["review_id"],
                date=row["date"],
                user_id=row["user_id"],
                business_id =row["business_id"],
                stars=row["stars"],
                useful=row["useful"],
                funny=row["funny"],
                cool=row["cool"],
                text=row["text"]
            )

            session.add(review)
        session.commit()

    session.close()


def insert_tips(dataset_path):
    session = Session()

    dfs = pd.read_json(
        os.path.join(dataset_path, "yelp_academic_dataset_tip.json"),
        lines=True,
        chunksize=10000
    )

    for df_chunk in dfs:
        for i, row in df_chunk.iterrows():
            tip = Tip(
                date = row["date"],
                user_id = row["user_id"],
                business_id = row["business_id"],
                text = row["text"],
                compliment_count = row["compliment_count"]
            )
            session.add(tip)
        session.commit()
    session.close()


def insert_checkins(dataset_path):
    session = Session()

    dfs = pd.read_json(
        os.path.join(dataset_path, "yelp_academic_dataset_checkin.json"),
        lines=True,
        chunksize=10000
    )

    for df_chunk in dfs:
        for i, row in df_chunk.iterrows():
            for date in row["date"].split(","):
                date = datetime.strptime(
                    date.strip(),
                    "%Y-%m-%d %H:%M:%S"
                )

                checkin = Checkin(
                    date=date,
                    business_id=row["business_id"]
                )

            session.add(checkin)
        session.commit()
    session.close()


if __name__ == "__main__":
    logging.info("Creating database")
    create_db(DATABASE_URL)

    logging.info("Inserting users")
    insert_users(DATASET_PATH)

    logging.info("Inserting businesses")
    insert_businesses(DATASET_PATH)

    logging.info("Inserting reviews")
    insert_reviews(DATASET_PATH)

    logging.info("Inserting tips")
    insert_tips(DATASET_PATH)

    logging.info("Inserting checkins")
    insert_checkins(DATASET_PATH)
