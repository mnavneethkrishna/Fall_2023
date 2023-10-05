-- Create the DEPARTMENT table
CREATE TABLE DEPARTMENT (
    Dnumber INT NOT NULL PRIMARY KEY,
    Dname VARCHAR(15) NOT NULL,
    Mgr_ssn CHAR(9) NOT NULL UNIQUE,
    Mgr_start_date DATE
);

-- Create the EMPLOYEE table with OverTimeCount attribute
CREATE TABLE EMPLOYEE (
    Fname VARCHAR(15) NOT NULL,
    Minit CHAR,
    Lname VARCHAR(15) NOT NULL,
    Ssn CHAR(9) NOT NULL PRIMARY KEY,
    Bdate DATE,
    Address VARCHAR(30),
    Sex CHAR(1),
    Salary DECIMAL(10, 2),
    Super_ssn CHAR(9),
    Dno INT NOT NULL,
    OverTimeCount INT DEFAULT 0, -- Added 'OverTimeCount' attribute
    FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber),
    FOREIGN KEY (Super_ssn) REFERENCES EMPLOYEE(Ssn)
);

-- Create the DEPT_LOCATIONS table
CREATE TABLE DEPT_LOCATIONS (
    Dnumber INT NOT NULL,
    Dlocation VARCHAR(15) NOT NULL,
    PRIMARY KEY (Dnumber, Dlocation),
    FOREIGN KEY (Dnumber) REFERENCES DEPARTMENT(Dnumber)
);

-- Create the PROJECT table
CREATE TABLE PROJECT (
    Pname VARCHAR(15) NOT NULL,
    Pnumber INT NOT NULL PRIMARY KEY,
    Plocation VARCHAR(15),
    Dnum INT NOT NULL,
    FOREIGN KEY (Dnum) REFERENCES DEPARTMENT(Dnumber)
);

-- Create the WORKS_ON table
CREATE TABLE WORKS_ON (
    Essn CHAR(9) NOT NULL,
    Pno INT NOT NULL,
    Hours DECIMAL(3, 1) NOT NULL,
    PRIMARY KEY (Essn, Pno),
    FOREIGN KEY (Essn) REFERENCES EMPLOYEE(Ssn),
    FOREIGN KEY (Pno) REFERENCES PROJECT(Pnumber)
);

-- Create the DEPENDENT table
CREATE TABLE DEPENDENT (
    Essn CHAR(9) NOT NULL,
    Dependent_name VARCHAR(15) NOT NULL,
    Sex CHAR(1),
    Bdate DATE,
    Relationship VARCHAR(8),
    PRIMARY KEY (Essn, Dependent_name),
    FOREIGN KEY (Essn) REFERENCES EMPLOYEE(Ssn)
);

-- Create the trigger to update OverTimeCount
DELIMITER //
CREATE TRIGGER calculate_overtime
AFTER INSERT ON WORKS_ON
FOR EACH ROW
BEGIN
    DECLARE total_hours DECIMAL(10, 2);
    DECLARE weekly_threshold DECIMAL(10, 2) DEFAULT 40.0;

    -- Calculate the total hours worked by the employee on all projects in the current week
    SELECT SUM(Hours) INTO total_hours
    FROM WORKS_ON
    WHERE Essn = NEW.Essn;

    -- Check if the total hours exceed the weekly threshold
    IF total_hours > weekly_threshold THEN
        -- Update the OverTimeCount for the employee
        UPDATE EMPLOYEE
        SET OverTimeCount = OverTimeCount + 1
        WHERE Ssn = NEW.Essn;
    END IF;
END;
//
DELIMITER ;
