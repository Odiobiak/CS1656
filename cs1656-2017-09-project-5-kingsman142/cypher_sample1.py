from neo4j.v1 import GraphDatabase, basic_auth

#driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "cs1656"), encrypted=False)
driver = GraphDatabase.driver("bolt://localhost", encrypted=False)
session = driver.session()

result = session.run("MATCH (people:Person) RETURN people.name LIMIT 10")
for record in result:
   print (record['people.name'])

session.close()
