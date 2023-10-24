from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import sqlite3


def create_routes(user_input):

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
    # network = [(user_input)]
    network = [(user_input[i], user_input[i + 1]) for i in range(0, len(user_input), 2)]
    print(network)
    # Create a set of unique cities from user_input
    if len(network) > 1:
        # Create an empty set to store unique cities
        unique_cities = set()

        # Loop through the pairs and add cities to the set
        for pair in network:
            print(pair)
            print(pair[0])
            print(pair[1])
            unique_cities.add(pair[0])  # Add the first city of the pair
            unique_cities.add(pair[1])  # Add the second city of the pair
        print("unique cities: " + str(unique_cities))
    else:
        print(network[0][0])
        print(network[0][1])
        cities_to_extract = [network[0][0], network[0][1]]
        unique_cities = set(cities_to_extract)
        print(unique_cities)
    # Create a comma-separated string of city names for the SQL query
    city_names = ', '.join(['?' for _ in unique_cities])
    print("city names: " + city_names)
    # Execute an SQL query to fetch the data for the selected cities
    query = f"SELECT City, Latitude, Longitude, Name FROM airports WHERE Name IN ({city_names})"
    cur.execute(query, tuple(unique_cities))

    # Fetch all rows from the query result
    rows = cur.fetchall()
    print(rows)
    # Create a dictionary from the fetched data
    city_coordinates = {row[3]: (float(row[1]), float(row[2])) for row in rows}
    airports = {row[0]: (row[3]) for row in rows}
    print(airports)
    print(network)
    for source, target in network:
        print(source)
        print(target)
        print(city_coordinates)
        lat1, lon1 = city_coordinates[source]
        x, y = m(lon1, lat1)
        plt.text(x, y, source, fontsize=8, ha='center', va='bottom', color='black')
        lat2, lon2 = city_coordinates[target]
        x, y = m(lon2, lat2)
        plt.text(x, y, target, fontsize=8, ha='center', va='bottom', color='black')

        # Calculate the distance using geopy
        # coord1 = (lat1, lon1)
        # coord2 = (lat2, lon2)
        # distance = geodesic(coord1, coord2).kilometers
        # # Display the distance on the map
        # plt.text((lon1 + lon2) / 2, (lat1 + lat2) / 2, f'{distance:.2f} km', fontsize=8, ha='center', va='top',
        #          color='red')

        line, = m.drawgreatcircle(lon1, lat1, lon2, lat2, lw=1)

        p = line.get_path()
        # find the index which crosses the dateline (the delta is large)
        cut_point = np.where(np.abs(np.diff(p.vertices[:, 0])) > 200)[0]
        if cut_point:
            cut_point = cut_point[0]

            # create new vertices with a nan inbetween and set those as the path's vertices
            new_verts = np.concatenate(
                [p.vertices[:cut_point, :],
                 [[np.nan, np.nan]],
                 p.vertices[cut_point + 1:, :]]
            )
            p.codes = None
            p.vertices = new_verts

    # Save the plot as an image
    plt.savefig('static/media/map.png', bbox_inches='tight')
    # Show the HTML file path
    print("Map saved as 'index.html'")
