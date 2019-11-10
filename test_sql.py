import sqlite3
# from api import api_image

conn = sqlite3.connect('database.db')

c = conn.cursor()

# c.execute("select * from CreateUser")
# c.execute("select * from MyUsers where firstName = 'Pragya'")

email = "pragya9590@yahoo.in"
password = "Iampragya"
# c.execute("select * from CreateUser where email = \'{}\' and password =\'{}\'".format(email,password))
c.execute("select * from CreateUser")
print(c.fetchall())

conn.commit()
conn.close()