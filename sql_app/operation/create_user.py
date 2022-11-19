# -*- coding: utf-8 -*-
import traceback

from sql_app import models
from sql_app.database import SessionLocal
from common import logger
from utils.crypts import EncryptAES


def get_db():
    """ Session generator """
    db_session = SessionLocal()
    try:
        # this is where the "work" happens!
        yield db_session
        # always commit changes!
        db_session.commit()
    except:
        # if any kind of exception occurs, rollback transaction
        db_session.rollback()
        raise
    finally:
        db_session.close()


def create_user(username: str, password: str, email: str, active: bool = True):
    """ 增加条目（insert语句） """
    passwd = EncryptAES().encode_aes(password)
    insert_data = models.AuthInfo(username=username, encrypted_password=passwd, email=email, is_active=active)
    try:
        db_gen = get_db()
        db = next(db_gen)
        db.add(insert_data)
        db.commit()
        db.refresh(insert_data)
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())


if __name__ == '__main__':
    create_user(
        username="admin",
        password="d888edf8-c9cc-444f-83e2-39bdac05c0c6",
        email="xiaoming@gmail.com",
        active=True
    )
