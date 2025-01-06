import mysql.connector

def test_connection():
    print("Attempting to connect to the database...")
    try:
        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database='pandeyji_eatery' 
        )
        print("Connection successful!")
        cnx.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_connection()
