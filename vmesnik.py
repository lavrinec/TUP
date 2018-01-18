import pyodbc
import tkinter



#connString = ""

#connection = pyodbc.connect(connString)

#cursor = connection.cursor()

import settings
conn = settings.moobar()
cn1 = pyodbc.connect(conn, autocommit=False)
cursor=cn1.cursor()


#okno
okno = tkinter.Tk()
okno.title('Izbira algoritma')
okno.geometry('300x400')

#input
entry=tkinter.Entry(okno)
entry.insert(0,"1")
entry.pack()


moznosti = tkinter.StringVar(okno)
moznosti.set("kolaborativni algoritem")
#drop down menu
opcije = tkinter.OptionMenu(okno, moznosti, "kolaborativni algoritem", "vsebinski algoritem", "hibridni algoritem")
opcije.pack()

def poizvedba():
    uporabnik=entry.get();
    if(moznosti.get()=="kolaborativni algoritem"):
        #poizvedba
        data1 = cursor.execute("SET @user="+uporabnik+";\n"
                              "SELECT movieId, (sum(ratings.rating)/100) as score\n, count(sim.userid) as nbratings\n"
                              "FROM (SELECT distances.userid AS userid,\n dist/(sqrt(my.norm)*sqrt(users.norm)) AS score\n"
                                "FROM (SELECT r.userId, sum((m.rating)*(r.rating)) AS dist\n"
                                "FROM ratings r, ratings m \n"
                                "WHERE m.movieId = r.movieId\n"
                                "AND r.userId != @user\n"
                                "AND m.userId = @user\n"
                                "GROUP BY r.userId\n"
                                ") as distances, \n"
                                "(SELECT userid, SUM((rating)*(rating)) AS norm FROM ratings GROUP BY userid) as users, \n"
                                "(SELECT sum((rating)*(rating)) AS norm FROM ratings WHERE userId = 1) as my \n"
                                "WHERE users.userid = distances.userid \n"
                                "ORDER BY score DESC\n"
                                "LIMIT 100 ) AS sim, ratings\n"
                                "WHERE sim.userid= ratings.userid\n"
                                "AND ratings.movieId NOT IN (SELECT movieId FROM ratings WHERE userId = 1)\n"
                                "GROUP BY movieId\n"
                                "ORDER BY score desc\n"
                                "LIMIT 15").fetchall()
        text="Rezultati poizvedbe: \n"


        for x in range(0, 15):#izpise rezultat
            text += str(data1[x][0]) + ", " + str(data1[x][1]) + ", " + str(data1[x][2]) + "\n"

            label.configure(text=text)




    if (moznosti.get() == "vsebinski algoritem"):
        #poizvedba
        data = cursor.execute("SET @user=" + uporabnik + ";\n"
                  "SELECT vsakfilm.movieId, vsakfilm.title, ROUND((vsakfilm.povprecje*(1+(stgenre/5))*(1-\n"
                  "ABS(leto.povleto-LEFT(RIGHT(vsakfilm.title,5),4))/100)),2) as fscore   FROM (SELECT\n"
                  "movies.movieId, movies.title, SUM(1) as stgenre, AVG(kriterij.score) as povprecje from \n"
                  "movies,(SELECT rating.genreIme, \n"
                  "AVG(((rating.stevilo/skup.sestevek)/(genr.genreSkupaj/skupina.sestevek))* rating.ratingi) as score\n"
                  "FROM (SELECT COUNT(filmi.genreIme) as stevilo, genreIme, AVG(filmi.rating) as ratingi \n"
                  " from (SELECT us.movieId, genr.genreIme, ratings.rating \n"
                  "FROM (SELECT movieId, userId \n"
                    "From ratings where userId=1) as us, genr, movies, ratings \n"
                  "where LOCATE(genr.genreIme, movies.genres) and us.movieId=movies.movieId and  \n"
                  "ratings.movieId=us.movieId and us.userId=ratings.userId \n"
                  "            ORDER by us.movieId ASC) as filmi  \n"
                  "  GROUP BY genreIme DESC) as rating, genr, (SELECT SUM(genreSkupaj) as sestevek FROM genr) as \n"
                  "skupina, (SELECT SUM(pos) as sestevek FROM(SELECT COUNT(genr.genreIme) as pos,genr.genreIme \n"
                  "from (SELECT movieId from ratings where userId=@user) as us, genr, movies\n"
                  "where LOCATE(genr.genreIme, movies.genres) and movies.movieId=us.movieId GROUP BY \n"
                  "genr.genreIme) as posebej) as skup  WHERE rating.genreIme=genr.genreIme\n"
                  "GROUP BY genreIme desc) as kriterij\n"
                  " where LOCATE(kriterij.genreIme,movies.genres) GROUP BY movies.movieId ORDER BY SUM(1)  desc) \n"
                    "as vsakfilm, (SELECT ROUND(AVG(LEFT(RIGHT(movies.title,5),4)),0) as povleto FROM ratings, movies  \n"
                    "WHERE ratings.userId=@user and ratings.movieId=movies.movieId) as leto\n"
                    "ORDER BY fscore desc\n"
                    "\n"
                  "LIMIT 15").fetchall()

        text = "Rezultati poizvedbe: \n"#izpise rezultat
        for x in range(0, 15):
            text+= str(data[x][0])+", "+data[x][1]+", "+str(data[x][2])+"\n"

        label.configure(text=text)


    if (moznosti.get() == "hibridni algoritem"):

        #poizvedbi
        data = cursor.execute("SET @user=" + uporabnik + ";\n"
             "SELECT vsakfilm.movieId, vsakfilm.title, ROUND((vsakfilm.povprecje*(1+(stgenre/5))*(1-\n"
             "ABS(leto.povleto-LEFT(RIGHT(vsakfilm.title,5),4))/100)),2) as fscore   FROM (SELECT\n"
             "movies.movieId, movies.title, SUM(1) as stgenre, AVG(kriterij.score) as povprecje from \n"
             "movies,(SELECT rating.genreIme, \n"
             "AVG(((rating.stevilo/skup.sestevek)/(genr.genreSkupaj/skupina.sestevek))* rating.ratingi) as score\n"
             "FROM (SELECT COUNT(filmi.genreIme) as stevilo, genreIme, AVG(filmi.rating) as ratingi \n"
             " from (SELECT us.movieId, genr.genreIme, ratings.rating \n"
             "FROM (SELECT movieId, userId \n"
             "From ratings where userId=@user) as us, genr, movies, ratings \n"
             "where LOCATE(genr.genreIme, movies.genres) and us.movieId=movies.movieId and  \n"
             "ratings.movieId=us.movieId and us.userId=ratings.userId \n"
             "            ORDER by us.movieId ASC) as filmi  \n"
             "  GROUP BY genreIme DESC) as rating, genr, (SELECT SUM(genreSkupaj) as sestevek FROM genr) as \n"
             "skupina, (SELECT SUM(pos) as sestevek FROM(SELECT COUNT(genr.genreIme) as pos,genr.genreIme \n"
             "from (SELECT movieId from ratings where userId=@user) as us, genr, movies\n"
             "where LOCATE(genr.genreIme, movies.genres) and movies.movieId=us.movieId GROUP BY \n"
             "genr.genreIme) as posebej) as skup  WHERE rating.genreIme=genr.genreIme\n"
             "GROUP BY genreIme desc) as kriterij\n"
             " where LOCATE(kriterij.genreIme,movies.genres) GROUP BY movies.movieId ORDER BY SUM(1)  desc) \n"
             "as vsakfilm, (SELECT ROUND(AVG(LEFT(RIGHT(movies.title,5),4)),0) as povleto FROM ratings, movies  \n"
             "WHERE ratings.userId=1 and ratings.movieId=movies.movieId) as leto\n"
             "ORDER BY fscore desc\n"
             "\n"
             "LIMIT 15").fetchall()

        data1 = cursor.execute("SET @user=" + uporabnik + ";\n"
                  "SELECT movieId, (sum(ratings.rating)/100) as score\n, count(sim.userid) as nbratings\n"
                  "FROM (SELECT distances.userid AS userid,\n dist/(sqrt(my.norm)*sqrt(users.norm)) AS score\n"
                  "FROM (SELECT r.userId, sum((m.rating)*(r.rating)) AS dist\n"
                  "FROM ratings r, ratings m \n"
                  "WHERE m.movieId = r.movieId\n"
                  "AND r.userId != @user\n"
                  "AND m.userId = @user\n"
                  "GROUP BY r.userId\n"
                  ") as distances, \n"
                  "(SELECT userid, SUM((rating)*(rating)) AS norm FROM ratings GROUP BY userid) as users, \n"
                  "(SELECT sum((rating)*(rating)) AS norm FROM ratings WHERE userId = 1) as my \n"
                  "WHERE users.userid = distances.userid \n"
                  "ORDER BY score DESC\n"
                  "LIMIT 100 ) AS sim, ratings\n"
                  "WHERE sim.userid= ratings.userid\n"
                  "AND ratings.movieId NOT IN (SELECT movieId FROM ratings WHERE userId = 1)\n"
                  "GROUP BY movieId\n"
                  "ORDER BY score desc\n"
                  "LIMIT 15").fetchall()

        text = "Rezultati poizvedbe: \n"
        for x in range(0, 3):#10x poveca kolaborativni score
            data1[x][1]=data1[x][1]*10;

        for x in range(0,15):#ce sta dva filma ista pusti tistega z vecjim score
            for y in range(0,15):
                if data[x][0]==data1[y][0]:
                    if data[x][2]>data1[x][1]:
                        data1[x][1]=-1
                    else:
                        data[x][2]=-1

        for x in range (0,15):#izpis poizvedbe
            text += str(data[x][0]) + ", " + data[x][1] + ", " + str(data[x][2]) + "\n"


        label.configure(text=text)

#gumb ki vodi do poizvedba
gumb = tkinter.Button(okno, text="Začni poizvedbo", command=poizvedba)
gumb.pack()

text="Rezultati poizvedb:\n"
#label
label = tkinter.Label(okno, text=text)
label.pack()
label.configure()


okno.mainloop()
