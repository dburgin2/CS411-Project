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
   if len(return_arr) == 0:
      return False, return_arr
   return True, return_arr

def symbol_search(ticker):
   db = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="CS411RADS",
      database="Financial_Database"
   )
   mycursor = db.cursor()
   query = '''SELECT * FROM Symbols WHERE Symbol = "''' + ticker + '''" LIMIT 1;'''
   mycursor.execute(query)
   return_arr = []
   for x in mycursor:
      return_arr.append(x)
   return return_arr

#This function inserts a new Symbol and Security_Name into the Symbol table.
def insert_security(ticker, security_name):
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="CS411RADS",
		database="Financial_Database"
	)
	mycursor = db.cursor()
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
def insert_stocks(symbol, date, open, high, low, close, adj_close, volume):
   db = mysql.connector.connect(
         host="localhost",
         user="root",
         passwd="CS411RADS",
         database="Financial_Database"
      )
   mycursor = db.cursor()
   query = "INSERT INTO Stocks (Symbol, Date_Recorded, Open, High, Low, Close, Adj_Close, Volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
   val = (symbol, date, open, high, low, close, adj_close, volume)
   print(query)
   print(val)
   mycursor.execute(query, val)
   db.commit()

#This function deletes a ticker (a Symbol from the Symbols table) completely. This will cascade to Stocks, so all the company records in Stocks will be deleted.
def delete_security(ticker):
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="CS411RADS",
		database="Financial_Database"
	)
	mycursor = db.cursor()
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

#This function takes in a Symbol and outputs the Security_Name (Company_Name)
def get_security_name(ticker):
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="CS411RADS",
		database="Financial_Database"
	)
	mycursor = db.cursor()
	if(type(ticker) == str):
		query = "SELECT DISTINCT Security_Name FROM Symbols Where Symbol = %(value)s "
		param = {'value' : ticker}
		mycursor.execute(query, param)
		row = mycursor.fetchone()
		if row == None:
			return False, None
		else:
			return True, row[0]
	else:
		return False, None

#This function can update a Symbol in the Symbols table only - it changes a Symbol corresponding with old_ticker to new_ticker
def update_ticker(new_ticker, old_ticker):
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="CS411RADS",
		database="Financial_Database"
	)
	mycursor = db.cursor()
	if(type(new_ticker) == str and type(old_ticker) == str):
		mycursor.execute("UPDATE Symbols SET Symbol = %s WHERE Symbol = %s", (new_ticker, old_ticker))
		db.commit()
		print("Success, "  +old_ticker +" has been changed to "+new_ticker)
		return True
	else:
		print("Invalid parameters.")
		return False

#This function can update a Security_name in the Symbols table only - it changes a Security_name corresponding with a ticker Symbol
def update_security_name(ticker, new_security_name):
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="CS411RADS",
		database="Financial_Database"
	)
	mycursor = db.cursor()
	if(type(ticker) == str and type(new_security_name) == str):
		mycursor.execute("UPDATE Symbols SET Security_Name = %s WHERE Symbol = %s", (new_security_name, ticker))
		db.commit()
		print("Success.")
		return True
	else:
		print("Invalid parameters")
		return False

#This function gives the top 10 average(Open) from the Stocks table, and also provides the Security_Name
#It uses GROUP BY and a JOIN between 2 tables
def top_ten_price():
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="CS411RADS",
		database="Financial_Database"
	)
	mycursor = db.cursor()
	mycursor.execute("SELECT Stocks.Symbol, Symbols.Security_Name, avg(Open) as avgPrice FROM Stocks NATURAL JOIN Symbols GROUP BY Stocks.Symbol ORDER BY avgPrice DESC LIMIT 10")
	top_ten_list = []
	for x in mycursor:
		top_ten_list.append(list(x))
	return top_ten_list

def select_active_stocks():
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="CS411RADS",
		database="Financial_Database"
	)
	mycursor = db.cursor()
	mycursor.execute(
		"SELECT * FROM Active_Stocks")

	list_stocks = []
	for x in mycursor:
		list_stocks.append(list(x))
	return list_stocks

def second_complex_query():
   db = mysql.connector.connect(
               host="localhost",
               user="root",
               passwd="CS411RADS",
               database="Financial_Database"
            )
   mycursor = db.cursor()
   query = """SELECT Symbol, MAX(Volume) as MaxVolume FROM Stocks GROUP BY Symbol
         UNION
         SELECT Symbol, MIN(Volume) AS Volume
         FROM Stocks
         GROUP BY Symbol
         ORDER BY MaxVolume DESC
         LIMIT 10"""
   mycursor.execute(query)
   return_arr = []
   for x in mycursor:
      return_arr.append(list(x))
   if len(return_arr) == 0:
      return False
   return True, return_arr


def GetUserStocks(input_price, input_sector, input_volatility):
   db = mysql.connector.connect(
                  host="localhost",
                  user="root",
                  passwd="CS411RADS",
                  database="Financial_Database"
               )
   mycursor = db.cursor()
   mycursor.callproc('GetUserStocks', (input_price, input_sector, input_volatility))
   return_arr = []
   for result in mycursor.stored_results():
      return_arr.append(result.fetchall())
   if len(return_arr[0]) == 0:
      return False
   return return_arr[0]

def GetGOOGLPrediction(input_date):
   db = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="CS411RADS",
      database="Financial_Database"
   )
   mycursor = db.cursor()
   mycursor.callproc('GetGOOGLPrediction', (input_date,))
   return_arr = []
   for result in mycursor.stored_results():
      return_arr.append(result.fetchall())
   if len(return_arr[0]) == 0:
      return False
   return list(return_arr[0][0])