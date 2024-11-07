import requests
import json
import csv
import time
from urllib.parse import urlencode

# Set up the endpoint URL and query
SPARQL_ENDPOINT = "https://query.mbi.kgi.uni-mannheim.de/proxy/wdqs/bigdata/namespace/wdq/sparql"
QUERY_TEMPLATE = """SELECT DISTINCT ?companyQID ?companyLabel ?SIEHE ?ROH_TEXT (YEAR(?Gründ) AS ?Gründung) ?POSTSCHECKKONTO ?FERNRUF ?DRAHTANSCHRIFT ?ist_ein ?FILE_SEGMENT ?FABRIKATIONSPROGRAMM ?BANKVERBINDUNGEN ?ANLAGEN ?INHABER ?GRUNDBESITZ ?ANGABEN ?PROKURISTEN ?GEFOLGSCHAFT ?EIGENE_VERTRETUNGEN ?GESCHÄFTSFÜHRER ?AUFSICHTSRAT ?ANTEILSEIGNER ?VORSTAND ?KAPITAL ?TOCHTERGESELLSCHAFTEN ?AKTIONÄRE ?NUTZFLÄCHE ?GESELLSCHAFTER ?GESCHÄFTSJAHR ?FIRMA_GEHÖRT ?BETEILIGUNGEN ?KOMPLEMENTÄRE ?SPEZIALITÄT ?BEVOLLMÄCHTIGTE ?GESCHÄFTSINHABER_FÜHRER ?NIEDERLASSUNGEN ?UMSATZ ?VERTRÄGE ?VERKAUFSBÜRO ?KOMMANDITISTEN ?FABRIKATIONSANLAGEN ?RECHTSFORM ?STADT ?STRASSE 
(GROUP_CONCAT(DISTINCT ?Rechtsform; SEPARATOR = "; ") AS ?Rechtsformen)
(GROUP_CONCAT(DISTINCT ?RechtsformWikidataQID; SEPARATOR = "; ") AS ?RechtsformWikidataQIDs)
?Land ?Hauptstandort
(GROUP_CONCAT(DISTINCT ?HauptstandortWikidataQID; SEPARATOR = "; ") AS ?HauptstandortWikidataQIDs)
?HauptstandortBreite ?HauptstandortLänge ?im_Eigentum_von ?hat_Prokurist
WHERE {{
  ?companyQID rdfs:label ?companyLabel;
    wdt:P3 wd:Q1.
  OPTIONAL {{ ?companyQID wdt:P3 ?ist_ein. }}
  OPTIONAL {{ ?companyQID wdt:P4 ?ROH_TEXT. }}
  OPTIONAL {{ ?companyQID wdt:P5 ?FILE_SEGMENT. }}
  OPTIONAL {{ ?companyQID wdt:P6 ?FABRIKATIONSPROGRAMM. }}
  OPTIONAL {{ ?companyQID wdt:P7 ?POSTSCHECKKONTO. }}
  OPTIONAL {{ ?companyQID wdt:P8 ?FERNRUF. }}
  OPTIONAL {{ ?companyQID wdt:P9 ?DRAHTANSCHRIFT. }}
  OPTIONAL {{ ?companyQID wdt:P10 ?BANKVERBINDUNGEN. }}
  OPTIONAL {{ ?companyQID wdt:P11 ?ANLAGEN. }}
  OPTIONAL {{ ?companyQID wdt:P12 ?INHABER. }}
  OPTIONAL {{ ?companyQID wdt:P13 ?GRUNDBESITZ. }}
  OPTIONAL {{ ?companyQID wdt:P14 ?ANGABEN. }}
  OPTIONAL {{ ?companyQID wdt:P15 ?PROKURISTEN. }}
  OPTIONAL {{ ?companyQID wdt:P16 ?GEFOLGSCHAFT. }}
  OPTIONAL {{ ?companyQID wdt:P17 ?EIGENE_VERTRETUNGEN. }}
  OPTIONAL {{ ?companyQID wdt:P18 ?GESCHÄFTSFÜHRER. }}
  OPTIONAL {{ ?companyQID wdt:P19 ?GRÜNDUNG. }}
  OPTIONAL {{ ?companyQID wdt:P20 ?SIEHE. }}
  OPTIONAL {{ ?companyQID wdt:P21 ?AUFSICHTSRAT. }}
  OPTIONAL {{ ?companyQID wdt:P22 ?ANTEILSEIGNER. }}
  OPTIONAL {{ ?companyQID wdt:P23 ?VORSTAND. }}
  OPTIONAL {{ ?companyQID wdt:P24 ?KAPITAL. }}
  OPTIONAL {{ ?companyQID wdt:P25 ?TOCHTERGESELLSCHAFTEN. }}
  OPTIONAL {{ ?companyQID wdt:P26 ?AKTIONÄRE. }}
  OPTIONAL {{ ?companyQID wdt:P27 ?NUTZFLÄCHE. }}
  OPTIONAL {{ ?companyQID wdt:P28 ?GESELLSCHAFTER. }}
  OPTIONAL {{ ?companyQID wdt:P29 ?GESCHÄFTSJAHR. }}
  OPTIONAL {{ ?companyQID wdt:P30 ?FIRMA_GEHÖRT. }}
  OPTIONAL {{ ?companyQID wdt:P31 ?BETEILIGUNGEN. }}
  OPTIONAL {{ ?companyQID wdt:P32 ?KOMPLEMENTÄRE. }}
  OPTIONAL {{ ?companyQID wdt:P33 ?SPEZIALITÄT. }}
  OPTIONAL {{ ?companyQID wdt:P34 ?BEVOLLMÄCHTIGTE. }}
  OPTIONAL {{ ?companyQID wdt:P35 ?GESCHÄFTSINHABER_FÜHRER. }}
  OPTIONAL {{ ?companyQID wdt:P36 ?NIEDERLASSUNGEN. }}
  OPTIONAL {{ ?companyQID wdt:P37 ?UMSATZ. }}
  OPTIONAL {{ ?companyQID wdt:P38 ?VERTRÄGE. }}
  OPTIONAL {{ ?companyQID wdt:P39 ?VERKAUFSBÜRO. }}
  OPTIONAL {{ ?companyQID wdt:P40 ?KOMMANDITISTEN. }}
  OPTIONAL {{ ?companyQID wdt:P41 ?FABRIKATIONSANLAGEN. }}
  OPTIONAL {{ ?companyQID wdt:P42 ?RECHTSFORM. }}
  OPTIONAL {{ ?companyQID wdt:P43 ?STADT. }}
  OPTIONAL {{ ?companyQID wdt:P44 ?STRASSE. }}
  OPTIONAL {{
    ?companyQID wdt:P45 ?Rechtsform.
    ?Rechtsform wdt:P2 ?RechtsformWikidataQID.
  }}
  OPTIONAL {{ ?companyQID wdt:P46 ?Gründ. }}
  OPTIONAL {{ ?companyQID wdt:P47 ?Land. }}
  OPTIONAL {{
    ?companyQID wdt:P48 ?Hauptstandort.
    ?Hauptstandort wdt:P2 ?HauptstandortWikidataQID;
      p:P50 ?statement.
    ?statement psv:P50 ?coordinateNode.
    ?coordinateNode wikibase:geoLatitude ?HauptstandortBreite;
      wikibase:geoLongitude ?HauptstandortLänge.
  }}
  OPTIONAL {{ ?companyQID wdt:P49 ?im_Eigentum_von. }}
  OPTIONAL {{ ?companyQID wdt:P54 ?hat_Prokurist. }}
  FILTER((LANG(?companyLabel)) = "de")
}}
GROUP BY ?companyQID ?companyLabel ?SIEHE ?ROH_TEXT ?Gründ ?POSTSCHECKKONTO ?FERNRUF ?DRAHTANSCHRIFT ?ist_ein ?FILE_SEGMENT ?FABRIKATIONSPROGRAMM ?BANKVERBINDUNGEN ?ANLAGEN ?INHABER ?GRUNDBESITZ ?ANGABEN ?PROKURISTEN ?GEFOLGSCHAFT ?EIGENE_VERTRETUNGEN ?GESCHÄFTSFÜHRER ?AUFSICHTSRAT ?ANTEILSEIGNER ?VORSTAND ?KAPITAL ?TOCHTERGESELLSCHAFTEN ?AKTIONÄRE ?NUTZFLÄCHE ?GESELLSCHAFTER ?GESCHÄFTSJAHR ?FIRMA_GEHÖRT ?BETEILIGUNGEN ?KOMPLEMENTÄRE ?SPEZIALITÄT ?BEVOLLMÄCHTIGTE ?GESCHÄFTSINHABER_FÜHRER ?NIEDERLASSUNGEN ?UMSATZ ?VERTRÄGE ?VERKAUFSBÜRO ?KOMMANDITISTEN ?FABRIKATIONSANLAGEN ?RECHTSFORM ?STADT ?STRASSE ?Land ?Hauptstandort ?HauptstandortBreite ?HauptstandortLänge ?im_Eigentum_von ?hat_Prokurist
LIMIT {limit}
OFFSET {offset}
"""

