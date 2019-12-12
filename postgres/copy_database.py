# -*- coding: utf-8 -*-

"""
Script that can copy schema + data from one PostgreSQL into another PostgreSQL even on another server.
It's mostly used for DB migration. Data are copied by tables so some tables may be copied during application is still
running if tables are not modified. Data are copied in more processes so it faster than classical pg_dump/pg_restore
and also data are copied directly from source DB into destination DB and PostgreSQL streams are used so this is another
speed-up. You need to create destination database manually before migration of schema and data.

Setup:
    sudo apt-get install python3 python3-pip
    sudo apt-get install libpq-dev python3-dev
    pip install -U psycopg2 invoke docopt

Usage:
    copy schema --src=<postgres-url> --dest=<potgres-url> [--only-dump --delete-file]
    copy data --src=<postgres-url> --dest=<potgres-url> [(--only-tables=<names> | --ignore-tables=<names>)]

Options:
    --src=<postgres-url>     URL into source PostgreSQL database with valid credentials. Example: postgresql://postgres:postgres@localhost/original-sheep
    --dest=<potgres-url>     URL into destination PostgreSQL database with valid credentials. Example: postgresql://postgres:postgres@localhost/dolly-sheep
    --only-tables=<names>    Copy only specified tables and their sequences. Comma separated list of table names.
    --ignore-tables=<names>  Don't copy these tables. You want this probably because you already copied these by "--only-tables".
    -D, --no-delete-file     Delete file with dumped schema.
    --only-dump              Don't create schema in target DB. Only create file.

http://stackoverflow.com/questions/6765310/piping-postgres-copy-in-python-with-psycopg2
"""

import math
import os
import os.path
import threading
from concurrent.futures.process import ProcessPoolExecutor
from contextlib import closing
from datetime import datetime
from multiprocessing import current_process

import psycopg2
import psycopg2.extras
from docopt import docopt
from invoke import run

WORKERS = 4


def copy_data(src_postgres_url, dest_postgres_url, only_tables, ignore_tables):
    if only_tables:
        tables = only_tables.split(",")
    else:
        ignore_tables = ignore_tables.split(",") if ignore_tables else []
        with Database(src_postgres_url) as src_db:
            copy_sequences_state(src_db, dest_postgres_url)

            result = src_db.query("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'")
            tables = list(sorted(r["tablename"] for r in result if r["tablename"] not in ignore_tables))

    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        executor.map(copy_data_with_setup, ((src_postgres_url, dest_postgres_url, t) for t in tables))


def copy_sequences_state(src_db, dest_postgres_url):
    result = src_db.query("SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = 'public'")
    sequences = [r["sequence_name"] for r in result]

    with Database(dest_postgres_url) as dest_db:
        for sequence in sequences:
            result = src_db.query(f'SELECT "last_value" FROM "{sequence}"')
            last_value = list(result)[0]["last_value"] + 1  # advance counter just to be sure no duplicate PK occures
            dest_db.execute(f"SELECT pg_catalog.setval('{sequence}', {last_value}, true)")


def copy_data_with_setup(args):
    src_postgres_url, dest_postgres_url, table = args
    process = current_process()

    with Database(src_postgres_url) as src_db:
        read_fd, write_fd = os.pipe()

        thread = threading.Thread(target=run_db_consumer, args=(dest_postgres_url, read_fd, table))
        thread.start()

        start_time = datetime.now()
        with closing(os.fdopen(write_fd, "wb")) as stream:
            print("Start:", table, "-", process.name)
            src_db.copy_to(stream, table)

        thread.join()
        delta = datetime.now() - start_time
        print("End:", table, "-", process.name, "took", humanize_time(delta), "seconds")


def run_db_consumer(dest_postgres_url, read_fd, table):
    with Database(dest_postgres_url) as dest_db:
        dest_db.execute(f"""ALTER TABLE "{table}" DISABLE TRIGGER ALL""")
        dest_db.copy_from(os.fdopen(read_fd, "rb"), table)
        dest_db.execute(f"""ALTER TABLE "{table}" ENABLE TRIGGER ALL""")


def copy_schema(src_postgres_url, dest_postgres_url, delete_file, only_dump_schema):
    # dump
    run(
        'pg_dump --schema-only --no-security-labels --no-owner --no-privileges --quote-all-identifiers'
        f' --schema=public -f schema.sql "{src_postgres_url}"'
    )

    # import
    if not only_dump_schema:
        result = run(f'psql -f schema.sql "{dest_postgres_url}"', capture=True, warn=True)
        if result.failed:
            print(result.stderr)

    # cleanup
    if delete_file:
        run("rm schema.sql")


class Database:

    def __init__(self, postgres_url):
        self._db = psycopg2.connect(postgres_url)
        self._cursor = self._db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def __enter__(self):
        return self

    def __exit__(self, e, t, tb):
        self._cursor.close()
        self._db.close()

    def commit(self):
        self._db.commit()

    def execute(self, query):
        self._cursor.execute(query)
        self.commit()

    def query(self, query):
        self._cursor.execute(query)
        self.commit()
        return self._cursor.fetchall()

    def copy_from(self, stream, table):
        self._cursor.copy_expert(f"""COPY "{table}" FROM STDIN WITH (FORMAT 'binary')""", stream)

    def copy_to(self, stream, table):
        self._cursor.copy_expert(f"""COPY "{table}" TO STDOUT WITH (FORMAT 'binary')""", stream)


def humanize_time(time_delta):
    seconds = time_delta.total_seconds()
    times = [0, 0, 0]

    MINUTE_IN_SECONDS = 60
    HOUR_IN_SECONDS = 60 * MINUTE_IN_SECONDS

    if seconds > HOUR_IN_SECONDS:
        times[0] = int(seconds / HOUR_IN_SECONDS)
        seconds -= times[0] * HOUR_IN_SECONDS
    if seconds > MINUTE_IN_SECONDS:
        times[1] = int(seconds / MINUTE_IN_SECONDS)
        seconds -= times[1] * MINUTE_IN_SECONDS
    times[2] = math.ceil(seconds)

    return ":".join(str(t) for t in times if t > 0)


if __name__ == "__main__":
    args = docopt(__doc__)

    start_time = datetime.now()

    if args["schema"]:
        copy_schema(args["--src"], args["--dest"], args["--delete-file"], args["--only-dump"])
    elif args["data"]:
        copy_data(args["--src"], args["--dest"], args["--only-tables"], args["--ignore-tables"])

    delta = datetime.now() - start_time
    print("Total time =", humanize_time(delta), "seconds")
