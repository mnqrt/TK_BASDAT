from collections import namedtuple
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

try:
    connection = psycopg2.connect(user="postgres.bifgoiocecmaulszyldt",
                        password="ZtQSa7t2(7Va.@e",
                        host="aws-0-ap-southeast-1.pooler.supabase.com",
                        port="5432",
                        database="postgres")

    connection.autocommit = True
    cursor = connection.cursor()
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)


def map_cursor(cursor):
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [dict(row) for row in cursor.fetchall()]


def query(query_str: str):
    hasil = []
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SET SEARCH_PATH TO TK_BASDAT")
        try:
            cursor.execute(query_str)
            if query_str.strip().upper().startswith("SELECT"):
                hasil = map_cursor(cursor)
            else:
                hasil = cursor.rowcount
                connection.commit()
        except Exception as e:
            hasil = e

    return hasil