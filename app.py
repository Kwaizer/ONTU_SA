# Searches for shows using Ajax with JSON

from flask import Flask, jsonify, render_template, request
import sqlite3
from create_routes import create_routes


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


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
    # departure = request.args.get("departure1")
    # arrival = request.args.get("arrival1")
    arrival1 = request.args.getlist("arrivaldeparture")
    user_input = arrival1
    create_routes(user_input)
    return render_template("geomap.html", user_input=user_input)

