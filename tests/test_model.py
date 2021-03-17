from src.model import Session, User, Business, Review


def test_users():
    session = Session()
    assert session.query(User).first()
    session.close()


def test_business():
    session = Session()
    assert session.query(Business).first()
    session.close()


def test_review():
    session = Session()
    assert session.query(Review).first()
    session.close()
