import sqlite3
import xml.etree.ElementTree as ET

def create_tables(cursor):
    # Create the Events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            time REAL,
            type TEXT,
            link TEXT,
            vehicle TEXT,
            facility TEXT,
            delay REAL,
            person TEXT,
            networkMode TEXT,
            relativePosition REAL,
            legMode TEXT,
            actType TEXT,
            taskType TEXT,
            taskIndex INTEGER,
            dvrpMode TEXT
        )
    ''')

    # Create the Nodes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            id TEXT,
            x REAL,
            y REAL
        )
    ''')

    # Create the Links table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            link_id INTEGER,
            from_id TEXT,
            to_id TEXT,
            length REAL,
            freespeed REAL,
            capacity REAL,
            permlanes REAL,
            oneway TEXT,
            modes TEXT
        )
    ''')

def insert_events_data(cursor, data):
    # Insert event data into the Events table
    cursor.execute('''
        INSERT INTO events (time, type, link, vehicle, facility, delay, person, networkMode, 
                            relativePosition, legMode, actType, taskType, taskIndex, dvrpMode)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('time'),
        data.get('type'),
        data.get('link'),
        data.get('vehicle'),
        data.get('facility'),
        data.get('delay'),
        data.get('person'),
        data.get('networkMode'),
        data.get('relativePosition'),
        data.get('legMode'),
        data.get('actType'),
        data.get('taskType'),
        data.get('taskIndex'),
        data.get('dvrpMode')
    ))

def insert_node_data(cursor, data):
    # Insert node data into the Nodes table
    cursor.execute('''
        INSERT INTO nodes (id, x, y)
        VALUES (?, ?, ?)
    ''', (
        data.get('id'),
        data.get('x'),
        data.get('y')
    ))

def insert_link_data(cursor, data):
    # Insert link data into the Links table
    cursor.execute('''
        INSERT INTO links (link_id, from_id, to_id, length, freespeed, capacity, permlanes, oneway, modes)
        VALUES (?,?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('link_id'),
        data.get('from_id'),
        data.get('to_id'),
        data.get('length'),
        data.get('freespeed'),
        data.get('capacity'),
        data.get('permlanes'),
        data.get('oneway'),
        data.get('modes')
    ))

# Connect to SQLite database
conn = sqlite3.connect('Transportation.db')
cursor = conn.cursor()

# Create tables if they don't exist
create_tables(cursor)

# Parse and insert events data
outevents_tree = ET.parse('output_events.xml')
outevents_root = outevents_tree.getroot()

for event_elem in outevents_root.findall('.//event'):
    event_data = {
        'time': event_elem.get('time'),
        'type': event_elem.get('type'),
        'link': event_elem.get('link'),
        'vehicle': event_elem.get('vehicle'),
        'facility': event_elem.get('facility'),
        'delay': event_elem.get('delay'),
        'person': event_elem.get('person'),
        'networkMode': event_elem.get('networkMode'),
        'relativePosition': event_elem.get('relativePosition'),
        'legMode': event_elem.get('legMode'),
        'actType': event_elem.get('actType'),
        'taskType': event_elem.get('taskType'),
        'taskIndex': event_elem.get('taskIndex'),
        'dvrpMode': event_elem.get('dvrpMode')
    }
    insert_events_data(cursor, event_data)

# Parse and insert node data
network_tree = ET.parse('network.xml')
network_root = network_tree.getroot()

for node_elem in network_root.findall('.//node'):
    node_data = {
        'id': node_elem.get('id'),
        'x': node_elem.get('x'),
        'y': node_elem.get('y')
    }
    insert_node_data(cursor, node_data)

# Parse and insert link data (Incomplete in your provided code)
for link_elem in network_root.findall('.//link'):
    link_data = {
        'link_id': link_elem.get('id'),
        'from_id': link_elem.get('from'),
        'to_id': link_elem.get('to'),
        'length': link_elem.get('length'),
        'freespeed': link_elem.get('freespeed'),
        'capacity': link_elem.get('capacity'),
        'permlanes': link_elem.get('permlanes'),
        'oneway': link_elem.get('oneway'),
        'modes': link_elem.get('modes')
    }
    insert_link_data(cursor, link_data)

# Commit changes and close connection
conn.commit()
conn.close()
