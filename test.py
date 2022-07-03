import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()


lang_list = [
    ("Fortran", 1957),
    ("Python", 1991),
    ("Go", 2009),
]
cur.executemany("insert into lang values (?, ?)", lang_list)


cur.execute("select * from lang")
print(cur.fetchall())

con.close()