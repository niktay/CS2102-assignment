import psycopg2


try:
    # TODO(Nik): Secrets management
    conn = psycopg2.connect(
        dbname='admin', user='admin',
        password='secret', host='localhost',
        port='5432',
    )
except Exception as e:
    # TODO(Nik): Error handling/logging
    print(e)

cur = conn.cursor()
try:
    # Create sample table to test database connection
    cur.execute('CREATE TABLE test (id serial PRIMARY KEY, num integer);')
except Exception as e:
    # TODO(Nik): Error handling/logging
    print(e)

conn.commit()
conn.close()
cur.close()
