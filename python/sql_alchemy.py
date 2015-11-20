# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sqlalchemy import create_engine, MetaData, select


def main():
    engine = create_engine("postgresql://postgres:postgres@localhost/sqlalchemy")
    metadata = MetaData(bind=engine)
    metadata.reflect(schema="public")
    first_table = metadata.tables["public.first"]
    query = first_table.insert().values(data="styri")
    connection = engine.connect()
    print(query)
    result = connection.execute(query)
    print(result)
    query = select([first_table]).where(first_table.c.data.in_(["dva", "tri", "styri"]))
    print(query)
    result = connection.execute(query)
    print(list(result))

if __name__ == "__main__":
    main()
