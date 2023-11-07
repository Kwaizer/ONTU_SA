from geopy.distance import geodesic


def find_distance_between_two_cities(lat1, lon1, lat2, lon2):
    coord1 = (lat1, lon1)
    coord2 = (lat2, lon2)
    return geodesic(coord1, coord2).kilometers
