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
    with open('DEPENDENT.csv', 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Iterate through the rows in the .csv file
        for row in csv_reader:
            # Extract data from the row
            Essn = row[0]
            Essn = Essn.replace("'", "").replace(" ","")

            Dependent_name = row[1]
            Dependent_name = Dependent_name.replace("'", "")
            Dependent_name = Dependent_name.replace(" ", "")

            Sex = row[2]
            Sex = Sex.replace("'", "")
            Sex = Sex.replace(" ", "")
            
            Bdate = row[3]
            Bdate = Bdate.replace("'", "")
            Bdate = Bdate.replace(" ", "")
            if Bdate == "null":
                Bdate = ""
            else:
                Bdate = datetime.strptime(Bdate.strip(), '%d-%b-%Y').date()

            
            Relationship = row[4]
            Relationship = Relationship.replace("'", "")
            Relationship = Relationship.replace(" ", "") 

            # Define the SQL INSERT statement using parameterized query
            insert_query = """
                INSERT INTO DEPENDENT (Essn, Dependent_name, Sex, Bdate, Relationship)
                VALUES (%s, %s, %s, %s, %s)
            """

            # Execute the INSERT statement with data from the .csv file
            cursor.execute(insert_query, (Essn, Dependent_name, Sex, Bdate, Relationship))
            
            # Commit the transaction after each INSERT
            connection.commit()

except mysql.connector.Error as error:
    print("Error: {}".format(error))

finally:
    # Close the cursor and database connection
    cursor.close()
    connection.close()
