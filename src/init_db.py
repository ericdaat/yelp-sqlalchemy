import os
import logging
from collections import defaultdict

import pandas as pd
from sqlalchemy_utils import create_database, database_exists

from src.config import DATABASE_URL, DATASET_PATH
from src.model import (
    metadata, engine, Session,
    User, Business, BusinessCategory,
    Review
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
            user = User(user_id=row["user_id"])
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


if __name__ == "__main__":
    logging.info("Creating database")
    create_db(DATABASE_URL)

    logging.info("Inserting users")
    insert_users(DATASET_PATH)

    logging.info("Inserting businesses")
    insert_businesses(DATASET_PATH)

    logging.info("Creating reviews")
    insert_reviews(DATASET_PATH)
