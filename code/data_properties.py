import pandas as pd

# Load the main dataset
data = pd.read_csv('../data/kg_dataset/MBI_KG_bulk_api_v1.0.csv')

# Create the non-empty count table
non_empty_counts = data.count().reset_index()
non_empty_counts = non_empty_counts.rename(columns={'index': 'Property', 0: 'Count of non-empty values'})

# Define the mapping table from the provided data
property_info = {
    "URL-Formatierer": {"Property PID": "P1", "Property type": "wikibase:String", "Property English label": "formatter URL"},
    "Wikidata QID": {"Property PID": "P2", "Property type": "wikibase:ExternalId", "Property English label": "Wikidata QID"},
    "ist_ein": {"Property PID": "P3", "Property type": "wikibase:WikibaseItem", "Property English label": "instance of"},
    "ROH_TEXT": {"Property PID": "P4", "Property type": "wikibase:String", "Property English label": "RAW_TEXT"},
    "FILE_SEGMENT": {"Property PID": "P5", "Property type": "wikibase:String", "Property English label": "FILE_SEGMENT"},
    "FABRIKATIONSPROGRAMM": {"Property PID": "P6", "Property type": "wikibase:String", "Property English label": "PRODUCTION_PLAN"},
    "POSTSCHECKKONTO": {"Property PID": "P7", "Property type": "wikibase:String", "Property English label": "POSTAL_GIRO_ACCOUNT"},
    "FERNRUF": {"Property PID": "P8", "Property type": "wikibase:String", "Property English label": "TELEPHONE_NUMBER"},
    "DRAHTANSCHRIFT": {"Property PID": "P9", "Property type": "wikibase:String", "Property English label": "TELEGRAPHIC_ADDRESS"},
    "BANKVERBINDUNGEN": {"Property PID": "P10", "Property type": "wikibase:String", "Property English label": "BANK_ACCOUNTS"},
    "ANLAGEN": {"Property PID": "P11", "Property type": "wikibase:String", "Property English label": "FACILITIES"},
    "INHABER": {"Property PID": "P12", "Property type": "wikibase:String", "Property English label": "OWNER"},
    "GRUNDBESITZ": {"Property PID": "P13", "Property type": "wikibase:String", "Property English label": "PROPERTY"},
    "ANGABEN": {"Property PID": "P14", "Property type": "wikibase:String", "Property English label": "STATEMENTS"},
    "PROKURISTEN": {"Property PID": "P15", "Property type": "wikibase:String", "Property English label": "AUTHORIZED_SIGNATORIES"},
    "GEFOLGSCHAFT": {"Property PID": "P16", "Property type": "wikibase:String", "Property English label": "FOLLOWERS"},
    "EIGENE_VERTRETUNGEN": {"Property PID": "P17", "Property type": "wikibase:String", "Property English label": "REPRESENTATIONS"},
    "GESCHÄFTSFÜHRER": {"Property PID": "P18", "Property type": "wikibase:String", "Property English label": "MANAGING_DIRECTOR"},
    "GRÜNDUNG": {"Property PID": "P19", "Property type": "wikibase:String", "Property English label": "INCORPORATION"},
    "SIEHE": {"Property PID": "P20", "Property type": "wikibase:String", "Property English label": "SEE"},
    "AUFSICHTSRAT": {"Property PID": "P21", "Property type": "wikibase:String", "Property English label": "SUPERVISORY_BOARD"},
    "ANTEILSEIGNER": {"Property PID": "P22", "Property type": "wikibase:String", "Property English label": "SHAREHOLDERS"},
    "VORSTAND": {"Property PID": "P23", "Property type": "wikibase:String", "Property English label": "MANAGEMENT_BOARD"},
    "KAPITAL": {"Property PID": "P24", "Property type": "wikibase:String", "Property English label": "CAPITAL"},
    "TOCHTERGESELLSCHAFTEN": {"Property PID": "P25", "Property type": "wikibase:String", "Property English label": "SUBSIDIARIES"},
    "AKTIONÄRE": {"Property PID": "P26", "Property type": "wikibase:String", "Property English label": "STOCKHOLDER"},
    "NUTZFLÄCHE": {"Property PID": "P27", "Property type": "wikibase:String", "Property English label": "USABLE_SPACE"},
    "GESELLSCHAFTER": {"Property PID": "P28", "Property type": "wikibase:String", "Property English label": "PARTNER"},
    "GESCHÄFTSJAHR": {"Property PID": "P29", "Property type": "wikibase:String", "Property English label": "FINANCIAL_YEAR"},
    "FIRMA_GEHÖRT": {"Property PID": "P30", "Property type": "wikibase:String", "Property English label": "COMPANY_OWNED_BY"},
    "BETEILIGUNGEN": {"Property PID": "P31", "Property type": "wikibase:String", "Property English label": "SHARES"},
    "KOMPLEMENTÄRE": {"Property PID": "P32", "Property type": "wikibase:String", "Property English label": "GENERAL_PARTNERS"},
    "SPEZIALITÄT": {"Property PID": "P33", "Property type": "wikibase:String", "Property English label": "SPECIALIZATION"},
    "BEVOLLMÄCHTIGTE": {"Property PID": "P34", "Property type": "wikibase:String", "Property English label": "AUTHORISED_REPRESENTATIVE"},
    "GESCHÄFTSINHABER_FÜHRER": {"Property PID": "P35", "Property type": "wikibase:String", "Property English label": "OWNER_MANAGER"},
    "NIEDERLASSUNGEN": {"Property PID": "P36", "Property type": "wikibase:String", "Property English label": "BRANCHES"},
    "UMSATZ": {"Property PID": "P37", "Property type": "wikibase:String", "Property English label": "REVENUE"},
    "VERTRÄGE": {"Property PID": "P38", "Property type": "wikibase:String", "Property English label": "CONTRACTS"},
    "VERKAUFSBÜRO": {"Property PID": "P39", "Property type": "wikibase:String", "Property English label": "SALES_OFFICE"},
    "KOMMANDITISTEN": {"Property PID": "P40", "Property type": "wikibase:String", "Property English label": "LIMITED_PARTNERS"},
    "FABRIKATIONSANLAGEN": {"Property PID": "P41", "Property type": "wikibase:String", "Property English label": "MANUFACTURING_PLANTS"},
    "RECHTSFORM": {"Property PID": "P42", "Property type": "wikibase:String", "Property English label": "LEGAL_FORM"},
    "STADT": {"Property PID": "P43", "Property type": "wikibase:String", "Property English label": "CITY"},
    "STRASSE": {"Property PID": "P44", "Property type": "wikibase:String", "Property English label": "STREET"},
    "Rechtsformen": {"Property PID": "P45", "Property type": "wikibase:WikibaseItem", "Property English label": "legal form"},
    "RechtsformWikidataQIDs": {"Property PID": "same as P2", "Property type": "wikibase:ExternalId", "Property English label": "legal form Wikidata QID"},
    "Gründung": {"Property PID": "P46", "Property type": "wikibase:WikibaseItem", "Property English label": "inception"},
    "Land": {"Property PID": "P47", "Property type": "wikibase:WikibaseItem", "Property English label": "country"},
    "Hauptstandort": {"Property PID": "P48", "Property type": "wikibase:WikibaseItem", "Property English label": "headquarters location"},
    "im_Eigentum_von": {"Property PID": "P49", "Property type": "wikibase:WikibaseItem", "Property English label": "owned by"},
    "geographische Koordinaten": {"Property PID": "P50", "Property type": "wikibase:GlobeCoordinate", "Property English label": "coordinate location"},
    "HauptstandortBreite": {"Property PID": "part of P48", "Property type": "wikibase:GlobeCoordinate", "Property English label": "headquarters latitude"},
    "HauptstandortLänge": {"Property PID": "part of P48", "Property type": "wikibase:GlobeCoordinate", "Property English label": "headquarters longitude"},
    "HauptstandortWikidataQIDs": {"Property PID": "same as P2", "Property type": "wikibase:ExternalId", "Property English label": "headquarters Wikidata QID"},
    "Inhaber von": {"Property PID": "P52", "Property type": "wikibase:WikibaseItem", "Property English label": "owner of"},
    "Bevollmächtigter von": {"Property PID": "P53", "Property type": "wikibase:WikibaseItem", "Property English label": "authorized signatory of"},
    "hat_Prokurist": {"Property PID": "P54", "Property type": "wikibase:WikibaseItem", "Property English label": "has authorized signatory"},
    "inverse Eigenschaft": {"Property PID": "P55", "Property type": "wikibase:WikibaseProperty", "Property English label": "inverse property"},
}

# Convert the dictionary to a DataFrame
property_info_df = pd.DataFrame.from_dict(property_info, orient='index').reset_index()
property_info_df = property_info_df.rename(columns={'index': 'Property'})

# Merge the non_empty_counts with property_info_df
non_empty_counts = pd.merge(non_empty_counts, property_info_df, on='Property', how='left')

# Change the order of the columns and rename "Property" to "Property German label"
non_empty_counts = non_empty_counts[['Property PID', 'Property', 'Property English label', 'Count of non-empty values', 'Property type']]
non_empty_counts = non_empty_counts.rename(columns={'Property': 'Property German label'})


# Sort by 'Count of non-empty values' in descending order
non_empty_counts = non_empty_counts.sort_values(by='Count of non-empty values', ascending=False)

# Display the resulting DataFrame
print(non_empty_counts)
