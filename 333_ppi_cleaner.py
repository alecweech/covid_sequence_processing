import pandas as pd
import numpy as np

ppi_data = pd.read_excel('ppi_332.xlsx', header = 1)

uniprot_ids = ppi_data['Uniprot Protein ID']
covid_proteins = ppi_data['Bait']

np.save('human_ids', uniprot_ids.unique())
np.save('covid_ids', covid_proteins.unique())