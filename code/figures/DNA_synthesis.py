#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import prot.viz
colors, palette = prot.viz.bokeh_theme()
prot.viz.plotting_style()

# Load the data and restrict
data = pd.read_csv('../../data/compiled_estimate_categories.csv')
dnap = data[data['shorthand']=='dnap']
rnr = data[data['shorthand']=='dntp']
dataset_colors = {'li_2014':colors['purple'], 'schmidt_2016':colors['light_blue'],
                   'peebo_2015':colors['green'], 'valgepea_2013':colors['red']}


# %%
fig, ax = plt.subplots(1, 1, figsize=(3, 2))
ax.xaxis.set_tick_params(labelsize=6)
ax.yaxis.set_tick_params(labelsize=6)
ax.set_xlabel('growth rate [hr$^{-1}$]', fontsize=6)
ax.set_ylabel('DNA polymerase III per cell', fontsize=6)

# Format the axes
ax.set_yscale('log')
ax.set_ylim([1, 5E2])
ax.set_xlim([0, 2])
# Plot the predictions
ax.plot(0.5, 3, 'o', ms=6, color=colors['dark_brown'], alpha=0.75, label='estimated value')
ax.hlines(3, 0, 0.5, 'k', linestyle='--', lw=0.75, label='__nolegend__')
ax.vlines(0.5, 1, 3, 'k', linestyle='--', lw=0.75, label='__nolegend__')

for g, d in dnap.groupby(['dataset', 'dataset_name']):
    ax.plot(d['growth_rate_hr'], d['n_complex'], 'o', ms=4, color=dataset_colors[g[0]],
            alpha=0.75, markeredgewidth=0.5, markeredgecolor='k', label=g[1])

ax.legend(fontsize=6)
plt.savefig('../../figures/DNA_polymerase_plots.svg', bbox_inches='tight')

# %%
fig, ax = plt.subplots(1, 1, figsize=(3, 2))
ax.xaxis.set_tick_params(labelsize=6)
ax.yaxis.set_tick_params(labelsize=6)
ax.set_xlabel('growth rate [hr$^{-1}$]', fontsize=6)
ax.set_ylabel('ribonucleo reductases per cell', fontsize=6)

# Format the axes
ax.set_yscale('log')
ax.set_ylim([1E1, 1E4])
ax.set_xlim([0, 2])
# Plot the predictions
ax.plot(0.5, 300, 'o', ms=6, color=colors['dark_brown'], alpha=0.75, label='estimated value')
ax.hlines(300, 0, 0.5, 'k', linestyle='--', lw=0.75, label='__nolegend__')
ax.vlines(0.5, 10, 300, 'k', linestyle='--', lw=0.75, label='__nolegend__')

for g, d in rnr.groupby(['dataset', 'dataset_name']):
    ax.plot(d['growth_rate_hr'], d['n_complex'], 'o', ms=4, color=dataset_colors[g[0]],
            alpha=0.75, markeredgewidth=0.5, markeredgecolor='k', label=g[1])

ax.legend(fontsize=6)
plt.savefig('../../figures/dNTP_plots.svg', bbox_inches='tight')

# %%