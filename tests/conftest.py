import os

from src import init_db
from src.config import TEST_DATABASE_URL, TEST_DATASET_PATH


def pytest_configure():
    init_db.create_db(TEST_DATABASE_URL)
    init_db.insert_users(TEST_DATASET_PATH)
    init_db.insert_businesses(TEST_DATASET_PATH)
    init_db.insert_reviews(TEST_DATASET_PATH)
    init_db.insert_tips(TEST_DATASET_PATH)
    init_db.insert_checkins(TEST_DATASET_PATH)
