# Objectives
## Obj:  Learn and apply essential Data Science libraries used for data exploration, processing and transformation for further analysis

### Pandas Visualization
[Reference](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html)


```python
# loading dataframe
import pandas as pd
df = pd.read_csv('cv_cases.csv', encoding='unicode_escape')
df.head()
```



```python
# line plot
line_df = df.groupby('year_week').size().reset_index()
line_df.rename(columns={0:'count'}, inplace=True)
line_df.plot('year_week', 'count', kind='line')

# bar chart
# grouping
bar_df = df.groupby('SexID').size().reset_index()
bar_df.rename(columns={0:'count'}, inplace=True)
bar_df.plot('SexID', 'count', kind='bar')
```

<div style="page-break-after: always;"></div>

## Obj: Acquire fundamental knowledge and common operations for Geospatial Analysis


### What is geographical / spatial analysis and why should we care?
* Placing things in geographic context brings those things into immediate perspective. 

* “Everything is related to everything else, but near things are more related than distant things.”

*  Finding out what’s nearby can help bring context to dynamic situations and deepen your understanding of a location. In many cases, things are connected to other things.

* Understanding how and where all those things are connected will help you better manage, monitor and maintain the system.

* Different Sources put together provide information

<img src="./media/gis.png" width="250"/>

<img src="./media/gis2.png" width="500"/>

<div style="page-break-after: always;"></div>

### Data Types
* Vector Data
    * Point: a pair of x and y coordinates
    * Line: a series of points connected together
    * Polygon: a line enclosed from end to end
    
    <img src="./media/vector_data.png" width=500>
    <img src="./media/vector_coordinates.png" width=500>
    
* Raster Data
    * pixel, value
    * example: the values might be:
        * 1 = water (colored blue)
        * 2 = forest (dark green)
        * 3 = desert (dark brown)
        * etc…
    <img src="./media/raster_data.png" width=250>
    
<div style="page-break-after: always;"></div>

### GIS Terms

* Geocoding
  * Process of assigning alphanumeric locational identifiers (such as the municipal address or physical location) to spatially related information. For example, an address may be matched to an address range on a street segment, or a given spatial area
* Euclidean Distance
  * The shortest distance joining two points in the plane
* Label
  *A vector element that contains text used to identify a node, line, or polygon element
* Layer 
  * Refers to the various overlays of data, each of which normally deals with one thematic topic. These overlays are registered to each other by the common coordinate system of the database.
* Legends
  * The part of the drawn map explaining the meaning of the symbols used to code the depicted geographical elements
* Map scale 
  * The relationship that exists between a distance on a map and the corresponding distance on the Earth. It may be expressed as an equivalence, one inch equals 16 statute miles; as a fraction or ratio, 1:1,000,000; or as a bar graph subdivided to show the distance that each of its parts represents on the Earth.
* Network analysis
  * Analytical techniques concerned with the relationships between locations on a network, such as the calculation of optimal routes through road networks, capacities of network systems, best location for facilities along networks, etc.
* Coordinate Systems 
  * A particular kind of reference frame or system, such as plane rectangular coordinates or spherical coordinates, which use linear or angular quantities to designate the position of points within that particular reference frame or system.

**Types of Coordinate Systems**
* Polar / Geographic coordinate System: Degrees, Minutes, Seconds
* Rectangular / Planar coordinate System: longitude, latitude, altitude

<div style="page-break-after: always;"></div>

### Project Coordinate System

