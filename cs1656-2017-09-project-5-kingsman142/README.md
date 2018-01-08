# Repository: 2017-09.template.project-5
# Assignment #5: Neo4j / Cypher

> Course: **[CS 1656 - Introduction to Data Science](http://cs1656.org)** (CS 2056) -- Fall 2017    
> Instructor: [Alexandros Labrinidis](http://labrinidis.cs.pitt.edu)  
> 
> Assignment: #5
> Released: December 3, 2017  
> **Due:      December 13, 2017**

### Description
This is the **fifth assignment** for the CS 1656 -- Introduction to Data Science (CS 2056) class, for the Fall 2017 semester.

### Goal
The goal of this assignment is for you to gain familiarity with Graph Databases in general, and with Neo4j and, its query language, Cypher, in particular.

---

### What to do

In this assignment you are asked to:  
* download neo4j locally,  
* download the Movies database locally,   
* provide Cypher queries that answer 6 questions, and        
* write a Python script ('movie-queries.py') that will run your solutions for the 6 queries and store the query output in a file. 

### Database Model

We will use the Movies database <https://neo4j.com/developer/movie-database/>, which has the following node labels:
* Actor  
* Director  
* Movie  
* Person  
* User  
and the following relationship types (i.e., edge labels):
* ACTS_IN  
* DIRECTED  
* FRIEND  
* RATED  

The nodes in the Movies database have a number of attributes, including the following:
* name (for Actor/Director/Person/User)  
* birthday (for Actor/Director/Person/User)  
* title (for Movie)  
* genre (for Movie)  


### Setup 

You are asked to follow the installation instructions provided as part of this repository (`Installation.Setup.Neo4j.Linux.pdf` or `Installation.Setup.Neo4j.Windows.pdf`). This will enable you to have a locally running neo4j server, along with an interactive query interface. You will also be able to download the Movies database directly into neo4j.

Please note that although we will use the same database model for testing your submissions, it will not necessarily be identical to the one you will download.


### Connecting to neo4j using Python

As part of this repository, you are provided with a sample Python script (`cypher_sample1.py`) that connects to the local graph database (which you have established by following the previous steps).


### Queries

You are asked to provide Cypher queries that provide answers for the following questions. Note that **actors** refers to both male and female actors, unless explicitly specified otherwise. 

* **[Q1]** List all the actors who played in the movie entitled `"Apollo 13"`.  
*OUTPUT*: actor_name

* **[Q2]** List all the directors in descending order of the number of films they directed.  
*OUTPUT*: director_name, number_of_films_directed 

* **[Q3]** Find the movie with the largest cast.    
*OUTPUT*: movie_title, number_of_cast_members

* **[Q4]** Find all the actors who have worked with at least 3 different directors (i.e., acted in at least 3 different movies with distinct directors).    
*OUTPUT*: actor_name, number_of_directors_he/she_has_worked_with

* **[Q5]** The Bacon number of an actor is the length of the shortest path between the actor and Kevin Bacon in the *"co-acting"* graph. That is, Kevin Bacon has Bacon number 0; all actors who acted in the same movie as him have Bacon number 1; all actors who acted in the same film as some actor with Bacon number 1 have Bacon number 2, etc. List all actors whose Bacon number is 2 (first name, last name). You can familiarize yourself with the concept, by visiting [The Oracle of Bacon](https://oracleofbacon.org).  
*OUTPUT*: actor_name

* **[Q6]** Should the Kevin Bacon game be renamed? Is there a different actor with a higher number of first-level connections in the co-acting graph? Compute the number of co-actors for each actor and return the top 50 highest (sorted in descending order).  
*OUTPUT*: actor_name, number_of_co_actors

### Output Format (ignore at your own risk!)

You are asked to store the output for running all Cypher queries by your python script in a **single** file, named `output.txt`. For each query, you should have a header line `### Q1 ###`, followed by the results of the query (one row at a time, with commas separating multiple fields). If you do not provide an answer for the query, you should still print the header line in your output file, but leave a blank line after it.

For example, for the following question:

Q0: show the 3 oldest actors in the database, with the oldest one first.  
*OUTPUT*: name, id

The corresponding Cypher query should be:
```
match (n:Actor) return n.name, n.id order by n.birthday ASC LIMIT 3
```

The output file should be as follows:
```
### Q0 ###
Claudia Cardinale,4959
Oliver Reed,936
Anthony Hopkins,4173
```


---


### Important notes about grading
It is absolutely imperative that your python program:  
* runs without any syntax or other errors (using Python 3) -- we will run it using the following command:  
`python3 movie-queries.py`  
* generates file `output.txt` with the answers of all 6 queries  
* strictly adheres to the format specifications for output, as explained above.     

Failure in any of the above will result in **severe** point loss. 


### Allowed Python Libraries
You are allowed to use the following Python libraries:
```
argparse
collections
csv
glob
neo4j.v1
os
pandas
re
string
sqlite3
sys
```
If you would like to use any other libraries, you must ask permission by Friday, December 8th, 2017, using [piazza](http://piazza.cs1656.org).

---


### How to submit your assignment
For this assignment, you must use the repository that was created for you after visiting the classroom link. You need to create the  file `movie-queries.py` as described above, and add other files that are needed for running your program. You need to make sure to commit your code to the repository provided. We will clone all repositories shortly after midnight:  
* the day of the deadline **Wednesday, December 13th, 2017 (i.e., at 12:15am, Thursdsay, December 14th, 2017)**  
* no late submissions are allowed.


### About your github account
It is very important that:  
* Your github account can do **private** repositories. If this is not already enabled, you can do it by visiting <https://education.github.com/>  
* You use the same github account for the duration of the course.  
* You use the github account that you specified during the test assignment.    
