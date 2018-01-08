
# coding: utf-8

# # CS 1656 – Introduction to Data Science 
# 
# ## Instructor: Alexandros Labrinidis / Teaching Assistant: Phuong Pham
# ### Additional credits: Zuha Agha, Anatoli Shein
# 
# ## Recitation 11: Cypher+Neo4j+Python
# ---
# In this recitation, we will query a Neo4j graph database using with Cypher language and Python.
# 
# Neo4j is a highly scalable, native graph database purpose-built to leverage not only data but also its relationships.
# 
# Cypher is a declarative graph query language that allows for expressive and efficient querying and updating of the graph store.

# In[1]:

from neo4j.v1 import GraphDatabase

#Connect to the database
driver = GraphDatabase.driver("bolt://localhost", encrypted=False)

#Start new session
session = driver.session()

#Start new transaction
transaction = session.begin_transaction()


# ### Queries
# __Q1) List any 10 actor names.__

# In[2]:

result = transaction.run("""
MATCH (people:Actor)
RETURN people.name
LIMIT 10
;""")
for record in result:
    print (record)


# __Q2) List any 10 movie titles.__

# In[3]:

result = transaction.run("""
MATCH (m:Movie)
RETURN m.title
LIMIT 10
;""")
for record in result:
    print (record)


# __Q3) List all actors in 'The Matrix' movie.__

# In[4]:

result = transaction.run("""
MATCH (m:Movie {title: 'The Matrix'})<-[:ACTS_IN]-(a:Actor)
RETURN a.name
;""")
for record in result:
    print (record)


# __Q4) List all actors who are also directors.__

# In[5]:

result = transaction.run("""
MATCH (a:Person)-[:DIRECTED]->(m:Movie)<-[:ACTS_IN]-(a:Person)
RETURN DISTINCT a.name
;""")
for record in result:
    print (record)


# __Q5) List acctors who acted in more than 50 movies, ordered by the number of the movies they acted in.__

# In[6]:

result = transaction.run("""
MATCH (a:Actor)-[:ACTS_IN]->(m:Movie)
WITH a, collect(m) AS movies
WHERE length(movies) >= 50
RETURN a.name, length(movies)
ORDER BY length(movies)
;""")
for record in result:
    print (record)


# ### Tasks
# __T1) Find the actor named "Tom Hanks".__

# In[ ]:




# __T2) Find the movie with title "Avatar".__

# In[ ]:




# __T3) Find movies released in the 1990s.__

# In[ ]:




# __T4) List all Tom Hanks movies.__

# In[ ]:




# __T5) Who directed "Avatar"?__

# In[ ]:




# __T6) Tom Hanks' co-actors.__

# In[ ]:




# __T7) How people are related to "Avatar".__

# In[ ]:




# __T8) Extend Tom Hanks co-actors, to find co-co-actors who haven't worked with Tom Hanks.__

# In[ ]:




# __T9) Find someone to introduce Tom Hanks to Tom Cruise.__

# In[ ]:




# __Let's close the session and the transaction.__

# In[7]:

transaction.close()
session.close()

