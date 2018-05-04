import sqlite3

connection  =  sqlite3.Connection("User.db")
cursor  =  connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS User(id Integer Primary Key,public_id str unique, username str unique, password str, email str unique, admin boolean)")

inital_admin_user = ("1111_2222_3333_4444", "admin","12345","admin@palmerswole.com",False)

insert_inital_admin = "INSERT INTO User VALUES( NULL, ?, ?, ?, ?, ?)"

cursor.execute(insert_inital_admin,inital_admin_user)


connection.commit()
connection.close()

