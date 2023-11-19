import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta

# Function to connect to the MySQL database
def connect_to_database():
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='****',
            host='localhost',
            database='project_2'
        )
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Please check your credentials.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print(f"Error: {err}")
        return None

# Function to add information about a new member
def add_new_member(cnx):
    print("Enter information for a new member:")
    ssn = input("SSN: ")
    name = input("Name: ")
    home_address = input("Home Address: ")
    campus_address = input("Campus Address: ")
    phone_no = input("Phone Number: ")
    member_type = input("Member Type: ")
    grace_period = int(input("Grace Period: "))
    borrow_period = int(input("Borrow Period: "))
    employee_type = input("Employee Type: ")
    staff_type = input("Staff Type: ")

    query = "INSERT INTO MEMBER (SSN, NAME, HOME_ADDRESS, CAMPUS_ADDRESS, PHONE_NO, MEMBER_TYPE, GRACE_PERIOD, BORROW_PERIOD, EMPLOYEE_TYPE, STAFF_TYPE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (ssn, name, home_address, campus_address, phone_no, member_type, grace_period, borrow_period, employee_type, staff_type)

    execute_query(cnx, query, data)

# Function to add information about a new book
def add_new_book(cnx):
    print("Enter information for a new book:")
    isbn = int(input("ISBN: "))
    title = input("Title: ")
    binding = input("Binding: ")
    language = input("Language: ")
    edition = input("Edition: ")
    author = input("Author: ")
    description = input("Description: ")
    volume = input("Volume: ")
    subject_area = input("Subject Area: ")
    book_type = input("Book Type: ")
    availability = input("Availability (Y/N): ").upper()
    status_type = input("Status Type: ")

    query = "INSERT INTO BOOK (ISBN, TITLE, BINDING, LANGUAGE, EDITION, AUTHOR, DESCRIPTION, VOLUME, SUBJECT_AREA, BOOK_TYPE, AVAILABILITY, STATUS_TYPE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = (isbn, title, binding, language, edition, author, description, volume, subject_area, book_type, availability, status_type)

    execute_query(cnx, query, data)

# Function to add information about a new borrow (loan)
def add_new_borrow(cnx):
    print("Enter information for a new borrow:")
    book_id = int(input("Book ID: "))
    m_ssn = int(input("Member SSN: "))
    issued_by = int(input("Issued By (Staff SSN): "))
    issue_date = input("Issue Date (YYYY-MM-DD): ")
    due_date = input("Due Date (YYYY-MM-DD): ")

    query = "INSERT INTO BORROW (BOOK_ID, M_SSN, ISSUED_BY, ISSUE_DATE, DUE_DATE) VALUES (%s, %s, %s, %s, %s)"
    data = (book_id, m_ssn, issued_by, issue_date, due_date)

    execute_query(cnx, query, data)

# Function to handle the return of a book
def handle_book_return(cnx):
    print("Enter information to handle the return of a book:")
    book_id = int(input("Book ID: "))
    m_ssn = int(input("Member SSN: "))
    issue_date = input("Issue Date (YYYY-MM-DD): ")
    return_date = input("Return Date (YYYY-MM-DD): ")

    query = "UPDATE BORROW SET RETURN_DATE = %s WHERE BOOK_ID = %s AND M_SSN = %s AND ISSUE_DATE = %s"
    data = (return_date, book_id, m_ssn, issue_date)

    execute_query(cnx, query, data)

    # Print return receipt
    print(f"Return Receipt:")
    print(f"Book ID: {book_id}")
    print(f"Member SSN: {m_ssn}")
    print(f"Issue Date: {issue_date}")
    print(f"Return Date: {return_date}")

# Function to renew membership
def renew_membership(cnx):
    print("Enter information to renew membership:")
    ssn = int(input("Member SSN: "))
    new_expiry_date = input("New Expiry Date (YYYY-MM-DD): ")

    query = "UPDATE CARD SET EXPIRY_DATE = %s WHERE M_SSN = %s"
    data = (new_expiry_date, ssn)

    execute_query(cnx, query, data)

    print(f"Membership renewed for Member SSN: {ssn}")

# Function to execute a SQL query with data
def execute_query(cnx, query, data):
    try:
        cursor = cnx.cursor()
        cursor.execute(query, data)
        cnx.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Main function
def main():
    # Connect to the database
    cnx = connect_to_database()
    if not cnx:
        return

    try:
        # Example of calling transactions
        add_new_member(cnx)
        add_new_book(cnx)
        add_new_borrow(cnx)
        handle_book_return(cnx)
        renew_membership(cnx)

    finally:
        # Close the database connection
        cnx.close()

if __name__ == "__main__":
    main()
