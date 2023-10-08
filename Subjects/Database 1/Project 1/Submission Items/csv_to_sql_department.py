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
    with open('DEPARTMENT.csv', 'r', newline='\n') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Iterate through the rows in the .csv file
        for row in csv_reader:
            # Extract data from the row
            Dname = row[0]
            Dname = Dname.replace("'","")
            Dname = Dname.replace(" ","")

            Dno = row[1]
            Dno = Dno.replace("'","")
            Dno = Dno.replace(" ","")
            Dno = int(Dno)

            Mgr_ssn = row[2]
            Mgr_ssn = Mgr_ssn.replace("'","")
            Mgr_ssn = Mgr_ssn.replace(" ","")

            Mgr_start_date = row[3]
            Mgr_start_date = Mgr_start_date.replace("'","")
            Mgr_start_date = Mgr_start_date.replace(" ","")
            Mgr_start_date = datetime.strptime(Mgr_start_date.strip(), '%d-%b-%Y').date()

            # Define the SQL INSERT statement using parameterized query
            insert_query = """
                INSERT INTO DEPARTMENT (Dname, Dnumber, Mgr_ssn, Mgr_start_date)
                VALUES (%s, %s, %s, %s)
            """
            print("Dno", Dno)
            # Execute the INSERT statement with data from the .csv file
            cursor.execute(insert_query, (Dname, Dno, Mgr_ssn, Mgr_start_date))
            
            # Commit the transaction after each INSERT
            connection.commit()

except mysql.connector.Error as error:
    print("Error: {}".format(error))

finally:
    # Close the cursor and database connection
    cursor.close()
    connection.close()
