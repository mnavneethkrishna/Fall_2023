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
    with open('EMPLOYEE.csv', 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        # Iterate through the rows in the .csv file
        for row in csv_reader:
            # Extract data from the row
            Fname = row[0]
            Fname = Fname.replace("'", "")
            if Fname == "null":
                Fname = ""
            Minit = row[1]
            Minit = Minit.replace("'", "")
            Minit = Minit.replace(" ", "")
            if Minit == "null":
                Minit = ""

            Lname = row[2]
            Lname = Lname.replace("'", "")
            Lname = Lname.replace(" ", "")
            if Lname == "null":
                Lname = ""

            Ssn = row[3]
            Ssn = Ssn.replace("'", "")
            Ssn = Ssn.replace(" ", "")
            if Ssn == "null":
                Ssn = ""
            
            Birthday = row[4]
            Birthday = Birthday.replace("'", "")
            Birthday = Birthday.replace(" ", "")
            if Birthday == "null":
                Birthday = ""
            else:
                Birthday = datetime.strptime(Birthday.strip(), '%d-%b-%Y').date()

            Address = row[5] + " " + row[6] + " " + row[7]
            Address = Address.replace("'", "")
            
            Sex = row[8]
            Sex = Sex.replace("'", "")
            Sex = Sex.replace(" ", "")
            if Sex == "null":
                Sex = ""
            
            Salary = row[9]
            Salary = float(Salary)
            
            Super_ssn = row[10]
            Super_ssn = Super_ssn.replace("'", "")
            Super_ssn = Super_ssn.replace(" ", "")

            Dno = row[11]
            Dno = Dno.replace("'", "")
            Dno = Dno.replace(" ", "")
            Dno = int(Dno)  

            # Define the SQL INSERT statement using parameterized query
            insert_query = """
                INSERT INTO EMPLOYEE (Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Execute the INSERT statement with data from the .csv file
            cursor.execute(insert_query, (Fname, Minit, Lname, Ssn, Birthday, Address, Sex, Salary, Super_ssn, Dno))
            
            # Commit the transaction after each INSERT
            connection.commit()

except mysql.connector.Error as error:
    print("Error: {}".format(error))

finally:
    # Close the cursor and database connection
    cursor.close()
    connection.close()
