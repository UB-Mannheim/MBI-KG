# SPARQL examples

This page contains SPARQL queries from https://mbi.kgi.uni-mannheim.de/wiki/SPARQL_examples.

== Companies ==

=== Companies with labels, inception, Postscheckkonto, Fernruf and Drahtanschrift ===

{{SPARQL|query=
SELECT DISTINCT ?company ?companyLabel (year(?inc) as ?inception) ?POSTSCHECKKONTO ?FERNRUF ?DRAHTANSCHRIFT WHERE {
  ?company rdfs:label ?companyLabel;
    wdt:P3 wd:Q1.
  OPTIONAL { ?company wdt:P46 ?inc. }
  OPTIONAL { ?company wdt:P7 ?POSTSCHECKKONTO. }
  OPTIONAL { ?company wdt:P8 ?FERNRUF. }
  OPTIONAL { ?company wdt:P9 ?DRAHTANSCHRIFT. }
  FILTER((LANG(?companyLabel)) = "de")
}
}}

=== Companies with labels, Inhaber, Geschäftsführer and Bankverbindungen ===

{{SPARQL|query=
SELECT DISTINCT ?company ?companyLabel ?INHABER ?GESCHÄFTSFÜHRER ?BANKVERBINDUNGEN WHERE {
  ?company rdfs:label ?companyLabel;
    wdt:P3 wd:Q1.
  OPTIONAL { ?company wdt:P12 ?INHABER. }
  OPTIONAL { ?company wdt:P18 ?GESCHÄFTSFÜHRER. }
  OPTIONAL { ?company wdt:P10 ?BANKVERBINDUNGEN. }
  FILTER((LANG(?companyLabel)) = "de")
}
}}

=== Companies with labels, raw texts and file segments ===

{{SPARQL|query=
SELECT DISTINCT ?company ?companyLabel ?RAW_TEXT ?FILE_SEGMENT WHERE {
  ?company rdfs:label ?companyLabel;
    wdt:P3 wd:Q1;
    wdt:P4 ?RAW_TEXT;
    wdt:P5 ?FILE_SEGMENT.
  FILTER((LANG(?companyLabel)) = "de")
}
}}

=== Companies with labels, Postscheckkonto, Fernruf, Drahtanschrift and inception in time interval 1905-1910 ===

{{SPARQL|query=
SELECT DISTINCT ?company ?companyLabel (YEAR(?inc) AS ?inception) ?POSTSCHECKKONTO ?FERNRUF ?DRAHTANSCHRIFT WHERE {
  ?company rdfs:label ?companyLabel;
    wdt:P3 wd:Q1.
  OPTIONAL { ?company wdt:P46 ?inc. }
  FILTER(?inc >= "1905-01-01T00:00:00Z"^^xsd:dateTime)
  FILTER(?inc <= "1910-01-01T00:00:00Z"^^xsd:dateTime)
  OPTIONAL { ?company wdt:P7 ?POSTSCHECKKONTO. }
  OPTIONAL { ?company wdt:P8 ?FERNRUF. }
  OPTIONAL { ?company wdt:P9 ?DRAHTANSCHRIFT. }
  FILTER((LANG(?companyLabel)) = "de")
}
}}

=== Map with headquarters of companies ===

{{SPARQL|query=
#defaultView:Map
SELECT DISTINCT ?item ?itemLabel ?city ?cityLabel ?geo WHERE {
  ?item wdt:P3 wd:Q1;
    wdt:P48 ?city.
  ?city wdt:P3 wd:Q5157;
    wdt:P50 ?geo.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "de". }
}
}}

== Entities ==

=== Entities with labels  ===

{{SPARQL|query=
SELECT DISTINCT ?entity ?entityLabel WHERE {
  ?entity rdfs:label ?entityLabel.
  FILTER((LANG(?entityLabel)) = "en")
}
}}

== Properties ==

=== Properties with labels, aliases, descriptions and datatypes  ===

{{SPARQL|query=
SELECT DISTINCT ?propertyWikibase ?propertyLabel ?propertyAlias ?propertyDescription ?propertyType WHERE {
  ?propertyWikibase wikibase:directClaim ?p;
    wikibase:propertyType ?propertyType;
    schema:description ?propertyDescription;
    rdfs:label ?propertyLabel.
  OPTIONAL { ?propertyWikibase skos:altLabel ?propertyAlias. }
}
}}

=== Properties with non-capitalized labels and their datatypes  ===

{{SPARQL|query=
SELECT DISTINCT ?propertyWikibase ?propertyLabel ?propertyType WHERE {
  ?propertyWikibase wikibase:directClaim ?p;
    wikibase:propertyType ?propertyType;
    rdfs:label ?propertyLabel.
  FILTER(REGEX(?propertyLabel, "[a-z].+"))
  OPTIONAL { ?propertyWikibase skos:altLabel ?propertyAlias. }
}
}}

=== Properties with capitalized labels and their datatypes  ===

{{SPARQL|query=
SELECT DISTINCT ?propertyWikibase ?propertyLabel ?propertyType WHERE {
  ?propertyWikibase wikibase:directClaim ?p;
    wikibase:propertyType ?propertyType;
    rdfs:label ?propertyLabel.
  FILTER(!REGEX(?propertyLabel, "[a-z].+"))
  OPTIONAL { ?propertyWikibase skos:altLabel ?propertyAlias. }
}
}}

== Federated queries ==

=== Companies in MBI-KG with the labels identical to aliases of companies at Wikidata  ===

{{SPARQL|query=
PREFIX wd-wd: <http://www.wikidata.org/entity/>
PREFIX wd-wdt: <http://www.wikidata.org/prop/direct/>
SELECT DISTINCT ?MBI_company ?MBI_companyLabel ?WD_company ?WD_companyLabel WHERE {
  ?MBI_company rdfs:label ?MBI_companyLabel;
    wdt:P3 wd:Q1.
  FILTER((LANG(?MBI_companyLabel)) = "de")
  SERVICE <https://query.wikidata.org/sparql> {
    ?WD_company rdfs:label ?WD_companyLabel;
      skos:altLabel ?MBI_companyLabel;
      wd-wdt:P452 ?industry;
      wd-wdt:P17 wd-wd:Q183.
    FILTER((LANG(?WD_companyLabel)) = "de")
  }
}
}}

=== MBI-KG-companies and AKF-KG-companies with identical labels  ===

{{SPARQL|query=
PREFIX akfd: <http://akf.kgi.uni-mannheim.de/entity/>
PREFIX akfdt: <http://akf.kgi.uni-mannheim.de/prop/direct/>
SELECT DISTINCT ?MBI_company ?MBI_companyLabel ?AKF_company ?AKF_companyLabel WHERE {
  ?MBI_company rdfs:label ?MBI_companyLabel;
    wdt:P3 wd:Q1.
  FILTER((LANG(?MBI_companyLabel)) = "de")
  SERVICE <https://query.akf.kgi.uni-mannheim.de/proxy/wdqs/bigdata/namespace/wdq/sparql> {
    ?AKF_company rdfs:label ?AKF_companyLabel;
      akfdt:P346 ?MBI_companyLabel;
      akfdt:P325 akfd:Q1.
    FILTER((LANG(?AKF_companyLabel)) = "de")
  }
}
}}
