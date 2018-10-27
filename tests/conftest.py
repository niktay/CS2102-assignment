from datetime import datetime

import psycopg2
import pytest

from app.log import setup_logger

logger = setup_logger(__name__)
MOCK_TIME = datetime(1990, 12, 12, 12, 12, 12)


@pytest.fixture(scope='function')
def mock_db(monkeypatch):
    try:
        conn = psycopg2.connect(
            dbname='admin', user='admin', password='secret',
            host='127.0.0.1', port='1234',
        )

        conn.set_session(autocommit=True)

        cursor = conn.cursor()

        cursor.execute('DELETE FROM ride;')
        cursor.execute('DELETE FROM bid;')
        cursor.execute('DELETE FROM advertisement;')
        cursor.execute('DELETE FROM car;')
        cursor.execute('DELETE FROM driver;')
        cursor.execute('DELETE FROM account;')

        class mockdatetime():
            @classmethod
            def now(cls):
                return MOCK_TIME

        monkeypatch.setattr(f'app.model.driver.dt', mockdatetime)

        yield conn

        conn.close()
    except Exception as e:
        logger.error('Failed to establish database connection')
        logger.error(e)
