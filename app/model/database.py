from logging import getLogger

import psycopg2

logger = getLogger(__name__)


def connection_required(f):
    def wrapper(*args, **kwargs):
        if 'conn' in kwargs.keys():
            return f(*args, **kwargs)
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
