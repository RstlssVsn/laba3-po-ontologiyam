from SPARQLWrapper import SPARQLWrapper, JSON

def do_sparql_query(query):
	sparql = SPARQLWrapper("http://sparql.org/sparql")
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	return sparql.query().convert()

def get_contributors_for_movie(name: str):
	results = do_sparql_query("""
PREFIX imdb: <http://data.linkedmdb.org/resource/movie/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT ?musicContributor ?genreName {
	{ SERVICE <http://data.linkedmdb.org/sparql>
		{ SELECT ?plainMusicContributor WHERE {
				?movie rdfs:label "%s" .
				?movie imdb:music_contributor ?musicContributorURI .
				?musicContributorURI imdb:music_contributor_name ?plainMusicContributor .
			}
		}
	}
	BIND(STRLANG(?plainMusicContributor, "en") as ?musicContributor).
	{ SERVICE <http://dbpedia.org/sparql>
		{ SELECT ?genreName ?musicContributor WHERE {
				?genreMusicContributor foaf:name ?musicContributor .
				?genreMusicContributor dbo:genre ?genre .
				?genreMusicContributor rdf:type dbo:Group .
				?genre rdf:type dbo:MusicGenre .
				?genre rdfs:label ?genreName .
				FILTER(langMatches(lang(?genreName), "en"))
			}
		}
	}
}
LIMIT 250
""" % name)
	return [{ 'contributor': row['musicContributor']['value'], 'genre': row['genreName']['value'] } for row in results['results']['bindings']]

def get_movies_for_genre(genre: str):
	results = do_sparql_query("""
PREFIX imdb: <http://data.linkedmdb.org/resource/movie/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT ?movieName ?contributorName {
        { SERVICE <http://dbpedia.org/sparql>
                { SELECT DISTINCT ?contributorName WHERE {
                                ?genre rdfs:label "%s"@en .
                                ?genre rdf:type dbo:MusicGenre .
                                ?matchingGenreMusicContributor dbo:genre ?genre .
                                ?matchingGenreMusicContributor foaf:name ?fullContributorName .
				?matchingGenreMusicContributor rdf:type dbo:Group .
				BIND(STR(?fullContributorName) as ?contributorName)
                        }
                }
        }
        { SERVICE <http://data.linkedmdb.org/sparql>
                { SELECT DISTINCT ?movieName ?contributorName WHERE {
                                ?musicContributorURI imdb:music_contributor_name ?contributorName .
                                ?movie rdfs:label ?movieName .
                                ?movie imdb:music_contributor ?musicContributorURI .
                        }
                }
        }
}
LIMIT 250
""" % genre)
	return [{ 'movie': row['movieName']['value'], 'contributor': row['contributorName']['value'] } for row in results['results']['bindings']]

def get_movies_for_contributor(name: str):
	results = do_sparql_query("""
PREFIX imdb: <http://data.linkedmdb.org/resource/movie/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?movieName {
	{ SERVICE <http://data.linkedmdb.org/sparql>
		{ SELECT DISTINCT ?movieName WHERE {
				?movie rdfs:label ?movieName .
				?movie imdb:music_contributor ?musicContributorURI .
				?musicContributorURI imdb:music_contributor_name "%s" .
			}
		}
	}
}""" % name)
	return [{ 'movie': row['movieName']['value'] } for row in results['results']['bindings']]

def get_genres_for_contributor(name: str):
	results = do_sparql_query("""
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT ?genreName {
	{ SERVICE <http://dbpedia.org/sparql>
		{ SELECT DISTINCT ?genreName WHERE {
				?musicContributor foaf:name "%s"@en .
				?musicContributor dbo:genre ?genre .
				?genre rdf:type dbo:MusicGenre .
				?genre rdfs:label ?genreName .
				FILTER(langMatches(lang(?genreName), "en"))
			}
		}
	}
}""" % name)
	return [{ 'genre': row['genreName']['value'] } for row in results['results']['bindings']]

