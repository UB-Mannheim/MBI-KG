import os
from tqdm import tqdm
from wikidataintegrator import wdi_core, wdi_login
from enricher import enrich

# Configuration
wikibase = "https://mbi.kgi.uni-mannheim.de"
api = f"{wikibase}/w/api.php"
sparql = f"{wikibase}/proxy/wdqs/bigdata/namespace/wdq/sparql"
login = wdi_login.WDLogin(os.getenv("WBUSER"), os.getenv("WBPASS"), mediawiki_api_url=api)

# Helper functions
def execute_sparql(query):
    return wdi_core.WDItemEngine.execute_sparql_query(query, endpoint=sparql, as_dataframe=True)

def create_property(label, description, datatype, wdprop=None, formatterURLs=None):
    s = [wdi_core.WDExternalID(wdprop, prop_nr="P2")] if wdprop else []
    if formatterURLs:
        for url in formatterURLs.split('; '):
            s.append(wdi_core.WDString(url, prop_nr="P1"))
    localEntityEngine = wdi_core.WDItemEngine.wikibase_item_engine_factory(api,sparql)
    item = localEntityEngine(data=s)
    item.set_label(label)
    item.set_description(description)
    item.write(login, entity_type="property", property_datatype=datatype)

def create_item(label, description, aliases=None, wdprop=None):
    s = [wdi_core.WDExternalID(wdprop, prop_nr="P2")] if wdprop else []
    localEntityEngine = wdi_core.WDItemEngine.wikibase_item_engine_factory(api,sparql)
    item = localEntityEngine(data=s)
    item.set_label(label)
    item.set_description(description)
    if aliases:
        item.set_aliases(aliases)
    item.write(login)

def update_item_statements(qid, statements):
    item = wdi_core.WDItemEngine(wd_item_id=qid, mediawiki_api_url=api)
    item.update(data=statements)
    item.write(login, max_retries=5, retry_after=0.5)

# Using kg-enricher for city linking
def enrich_city(name):
    try:
        result = enrich(name)
        if 'id' in result:
            return result['id']
        return None
    except Exception as e:
        print(f"Error enriching {name}: {e}")
        return None

# Retrieve and enrich cities
def get_cities():
    query = """
    SELECT ?item ?itemLabel ?city ?cityN ?revision
    WHERE 
    {
      ?item wdt:P3 wd:Q1.
      ?item p:P43 ?cityN;
            schema:version ?revision;
            wdt:P43 ?city.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } 
    }
    """
    return execute_sparql(query)

def update_city_wikidata(cities):
    for _, row in tqdm(cities.iterrows(), desc="Updating cities with Wikidata QIDs"):
        if row['city_wqid']:
            item = wdi_core.WDItemEngine(wd_item_id=row['item'], mediawiki_api_url=api)
            statements = [wdi_core.WDItemID(row['city_wqid'], prop_nr="P48")]
            item.update(data=statements)
            item.write(login)

# Main function to update cities with kg-enricher
def process_and_update_cities():
    cities = get_cities()
    cities['item'] = cities['item'].apply(lambda x: x.replace('http://mbi.kgi.uni-mannheim.de/entity/', ''))
    cities['city_wqid'] = cities['city'].apply(lambda x: enrich_city(x))
    update_city_wikidata(cities)

# Function to update legal forms
def get_rechtsformen():
    query = """
    SELECT ?item ?itemLabel ?rechtsform
    WHERE {
        ?item wdt:P3 wd:Q1; wdt:P42 ?rechtsform.
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """
    return execute_sparql(query)

def update_legal_forms(RFs, legal_form_map):
    RFs['legal_form'] = RFs['rechtsform'].apply(lambda x: [legal_form_map.get(f.strip()) for f in x.split(';')])
    RFs['item'] = RFs['item'].apply(lambda x: x.replace(f"{entityUri}entity/", ''))

    for _, row in tqdm(RFs.iterrows(), desc="Updating Legal Forms"):
        statements = [wdi_core.WDItemID(legal_form, prop_nr='P45') for legal_form in row['legal_form'] if legal_form]
        update_item_statements(row['item'], statements)

