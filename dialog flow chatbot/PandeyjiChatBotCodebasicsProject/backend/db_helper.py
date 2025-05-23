# Author: Dhaval Patel. Codebasics YouTube Channel

import mysql.connector

# Global variable for the connection
global cnx

try:
    # Attempting to connect to the MySQL database
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pandeyji_eatery"
    )
    print("Connection to database established successfully!")

except mysql.connector.Error as err:
    print(f"Error connecting to the database: {err}")
    cnx = None

# Function to check if the connection is active
def check_connection():
    if cnx is not None and cnx.is_connected():
        return "Database connection is active."
    else:
        return "Database connection is not established."

# Function to call the MySQL stored procedure and insert an order item
def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        # Committing the changes
        cnx.commit()

        # Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1

# Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    try:
        cursor = cnx.cursor()

        # Inserting the record into the order_tracking table
        insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        cursor.execute(insert_query, (order_id, status))

        # Committing the changes
        cnx.commit()

        # Closing the cursor
        cursor.close()
        print("Order tracking updated successfully!")

    except mysql.connector.Error as err:
        print(f"Error inserting order tracking: {err}")
        cnx.rollback()

# Function to fetch the total order price
def get_total_order_price(order_id):
    try:
        cursor = cnx.cursor()

        # Executing the SQL query to get the total order price
        query = f"SELECT get_total_order_price({order_id})"
        cursor.execute(query)

        # Fetching the result
        result = cursor.fetchone()[0]

        # Closing the cursor
        cursor.close()

        return result

    except mysql.connector.Error as err:
        print(f"Error fetching total order price: {err}")
        return -1

# Function to get the next available order_id
def get_next_order_id():
    try:
        cursor = cnx.cursor()

        # Executing the SQL query to get the next available order_id
        query = "SELECT MAX(order_id) FROM orders"
        cursor.execute(query)

        # Fetching the result
        result = cursor.fetchone()[0]

        # Closing the cursor
        cursor.close()

        # Returning the next available order_id
        if result is None:
            return 1
        else:
            return result + 1

    except mysql.connector.Error as err:
        print(f"Error fetching next order ID: {err}")
        return -1

# Function to fetch the order status from the order_tracking table
def get_order_status(order_id):
    try:
        cursor = cnx.cursor()

        # Executing the SQL query to fetch the order status
        query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
        cursor.execute(query)

        # Fetching the result
        result = cursor.fetchone()

        # Closing the cursor
        cursor.close()

        # Returning the order status
        if result:
            return result[0]
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Error fetching order status: {err}")
        return None


if __name__ == "__main__":
    # Check database connection
    print(check_connection())

    # Example usage
    if cnx and cnx.is_connected():
        print(get_total_order_price(56))
        insert_order_item('Samosa', 3, 105)
        insert_order_item('Pav Bhaji', 1, 106)
        insert_order_tracking(105, "in progress")
        print(get_next_order_id())
