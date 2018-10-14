from logging import getLogger

import psycopg2


logger = getLogger(__name__)


class Model(object):

    def __init__(self):
        try:
            logger.info('Attempting to establish database connection')

            # TODO(Nik): Secrets management
            conn = psycopg2.connect(
                dbname='admin', user='admin', password='secret', host='db',
                port='5432',
            )

            logger.info('Database connection established')

        except Exception as e:
            logger.error('Failed to establish database connection')

        self.conn = conn

    def __del__(self):
        if self.conn:
            logger.info('Closing database connection')
            self.conn.close()
