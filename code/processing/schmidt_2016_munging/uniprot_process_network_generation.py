#%%
import numpy as np
import pandas as pd

# Load the complete gene-linked dataset
data = pd.read_csv('../../data/uniprot_biological_processes.csv')

# %%
# Instantiate an empty list to keep track of what classes have already been
# linked
connected_pairs = []

# Instantiate an empty dataframe of connections
df = pd.DataFrame([], columns=['process_1', 'process_2', 'n_genes'])

for i, process_i in enumerate(data['process'].unique()):
    for j, process_j in enumerate(data['process'].unique()):
        # If the process is the same, move on
        if process_i == process_j:
            continue

        # Find the number of common genes
        n_genes = len(set(data[data['process']==process_i]['gene'].values).intersection(
                data[data['process']==process_j]['gene'].values))

        # update the dataframe (keep connections of 0)
        df = df.append({'process_1':process_i, 
                        'process_2':process_j,
                        'n_genes':n_genes}, ignore_index=True)

# %%
# Save the data to disk.
df.to_csv('../../data/uniprot_process_gene_network.csv', index=False)


# %%
