# pyODBC
import settings
import pyodbc
try:
 cn2.close()
except:
 pass
# MariaDB/MySQL
#execfile("./settings.py")
conn = settings.moobar()

cn1 = pyodbc.connect(conn, autocommit=False)
c1=cn1.cursor()

def tabela(rez):
	try:
		for g in rez.description:
			print (g[0], end="\t")
		print("\n"+"-"*31)
		for r in rez.fetchall():
			for a in r:
				print(a, end="\t")
			print()
		print("Vseh vrstic je", rez.rowcount)
	except Exception(e):
	 pass


c1.execute("SELECT * FROM movies LIMIT 5")
tabela(c1)