# Update inceptions
def update_inceptions():
    query = """
    SELECT ?item ?inception WHERE {
      ?item wdt:P3 wd:Q1; wdt:P19 ?inception.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """
    inceptions = execute_sparql(query)
    inceptions['inception_cleaned'] = inceptions['inception'].apply(lambda x: x[:4] if x[:4].isnumeric() else None)

    for _, row in tqdm(inceptions.iterrows(), desc="Updating Inceptions"):
        if row['inception_cleaned']:
            statements = [wdi_core.WDTime(f"+{row['inception_cleaned']}-00-00T00:00:00Z", prop_nr='P46', precision=9)]
            update_item_statements(row['item'].replace(f"{entityUri}entity/", ''), statements)

# Update country information
def update_countries():
    query = """
    SELECT ?item WHERE { ?item wdt:P3 wd:Q1. SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } }
    """
    all_companies = execute_sparql(query)
    all_companies['item'] = all_companies['item'].apply(lambda x: x.replace(f"{entityUri}entity/", ''))

    for _, row in tqdm(all_companies.iterrows(), desc="Updating Countries"):
        statements = [wdi_core.WDItemID('Q5156', prop_nr='P47')]
        update_item_statements(row['item'], statements)

# Update person role (owners and signatories)
def update_person_role(companies_df, person_col, prop_nr, person_role):
    companies_df = companies_df[companies_df[person_col].apply(lambda x: len(x.split(' ')) == 2)]
    for _, row in tqdm(companies_df.iterrows(), desc=f"Updating {person_role}"):
        person_qid = create_item(row[person_col], f"{person_role} of {row['COMPANY_NAME']}")
        update_item_statements(row['item'], [wdi_core.WDItemID(person_qid, prop_nr=prop_nr)])

# Update geographic coordinates for mbi_cities using kg-enricher
def update_geographic_coordinates(mbi_cities):
    for i, (iqid, wqid, iLabel) in tqdm(mbi_cities.iterrows(), desc="Updating geographic coordinates"):
        enriched_city = enrich(iLabel)

        # Extract latitude and longitude from the enriched data
        try:
            latitude = enriched_city.get('Geographic coordinates', {}).get('latitude')
            longitude = enriched_city.get('Geographic coordinates', {}).get('longitude')
            precision = enriched_city.get('Geographic coordinates', {}).get('precision', 0.0001)
            globe = enriched_city.get('Geographic coordinates', {}).get('globe', 'http://www.wikidata.org/entity/Q2')

            if latitude is None or longitude is None:
                print(f"Coordinates not found for {iLabel}")
                continue
        except (KeyError, TypeError) as e:
            print(f"Error extracting coordinates for {iLabel}: {e}")
            continue

        # Update the item with geographic coordinates
        gitem = wdi_core.WDItemEngine(wd_item_id=iqid, mediawiki_api_url=api)
        s = [wdi_core.WDGlobeCoordinate(latitude=latitude, longitude=longitude, 
                                        precision=precision, prop_nr='P50', globe=globe)]
        gitem.update(data=s)
        gitem.write(login, max_retries=5, retry_after=0.5)


# Main function
def main():
    # Creating initial properties
    create_property("legal form", "Legal form of an entity", "wikibase-item", wdprop='P1454')
    create_property("inception", "Time when an entity begins to exist", "time", wdprop='P571')
    create_property("country", "Sovereign state this item is in", "wikibase-item", wdprop='P17')

    # Update legal forms
    legal_form_map = {'AG': 'Q5152', 'GmbH': 'Q5153', 'KG': 'Q5154', 'oHG': 'Q5155'}
    RFs = get_rechtsformen()
    update_legal_forms(RFs, legal_form_map)

    # Update other properties
    update_inceptions()
    update_countries()

    # Process and update cities using kg-enricher
    process_and_update_cities()

    # Update roles like owners, signatories, and managers
    update_person_role(prep_inhaber, 'INHABER', 'P49', "owner")
    update_person_role(prep_prokuristen, 'PROKURISTEN', 'P53', "authorized signatory")

    # Updating geographic coordinates for mbi_cities
    mbi_cities = get_cities()
    update_geographic_coordinates(mbi_cities)

if __name__ == "__main__":
    main()
