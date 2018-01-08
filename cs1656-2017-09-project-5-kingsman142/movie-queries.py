from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost", encrypted=False)
session = driver.session()

output_string = ""

#print("### Q1 ###")
output_string += "### Q1 ###\n"
result = session.run("MATCH (actor:Actor)-[:ACTS_IN]->(movie:Movie {title: 'Apollo 13'}) RETURN actor.name AS actor_name")
for record in result:
   output_string += record['actor_name'] + "\n"
output_string += "\n"

#print("### Q2 ###")
output_string += "### Q2 ###\n"
result = session.run("MATCH (director:Director)-[:DIRECTED]->(movie:Movie) RETURN director.name AS director_name, COUNT(movie) AS number_of_films_directed ORDER BY number_of_films_directed DESC")
for record in result:
   output_string += record['director_name'] + "," + str(record['number_of_films_directed']) + "\n"
output_string += "\n"

#print("### Q3 ###")
output_string += "### Q3 ###\n"
result = session.run("MATCH (actor:Actor)-[:ACTS_IN]->(movie:Movie) RETURN movie.title AS movie_title, COUNT(actor) AS number_of_cast_members ORDER BY number_of_cast_members DESC LIMIT 1")
for record in result:
   output_string += record['movie_title'] + "," + str(record['number_of_cast_members']) + "\n"
output_string += "\n"

#print("### Q4 ###")
output_string += "### Q4 ###\n"
result = session.run("MATCH ((actor:Actor)-[:ACTS_IN]->(movie:Movie)<-[:DIRECTED]-(director:Director)) WITH actor, collect(DISTINCT director) AS num_directors WHERE length(num_directors) >= 3 RETURN actor.name AS actor_name, length(num_directors) AS `number_of_directors_he/she_has_worked_with`")
for record in result:
   output_string += record['actor_name'] + "," + str(record['number_of_directors_he/she_has_worked_with']) + "\n"
output_string += "\n"

#print("### Q5 ###")
output_string += "### Q5 ###\n"
result = session.run("MATCH (bacon2:Actor)-[:ACTS_IN]->(movie2:Movie)<-[:ACTS_IN]-(bacon1:Actor)-[:ACTS_IN]->(movie:Movie)<-[:ACTS_IN]-(bacon0:Actor {name: 'Kevin Bacon'}) RETURN bacon2.name AS actor_name")
for record in result:
   output_string += record['actor_name'] + "\n"
output_string += "\n"

#print("### Q6 ###")
output_string += "### Q6 ###\n"
result = session.run("MATCH (newBacon:Actor)-[:ACTS_IN]->(movie:Movie)<-[:ACTS_IN]-(actor2:Actor) RETURN newBacon.name AS actor_name, COUNT(actor2) AS number_of_co_actors ORDER BY number_of_co_actors DESC LIMIT 50")
for record in result:
   output_string += record['actor_name'] + "," + str(record['number_of_co_actors']) + "\n"
output_string += "\n"

with open("output.txt", "w", encoding='utf-8') as output_file:
    output_file.write(output_string)

session.close()