[Sample](http://i.stack.imgur.com/7zI6N.jpg)

### Common File Types

* .kml - keyhole markup language (google maps / earth)
* .shp - shapefile
* .geojson
* .bmp - for raster files

### Common Spatial Visualizations

* Scatter Plot -> Point Data and Line Data
    * A scatter plot (aka scatter chart, scatter graph) uses dots to represent values based on coordinates
    * based on basic scatter plot
* Choropleth Map -> Polygon Data
    * Choropleth maps are thematic maps that use different shading patterns and sequential color schemes for geographical areas, based on the statistical data within them. 
    * Derived from basic heatmap

<div style="page-break-after: always;"></div>

## Obj: Learn and apply Python Libraries for Geospatial Analysis


```python
import geopandas as gpd
# Importing File
bdy_gdf = gpd.read_file('municity_boundaries.geojson')
bdy_gdf
```


```python
# visualizing map
bdy_gdf.plot()
```



```python
# creating choropleth map / heatmap
import numpy as np

# Setting our plot

# Setting a seed allows you to get the same "random" numbers that we do
# This is really nice for testing, so you can compare results
np.random.seed(101)

# randint(LB, UB, num_elements)
series = np.random.randint(0,100,len(bdy_gdf))
bdy_gdf['random_count'] = series

# plot
bdy_gdf.plot('random_count')

# changing color scale. reference: https://matplotlib.org/stable/tutorials/colors/colormaps.html
bdy_gdf.plot('random_count', cmap='Oranges')
```


```python
# converting dataframes with coordinates to geodataframes
evac_df = pd.read_csv('./evacuation_sites.csv')

evac_df = evac_df.loc[evac_df['latitude']>0] #trimming latitude out of bound / dataset error

# Note, we need to specify the crs = Coordinate Reference System -> dictates projection type. Normally used: epsg:4326
evac_gdf = gpd.GeoDataFrame(evac_df, geometry=gpd.points_from_xy(evac_df.longitude, evac_df.latitude), crs='epsg:4326')
evac_gdf.plot()
```

```python
# overlaying geodataframe layers
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
#bdy_gdf.boundary.plot(ax=ax)

# since evacuation site dataset is only available for ilagan
# we try to trim the geodataframe to scope only ilagan
ilagan_gdf = bdy_gdf[bdy_gdf['ADM3_EN'].str.contains('Ilagan')]

# 1st plot
ilagan_gdf.plot(ax=ax)

# 2nd plot
evac_gdf.plot(ax=ax, color='black', markersize=3)
```

<div style="page-break-after: always;"></div>


### Basic Spatial Operations

<img src="https://geopandas.org/_images/overlay_operations.png">


```python
from shapely.geometry import Polygon
# preparing shapes

polys1 = gpd.GeoSeries([Polygon([(0,0), (2,0), (2,2), (0,2)]), 
                        Polygon([(2,2), (4,2), (4,4), (2,4)])])


polys2 = gpd.GeoSeries([Polygon([(1,1), (3,1), (3,3), (1,3)]), 
                        Polygon([(3,3), (5,3), (5,5), (3,5)])])


gdf1 = gpd.GeoDataFrame({'geometry': polys1, 'df1':[1,2]})
gdf2 = gpd.GeoDataFrame({'geometry': polys2, 'df2':[1,2]})

ax = df1.plot(color='red');
df2.plot(ax=ax, color='green', alpha=0.5);
```


```python
# spatial operations
res_union = gpd.overlay(df1, df2, how='union')
res_union.plot()
```


```python
res_intersection = gpd.overlay(df1, df2, how='intersection')
res_intersection.plot()
```


```python
res_symdiff = gpd.overlay(df1, df2, how='symmetric_difference')
res_symdiff.plot()
```



```python
res_identity = gpd.overlay(df1, df2, how='identity')
res_identity.plot()
```

<div style="page-break-after: always;"></div>


### Joins

**Attribute Join**

Attribute joins are accomplished using the merge method. In general, it is recommended to use the merge method called from the spatial dataset. With that said, the stand-alone merge function will work if the GeoDataFrame is in the left argument; if a DataFrame is in the left argument and a GeoDataFrame is in the right position, the result will no longer be a GeoDataFrame.

**Spatial Join**
Two geometry objects are merged based on their spatial relationship to one another.

(Useful for non-type data types like polygon and point, polygon and line, etc)

*In geopandas*
sjoin() has two core arguments: how and op.

op

    * intersects
    * contains
    * within
    * touches
    * crosses
    * overlaps

how

    * left: retain only the left_df geometry column
    * right: retain only the right_df geometry column
    * inner: use intersection of index values from both geodataframes; retain only the left_df geometry column


```python
# Attribute join
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

gdf = world[['name', 'pop_est', 'geometry']]
df = pd.DataFrame(world[['name', 'continent']])

print(gdf.columns)
print(df.columns)

merged_gdf = gdf.merge(df, on='name')

# merged_gdf is still plottable
merged_gdf.plot()
```


```python
# Spatial Join

# evac_gdf does not have information regarding which what city are these building located
print(evac_gdf.columns)

# how can we see in which cities they fall under like how they are bounded in flat maps?
sjoin_gdf = gpd.sjoin(evac_gdf, bdy_gdf, op='intersects', how='left')
sjoin_gdf['ADM3_EN'].unique()
```


<div style="page-break-after: always;"></div>

# Exercises

**Spatial Operations**

Copy the code block below and run it:

```python
import geopandas as gpd
from shapely.geometry import Polygon

square = [(1,0), (4, 0), (4, 3), (1,3), (1,0)]
triangle_low = [(0,0), (5, 0), (5/2, 3.5), (0,0)]
triangle_up = [(0, 2), (5, 2), (2.5, 4.5), (0, 2)]

# initialized geodataframe
sq_gdf = gpd.GeoDataFrame({'a':[0], 'geometry':Polygon(square)})
low_gdf = gpd.GeoDataFrame({'a':[0], 'geometry':Polygon(triangle_low)})
up_gdf = gpd.GeoDataFrame({'a':[0], 'geometry':Polygon(tria_up)})
```

Using the geodataframes initialized in the code block, use the basic spatial operations to create the following shapes:

* House
    
![](./media/house.png)

* Trapezoid

![](./media/trapezoid.png)

* Hut

![](./media/hut.png)

<div style="page-break-after: always;"></div>

**Choropleth**

* Given `province_boundaries.geojson` and `cv_cases.csv`)
* Display the choropleth map for the accumulated cases per province

![](./media/choropleth.png)

# Recap

## Objectives

* Install, setup, and run python applications
* Learn and apply basic and advanced programming skills in core python
* Learn and apply essential Data Science libraries used for data exploration, processing and transformation for further analysis
* Acquire fundamental knowledge and common operations for Geospatial Analysis
* Learn and apply Python Libraries for Geospatial Analysis
