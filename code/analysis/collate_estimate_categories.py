#%%
import pandas as pd 
import tqdm

# Load  the necessary datasets. 
data = pd.read_csv('../../data/compiled_annotated_complexes.csv', comment='#')

# define necessary complexes. 
complexes = {'dnap': {'name': 'DNA polymerase III (core enzyme)', 
                       'complexes': ['CPLX0-3803'],
                       'rate_per_sec': 600,
                       'units': 'bp/s',
                       'method': 'sum',
                       'category':'synthesis'},
             'rnap': {'name':'RNA polymerase (core enzyme)',
                       'complexes': ['APORNAP-CPLX'],
                       'rate_per_sec': 20,
                       'units':'nt/s',
                       'method':'sum',
                       'category':'synthesis'},
             'trna': {'name': 'tRNA ligase', 
                      'complexes': ['ALAS-MONOMER', 'ARGS-MONOMER', 'ASPS-MONOMER', 
                                    'ASNS-MONOMER', 'CYSS-MONOMER', 'GLURS-MONOMER',
                                    'GLNS-MONOMER', 'GLYS-CPLX', 'HISS-MONOMER', 
                                    'ILES-MONOMER', 'LEUS-MONOMER', 'LYSS-MONOMER',
                                    'METG-MONOMER', 'PHES-CPLX', 'PROS-MONOMER', 
                                    'SERS-MONOMER', 'THRS-MONOMER', 'TRPS-MONOMER',
                                    'TYRS-MONOMER', 'VALS-MONOMER'],
                    'rate_per_sec': 300,
                    'units': 'AA/s',
                    'method':'avg',
                    'category':'synthesis'},
            'glucose_tport': {'name': 'Glucose Transporters', 
                              'complexes': ['CPLX-165', 'CPLX-157'],
                              'rate_per_sec': 200,
                              'units': 'glucose/s',
                              'method': 'sum',
                              'category':'transport'},
            'ribosome': {'name': 'Ribosome (50S + 30S)',
                         'complexes': ['CPLX0-3964'],
                         'rate_per_sec': 15,
                         'units': 'AA/s',
                         'method':'sum',
                         'category':'synthesis'},
            'eftu': {'name': 'Elongation Factor EF-Tu', 
                     'complexes': ['EG11037-MONOMER', 'EG11036-MONOMER'],
                     'method': 'sum',
                     'rate_per_sec': 20,
                     'units':'peptide bonds/s',
                     'category':'synthesis'},
            'atp_synthase': {'name': 'F1-F0 ATP Synthase',
                            'complexes':  ['ATPSYN-CPLX'],
                            'method': 'sum', 
                            'rate_per_sec': 300,
                            'units':'atp/s',
                            'category': 'energy production'}, 
            'ndhI': {'name': 'NADH Dehydrogenase I', 
                    'complexes': ['NADH-DHI-CPLX'],
                    'method':'sum',
                    'rate_per_sec': 6E3,
                    'units': 'protons/s',
                    'category': 'energy production'},
            'fas': {'name': 'Fatty Acid Synthesis',
                    'complexes': ['FABB-CPLX',
                                  '3-OXOACYL-ACP-SYNTHII-CPLX',
                                  'CPLX0-252'],
                    'method': 'sum', 
                    'rate_per_sec': 1,
                    'units':'lipid/s',
                    'category': 'synthesis'}}

# %%
complex_df = pd.DataFrame([])
for g, d in tqdm.tqdm(data.groupby(['dataset', 'dataset_name', 'condition', 'growth_rate_hr'])):
    for k, v in complexes.items():
        _d = d[d['complex'].isin(v['complexes'])]
        if len(_d) > 0:
            _d = _d.drop_duplicates(subset=['gene_name'])
            _d = _d.groupby(['complex'])['n_units'].mean().reset_index()
            if v['method'] == 'sum':
                units = _d['n_units'].sum()
                _method = 'sum total'
            if v['method'] == 'avg':
                units = _d['n_units'].mean()
                _method = 'average'

            # assemble a dictionary 
            _data = {'dataset':g[0], 'dataset_name':g[1],
                     'condition':g[2], 'growth_rate_hr':g[3],
                     'n_complex':units, 
                     'rate': v['rate_per_sec'],
                     'rate_units': v['units'],
                     'components':v['complexes'],
                     'shorthand': k,
                     'name': v['name'],
                     'aggregation_method': _method,
                     'category': v['category']}
        
            complex_df = complex_df.append(_data, ignore_index=True)


complex_df.to_csv('../../data/compiled_estimate_categories.csv', index=False)
# %%







# %%
