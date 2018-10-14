#! /bin/sh

function postgres_ready() {
	python << END
import sys
import psycopg2

try:
	conn = psycopg2.connect(
		dbname='admin', user='admin', password='secret', host='db', port='5432',
	)
except psycopg2.OperationalError:
	sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
	>&2 echo "Waiting for Postgres - Sleeping"
	sleep 1
done

>&2 echo "Postgres started - Running Flask application"

python -u -m flask run --host=0.0.0.0
