from logging import getLogger

import psycopg2

logger = getLogger(__name__)


def connection_required(f):
    def wrapper(*args, **kwargs):
        if 'conn' in kwargs.keys():
            return f(*args, **kwargs)
        try:
            # TODO(Nik): Secrets management
            credentials = {
                'dbname': 'admin',
                'user': 'admin',
                'password': 'secret',
                'host': 'db',
                'port': '5432',
            }
            conn = psycopg2.connect(**credentials)

            result = f(*args, **kwargs, conn=conn)
            conn.close()
        except psycopg2.OperationalError:
            logger.error('Failed to establish database connection')
            logger.debug(credentials)
            raise

        return result
    return wrapper
