# import sqlite3

# connection  =  sqlite3.Connection("User.db")
# cursor  =  connection.cursor()

# cursor.execute("CREATE TABLE IF NOT EXISTS User(id Integer Primary Key,public_id str unique, username str unique, password str, email str unique, admin boolean)")

# inital_admin_user = ("1111_2222_3333_4444", "admin","admin","admin@palmerswole.com",False)

# insert_inital_admin = "INSERT INTO User VALUES( NULL, ?, ?, ?, ?, ?)"

# cursor.execute(insert_inital_admin,inital_admin_user)


# connection.commit()
# connection.close()

import psycopg2

connection  =  psycopg2.connect(host='localhost', user='PalmerstonAdmin'  , password='Admin', dbname='Palmerswole')
print(connection)
cursor  =  connection.cursor()
print(cursor)
#cursor.execute("CREATE TABLE IF NOT EXISTS Users (id serial Primary Key,public_id varchar(60) unique not null, username varchar(50) not null unique, password varchar(50), email varchar(50) not null unique, admin boolean)")

#cursor.execute("""insert into Users (public_id , username, password, email, admin)
#values ('1111_2222_3333_4444', 'admin','admin','admin@palmerswole.com', 'false' );""")

cursor.execute("select * from users")
x= cursor.fetchall()
print(type(x))
for a in x:
    print(a)


connection.commit()
connection.close()

##select column_name, data_type from information_schema.columns
# where table_name = 'users'