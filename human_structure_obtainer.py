import numpy as np
import pandas as pd
import requests
import bs4
import re

human_ids = np.load('human_ids.npy', allow_pickle =True)
#ah shoot, last vlaue is nan
human_ids = human_ids[0:len(human_ids)-1]

#human_ids = ['BRD4_HUMAN']

structures_df = pd.DataFrame(columns = ['ID', 'pdb_data', 'pdb_id', 'uniprot_id'])

#Setup to scrape
root_url = 'https://www.uniprot.org/uniprot/'
header = {'User-Agent' : 'UVA covid interactome project, aaw3ff@virginia.edu'}


for uniprot_id in human_ids:
    page = requests.get(root_url + uniprot_id)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')

    ### Get uniprot ID
    header = soup.find('main').findChild('section', {'id': 'page-header'})
    name = header.findChild('h2', {'property': 'alternateName'}).getText()
    name = name.split('-')[1]
    name = name.split('(')[0]
    name = name.strip(' ')
    name = name.replace('\n', '')
    name = re.sub('\s', '', name)
    print('doing: {}'.format(name))
    #Get the structure table
    struct_tables = soup.find_all('table', 'databaseTable STRUCTURE', recursive=True)
    if len(struct_tables) == 2:
        print('entered_loop')
        struct_table = struct_tables[1]

        pdb_data = []
        #Parse table and extract relevant values
        for row in struct_table.findAll('tr'):
            col = row.findAll('td')
            #Ignore header, which has len 7
            if len(col) == 6:
                range = col[4].getText()
                lower = int(range.split('-')[0])
                upper = int(range.split('-')[1])
                resolution = col[2].getText()

                #assume that NMR structures with no specified resolution are bad
                if resolution == '-':
                    resolution = 1000
                else:
                    resolution = float(resolution)
                #Stick the values in a list
                pdb_id = col[0].getText()
                pdb_data.append((pdb_id, resolution, lower, upper))

        #Get sequence lengths
        lens =soup.find_all('span', "sequence-field-header tooltiped", recursive = True)
        sequence_lengths = []
        lens = [tag for tag in lens if tag.getText() == 'Length:']
        for tag in lens:
            sequence_lengths.append(int(tag.findNext().getText().replace(',','')))
        #Assume we want to cover the maximum sequence identified (maybe switch to canonical?)
        max_len = max(sequence_lengths)

        acceptable_ranges = [pdb for pdb in pdb_data if pdb[2] < 5 and pdb[3] > max_len - 5]
        if acceptable_ranges == []:
            row = {'ID': uniprot_id, 'pdb_data': 'None', 'pdb_id': "None", 'uniprot_id': name}
        else:
            best_pdb = min(acceptable_ranges, key = lambda x:x[1])
            row = {'ID': uniprot_id, 'pdb_data':  best_pdb, 'pdb_id': best_pdb[0], 'uniprot_id': name}
    else:
        row = {'ID': uniprot_id, 'pdb_data': 'None', 'pdb_id': "None", 'uniprot_id': name}

    structures_df = structures_df.append(row, ignore_index=True)


structures_df.to_csv('structures_with_5AA_cutoff.csv')



