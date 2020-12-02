import os
import mysql.connector
import csv

db = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = "CS411RADS",
	database = "Financial_Database"
	)


mycursor = db.cursor()

mycursor.execute("DROP TABLE Company_Sectors")
mycursor.execute("CREATE TABLE IF NOT EXISTS Company_Sectors (Symbol VARCHAR(255) PRIMARY KEY, Company_Name VARCHAR(255), Sector VARCHAR(255), Industry VARCHAR(255))")
with open(r'Backend/set_up_backend/companylist.csv', 'r') as f:
   csv_reader = csv.reader(f)
   next(csv_reader)
   for line in csv_reader:
      sql_query = "INSERT INTO Company_Sectors(Symbol, Company_Name, Sector, Industry) VALUES (%s, %s, %s, %s)"
      line_tuple = tuple(line)
      mycursor.execute(sql_query, line_tuple)
      db.commit()