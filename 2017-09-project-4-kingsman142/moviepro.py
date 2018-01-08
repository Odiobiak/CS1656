import sqlite3 as lite
import csv
import re
import pandas
import string
con = lite.connect('cs1656.sqlite')

with con:
	cur = con.cursor()

	########################################################################
	### CREATE TABLES ######################################################
	########################################################################
	# DO NOT MODIFY - START
	cur.execute('DROP TABLE IF EXISTS Actors')
	cur.execute("CREATE TABLE Actors(aid INT, fname TEXT, lname TEXT, gender CHAR(6), PRIMARY KEY(aid))")

	cur.execute('DROP TABLE IF EXISTS Movies')
	cur.execute("CREATE TABLE Movies(mid INT, title TEXT, year INT, rank REAL, PRIMARY KEY(mid))")

	cur.execute('DROP TABLE IF EXISTS Directors')
	cur.execute("CREATE TABLE Directors(did INT, fname TEXT, lname TEXT, PRIMARY KEY(did))")

	cur.execute('DROP TABLE IF EXISTS Cast')
	cur.execute("CREATE TABLE Cast(aid INT, mid INT, role TEXT)")

	cur.execute('DROP TABLE IF EXISTS Movie_Director')
	cur.execute("CREATE TABLE Movie_Director(did INT, mid INT)")
	# DO NOT MODIFY - END

	########################################################################
	### READ DATA FROM FILES ###############################################
	########################################################################
	# actors.csv, cast.csv, directors.csv, movie_dir.csv, movies.csv
	# UPDATE THIS
	actors = []
	with open('actors.csv') as actor_file:
		reader = csv.reader(actor_file)
		for row in reader:
			actors.append(row)

	cast = []
	with open('cast.csv') as cast_file:
		reader = csv.reader(cast_file)
		for row in reader:
			cast.append(row)

	directors = []
	with open('directors.csv') as directors_file:
		reader = csv.reader(directors_file)
		for row in reader:
			directors.append(row)

	movie_dir = []
	with open('movie_dir.csv') as movie_dir_file:
		reader = csv.reader(movie_dir_file)
		for row in reader:
			movie_dir.append(row)

	movies = []
	with open('movies.csv') as movies_file:
		reader = csv.reader(movies_file)
		for row in reader:
			movies.append(row)

	########################################################################
	### INSERT DATA INTO DATABASE ##########################################
	########################################################################
	# UPDATE THIS TO WORK WITH DATA READ IN FROM CSV FILES
	for actor in actors:
		actor[0] = actor[0].replace("'", "''")
		actor[1] = actor[1].replace("'", "''")
		actor[2] = actor[2].replace("'", "''")
		actor[3] = actor[3].replace("'", "''")
		cur.execute("INSERT INTO Actors VALUES(" + actor[0] + ", '" + actor[1] + "', '" + actor[2] + "', '" + actor[3] + "')")
	for person in cast:
		person[0] = person[0].replace("'", "''")
		person[1] = person[1].replace("'", "''")
		person[2] = person[2].replace("'", "''")
		cur.execute("INSERT INTO Cast VALUES(" + person[0] + ", " + person[1] + ", '" + person[2] + "')")
	for director in directors:
		director[0] = director[0].replace("'", "''")
		director[1] = director[1].replace("'", "''")
		director[2] = director[2].replace("'", "''")
		cur.execute("INSERT INTO Directors VALUES(" + director[0] + ", '" + director[1] + "', '" + director[2] + "')")
	for mov_dir in movie_dir:
		mov_dir[0] = mov_dir[0].replace("'", "''")
		mov_dir[1] = mov_dir[1].replace("'", "''")
		cur.execute("INSERT INTO Movie_Director VALUES(" + mov_dir[0] + ", " + mov_dir[1] + ")")
	for movie in movies:
		movie[0] = movie[0].replace("'", "''")
		movie[1] = movie[1].replace("'", "''")
		movie[2] = movie[2].replace("'", "''")
		movie[3] = movie[3].replace("'", "''")
		cur.execute("INSERT INTO Movies VALUES(" + movie[0] + ", '" + movie[1] + "', " + movie[2] + ", " + movie[3] + ")")

	con.commit()

	########################################################################
	### QUERY SECTION ######################################################
	########################################################################
	queries = {}

	# DO NOT MODIFY - START
	# DEBUG: all_movies ########################
	queries['all_movies'] = '''
SELECT * FROM Movies
'''
	# DEBUG: all_actors ########################
	queries['all_actors'] = '''
SELECT * FROM Actors
'''
	# DEBUG: all_cast ########################
	queries['all_cast'] = '''
SELECT * FROM Cast
'''
	# DEBUG: all_directors ########################
	queries['all_directors'] = '''
SELECT * FROM Directors
'''
	# DEBUG: all_movie_dir ########################
	queries['all_movie_dir'] = '''
SELECT * FROM Movie_Director
'''
	# DO NOT MODIFY - END

	########################################################################
	### INSERT YOUR QUERIES HERE ###########################################
	########################################################################
	# NOTE: You are allowed to also include other queries here (e.g.,
	# for creating views), that will be executed in alphabetical order.
	# We will grade your program based on the output files q01.csv,
	# q02.csv, ..., q12.csv

	# Q01 ########################
	queries['q01'] = '''
	SELECT a.fname, a.lname
	FROM Cast AS c
	INNER JOIN Actors AS a ON c.aid = a.aid
	WHERE c.aid in (SELECT c.aid
	                FROM Cast AS c
	                INNER JOIN Movies AS m ON m.mid = c.mid
	                WHERE m.year < 1951 AND m.year > 1900)
	  AND c.aid in (SELECT c.aid
	                FROM Cast AS c
	                INNER JOIN Movies AS m ON m.mid = c.mid
	                WHERE m.year > 1950 AND m.year < 2001)
	GROUP BY c.aid
'''

	# Q02 ########################
	queries['q02'] = '''
	SELECT title, year
	FROM Movies
	WHERE year IN (SELECT year
	               FROM Movies
	               WHERE title = "Rogue One: A Star Wars Story")
	   AND rank > (SELECT rank
	               FROM Movies
	               WHERE title = "Rogue One: A Star Wars Story"
	               LIMIT 1)
'''

	# Q03 ########################
	queries['q03'] = '''
	SELECT a.fname, a.lname
	FROM Actors AS a
	INNER JOIN Cast AS c ON a.aid = c.aid
	INNER JOIN Movies AS m ON m.mid = c.mid
	WHERE m.title = "Star Wars VII: The Force Awakens"
'''

	# Q04 ########################
	queries['q04'] = '''
	SELECT a.fname, a.lname
	FROM Actors AS a
	WHERE NOT a.aid IN (SELECT a2.aid
	                    FROM Actors AS a2
	                    INNER JOIN Cast AS c2 ON a2.aid = c2.aid
	                    INNER JOIN Movies AS m2 ON m2.mid = c2.mid
	                    WHERE m2.year > 1984)
'''

	# Q05 ########################
	queries['q05'] = '''
	SELECT d.fname, d.lname, COUNT(DISTINCT md.mid) AS num_films
	FROM Directors as d
	INNER JOIN Movie_Director as md ON d.did = md.did
	GROUP BY d.did
	ORDER BY num_films DESC
	LIMIT 20
'''

	# Q06 ########################
	queries['q06'] = '''
	SELECT m.title, COUNT(DISTINCT c.aid) AS num_cast
	FROM Movies AS m
	INNER JOIN Cast AS c ON c.mid = m.mid
	GROUP BY m.mid
	HAVING num_cast >= (SELECT MIN(num_cast2)
	                    FROM (SELECT COUNT(c2.aid) AS num_cast2
	                          FROM Movies AS m2
	                          INNER JOIN Cast AS c2 ON c2.mid = m2.mid
	                          GROUP BY m2.mid
	                          ORDER BY num_cast2 DESC
	                          LIMIT 10))
	ORDER BY num_cast DESC
'''

	# Q07 ########################
	queries['q07'] = '''
	SELECT m.title, IFNULL(WT.num_women_wt, 0) AS num_women, IFNULL(MT.num_men_mt, 0) AS num_men
	FROM Movies AS m
	INNER JOIN Cast AS c ON c.mid = m.mid
	INNER JOIN Actors AS a ON c.aid = a.aid
	LEFT JOIN (SELECT m2.mid, COUNT(*) AS num_men_mt
	           FROM Movies AS m2
	           INNER JOIN Cast AS c2 ON c2.mid = m2.mid
	           INNER JOIN Actors AS a2 ON c2.aid = a2.aid
	           WHERE a2.gender = "Male"
	           GROUP BY m2.mid) MT ON MT.mid = m.mid
	LEFT JOIN (SELECT m3.mid, COUNT(*) AS num_women_wt
	           FROM Movies AS m3
	           INNER JOIN Cast AS c3 ON c3.mid = m3.mid
	           INNER JOIN Actors AS a3 ON c3.aid = a3.aid
	           WHERE a3.gender = "Female"
	           GROUP BY m3.mid) WT ON WT.mid = m.mid
	WHERE num_women > num_men
	GROUP BY m.mid
'''

	# Q08 ########################
	queries['q08'] = '''
	SELECT a.fname, a.lname, COUNT(DISTINCT md.did) AS num_directors
	FROM Actors AS a
	INNER JOIN Cast AS c ON a.aid = c.aid
	INNER JOIN Movie_Director AS md ON c.mid = md.mid
	GROUP BY a.aid
	HAVING num_directors > 5
	    AND a.aid IN (SELECT a2.aid
	                  FROM Actors AS a2
	                  INNER JOIN Cast AS c2 ON c2.aid = a2.aid
	                  INNER JOIN Movies AS m2 ON m2.mid = c2.mid
	                  GROUP BY a2.aid
	                  HAVING COUNT(DISTINCT m2.mid) > 5)
'''

	# Q09 ########################
	queries['q09'] = '''
	SELECT a.fname, a.lname, COUNT(m.mid) AS num_movies
	FROM Actors AS a
	INNER JOIN Cast AS c ON a.aid = c.aid
	INNER JOIN Movies AS m ON c.mid = m.mid
	WHERE SUBSTR(a.fname, 1, 1) = 'S'
	    AND m.mid IN (SELECT m2.mid
	                  FROM Actors AS a2
	                  INNER JOIN Cast AS c2 ON a2.aid = c2.aid
	                  INNER JOIN Movies AS m2 ON c2.mid = m2.mid
	                  WHERE m.year = (SELECT MIN(m3.year)
	                                  FROM Actors AS a3
	                                  INNER JOIN Cast AS c3 ON a3.aid = c3.aid
	                                  INNER JOIN Movies AS m3 ON c3.mid = m3.mid
	                                  WHERE a3.aid = a.aid))
	GROUP BY a.aid
	ORDER BY num_movies DESC
'''

	# Q10 ########################
	queries['q10'] = '''
	SELECT a.lname, m.title
	FROM Actors AS a
	INNER JOIN Cast AS c ON a.aid = c.aid
	INNER JOIN Movies AS m ON c.mid = m.mid
	INNER JOIN Movie_Director AS md ON c.mid = md.mid
	INNER JOIN Directors AS d ON d.did = md.did
	WHERE a.lname = d.lname
	ORDER BY a.lname
'''

	# Q11 ########################
	# Get all actors with a movie ID in:
	# 	Get list of movie IDs with one of the following actors:
	# 		Get list of actor IDs that have acted in a movie with Kevin Bacon:
	# 			Get list of movie IDs that Kevin Bacon acted in
	queries['q11'] = '''
	SELECT DISTINCT(a.fname), a.lname
	FROM Actors AS a
	INNER JOIN Cast AS c ON a.aid = c.aid
	INNER JOIN Movies AS m ON m.mid = c.mid
	WHERE m.mid IN (SELECT DISTINCT(m2.mid)
	                FROM Actors AS a2
	                INNER JOIN Cast AS c2 ON a2.aid = c2.aid
	                INNER JOIN Movies AS m2 ON m2.mid = c2.mid
	                WHERE c2.aid IN (SELECT DISTINCT(a3.aid)
	                                 FROM Actors AS a3
	                                 INNER JOIN Cast AS c3 ON a3.aid = c3.aid
	                                 INNER JOIN Movies AS m3 ON c3.mid = m3.mid
	                                 WHERE m3.mid IN (SELECT c4.mid
	                                                  FROM Actors AS a4
	                                                  INNER JOIN Cast AS c4 ON a4.aid = c4.aid
	                                                  INNER JOIN Movies AS m4 ON c4.mid = m4.mid
	                                                  WHERE a4.fname = "Kevin" AND a4.lname = "Bacon")
	                                    AND NOT (a3.fname = "Kevin" AND a3.lname = "Bacon"))
	                    AND NOT (a2.fname = "Kevin" AND a2.lname = "Bacon")
	                    AND NOT m2.mid IN (SELECT c5.mid
	                                       FROM Actors AS a5
	                                       INNER JOIN Cast AS c5 ON a5.aid = c5.aid
	                                       INNER JOIN Movies AS m5 ON c5.mid = m5.mid
	                                       WHERE a5.fname = "Kevin" AND a5.lname = "Bacon"))
	    AND NOT (a.fname = "Kevin" AND a.lname = "Bacon")
	    AND NOT m.mid IN (SELECT c6.mid
	                      FROM Actors AS a6
	                      INNER JOIN Cast AS c6 ON a6.aid = c6.aid
	                      INNER JOIN Movies AS m6 ON c6.mid = m6.mid
	                      WHERE a6.fname = "Kevin" AND a6.lname = "Bacon")
	    AND NOT a.aid IN (SELECT DISTINCT(a7.aid)
	                      FROM Actors AS a7
	                      INNER JOIN Cast AS c7 ON a7.aid = c7.aid
	                      INNER JOIN Movies AS m7 ON c7.mid = m7.mid
	                      WHERE m7.mid IN (SELECT c8.mid
	                                       FROM Actors AS a8
	                                       INNER JOIN Cast AS c8 ON a8.aid = c8.aid
	                                       INNER JOIN Movies AS m8 ON c8.mid = m8.mid
	                                       WHERE a8.fname = "Kevin" AND a8.lname = "Bacon")
	                          AND NOT (a7.fname = "Kevin" AND a7.lname = "Bacon"))
'''

	# Q12 ########################
	queries['q12'] = '''
	SELECT a.fname, a.lname, COUNT(m.mid), AVG(m.rank) AS popularity
	FROM Actors AS a
	INNER JOIN Cast AS c ON a.aid = c.aid
	INNER JOIN Movies AS m ON c.mid = m.mid
	GROUP BY a.aid
	ORDER BY popularity DESC
	LIMIT 20
'''

	########################################################################
	### SAVE RESULTS TO FILES ##############################################
	########################################################################
	# DO NOT MODIFY - START
	for (qkey, qstring) in sorted(queries.items()):
		try:
			cur.execute(qstring)
			all_rows = cur.fetchall()

			print ("=========== ",qkey," QUERY ======================")
			print (qstring)
			print ("----------- ",qkey," RESULTS --------------------")
			for row in all_rows:
				print (row)
			print (" ")

			save_to_file = (re.search(r'q0\d', qkey) or re.search(r'q1[012]', qkey))
			if (save_to_file):
				with open(qkey+'.csv', 'w') as f:
					writer = csv.writer(f)
					writer.writerows(all_rows)
					f.close()
				print ("----------- ",qkey+".csv"," *SAVED* ----------------\n")

		except lite.Error as e:
			print ("An error occurred:", e.args[0])
	# DO NOT MODIFY - END
