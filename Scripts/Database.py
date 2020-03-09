import sqlite3
from sqlite3 import Error
from datetime import date, timedelta

class DBConnector:

	def __init__(self, db_file):
		self.db_file = db_file
		self.connection = None
		self.cursor = None		

	## Creates a database connection	
	def createConnection(self):
		conn = None
		try:
			conn = sqlite3.connect(self.db_file)			
			print("Database Connected")
		except Error as e:
			print(e)		
					
		self.connection = conn
		self.cursor = self.connection.cursor()


	## Closes the current database connection
	def closeConnection(self):
		self.connection.close()
		print("Database Closed")


	## Creates a new table in the database if it doesn't exist already
	def createTable(self, table):
		create_main_table = "CREATE TABLE IF NOT EXISTS "+table+""" 		         			
							(
							id INTEGER PRIMARY KEY,
							body TEXT NOT NULL,
							claim TEXT NOT NULL,
							score NUMERIC NOT NULL,
							context TEXT NOT NULL,
							newsInsert TEXT NOT NULL,
							pdfLink TEXT NOT NULL
							);
							"""

		self.cursor.execute(create_main_table)


	## Checks if the table exists
	def tableExists(self, table):
		sql = "SELECT count(name) FROM sqlite_master WHERE type=\"table\" AND name=\""+table+"\" ;"

		self.cursor.execute(sql)

		if self.cursor.fetchone()[0] == 1:
			return True
		else:
			return False


	## Inserts the data into the given table
	def insertData(self, table, data):
		sql = "INSERT INTO "+table+""" (body, claim, score, context, newsInsert, pdfLink)
					VALUES(?,?,?,?,?,?);"""

		self.cursor.execute(sql, data)
		self.connection.commit()

	## Selects all data from the table
	def selectAll(self, table):
		sql = "SELECT * FROM "+table+" ;"

		self.cursor.execute(sql)
		return self.cursor.fetchall()

	## Selects with given conditions - the SQL will need to be supplied for this function
	def selectByCondition(self, sql):
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	## Select daily claims to be put in the newsletter
	def selectDaily(self, table):
		sql = "SELECT id, body, claim, score, context, newsInsert, pdfLink FROM "+table+""" 
				ORDER BY score DESC
				LIMIT 10;
				"""

		self.cursor.execute(sql)
		return self.cursor.fetchall()

	## Updates the data for the table
	def updateData(self, table, data):
		sql = "UPDATE "+table+"""
				SET claim = ?,
					body = ?,
					score = ?,
					context = ?,
					newsInsert = ?,
					pdfLink = ?
				WHERE id = ?;
				"""

		self.cursor.execute(sql, data)
		self.connection.commit()

	## Deletes the selected data from the table
	def deleteData(self, table, id):
		sql = "DELETE FROM "+table+" WHERE id = ?;"

		self.cursor.execute(sql, data)
		self.connection.commit()

	## Deletes all data from the table
	def deleteAll(self, table):
		sql = "DELETE FROM "+table+" ;"

		self.cursor.execute(sql)
		self.connection.commit()

	## Deletes the table from the database
	def deleteTable(self, table):
		sql = "DROP TABLE "+table+" ;"
		
		self.cursor.execute(sql)
		self.connection.commit()
					









