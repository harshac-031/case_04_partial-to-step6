import streamlit as st
import folium
from streamlit_folium import st_folium
from sklearn.cluster import KMeans
import geonamescache

st.title("Dream Trip: Plan Your Visit")
st.write("Pick a city you dream of visiting. We will find where it is on Earth, and a second stop in ANOTHER country!")
gc = geonamescache.GeonamesCache()
countries = gc.get_countries()
cities = [city for city in gc.get_cities().values() if city["population"] >= 1_000_000]
city_names = {f"{city['name']}, {countries[city['countrycode']]['name']}": city for city in cities}
colours = ["red", "blue", "green"]

# LEVEL 1: your dream city
dream_name = st.selectbox("Which city do you dream of visiting?", sorted(city_names), index=None, placeholder="Choose a city")   # Step 1
if dream_name is None:
    st.stop()
dream = city_names[dream_name]                           # Step 2
lat, lon = dream["latitude"], dream["longitude"]
st.write(f"{dream_name} is at latitude {lat:.2f} and longitude {lon:.2f}. {dream['population']:,} people live there.")

# LEVEL 2: your second stop (the closest big city in ANOTHER country)
def gap(city):                                           # Step 3: smaller gap = closer
    return (city["latitude"] - lat) ** 2 + (city["longitude"] - lon) ** 2
others = [city for city in cities if city["countrycode"] != dream["countrycode"]]     # Step 4: cities in other countries
second = min(others, key=gap)                            # Step 5: the closest one
country = countries[second["countrycode"]]               # Step 6
st.success(f"Add a second stop: {second['name']}, {country['name']}!")