COUNT_QUERY = """
SELECT (COUNT(?company) AS ?companyCount)
WHERE {
  ?company wdt:P3 wd:Q1.
}
"""

# Function to perform the SPARQL query and return results
def run_sparql_query(query, endpoint, retries=3):
    headers = {
        'Accept': 'application/sparql-results+json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = urlencode({'query': query})  # Properly URL encode the query
    
    for attempt in range(retries):
        try:
            response = requests.post(endpoint, data=data, headers=headers, timeout=60)
            if response.status_code == 200:
                return response.json()  # Return JSON results if successful
            else:
                print(f"Failed to execute query. Status code: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        
        print(f"Retrying... ({attempt+1}/{retries})")
        time.sleep(5)  # Wait 5 seconds before retrying
    
    return None

# Function to get the total number of companies
def get_total_records():
    print("Running query to count the number of companies...")
    results = run_sparql_query(COUNT_QUERY, SPARQL_ENDPOINT)
    if results and 'results' in results and 'bindings' in results['results']:
        company_count = int(results['results']['bindings'][0]['companyCount']['value'])
        print(f"Total number of companies: {company_count}")
        return company_count
    else:
        print("Failed to retrieve the company count.")
        return 0


# Function to save results into one CSV file
def save_to_csv(results, csv_filename):
    if results and 'head' in results and 'vars' in results['head']:
        headers = results['head']['vars']
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()

            # Write all results
            for result in results['results']['bindings']:
                row = {var: result[var]['value'] if var in result else '' for var in headers}
                writer.writerow(row)
        
        print(f"All results saved to {csv_filename}")

# Function to save results into an NDJSON file
def save_to_ndjson(results, ndjson_filename):
    if results and 'results' in results and 'bindings' in results['results']:
        with open(ndjson_filename, 'w', encoding='utf-8') as ndjson_file:
            for result in results['results']['bindings']:
                json.dump(result, ndjson_file)
                ndjson_file.write("\n")  # Write each result on a new line
        
        print(f"All results saved to {ndjson_filename}")

# Main function to paginate through SPARQL results and save them
def main():
    filenamebase = "../data/kg_dataset/MBI_KG_bulk_api_"
    version = 'v1.0' # Version of the MBI-KG dataset
    limit = 1000  # Number of results per query
    total_records = get_total_records()  # Total number of companies (5150 in v1.0)
    csv_filename = filenamebase + version + ".csv"
    ndjson_filename = filenamebase + version + ".ndjson"
    all_results = []
    for offset in range(0, total_records, limit):
        query = QUERY_TEMPLATE.format(limit=limit, offset=offset)
        print(f"Running query with OFFSET {offset}")
        
        results = run_sparql_query(query, SPARQL_ENDPOINT)
        
        if results and 'results' in results and 'bindings' in results['results']:
            all_results.extend(results['results']['bindings'])
        else:
            print(f"No results returned or query failed at OFFSET {offset}. Moving to next batch.")

    # Save all results into one JSON file
    if all_results:
        full_results = {'head': results['head'], 'results': {'bindings': all_results}}
        save_to_csv(full_results, csv_filename)
        save_to_ndjson(full_results, ndjson_filename)

if __name__ == "__main__":
    main()
