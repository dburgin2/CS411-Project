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

# mycursor.execute("CREATE TABLE IF NOT EXISTS Stocks (Symbol VARCHAR(255), Date_Recorded Date, Open DECIMAL(19,6), High DECIMAL(19,6), Low DECIMAL(19,6), Close DECIMAL(19,6), Adj_Close DECIMAL(19,6), Volume INT)")
#
# directory = r'/Users/hearth/PycharmProjects/UIUC/CS411/CS411-Project/Backend/archive/stocks/'
# for filename in os.listdir(directory):					# Filename = A.csv
# 	processed_filename = os.path.splitext(filename)[0]  # Processed_filename = A
# 	print(processed_filename)
# 	f = open((directory + filename), "r")
# 	first_line = f.readline()
# 	lines = f.readlines()
# 	last_lines = lines[-30:]
# 	for row in last_lines:
# 		processed_row = row.strip().split(",")
# 		processed_row.insert(0, processed_filename)
# 		if '' in processed_row:
# 			continue
# 		sql_insert_query = "INSERT INTO Stocks(Symbol, Date_Recorded, Open, High, Low, Close, Adj_Close, Volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
# 		val = tuple(processed_row)
# 		mycursor.execute(sql_insert_query, val)
# 		db.commit()
# ​
# mycursor.execute("CREATE TABLE IF NOT EXISTS Stocks (Symbol VARCHAR(255), Date_Recorded Date, Open DECIMAL(19,6), High DECIMAL(19,6), Low DECIMAL(19,6), Close DECIMAL(19,6), Adj_Close DECIMAL(19,6), Volume INT)")

# mycursor.execute("CREATE TABLE IF NOT EXISTS Symbols (Symbol VARCHAR(255) PRIMARY KEY, Security_Name VARCHAR(255))")
# with open('/Users/hearth/PycharmProjects/UIUC/CS411/CS411-Project/Backend/archive/symbols_valid_meta.csv', 'r') as f:
# 	csv_reader = csv.reader(f)
# 	next(csv_reader)
# 	for line in csv_reader:
# 		sql_query = "INSERT INTO Symbols(Symbol, Security_Name) VALUES (%s, %s)"
# 		del line[0:1]
# 		del line[2:]
# 		line_tuple = tuple(line)
# 		mycursor.execute(sql_query, line_tuple)
# 		db.commit()


#FIX UTX#, CARR#, AGM-A in new Symbol Table
mycursor.execute("UPDATE Symbols SET Symbol = %s WHERE Symbol = %s", ('UTX#','UTX.V'))
db.commit()
mycursor.execute("UPDATE Symbols SET Symbol = %s WHERE Symbol = %s", ('AGM-A','AGM$A'))
mycursor.execute("UPDATE Symbols SET Symbol = %s WHERE Symbol = %s", ('CARR#','CARR.V'))
db.commit()
mycursor.execute("ALTER TABLE Stocks ADD FOREIGN KEY(Symbol) REFERENCES Symbols(Symbol) ON DELETE CASCADE ON UPDATE CASCADE")
db.commit()