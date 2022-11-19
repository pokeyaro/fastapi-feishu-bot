# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from sql_app import models
from sql_app.database import SessionLocal


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


def get_auth_info(username: str = None, password: str = None, email: str = None):
    # 不支持组合查询，只能链式调用filter方法
    try:
        db_gen = get_db()
        db = next(db_gen)
        if email is None:
            query_obj = db.query(models.AuthInfo).filter_by(username=username).filter_by(
                encrypted_password=password).filter_by(is_active=True).first()
        else:
            query_obj = db.query(models.AuthInfo).filter_by(email=email).filter_by(is_active=True).first()
        if query_obj is not None:
            return query_obj.entry
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
    return None

