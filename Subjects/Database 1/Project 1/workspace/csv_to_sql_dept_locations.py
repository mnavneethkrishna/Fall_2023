import mysql.connector
import csv
from datetime import datetime


# Define your database connection parameters
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "kantrakutti",
    "database": "nxk0459",
}

# Create a connection to the MySQL database
connection = mysql.connector.connect(**db_config)

# Create a cursor to execute SQL statements
cursor = connection.cursor()

try:
    # Open the 'EMPLOYEE.csv' file for reading
    with open('DEPT_LOCATIONS.csv', 'r', newline='\n') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Iterate through the rows in the .csv file
        for row in csv_reader:
            # Extract data from the row
            Dnumber = row[0]
            Dnumber = Dnumber.replace("'","")
            Dnumber = Dnumber.replace(" ","")
            Dnumber = int(Dnumber)

            Dlocation = row[1]
            Dlocation = Dlocation.replace("'","")
            Dlocation = Dlocation.replace(" ","")

            # Define the SQL INSERT statement using parameterized query
            insert_query = """
                INSERT INTO DEPT_LOCATIONS (Dnumber, Dlocation)
                VALUES (%s, %s)
            """
            # Execute the INSERT statement with data from the .csv file
            cursor.execute(insert_query, (Dnumber, Dlocation))
            
            # Commit the transaction after each INSERT
            connection.commit()

except mysql.connector.Error as error:
    print("Error: {}".format(error))

finally:
    # Close the cursor and database connection
    cursor.close()
    connection.close()
