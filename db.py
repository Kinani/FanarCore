import psycopg2


def setup_db():
    dbconnection = psycopg2.connect("user='postgres' host='172.21.0.2' dbname='db'")
    db=dbconnection.cursor()
    db.execute("create extension if not exists cube;")
    db.execute("drop table if exists vectors")
    db.execute("create table vectors (id serial, file varchar, vec_low cube, vec_high cube);")
    db.execute("create index vectors_vec_idx on vectors (vec_low, vec_high);")


setup_db()
