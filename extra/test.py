import mysql.connector as mc

db_configs = {
    'host' : 'localhost',
    'user' : 'flaskuser',
    'password' : 'yourpassword',
    'database' : 'user_cred_db'
}
email = "ali@gmail.com"
password = "1213456789"
conn = mc.connect(**db_configs)
cursor = conn.cursor()

sql_query = "insert into users_cred (email, password) values (%s, %s)"
cursor.execute(sql_query, (email, password))
conn.commit()