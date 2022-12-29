import mysql.connector

# db_connect = mysql.connector.connect(
#     host="mysql",
#     user="root",
#     password="password"
# )
db_connect = mysql.connector.connect(
    host="172.17.0.2",
    user="root",
    password="password",
    port=3306
)
