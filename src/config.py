import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p"
)

DATABASE_URL = "sqlite:///db.sqlite"
DATASET_PATH = os.path.join("data", "real")

TEST_DATABASE_URL = "sqlite:///:memory:"
TEST_DATASET_PATH = os.path.join("data", "test")
