import os
import logging

logging.basicConfig(level=logging.INFO)

DATABASE_URL = "sqlite:///db.sqlite"
DATASET_PATH = os.path.join("data", "real")

TEST_DATABASE_URL = "sqlite:///:memory:"
TEST_DATASET_PATH = os.path.join("data", "test")
