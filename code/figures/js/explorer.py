#%%
import numpy as np
import pandas as pd 
import bokeh.io
from bokeh.models import *
import bokeh.layouts
import bokeh.plotting
import prot.viz
import tqdm
colors, palette = prot.viz.bokeh_theme()
dataset_colors = prot.viz.dataset_colors()

# ##############################################################################
# DATA CLEANING AND AGGREGATION
# ##############################################################################
# Load the three datasets
prots = pd.read_csv('../../../data/compiled_absolute_measurements.csv')
prots_source = ColumnDataSource(prots)


# Define the data sources
cplx_df = pd.read_csv('../../../data/compiled_annotated_complexes.csv')
cplx_desc_df = pd.read_csv('./cplx_desc.csv')
cplx_numeric_df = pd.read_csv('./cplx_numeric.csv')
cplx_source_data = ColumnDataSource(cplx_df)
cplx_desc_source = ColumnDataSource(cplx_desc_df)
cplx_numeric_source = ColumnDataSource(cplx_numeric_df)

# Define the display sources. 
cplx_display_source = ColumnDataSource({'x':[], 'y':[], 'c':[], 'l':[],
                                        'condition': [], 'cond':[]})
cplx_table_source = ColumnDataSource({'protein':[], 'subunits':[], 
                                      'relative_subunits':[],
                                      'observed':[],
                                      'func':[]})
subunit_display_source = ColumnDataSource({'x':[], 'y':[], 'mean_val':[], 'median_val':[]})
prots_display_source = ColumnDataSource({'x':[], 'y':[], 'c':[], 'l':[],
                                         'condition':[]})

# ##############################################################################
# FIGURE CANVAS DECLARATION AND INTERACTION INSTANTIATION
# ##############################################################################
bokeh.io.output_file('./explorer.html', mode='inline')


# Define the menu for selecting complexes 
complex_menu = {d:g for g, d in zip(cplx_desc_df['complex_annotation'].values, cplx_desc_df['complex'].values)}
complex_menu = [(k, v) for k, v in complex_menu.items()]
complex_selection = Select(
                           value='select annotation',
                           options=complex_menu,
                           width=400)

# Define th menu for selecting proteins
prots.sort_values(by='gene_name', inplace=True)
protein_menu = [(d, g) for g, d in zip(prots['gene_name'].unique(), prots['b_number'].unique())]
protein_selection = Select(title='protein name', options=protein_menu,
                           value='select gene product')

# Define the slector for min, max, or median complex abundance
agg_fn = RadioButtonGroup(labels=['minimum', 'maximum', 'median', 'mean'],
                         active=3)


# Define the hover for callbacks and interactions.
TOOLTIPS = [('growth rate [per hr]', '@x'),
            ('abundance [per cell]', '@y{int}'),
            ('growth condition', '@condition'),
            ('data source', '@l')]
            
# Define the figure canvases
complex_canvas = bokeh.plotting.figure(width=500, height=400, 
                                       x_axis_label='growth rate [per hr]',
                                       y_axis_label='complex abundance per cell',
                                       y_axis_type='log',
                                       tooltips=TOOLTIPS)
subunit_canvas = bokeh.plotting.figure(width=500, height=250,
                                       x_axis_label='protein subunit',
                                       y_axis_label='number of functional units')
GO_canvas = bokeh.plotting.figure(width=600, height=400, 
                                  x_axis_label='growth rate [per hr]',
                                  y_axis_label='process member abundance per cell',
                                  tooltips=TOOLTIPS)
prot_canvas = bokeh.plotting.figure(width=600, height=400, 
                                  x_axis_label='growth rate [per hr]',
                                  y_axis_label='protein abundance per cell',
                                  tooltips=TOOLTIPS)

# Populate the canvases.
complex_canvas.circle(x='x', y='y', color='c', legend_field='l',
                     source=cplx_display_source, line_color='black', size=10)
subunit_canvas.circle(x='x', y='y', color=colors['dark_green'], 
                     line_color='black', size=10, source=subunit_display_source)
mean_span = Span(location=0, dimension='width', line_color=colors['purple'])
median_span = Span(location=0, dimension='width', line_color='k')
# subunit_canvas.add_layout(mean_span)
# subunit_canvas.add_layout(median_span)


# Define description divs and tables. 
selector_title = Div(text='<b> EcoCyc complex annotation</b>')
agg_title = Div(text='<b>complex abundance aggregation method</b>')
complex_description_field = Div(text="")
complex_table_cols =  [
    TableColumn(field='protein', title='protein name'),
    TableColumn(field='subunits', title='number per complex'),
    TableColumn(field='relative_subunits', title='number relative to minimum'),
    TableColumn(field='observed', title='observed number relative to minimum')
]
complex_table = DataTable(columns=complex_table_cols, source=cplx_table_source,
                          width=400)
# ##############################################################################
# CALLBACK DEFINTITION AND ASSIGNMENT
# ##############################################################################

# Define the argument dictionaries
cplx_args = {'cplx_desc_source': cplx_desc_source, 
             'cplx_numeric_source':cplx_numeric_source, 
             'cplx_select_input': complex_selection,
             'cplx_table_source': cplx_table_source,
             'agg_method_input': agg_fn,
             'cplx_desc_field':complex_description_field,
             'cplx_display_source': cplx_display_source,
             'axis': complex_canvas.yaxis[0]
             }
cplx_hover_args = {'cplx_source_data':cplx_source_data, 
                   'cplx_select_input':complex_selection,
                   'cplx_table_source': cplx_table_source,
                   'cplx_display_source':cplx_display_source,
                   'subunit_display_source':subunit_display_source}

hover_cb = prot.viz.load_js('explorer_subunits.js', args=cplx_hover_args)
cplx_cb = prot.viz.load_js('explorer_complex.js', args=cplx_args)
complex_selection.js_on_change('value', cplx_cb)
agg_fn.js_on_change('active', cplx_cb)
complex_canvas.hover.callback = hover_cb
# Define the widget boxes 
complex_box = bokeh.layouts.column(selector_title,complex_selection, agg_title, agg_fn,
                                   complex_description_field, 
                                   complex_table)
go_box = bokeh.layouts.row(agg_fn)
prot_box = bokeh.layouts.column(protein_selection)
complex_plots = bokeh.layouts.column(complex_canvas, subunit_canvas)
complex_layout = bokeh.layouts.row(complex_plots, complex_box)
go_layout = bokeh.layouts.row(GO_canvas, go_box)
protein_layout = bokeh.layouts.row(prot_canvas, prot_box)

# Define the tabs
complex_tab = Panel(child=complex_layout, title='by functional complex')
GO_tab = Panel(child=go_layout, title='by GO annotation')
prot_tab = Panel(child=protein_layout, title='by protein')
tabs = Tabs(tabs=[complex_tab, GO_tab, prot_tab])
bokeh.io.save(tabs)

# %%
