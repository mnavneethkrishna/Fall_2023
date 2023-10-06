import mysql.connector
import csv

# Define your database connection parameters
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "*****",
    "database": "Project_1",
}

# Create a connection to the MySQL database
connection = mysql.connector.connect(**db_config)

# Create a cursor to execute SQL statements
cursor = connection.cursor()

try:
    # Open the 'EMPLOYEE.csv' file for reading
    with open('EMPLOYEE.csv', 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Skip the header row if present
        next(csv_reader)
        
        # Iterate through the rows in the .csv file
        for row in csv_reader:
            # Extract data from the row
            Fname = row[0].strip("'")
            Minit = row[1].strip("'")
            Lname = row[2].strip("'")
            Ssn = row[3].strip("'")
            
            # Check if there are enough values in the row
            if len(row) >= 5:
                Bdate_str = row[4].strip("'")
            else:
                Bdate_str = ""
            
            # Check if there are enough values in the row
            if len(row) >= 6:
                Address = row[5].strip("'")
            else:
                Address = ""
            
            # Check if there are enough values in the row
            if len(row) >= 7:
                Sex = row[6].strip("'")
            else:
                Sex = ""
            
            # Check if there are enough values in the row
            if len(row) >= 8:
                Salary = float(row[7].strip("'")) if row[7].strip("'") != "null" else None
            else:
                Salary = None
            
            # Check if there are enough values in the row
            if len(row) >= 9:
                Super_ssn = row[8].strip("'") if row[8].strip("'") != "null" else None
            else:
                Super_ssn = None
            
            # Check if there are enough values in the row
            if len(row) >= 10:
                Dno = int(row[9])
            else:
                Dno = None

            # Define the SQL INSERT statement using parameterized query
            insert_query = """
                INSERT INTO EMPLOYEE (Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Execute the INSERT statement with data from the .csv file
            cursor.execute(insert_query, (Fname, Minit, Lname, Ssn, Bdate_str, Address, Sex, Salary, Super_ssn, Dno))
            
            # Commit the transaction after each INSERT
            connection.commit()

except mysql.connector.Error as error:
    print("Error: {}".format(error))

finally:
    # Close the cursor and database connection
    cursor.close()
    connection.close()
