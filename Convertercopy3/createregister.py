import sqlite3

conn = sqlite3.connect('/Users/lol/Downloads/Convertercopy3/registration1.db')

conn.execute('CREATE TABLE register(id INT AUTO_INCREMENT PRIMARY KEY, name varchar(100), email varchar(100), username varchar(30), password varchar(100),register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')

conn.close()
