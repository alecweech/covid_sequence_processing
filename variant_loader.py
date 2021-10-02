'''Import all mutations into one standardized CSV'''

import os
import sys
import glob
import pandas as pd
import re

#Get csv files from path
path = os.getcwd()
path += '\covid_sequence_processing\MutationSummary'
csv_files = glob.glob(os.path.join(path, '*.csv'))
print(csv_files)
mutations = pd.DataFrame()

for file in csv_files:
    df = pd.read_csv(file)
    mutations = pd.concat([mutations, df])

mutations[['nucleotide', 'change']] = mutations['mutation_site'].str.replace(r'\'', '').str.split(':', expand = True)
mutations[['WT', 'SNP']] = mutations['change'].str.split('->', expand = True)
mutations[['WT_AA', 'SNP_AA']] = mutations['protein_site(actual)'].str.split(r"[^A-Z]+", expand = True)
mutations = mutations.drop(['mutation_site', 'protein_site(actual)', 'change'], axis = 'columns')


mutations.to_csv('cleaned_mutations.csv')