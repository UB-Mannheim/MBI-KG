import requests
import json
import csv
import time
from urllib.parse import urlencode

# Set up the endpoint URL and query
SPARQL_ENDPOINT = "https://query.mbi.kgi.uni-mannheim.de/proxy/wdqs/bigdata/namespace/wdq/sparql"
QUERY_TEMPLATE = """SELECT DISTINCT ?company ?companyLabel ?SIEHE ?RAW_TEXT (year(?inc) as ?inception) ?POSTSCHECKKONTO ?FERNRUF ?DRAHTANSCHRIFT 
  ?QID ?instanceOf ?FILE_SEGMENT ?FABRIKATIONSPROGRAMM ?BANKVERBINDUNGEN ?ANLAGEN ?INHABER ?GRUNDBESITZ ?ANGABEN 
  ?PROKURISTEN ?GEFOLGSCHAFT ?EIGENE_VERTRETUNGEN ?GESCHÄFTSFÜHRER ?GRÜNDUNG ?AUFSICHTSRAT ?ANTEILSEIGNER ?VORSTAND 
  ?KAPITAL ?TOCHTERGESELLSCHAFTEN ?AKTIONÄRE ?NUTZFLÄCHE ?GESELLSCHAFTER ?GESCHÄFTSJAHR ?FIRMA_GEHÖRT ?BETEILIGUNGEN 
  ?KOMPLEMENTÄRE ?SPEZIALITÄT ?BEVOLLMÄCHTIGTE ?GESCHÄFTSINHABER_FÜHRER ?NIEDERLASSUNGEN ?UMSATZ ?VERTRÄGE ?VERKAUFSBÜRO 
  ?KOMMANDITISTEN ?FABRIKATIONSANLAGEN ?RECHTSFORM ?CITY ?STREET ?legalForm ?country ?headquartersLocation ?ownedBy 
  ?coordinateLocation ?ownerOf ?authorizedSignatoryOf ?Prokurist ?inverseProperty
WHERE {{
  ?company rdfs:label ?companyLabel;
    wdt:P3 wd:Q1.
  
  OPTIONAL {{ ?company wdt:P2 ?QID. }}                     
  OPTIONAL {{ ?company wdt:P3 ?instanceOf. }}               
  OPTIONAL {{ ?company wdt:P4 ?RAW_TEXT. }}                 
  OPTIONAL {{ ?company wdt:P5 ?FILE_SEGMENT. }}             
  OPTIONAL {{ ?company wdt:P6 ?FABRIKATIONSPROGRAMM. }}     
  OPTIONAL {{ ?company wdt:P7 ?POSTSCHECKKONTO. }}          
  OPTIONAL {{ ?company wdt:P8 ?FERNRUF. }}                  
  OPTIONAL {{ ?company wdt:P9 ?DRAHTANSCHRIFT. }}           
  OPTIONAL {{ ?company wdt:P10 ?BANKVERBINDUNGEN. }}        
  OPTIONAL {{ ?company wdt:P11 ?ANLAGEN. }}                 
  OPTIONAL {{ ?company wdt:P12 ?INHABER. }}                 
  OPTIONAL {{ ?company wdt:P13 ?GRUNDBESITZ. }}             
  OPTIONAL {{ ?company wdt:P14 ?ANGABEN. }}                 
  OPTIONAL {{ ?company wdt:P15 ?PROKURISTEN. }}             
  OPTIONAL {{ ?company wdt:P16 ?GEFOLGSCHAFT. }}            
  OPTIONAL {{ ?company wdt:P17 ?EIGENE_VERTRETUNGEN. }}     
  OPTIONAL {{ ?company wdt:P18 ?GESCHÄFTSFÜHRER. }}         
  OPTIONAL {{ ?company wdt:P19 ?GRÜNDUNG. }}                
  OPTIONAL {{ ?company wdt:P20 ?SIEHE. }}                   
  OPTIONAL {{ ?company wdt:P21 ?AUFSICHTSRAT. }}            
  OPTIONAL {{ ?company wdt:P22 ?ANTEILSEIGNER. }}           
  OPTIONAL {{ ?company wdt:P23 ?VORSTAND. }}                
  OPTIONAL {{ ?company wdt:P24 ?KAPITAL. }}                 
  OPTIONAL {{ ?company wdt:P25 ?TOCHTERGESELLSCHAFTEN. }}   
  OPTIONAL {{ ?company wdt:P26 ?AKTIONÄRE. }}               
  OPTIONAL {{ ?company wdt:P27 ?NUTZFLÄCHE. }}              
  OPTIONAL {{ ?company wdt:P28 ?GESELLSCHAFTER. }}          
  OPTIONAL {{ ?company wdt:P29 ?GESCHÄFTSJAHR. }}           
  OPTIONAL {{ ?company wdt:P30 ?FIRMA_GEHÖRT. }}            
  OPTIONAL {{ ?company wdt:P31 ?BETEILIGUNGEN. }}           
  OPTIONAL {{ ?company wdt:P32 ?KOMPLEMENTÄRE. }}           
  OPTIONAL {{ ?company wdt:P33 ?SPEZIALITÄT. }}             
  OPTIONAL {{ ?company wdt:P34 ?BEVOLLMÄCHTIGTE. }}         
  OPTIONAL {{ ?company wdt:P35 ?GESCHÄFTSINHABER_FÜHRER. }} 
  OPTIONAL {{ ?company wdt:P36 ?NIEDERLASSUNGEN. }}         
  OPTIONAL {{ ?company wdt:P37 ?UMSATZ. }}                  
  OPTIONAL {{ ?company wdt:P38 ?VERTRÄGE. }}                
  OPTIONAL {{ ?company wdt:P39 ?VERKAUFSBÜRO. }}            
  OPTIONAL {{ ?company wdt:P40 ?KOMMANDITISTEN. }}          
  OPTIONAL {{ ?company wdt:P41 ?FABRIKATIONSANLAGEN. }}     
  OPTIONAL {{ ?company wdt:P42 ?RECHTSFORM. }}              
  OPTIONAL {{ ?company wdt:P43 ?CITY. }}                    
  OPTIONAL {{ ?company wdt:P44 ?STREET. }}                  
  OPTIONAL {{ ?company wdt:P45 ?legalForm. }}               
  OPTIONAL {{ ?company wdt:P46 ?inc. }}                     
  OPTIONAL {{ ?company wdt:P47 ?country. }}                 
  OPTIONAL {{ ?company wdt:P48 ?headquartersLocation. }}    
  OPTIONAL {{ ?company wdt:P49 ?ownedBy. }}                 
  OPTIONAL {{ ?company wdt:P50 ?coordinateLocation. }}      
  OPTIONAL {{ ?company wdt:P52 ?ownerOf. }}                 
  OPTIONAL {{ ?company wdt:P53 ?authorizedSignatoryOf. }}   
  OPTIONAL {{ ?company wdt:P54 ?Prokurist. }}               
  OPTIONAL {{ ?company wdt:P55 ?inverseProperty. }}         

  FILTER((LANG(?companyLabel)) = "de")
}}
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
    limit = 500  # Number of results per query
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
