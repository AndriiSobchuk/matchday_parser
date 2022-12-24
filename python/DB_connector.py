import mysql.connector

config = {
  'host': 'mysql',
  'user': 'root',
  'password': 'password'
}

db_connect = mysql.connector.connect(**config)
cursor = db_connect.cursor()