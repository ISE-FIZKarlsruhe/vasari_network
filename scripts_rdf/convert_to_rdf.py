from rdflib import Graph, Literal, URIRef, BNode, Namespace
from rdflib.namespace import FOAF , XSD, SKOS, RDFS
import csv
import json
import urllib.parse

# Create a Graph
g = Graph()

with open("./data/artists_names.json", "r", encoding="utf-8") as f:
    artists_names = json.load(f)

with open("./data/linked_artists.json", "r", encoding="utf-8") as f:
    linked_artists = json.load(f)

with open("./data/degrees.json", "r", encoding="utf-8") as f:
    degrees = json.load(f)

with open("./data/betweenness_centralities.json", "r", encoding="utf-8") as f:
    betweenness_centralities = json.load(f)

with open("./data/eigenvector_centralities.json", "r", encoding="utf-8") as f:
    eigenvector_centralities = json.load(f)


with open("./data/edges.csv", "r", encoding="utf-8") as f:
    edges = list(csv.DictReader(f))

ns1 = Namespace('https://ISE-FIZKarlsruhe.github.io/vasari_network/property/')

for artist, names in artists_names.items():
    first_name = names.get("first_name", "")
    full_name = names.get("full_name", "")
    surname = names.get("surname", "")
    alias = names.get("alias", "")
    artist_uri = URIRef("https://ISE-FIZKarlsruhe.github.io/vasari_network/entity/"+urllib.parse.quote(artist, safe=''))
    edges_artist = [row for row in edges if row["x"]==artist]
    wikidata_alias = linked_artists.get(artist, "")
    degree = degrees.get(artist, None)
    betweenness_centrality = betweenness_centralities.get(artist, None)
    eigenvector_centrality = eigenvector_centralities.get(artist, None)
    if len(first_name)>0:
        g.add((artist_uri, FOAF.firstName, Literal(first_name, lang="en")))
    if len(surname)>0:
        g.add((artist_uri, FOAF.surname, Literal(surname, lang="en")))
    if len(full_name)>0:
        g.add((artist_uri, FOAF.name, Literal(full_name, lang="en")))
    if len(alias)>0:
        g.add((artist_uri, SKOS.altLabel, Literal(alias, lang="en")))
    if len(wikidata_alias)>0:
        g.add((artist_uri, RDFS.seeAlso, URIRef(wikidata_alias[1:-1])))
    if degree:
        g.add((artist_uri, ns1.degree, Literal(degree, datatype=XSD.integer)))
    if betweenness_centrality:
        g.add((artist_uri, ns1.betweenness_centrality, Literal(betweenness_centrality, datatype=XSD.float)))
    if eigenvector_centrality:
        g.add((artist_uri, ns1.eigenvector_centrality, Literal(eigenvector_centrality, datatype=XSD.float)))
    for edge in edges_artist:
        bn = BNode()
        weight = Literal(edge["pmi_yx"], datatype=XSD.float)
        conn_node = URIRef("https://ISE-FIZKarlsruhe.github.io/vasari_network/entity/"+urllib.parse.quote(edge["y"], safe=''))
        g.add((bn, ns1.weight, weight))
        g.add((bn, ns1.isEdgeOf, artist_uri))
        g.add((bn, ns1.isEdgeOf, conn_node))

g.bind('vasari-property', ns1)
g.serialize(destination="../rdfs/vasari-kg.ttl")