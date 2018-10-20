import psycopg2
import pytest

from app.log import setup_logger

logger = setup_logger(__name__)


@pytest.fixture(scope='function')
def mock_db():
    try:
        conn = psycopg2.connect(
            dbname='admin', user='admin', password='secret',
            host='127.0.0.1', port='5432',
        )

        conn.set_session(autocommit=True)

        cursor = conn.cursor()

        cursor.execute('DELETE FROM account;')
        cursor.execute('DELETE FROM driver;')
        cursor.execute('DELETE FROM advertisement;')
        cursor.execute('DELETE FROM car;')
        cursor.execute('DELETE FROM bid;')
        cursor.execute('DELETE FROM ride;')

        yield conn

        conn.close()
    except Exception as e:
        logger.error('Failed to establish database connection')
        logger.error(e)
