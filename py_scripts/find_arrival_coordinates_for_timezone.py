import matplotlib.pyplot as plt
import sqlite3
plt.switch_backend('agg')


def find_arrival_coordinates(user_input):
    con = sqlite3.connect("airports.db")
    cur = con.cursor()

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
    # Get the last target tuple from the network
    source, last_target = network[-1]
    # Get the latitude and longitude of the last target
    lat2, lon2 = city_coordinates[last_target]
    return lat2, lon2
