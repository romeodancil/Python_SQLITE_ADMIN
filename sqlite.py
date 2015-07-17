#!/usr/bin/env python

import sqlite3 as liteDb
import sys

from prettytable import PrettyTable # pip install PrettyTable

# start checking database
if (len(sys.argv) > 1):
	con = liteDb.connect(sys.argv[1])
else:
	con = liteDb.connect("example.db")

cur = ''

def getTableList():
	con.row_factory = liteDb.Row
	global cur
	cur = con.cursor()
	c = con.cursor()
	cur.execute("Select name FROM sqlite_master Where type='table';")
	rows = cur.fetchall()
	tableList = PrettyTable(['Table(s)', 'No. Of Columns', 'Total Number of Rows'])
	for row in rows:
		cur.execute("Select * FROM "+row['name'])
		fetchdata = cur.fetchall()
		columnList = [description[0] for description in cur.description]

		tableList.add_row([row['name'], len(columnList), len(fetchdata)])
	print(tableList)

def getQueries():
	while True:
		try:
			query = input("Query> :")
			if query != "":
				selectQuery(query)
		except liteDb.OperationalError:
			print('Oops invalid query Please try it again')

def selectQuery(query):
	global cur
	cur.execute(query)
	columnList = [description[0] for description in cur.description]
	queryResult = PrettyTable(columnList)
	rows = cur.fetchall()
	count = (len(rows))
	rd = 0
	result = []
	while rd < len(columnList):
		result.append('i['+str(rd)+']')
		rd+=1
	for i in rows:
		finalResult =  ', '.join(result)
		queryResult.add_row(eval(finalResult))
	print('Total Number of Row(s) Affected: ', count)
	print(queryResult)

getTableList()
getQueries()