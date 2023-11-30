import sqlite3
# We created this file just to run the queries
# Connect to SQLite database
conn = sqlite3.connect('Transportation.db')
cursor = conn.cursor()

# Execute the SQL query
cursor.execute("SELECT * FROM Events WHERE person= 'p_9031'")

# Fetch all rows
rows = cursor.fetchall()

# Check if there are rows
if rows:
    # Print the results
    for row in rows:
        print(row)
else:
    print("No data found for the specified link ID.")

# Close the connection
conn.close()