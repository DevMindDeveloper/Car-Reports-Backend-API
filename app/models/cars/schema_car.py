import mysql.connector as mc
import config as c

## db creds
db_configs = {
    'host' : c.host,
    'user' : c.user,
    'password' : c.password,
    'database' : c.database
}

## initialization
conn = mc.connect(**db_configs)
cursor = conn.cursor()

table_sql_query = """
create table cars_report(
    id int auto_increment primary key,
    recordID varchar(50),
    date varchar(50),
    category varchar(50),
    model varchar(50),
    make varchar(50),
    year int(4)
);
"""
cursor.execute(table_sql_query)
conn.commit()

## close resources.
cursor.close()
conn.close()