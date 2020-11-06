import mysql.connector

def fin_search(ticker):
   db = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="CS411RADS",
      database="Financial_Database"
   )
   mycursor = db.cursor()
   query = '''SELECT * FROM Stocks WHERE Symbol = "''' + ticker + '''"ORDER BY Date_Recorded DESC LIMIT 1;'''
   mycursor.execute(query)
   return_arr = []
   for x in mycursor:
      return_arr.append(x)
   return return_arr


def insert_security(ticker, security_name):
	if(type(ticker) == str and type(security_name) == str):
		query = "SELECT Symbol, Security_Name FROM Symbols WHERE Symbol = %(value)s "
		param = {'value' : ticker}
		mycursor.execute(query, param)
		row = mycursor.fetchone()
		if row == None:
			mycursor.execute("INSERT INTO Symbols(Symbol, Security_Name) VALUES (%s, %s)", (ticker, security_name))
			db.commit()
			print("Success! The symbol has been added.")
			return True
		else:
			print("Process failed. That symbol is already in use.")
			return False
	else:
		print("Process failed. Not a valid symbol.")
		return False

def delete_security(ticker):
	if(type(ticker) == str):
		query = "SELECT Symbol, Security_Name FROM Symbols WHERE Symbol = %(value)s "
		param = {'value' : ticker}
		mycursor.execute(query, param)
		row = mycursor.fetchone()
		if row == None:
			print("This ticker does not exist in the database.")
			return False
		else:
			query = "DELETE FROM Symbols WHERE Symbol = %(value)s "
			param = {'value' : ticker}
			mycursor.execute(query, param)
			db.commit()
			print("Deletion was a success.")
			return True
	else:
		print("This is not a valid ticker.")
		return False

def get_security_name(ticker):
	if(type(ticker) == str):
		query = "SELECT DISTINCT Security_Name FROM Symbols Where Symbol = %(value)s "
		param = {'value' : ticker}
		mycursor.execute(query, param)
		row = mycursor.fetchone()
		if row == None:
			return False
		else:
			return True, row[0]
	else:
		return False

def update_ticker(new_ticker, old_ticker):
	if(type(new_ticker) == str and type(old_ticker) == str):
		mycursor.execute("UPDATE Symbols SET Symbol = %s WHERE Symbol = %s", (new_ticker, old_ticker))
		db.commit()
		print("Success, "  +old_ticker +" has been changed to "+new_ticker)
		return True
	else:
		print("Invalid parameters.")
		return False

def update_security_name(ticker, new_security_name):
	if(type(ticker) == str and type(new_security_name) == str):
		mycursor.execute("UPDATE Symbols SET Security_Name = %s WHERE Symbol = %s", (new_security_name, ticker))
		db.commit()
		print("Success.")
		return True
	else:
		print("Invalid parameters")
		return False