import numpy
import pandas as pd
import numpy_html
from pyecharts.charts import Pie
from pyecharts import options as opts
import sys
import webbrowser

website = 'https://www.worldometers.info/coronavirus/'
webbrowser.open(website)

data = pd.read_clipboard()
data

# remove "," from the dataset
for x in range(1, len(data.columns)):
    data[data.columns[x]] = data[data.columns[x]].str.replace(',', '')
# replace NaNs with zeros
data = data.fillna(0)
# change the datatype from object to integer
for i in range(1, len(data.columns)):
    data[data.columns[i]] = data[data.columns[i]].astype(float).astype(int)
# create a column 'Death Rate'
data['DeathRate'] = data['TotalDeaths'] / data['TotalCases']
# sort the data frame by 'Death Rate' in descending order
data.sort_values(by=['DeathRate'], inplace=True, ascending=False)

df = data[['Country', 'DeathRate']].head(15)  # select two columns and top 15 rows
df['DeathRate'] = (df['DeathRate'] * 100).round(1)
df

# create the color_series for the rosemary
color_series = ['#802200', '#B33000', '#FF4500', '#FAA327', '#9ECB3C',
                '#6DBC49', '#37B44E', '#14AFDC', '#209AC9', '#1E91CA',
                '#2C6BA0', '#2B55A1', '#2D3D8E', '#44388E', '#6A368B',
                '#D02C2A', '#D44C2D', '#F57A34', '#FA8F2F', '#D99D21']
rosemary = Pie(init_opts=opts.InitOpts(width='1350px', height='750px'))
# set the color
rosemary.set_colors(color_series)
# add the data to the rosemary
rosemary.add("", [list(z) for z in zip(c, d)],
             radius=["20%", "95%"],  # 20% inside radius，95% ourside radius
             center=["30%", "60%"],  # center of the chart
             rosetype="area")
# set the global options for the chart
rosemary.set_global_opts(title_opts=opts.TitleOpts(title='Nightingale Rose Chart', subtitle="Covid-19 Death Rate"),
                         legend_opts=opts.LegendOpts(is_show=False),
                         toolbox_opts=opts.ToolboxOpts())
# set the series options
rosemary.set_series_opts(
    label_opts=opts.LabelOpts(is_show=True, position="inside", font_size=12, formatter="{b}:{c}%", font_style="italic",
                              font_weight="bold", font_family="Century"), )
rosemary.render_notebook()
