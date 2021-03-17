# Yelp Dataset & SQLAlchemy ORM

This repository maps the [Yelp Dataset](https://www.yelp.com/dataset) to a
relational database model using [SQL Alchemy](https://www.sqlalchemy.org/).

## 1. Usage

### 1.1 Dataset

Download the dataset here: [Kaggle](https://www.kaggle.com/yelp-dataset/yelp-dataset).
The dataset files must go in the [data](./data) folder, at the root of
this repository.

### 1.2 Setup

``` bash
virtualenv venv -p python3;
source venv/bin/activate;
pip install -r requirements.txt;
```
