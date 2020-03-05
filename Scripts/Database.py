import sqlite3
from sqlite3 import Error
from datetime import date, timedelta

class DBConnector:

	def __init__(self, db_file):
		self.connection = self.createConnection(db_file)
		self.cursor = self.connection.cursor()		

	@staticmethod
	def createConnection(db_file):
		conn = None
		try:
			conn = sqlite3.connect(db_file)			
			print("Database Connected")
		except Error as e:
			print(e)		
					
		return conn

	def closeConnection(self):
		self.connection.close()
		print("Database Closed")

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

	def tableExists(self, table):
		sql = "SELECT count(name) FROM sqlite_master WHERE type=\"table\" AND name=\""+table+"\" ;"

		self.cursor.execute(sql)

		if self.cursor.fetchone()[0] == 1:
			return True
		else:
			return False

	def insertData(self, table, data):
		sql = "INSERT INTO "+table+""" (body, claim, score, context, newsInsert, pdfLink)
					VALUES(?,?,?,?,?,?);"""

		self.cursor.execute(sql, data)
		self.connection.commit()

	def selectAll(self, table):
		sql = "SELECT * FROM "+table+" ;"

		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def selectByCondition(self, sql):
		self.cursor.execute(sql)
		return self.cursor.fetchall()



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


	def deleteData(self, table, id):
		sql = "DELETE FROM "+table+" WHERE id = ?;"

		self.cursor.execute(sql, data)
		self.connection.commit()

	def deleteAll(self, table):
		sql = "DELETE FROM "+table+" ;"

		self.cursor.execute(sql)
		self.connection.commit()

	def deleteTable(self, table):
		sql = "DROP TABLE "+table+" ;"
		
		self.cursor.execute(sql)
		self.connection.commit()
					









