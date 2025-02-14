import sqlite3

# Connect to SQLite3
connection = sqlite3.connect("student.db")

# Create a cursor object to insert, record, create table, and retrieve
cursor = connection.cursor()

# Create the table if it does not exist
table_info = """
CREATE TABLE IF NOT EXISTS student (
    Name VARCHAR(30), 
    class VARCHAR(30), 
    section VARCHAR(30), 
    marks INT
);
"""
cursor.execute(table_info)

# Inserting records (use try-except to avoid duplicate inserts)
try:
    cursor.execute("INSERT INTO student VALUES ('krish', 'data science', 'A', 90)")
    cursor.execute("INSERT INTO student VALUES ('vaishu', 'data science', 'B', 54)")
    cursor.execute("INSERT INTO student VALUES ('vaishnavi', 'data science', 'A', 99)")
    cursor.execute("INSERT INTO student VALUES ('krishna', 'machine learning', 'A', 92)")
except sqlite3.IntegrityError:
    print("Some records already exist.")

# Display all the records
print("The inserted records are:")

# Correct the table name case and retrieve data
data = cursor.execute("SELECT * FROM student")

for row in data:
    print(row)

# Close the connection
connection.commit()
connection.close()
