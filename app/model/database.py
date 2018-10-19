from logging import getLogger

import psycopg2

logger = getLogger(__name__)


def connection_required(test=False):
    def connection_required_decorator(f):
        def wrapper(*args, **kwargs):
            if test:
                try:
                    # Connection for unit tests
                    logger.info('Connecting to test database')
                    conn = psycopg2.connect(
                        dbname='admin', user='admin', password='secret',
                        host='testdb', port='5432',
                    )
                except Exception as e:
                    logger.error('Failed to establish database connection')
            else:
                try:
                    # TODO(Nik): Secrets management
                    conn = psycopg2.connect(
                        dbname='admin', user='admin', password='secret',
                        host='db', port='5432',
                    )
                except Exception as e:
                    logger.error('Failed to establish database connection')

            result = f(*args, **kwargs, conn=conn)
            conn.close()

            return result

        return wrapper
    return connection_required_decorator
