#!/usr/bin/env python3

import sqlite3 as SqliteDb
import sys
import platform
import os
from prettytable import PrettyTable # pip install PrettyTable

class SqliteAdmin:
	con = ''
	cur = ''

	def __init__(self):
		if (len(sys.argv) > 1):
			SqliteAdmin.con = SqliteDb.connect(sys.argv[1])
		else:
			SqliteAdmin.con = SqliteDb.connect("example.db")
		self.getTableList()
		self.getQueries()	

	def getTableList(self):
		SqliteAdmin.con.row_factory = SqliteDb.Row
		SqliteAdmin.cur = SqliteAdmin.con.cursor()
		SqliteAdmin.cur.execute("Select name FROM sqlite_master Where type='table';")
		rows = SqliteAdmin.cur.fetchall()
		tableList = PrettyTable(['Table(s)', 'No. Of Columns', 'Total Number of Rows'])
		for row in rows:
			SqliteAdmin.cur.execute("Select * FROM "+row['name'])
			fetchdata = SqliteAdmin.cur.fetchall()
			columnList = [description[0] for description in SqliteAdmin.cur.description]

			tableList.add_row([row['name'], len(columnList), len(fetchdata)])
		print(tableList)

	def getQueries(self):
		while True: 
			try:
				query = input("Query> :")
				if query != "":
					self.executeQuery(query)
			except SqliteDb.OperationalError:
				print('Oops invalid query Please try it again')

	def executeQuery(self,query):
		global cur
		try:
			SqliteAdmin.cur.execute(query)
			columnList = [description[0] for description in SqliteAdmin.cur.description]
			queryResult = PrettyTable(columnList)
			rows = SqliteAdmin.cur.fetchall()
			count = (len(rows))
			rd = 0
			result = []
			while rd < len(columnList):
				result.append('i['+str(rd)+']')
				rd+=1
			#print(result)
			for i in rows:				
				finalResult =  ','.join(result)
				x = len(result) 
				if x < 2:
					queryResult.add_row([eval(finalResult)])
				else:
					queryResult.add_row(eval(finalResult))
			print('Total Number of Row(s) Affected: ', count)
			print(queryResult)
		except TypeError:
			osType = platform.system()
			SqliteAdmin.con.commit()
			if osType != "Windows":
				os.system("clear")
			else:
				os.system("cls")
			self.getTableList()

SqliteAdmin = SqliteAdmin()