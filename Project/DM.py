import pandas as pd
import numpy as np
import folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.templates.default = 'plotly_white'
import warnings
warnings.filterwarnings("ignore")

metro_data = pd.read_csv("C:\Project\Delhi-Metro-Network.csv")

print(metro_data.head())

print(metro_data.shape)

print(metro_data.dtypes)

print(metro_data.describe().T)

# checking the null values
metro_data.isnull().sum()

# converting Opening date to a datetime format

metro_data['Opening Date'] = pd.to_datetime(metro_data['Opening Date'])
print(metro_data.dtypes)

print(metro_data.columns)

print(metro_data.Line.unique())


# defining color scheme for the metro lines

line_colors = {
    'Red line' : 'red', 'Pink line': 'pink', 'Rapid Metro':'cadetblue',
    'Magenta line': 'darkblue','Blue line': 'blue',
    'Aqua line': 'black', 'Voilet line':'purple', 'Yellow line':'beige',
    'Green line':'green', 'Gray line':'lightgray', 'Orange line':'oragne',
    'Green line branch':'lightgreen',
    'Blue line branch':'lightblue'

}

map_with_tooltip = folium.Map(location=(28.7041, 77.1025), zoom_start=11)
map_with_tooltip.save("aa.html")

# adding colored markers for each metro stations with line name in tootip

for index, row in metro_data.iterrows():
  line = row['Line']
  color = line_colors.get(line, 'black') # default color is black if line not found in the dict.
  folium.Marker(
      location = [row['Latitude'], row['Longitude']],
      popup = f"{row['Station Name']}, {line}",
      icon = folium.Icon(color=color)
  ).add_to(map_with_tooltip)

# Displaying the updated map
map_with_tooltip.save("aa.html")
metro_data.columns

# create a new column Opening Year from Opening Date
metro_data['Opening Year'] = metro_data['Opening Date'].dt.year

print(metro_data.head())

print(metro_data.info())

# counting the number of stations opened each year
stations_per_year = metro_data['Opening Year'].value_counts().sort_index()
stations_per_year


# create a dataframe.
stations_per_year_df = stations_per_year.reset_index()
stations_per_year_df

# Giving names to the columns  in stations_per_year_df
stations_per_year_df.columns = ['Year', 'Number of Stations']
stations_per_year_df

# create a bar plot

fig = px.bar(stations_per_year_df, x = 'Year', y = 'Number of Stations',
             title = "Number of Stations Opened Each year in Delhi",
             labels = {'Year': 'Year', 'Number of Stations':'Number of Stations Opened'})

fig.update_layout(xaxis_tickangle = -45, xaxis = dict(tickmode = 'linear'),
                  yaxis = dict(title = 'Number of Stations Opened'),
                  xaxis_title = "Year"
                  )
fig.show()

stations_per_line = metro_data['Line'].value_counts().sort_index()
stations_per_line

metro_data.columns

# calculating the total distance of each metro line(max distance from start)
total_distance_per_line = metro_data.groupby('Line')['Distance from Start (km)'].max()
total_distance_per_line

# average distance
avg_distance_per_line = total_distance_per_line/(stations_per_line -1)

line_analysis = pd.DataFrame({
    'Line': stations_per_line.index,
    'Number of Stations': stations_per_line.values,
    'Average Distance Between Stations(km)': avg_distance_per_line
})
line_analysis.head()

# sorting the dataframe by the numbre of stations
line_analysis = line_analysis.sort_values(by = 'Number of Stations', ascending = False)
line_analysis

line_analysis.reset_index(drop=True, inplace=True)
line_analysis



# creating subplots
fig = make_subplots(rows=1, cols=2, subplot_titles=('Number of Stations Per Metro Line',
                                                    'Average Distance Between Stations Per Metro Line'),
                    horizontal_spacing=0.2)

# plot for Number of Stations per Line
fig.add_trace(
    go.Bar(y=line_analysis['Line'], x=line_analysis['Number of Stations'],
           orientation='h', name='Number of Stations', marker_color='crimson'),
    row=1, col=1
)
fig.show()
# plot for Average Distance Between Stations
fig.add_trace(
    go.Bar(y=line_analysis['Line'], x=line_analysis['Average Distance Between Stations(km)'],
           orientation='h', name='Average Distance (km)', marker_color='navy'),
    row=1, col=2
)
fig.show()
# update xaxis properties
fig.update_xaxes(title_text="Number of Stations", row=1, col=1)
fig.update_xaxes(title_text="Average Distance Between Stations (km)", row=1, col=2)
fig.show()
# update yaxis properties
fig.update_yaxes(title_text="Metro Line", row=1, col=1)
fig.update_yaxes(title_text="", row=1, col=2)
fig.show()
# update layout
fig.update_layout(height=600, width=1200, title_text="Metro Line Analysis", template="plotly_white")
fig.show()

metro_data.head()


layout_counts = metro_data['Station Layout'].value_counts().sort_index()
layout_counts


# creating the barplot usig plotly
fig = px.bar(x=layout_counts.index, y=layout_counts.values,
             labels = {'x':'Station Layout','y':'Number of Stations'},
             title = 'Distribution of Metro Layouts',
             color = layout_counts.index,
            )
fig.show()
fig.write_image("D:\plot.png")
fig.update_layout(xaxis_title = "Station Layout",
                  yaxis_title = "Number of Stations",
                  coloraxis_showscale = False,
                  template="plotly_white")
fig.show()

#one python file to another python file
s1=input("Do you want to see Delhi map route - yes or no :")
if(s1=="yes"):
 exec(open("dmrc.py").read())
else:
 print("Thank you Visit Again ☺☺☺")  
















