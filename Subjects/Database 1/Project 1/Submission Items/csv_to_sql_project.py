import mysql.connector
import csv
from datetime import datetime


# Define your database connection parameters
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "*****",
    "database": "nxk0459",
}

# Create a connection to the MySQL database
connection = mysql.connector.connect(**db_config)

# Create a cursor to execute SQL statements
cursor = connection.cursor()

try:
    # Open the 'EMPLOYEE.csv' file for reading
    with open('PROJECT.csv', 'r', newline='\n') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Iterate through the rows in the .csv file
        for row in csv_reader:
            # Extract data from the row
            Pname = row[0].replace("'","").replace(" ","")

            Pnumber = row[1].replace("'","").replace(" ","")
            Pnumber = int(Pnumber)

            Plocation = row[2].replace("'","").replace(" ","")

            Dnum = row[3].replace("'","").replace(" ","")
            Dnum = int(Dnum)

            # Define the SQL INSERT statement using parameterized query
            insert_query = """
                INSERT INTO PROJECT (Pname, Pnumber, Plocation, Dnum)
                VALUES (%s, %s, %s, %s)
            """
            # Execute the INSERT statement with data from the .csv file
            cursor.execute(insert_query, (Pname, Pnumber, Plocation, Dnum))
            
            # Commit the transaction after each INSERT
            connection.commit()

except mysql.connector.Error as error:
    print("Error: {}".format(error))

finally:
    # Close the cursor and database connection
    cursor.close()
    connection.close()
