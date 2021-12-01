import sqlite3

conn = sqlite3.connect('/Users/lol/Downloads/Convertercopy3/defaulttablefinal.db')

conn.execute('CREATE TABLE setdefault(selected_default_crypt varchar(50))')

conn.close()
