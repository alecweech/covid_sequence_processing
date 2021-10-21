#imports
import pandas as pd
import os
import glob
import re
import shutil
from wget import download
from Bio.PDB import *


#change your paths to the relevant locations!
workspace ='D:\\Covid_pipeline/covid_sequence_processing'
savespace = 'D:\\Covid_pipeline/human_pdbs'
alphafold_dir = 'D:\\Covid_pipeline/alphafold_precomputed/UP000005640_9606_HUMAN'
os.chdir(workspace)

df = pd.read_csv('structures_with_5AA_cutoff.csv')

#what's got a human pdb?

#setup a link to the pdb ftp server so we can dowload stuff
pdbl = PDBList(server='http://ftp.wwpdb.org')

#find human pdb ids
human_pdbs = df.loc[df['pdb_id'] != 'None']['pdb_id'].values

#Get files for each human pdb id
for pdb_id in human_pdbs:
    pdbl.retrieve_pdb_file(pdb_id, pdir = savespace, file_format='pdb')

#what needs an alphafold?
needs_alpha = df.loc[df['pdb_data'] == 'None']['uniprot_id']

#Search precomputed directory for files
os.chdir(alphafold_dir)
#get all pdb zipped archives
files = glob.glob('*.pdb.gz')

#move available precomputed files to our folder
precomputed_available = []
for value in needs_alpha.values:
    for file in files:
        if re.match('AF-{}-.*'.format(value), file) is not None:
            #move files
            shutil.move(alphafold_dir + '/' + file, savespace)
            #save already available files
            precomputed_available.append(value)


#Get the files not available in the precomputed directory
needs_alpha = needs_alpha.tolist()
needs_downloading = [x for x in needs_alpha if x not in precomputed_available]


#Let's try to download the rest!
unavailable = []
for alphafold in needs_downloading:
    url = "https://alphafold.ebi.ac.uk/files/AF-{}-F1-model_v1.pdb".format(alphafold)
    try:
        download(url, out = savespace)
    except:
        #save unavailable files
        unavailable.append(alphafold)

#print out what we need to manually fold
print(unavailable)

