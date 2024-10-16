import pandas as pd

data = pd.read_csv('../data/kg_dataset/MBI_KG_bulk_api_v1.0.csv')
non_empty_counts = data.count().reset_index()
non_empty_counts = non_empty_counts.rename(columns={'index': 'Property', 0: 'Count of non-empty values'})
print(non_empty_counts)

