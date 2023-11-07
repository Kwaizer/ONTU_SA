# Searches for shows using Ajax with JSON
import re
from flask import Flask, jsonify, render_template, request
import sqlite3
from datetime import datetime, timedelta
from create_routes import create_routes
from py_scripts.convert_time import convert_hours_to_days_hours_minutes
from py_scripts.distance_for_page import distance_for_page
from py_scripts.find_arrival_coordinates_for_timezone import find_arrival_coordinates
from py_scripts.find_timezone import get_timezone_from_coordinates

app = Flask(__name__)


@app.route("/")
def index():
    # Connect to the database
    conn = sqlite3.connect("aircrafts.db")
    cursor = conn.cursor()

    # Execute an SQL query to fetch the names of planes from the database
    cursor.execute("SELECT Aircraft FROM AircraftData")
    aircraft_names = [row[0] for row in cursor.fetchall()]

    # Close the database connection
    conn.close()

    return render_template("index.html", aircraft_names=aircraft_names)


@app.route("/search")
def search():
    q = request.args.get("q")
    if q:
        conn = sqlite3.connect("airports.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Name, City FROM airports WHERE City LIKE ? LIMIT 50", ("%" + q + "%",))
        airports = cursor.fetchall()
        conn.close()
    else:
        airports = []
    return jsonify(airports)


@app.route("/geomap")
def geomap():
    # Connect to the database
    conn = sqlite3.connect("aircrafts.db")
    cursor = conn.cursor()

    # Execute an SQL query to fetch the names of planes from the database
    cursor.execute("SELECT Aircraft FROM AircraftData")
    aircraft_names = [row[0] for row in cursor.fetchall()]

    # Close the database connection
    conn.close()
    user_input = request.args.getlist("arrivaldeparture")
    create_routes(user_input)
    distances = distance_for_page(user_input)
    # Extract numeric distances using regular expressions
    distances_float = []
    for distance_text in distances:
        match = re.search(r'(\d+\.\d+)', distance_text)
        if match:
            distances_float.append(float(match.group(1)))

    # Obtain avg speed and altitude
    selected_aircraft = request.args.get("planes")
    # Connect to the database
    conn = sqlite3.connect("aircrafts.db")
    cursor = conn.cursor()

    # Execute an SQL query to fetch the average speed of the selected aircraft
    cursor.execute("SELECT AverageSpeedKMH, AltitudeOfFlightMeters FROM AircraftData WHERE Aircraft=?",
                   (selected_aircraft,))
    data = cursor.fetchone()
    average_speed, altitude = data
    altitude_for_page = f"{altitude} meters"
    # Close the database connection
    conn.close()

    flight_datetime = request.args.get("flight_datetime")  # Get the selected flight date

    # Calculate total time based on the selected aircraft's average speed
    total_time = sum(distances_float) / average_speed
    # Check if the calculated distance is longer than 10,000
    if total_time * average_speed > 10000:
        # Add half an hour to the total_time
        total_time += 30 / 60
    days, hours, minutes = convert_hours_to_days_hours_minutes(total_time)
    time_for_page = f"{days} days, {hours} hours, {minutes} minutes"

    # Parse the flight_date string into a datetime object
    # Parse the flight_datetime string into a datetime object
    flight_datetime = datetime.strptime(flight_datetime, "%Y-%m-%dT%H:%M")

    # Calculate the date of arrival by adding the total flight time
    arrival_datetime = flight_datetime + timedelta(hours=total_time)

    # Get the local time of arrival based on the coordinates of the arrival location
    arrival_latitude, arrival_longitude = find_arrival_coordinates(user_input)
    arrival_timezone = get_timezone_from_coordinates(arrival_latitude, arrival_longitude)
    arrival_datetime_local = arrival_datetime.astimezone(arrival_timezone)

    # Parse the timestamp into a datetime object
    datetime_obj = datetime.strptime(str(arrival_datetime_local), "%Y-%m-%d %H:%M:%S.%f%z")

    # Extract the formatted date and time
    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M")
    return render_template("geomap.html", aircraft_names=aircraft_names, altitude=altitude_for_page,
                           selected_aircraft=selected_aircraft, distances=distances,
                           time_for_page=time_for_page, arrival_time=formatted_datetime)
