import psycopg2


class Model(object):

    def __init__(self):
        try:
            # TODO(Nik): Secrets management
            conn = psycopg2.connect(
                dbname='admin', user='admin', password='secret', host='db',
                port='5432',
            )
        except Exception as e:
            # TODO(Nik): Error handling/logging
            print(e)
        finally:
            self.conn = conn

    def __del__(self):
        if self.conn:
            self.conn.close()
