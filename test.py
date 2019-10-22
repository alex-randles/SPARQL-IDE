import rdflib 
g = rdflib.graph.Graph()
g.parse("output.ttl", format="n3")
result = g.query(" SELECT * WHERE { ?S ?P ?O }") 
dic = {"subjects":[],"predicates":[], "object":[]} 
for row in result:
	if row[2] in g.subjects():
		dic["subjects"].append(row[2])
	elif row[1] in g.predicates():
		dic["predicates"].append(row[1])
	elif row[0] in g.objects():
		dic["objects"].append(row[0])
print(dic) 
	
	
