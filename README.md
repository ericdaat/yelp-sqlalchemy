# Yelp Dataset & SQLAlchemy ORM

This repository maps the [Yelp Dataset](https://www.yelp.com/dataset) to a
relational database model using [SQL Alchemy](https://www.sqlalchemy.org/).

The database model schema can be found in [this PDF file](docs/db.pdf).

## 1. Usage

### 1.1 Dataset

Download the dataset here: [Kaggle](https://www.kaggle.com/yelp-dataset/yelp-dataset).
The dataset files must go in the [data/real](./data/real) folder.

### 1.2 Setup

Create a python virtual environment and install the required packages.

``` bash
virtualenv venv -p python3;
source venv/bin/activate;
pip install -r requirements.txt;
```

### 1.3 Running

Launch the [init_db.py](./src/init_db.py) script.

``` bash
python src/init_db.py
```

The sqlite database file will be located at the root of the repository,
under the name `db.sqlite`.
