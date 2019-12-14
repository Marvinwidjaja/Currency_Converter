import sqlite3

conn = sqlite3.connect('/Users/lol/Downloads/Convertercopy2/database.db')

conn.execute('CREATE TABLE students (amount INT, from_curr TEXT, to_curr TEXT, amount_final INT)')

conn.close()
