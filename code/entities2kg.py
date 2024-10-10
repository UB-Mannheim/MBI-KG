import logging
import pandas as pd
from wikidataintegrator import wdi_core, wdi_login
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API setup
wikibase = "https://mbi.kgi.uni-mannheim.de"
api = f"{wikibase}/w/api.php"
sparql = f"{wikibase}/proxy/wdqs/bigdata/namespace/wdq/sparql"
entityUri = wikibase.replace("https:", "http:")+"entity/"

# Authentication
WBUSER = os.environ.get("WBUSER")
WBPASS = os.environ.get("WBPASS")
if not WBUSER or not WBPASS:
    raise EnvironmentError("WBUSER and WBPASS must be set in environment variables")

login = wdi_login.WDLogin(WBUSER, WBPASS, mediawiki_api_url=api)

# Read data
data = pd.read_csv("../data/structured_data/MBI_1937_structured.csv")

def create_entity(login, data, label, description, entity_type="item", property_datatype=None):
    localEntityEngine = wdi_core.WDItemEngine.wikibase_item_engine_factory(api, sparql)
    item = localEntityEngine(data=data)
    item.set_label(label)
    item.set_description(description)
    
    if entity_type == "property" and property_datatype:
        return item.write(login, entity_type=entity_type, property_datatype=property_datatype)
    return item.write(login, entity_type=entity_type)

# Define properties
properties = {
    "formatter URL": {"label": "formatter URL", "description": "web page URL ...", "property_datatype": "string"},
    "Wikidata QID": {"label": "Wikidata QID", "description": "The same entity in Wikidata", "property_datatype": "external-id", "formatterURLs": "https://www.wikidata.org/entity/$1"},
}

# Create properties
def create_properties(properties, login):
    for name, props in properties.items():
        create_entity(login, data=[], label=props['label'], description=props['description'], entity_type="property", property_datatype=props['property_datatype'])

create_properties(properties, login)

def create_item(login, row, prop4creation):
    localEntityEngine = wdi_core.WDItemEngine.wikibase_item_engine_factory(api, sparql)
    s = []
    item = localEntityEngine(data=s)
    
    for lang in ['de', 'en']:
        item.set_label(row.COMPANY_NAME, lang=lang)

    statement = []
    for prop in prop4creation.itertuples():
        value = getattr(row, prop.column_name, None)
        if value:
            if prop.datatype == "string":
                statement.append(wdi_core.WDString(value=value.strip(), prop_nr=prop.PID))
            elif prop.datatype == "external-id":
                statement.append(wdi_core.WDExternalID(value=value.strip(), prop_nr=prop.PID))

    statement.append(wdi_core.WDItemID(value='Q1', prop_nr='P3'))
    item.update(data=statement)
    
    return item.write(login, entity_type="item", max_retries=5, retry_after=0.5)

# Create items
for i, row in tqdm(data.iterrows()):
    create_item(login=login, row=row, prop4creation=prop4creation)

