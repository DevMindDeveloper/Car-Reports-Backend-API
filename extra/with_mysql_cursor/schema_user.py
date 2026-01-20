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
create table users_cred(
    id int auto_increment primary key,
    name varchar(20),
    email varchar(50)
);
"""
cursor.execute(table_sql_query)
conn.commit()

## close resources.
cursor.close()
conn.close()