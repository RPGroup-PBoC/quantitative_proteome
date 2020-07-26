#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import prot.viz
colors, palette = prot.viz.bokeh_theme()
prot.viz.plotting_style()

# Load the categories
data = pd.read_csv('../../data/compiled_estimate_categories.csv', comment='#')
dataset_markers = {'li_2014':'o', 'schmidt_2016':'X',
                   'peebo_2015':'d', 'valgepea_2013':'^'}
cats = ['carbon_tport_tot', 'glucose_tport', 'glycerol_tport', 'fructose_tport', 'xylose_tport']


fig, ax = plt.subplots(2, 3, figsize=(6.5, 4))
axes = {c:a for c, a in zip(cats, ax.ravel())}
for a in ax.ravel():
    a.xaxis.set_tick_params(labelsize=6)
    a.yaxis.set_tick_params(labelsize=6)
    a.set_yscale('log')
    a.set_xlabel('growth rate [hr$^{-1}$]', fontsize=6)
    a.set_ylabel('complexes per cell', fontsize=6)
    a.set_xlim([0, 2])

_ax = ax.ravel()
_ax[-1].axis('off')
_ax[0].set_ylim([5E2,  1E6])
_ax[1].set_ylim([5E2,  1E6])
_ax[2].set_ylim([1,  5E3])
_ax[3].set_ylim([10,  1E4])
_ax[4].set_ylim([10,  1E4])

# Add the correct titles
titles = ['all carbohydrate transporters',
          'glucose transporters (PtsG + ManXYZ)',
          'glycerol facilitator (GlpF)',
          'fructose transporter (FruAB)',
          'xylose transporter (XylE + XylFGH)']
for a, t in zip(ax.ravel(), titles):
    prot.viz.titlebox(a, t, size=6, color='k', bgcolor=colors['pale_yellow'],
                    boxsize=0.12)



for g, d in data.groupby(['dataset', 'growth_rate_hr', 'condition']):
    for c, a in axes.items():
        _d = d[d['shorthand']==c]
        if (c.split('_tport')[0] in g[-1]) & ('glucose' not in g[-1]):
            _color = colors['red']
            alpha=1

            if 'pAA' in g[-1]:
                label = 'glycerol + A.A.'
            else:
                label = c.split('_tport')[0]
            a.text(_d['growth_rate_hr'] + 0.05, _d['n_complex'],
            label, fontsize=6)
        else:
            alpha = 0.5
            _color = colors['dark_green'] 

        marker = dataset_markers[g[0]]
        a.plot(_d['growth_rate_hr'], _d['n_complex'], linestyle='none',
              marker=marker, ms=4, alpha=alpha,
        color=_color, markeredgewidth=0.5, markeredgecolor='k')

# Add a legend. 
for g, d in data.groupby(['dataset', 'dataset_name']):
    _ax[-1].plot([], [], linestyle='none', marker=dataset_markers[g[0]], color=colors['dark_green'],
                alpha=0.5, markeredgecolor='k', markeredgewidth=0.5, label=g[1],
                ms=4)
_ax[-1].plot([], [], 's', color=colors['red'], markeredgecolor='k', markeredgewidth=0.5, 
            label='induced expression', ms=4)
_ax[-1].legend(fontsize=7.5, loc='center')
plt.tight_layout()

for a in ax.ravel()[:-1]:
    a.hlines(1E3, 0, 2, color='k', linestyle='--', lw=0.75)
# Add panel labels
# for a, lab in zip(ax.ravel(), ['(A)', '(B)', '(C)', '(D)', '(E)']):
    # a.text(-0.22, 1.1, lab, transform=a.transAxes, fontsize=6)
plt.savefig('../../figures/induced_expression.svg', bbox_inches='tight')
# %%


# %%