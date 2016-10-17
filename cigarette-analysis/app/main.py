import pandas as pd
import numpy as np
from bokeh.layouts import gridplot, layout, widgetbox, row
from bokeh.plotting import figure, show, ColumnDataSource, output_server, output_notebook
from bokeh.models import NumeralTickFormatter, LabelSet, Label, LinearAxis, Range1d, HoverTool, VBox
from bokeh.models.widgets import MultiSelect, CheckboxGroup
from bokeh.io import show, curdoc
from bokeh.resources import CSSResources

dataset = pd.read_csv('data/dataset.csv')
us_avg_price = pd.read_csv('data/us_avg_price.csv')
us_avg_sales = pd.read_csv('data/us_avg_sales.csv')


def plot_state_by_year():
    if 0 in checkbox_group.active:
        average = True
    else:
        average = False

    tools = []

    state_list = multi_select.value

    df = dataset[dataset['state'].isin(state_list)]

    # Seting the params for the first figure.
    s2 = figure(plot_width=800, plot_height=500, tools=tools, y_range=[1.00,3.00],
                title="Cigarette Prices in the US from 1963 to 1992")

    # Setting the second y axis range name and range
    s2.extra_y_ranges = {"sales": Range1d(start=40, end=180)}

    if average == True:
        s2.line(us_avg_price['year'],
                us_avg_price['mean'],
                color='orange',
                line_width=4,
                line_dash="dashed",
                legend="min price national average")

    for state in state_list:
        data = df[df['state'] == state]
        s2.line(data['year'], data['adjusted_min_price'],
                color='orange', legend='min price by state',
                line_width=0.5, line_alpha=0.5)

    if average == True:
        s2.line(us_avg_sales['year'],
                us_avg_sales['mean'],
                color='gray',
                line_width=4,
                y_range_name="sales",
                line_dash="dashed",
                legend="sales national average")

    for state in state_list:
        data = df[df['state'] == state]
        s2.line(data['year'], data['sales'], color='gray',
                legend='sales by state', line_width=0.5,
                line_alpha=0.75,  y_range_name="sales")

    s2.yaxis.axis_label = 'minimum price of cigarette pack (adjusted to 2016 USD)'
    s2.add_layout(LinearAxis(y_range_name="sales", axis_label='cigarette sales in packs per capita'), 'right')
    s2.xaxis.axis_label = 'year'

    s2.legend.location = "bottom_right"
    s2.grid.grid_line_alpha = 0.3
    s2.axis.axis_line_color = 'lightgray'
    s2.axis.minor_tick_line_color = 'lightgray'
    s2.axis.major_tick_line_color = 'lightgray'
    s2.yaxis[0].formatter = NumeralTickFormatter(format="$0.00")
    s2.axis.major_label_text_color = 'gray'

    return s2

def make_scatterplot():
    hover = HoverTool(
            tooltips=[
                ('state', '@state'),
                ('sales', '@sales'),
                ('year', '@year'),
                ('min price', '@adjusted_min_price')
            ]
        )
    tools=[hover]
    state_list = multi_select.value

    df = dataset[dataset['state'].isin(state_list)]
    df = df.dropna()

    source = ColumnDataSource(df)

    slope, intercept = np.polyfit(df['adjusted_min_price'], df['sales'], 1)
    x = np.linspace(1.20, 3.00, 10)
    y = intercept + slope * x

    sc = figure(title = "Cigarette Sales vs. Price of Cigarette in the US from 1963 to 1992",
                width=800, height=600, tools=tools)

    sc.xaxis.axis_label = 'minimum price of cigarette pack (adjusted to 2016 USD)'
    sc.yaxis.axis_label = 'cigarette sales in packs per capita'

    sc.circle('adjusted_min_price', 'sales',
              size=6, fill_alpha=0.5,
              line_alpha=0, color='#1f78b4',
              legend='average consumption states',
              source=source)

    if 1 in checkbox_group.active:
        sc.line(x, y, line_color="lightgray", line_width=4, legend='line of best fit average consumption states')
    else:
        pass


    sc.grid.grid_line_alpha = 0
    sc.axis.axis_line_color = 'lightgray'
    sc.axis.minor_tick_line_color = 'lightgray'
    sc.axis.major_tick_line_color = 'lightgray'
    sc.axis.major_label_text_color = 'gray'

    sc.xaxis[0].formatter = NumeralTickFormatter(format="$0.00")

    return sc

def update_plots(attr, old, new):
    b.children = [plot_state_by_year(), make_scatterplot()]

def update_plot_1(attr, old, new):
    b.children[0] = plot_state_by_year()


states = ['AL',
 'AR',
 'AZ',
 'CO',
 'CT',
 'DC',
 'DE',
 'GA',
 'HI',
 'IA',
 'ID',
 'IL',
 'IN',
 'KS',
 'KY',
 'LA',
 'MA',
 'MD',
 'ME',
 'MI',
 'MN',
 'MO',
 'MS',
 'MT',
 'NC',
 'NE',
 'NH',
 'NM',
 'NV',
 'NY',
 'OH',
 'OK',
 'OR',
 'PA',
 'RI',
 'SC',
 'SD',
 'TN',
 'TX',
 'UT',
 'VA',
 'VT']

multi_select = MultiSelect(title="States:", value=['VT'],
                           options=states)

checkbox_group = CheckboxGroup(
        labels=["show US average", "show regression line"], active=[0, 1])

multi_select.on_change('value', update_plots)

checkbox_group.on_change('active', update_plots)

controls = widgetbox(multi_select, checkbox_group)

b = VBox(plot_state_by_year(), make_scatterplot())
l = row(controls, b)

curdoc().add_root(l)
