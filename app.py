# Import necessary libraries
from flask import Flask, render_template, request
import sqlite3
from gevent.pywsgi import WSGIServer

# Create Flask app
app = Flask(__name__)

# Function to get events by person ID
def get_db():
    conn = sqlite3.connect('Transportation.db')
    return conn


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/searchbyperson')
def search_by_person():
    person_id = request.args.get('person_id')  
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Events WHERE person=?", [person_id])
    events = cur.fetchall()
    conn.close()
    return render_template('result.html', events=events)
    
@app.route('/searchbylink')
def search_by_link():
    link_id = request.args.get('link_id')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM links WHERE link_id = ?", [link_id]) 
    events = cur.fetchall()
    conn.close()
    return render_template('result.html', events=events)

@app.route('/linkdetails')
def link_details():
    link_id = request.args.get('link_id')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT freespeed, capacity, modes FROM Links WHERE link_id = ?", [link_id])
    events = cur.fetchall()
    conn.close()
    return render_template('result.html', events=events)



@app.route('/timerange')
def events_in_time_range():
    link_id = request.args.get('link_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # Convert start_time and end_time to seconds or use them directly based on your database schema
    # You may need to adjust this conversion based on your HTML input format and database schema
    start_time_seconds = convert_to_seconds(start_time)
    end_time_seconds = convert_to_seconds(end_time)

    conn = get_db()
    cur = conn.cursor()

    # Query events within the specified time range
    cur.execute("SELECT * FROM Events WHERE link = ? AND time BETWEEN ? AND ? ORDER BY time", [link_id, start_time_seconds, end_time_seconds])
    events = cur.fetchall()

    conn.close()
    return render_template('result.html', events=events)

def convert_to_seconds(time_str):
    # You may need to implement this function based on the format of your time input
    # This example assumes the time format is HH:MM
    hours, minutes = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60

if __name__ == '__main__':
    app.run(debug=True)