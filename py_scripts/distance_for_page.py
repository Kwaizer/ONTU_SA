from mpl_toolkits.basemap import Basemap
from py_scripts.calculate_distance import find_distance_between_two_cities
import matplotlib.pyplot as plt
import sqlite3
plt.switch_backend('agg')


def distance_for_page(user_input):
    distances_text = []
    con = sqlite3.connect("airports.db")
    cur = con.cursor()

    # Set the plot size for this notebook:
    plt.figure(figsize=(16, 12))

    # Background map
    m = Basemap(projection='cyl')
    m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
    m.fillcontinents(color='#f2f2f2', alpha=0.7)
    m.drawcoastlines(linewidth=0.1, color="white")
    m.drawcountries(linewidth=0.2, color='grey')

    # ADD a connection between cities
    network = [(user_input[i], user_input[i + 1]) for i in range(0, len(user_input), 2)]
    # Create a set of unique cities from user_input
    if len(network) > 1:
        # Create an empty set to store unique cities
        unique_cities = set()

        # Loop through the pairs and add cities to the set
        for pair in network:
            unique_cities.add(pair[0])  # Add the first city of the pair
            unique_cities.add(pair[1])  # Add the second city of the pair
    else:
        cities_to_extract = [network[0][0], network[0][1]]
        unique_cities = set(cities_to_extract)
    # Create a comma-separated string of city names for the SQL query
    city_names = ', '.join(['?' for _ in unique_cities])
    # Execute an SQL query to fetch the data for the selected cities
    query = f"SELECT City, Latitude, Longitude, Name FROM airports WHERE Name IN ({city_names})"
    cur.execute(query, tuple(unique_cities))

    # Fetch all rows from the query result
    rows = cur.fetchall()
    # Create a dictionary from the fetched data
    city_coordinates = {row[3]: (float(row[1]), float(row[2])) for row in rows}
    for source, target in network:
        lat1, lon1 = city_coordinates[source]
        x, y = m(lon1, lat1)
        plt.text(x, y, source, fontsize=8, ha='center', va='bottom', color='black')
        lat2, lon2 = city_coordinates[target]
        x, y = m(lon2, lat2)
        plt.text(x, y, target, fontsize=8, ha='center', va='bottom', color='black')

        # Calculate the distance using geopy
        distance = find_distance_between_two_cities(lat1, lon1, lat2, lon2)

        # Create the distance text and append it to the list
        distance_text = f"{source} -> {target}: {distance:.2f} km"
        distances_text.append(distance_text)

    return distances_text
