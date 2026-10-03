import folium as fm
import pandas as pd

data = pd.read_csv("Volcanoes.txt")
lon = list(data["LON"])
lat = list(data["LAT"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 3000 > elevation >= 1000:
        return "orange"
    else:
        return "red"

map = fm.Map(location =[14.63, 120.98], zoom_start=5, tiles="OpenStreetMap")


fgp = fm.FeatureGroup(name="Population")

fgp.add_child(fm.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
    style_function= lambda x:{'fillColor':'green' if x['properties']['POP2005'] < 10_000_000
    else 'orange' if 10_000_000 <= x['properties']['POP2005'] < 20_000_000 else 'red'}))

fgv = fm.FeatureGroup(name="Volcanoes")
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = fm.IFrame(html=html % (name , name, el), width=200, height=100)
    fgv.add_child(fm.CircleMarker(
        location=[lt, ln],
        radius=4.5,
        popup=fm.Popup(iframe),
        color="gray",
        fill=True,
        fill_color=color_producer(el),
        fill_opacity=0.7
    ).add_to(fgv))

map.add_child(fgp)
map.add_child(fgv)
map.add_child(fm.LayerControl())

map.save("Map_Exercise.html")