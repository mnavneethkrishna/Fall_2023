CREATE TABLE MEMBER
(
SSN INT,
NAME VARCHAR(50),
HOME_ADDRESS VARCHAR(1000),
CAMPUS_ADDRESS VARCHAR(1000),
PHONE_NO VARCHAR(50),
MEMBER_TYPE VARCHAR(50),
GRACE_PERIOD INT,
BORROW_PERIOD INT, 
EMPLOYEE_TYPE VARCHAR(50),
STAFF_TYPE VARCHAR(50),
PRIMARY KEY(SSN)
);

CREATE TABLE BOOK
(
ISBN INT,
TITLE VARCHAR(100),
BINDING VARCHAR(20),
LANGUAGE VARCHAR(100),
EDITION VARCHAR(30),
AUTHOR VARCHAR(50),
DESCRIPTION LONGTEXT,
VOLUME VARCHAR(30),
SUBJECT_AREA VARCHAR(100),
BOOK_TYPE VARCHAR(30),
AVAILABILITY CHAR(1) NOT NULL CHECK(AVAILABILITY IN('Y', 'N')),
STATUS_TYPE VARCHAR(30),
PRIMARY KEY(ISBN)
);

CREATE TABLE CARD
(
CARD_ID INT,
PHOTO BLOB,
ISSUE_DATE DATE,
EXPIRY_DATE DATE,
VALIDITY DATE,
M_SSN INT,
PRIMARY KEY (CARD_ID),
FOREIGN KEY (M_SSN) REFERENCES MEMBER(SSN) ON DELETE CASCADE
);

CREATE TABLE COPY( 
BOOK_ID INT, 
ISBN INT NOT NULL, 
STATUS VARCHAR(20), 
PRIMARY KEY(BOOK_ID),
FOREIGN KEY(ISBN) REFERENCES BOOK(ISBN) ON DELETE CASCADE
);

CREATE TABLE BORROW
(
BOOK_ID INT,
M_SSN INT,
ISSUED_BY INT,
ISSUE_DATE DATE,
DUE_DATE DATE,
RETURN_DATE DATE,
GRACE_PERIOD DATE,
STATUS VARCHAR(20),
PRIMARY KEY(BOOK_ID,M_SSN,ISSUE_DATE),
FOREIGN KEY(BOOK_ID) REFERENCES COPY(BOOK_ID),
FOREIGN KEY(M_SSN) REFERENCES MEMBER(SSN),
FOREIGN KEY(ISSUED_BY) REFERENCES MEMBER(SSN)
);

CREATE TABLE VISITS
(
M_SSN INT,
CHECK_IN DATE,
CHECK_OUT DATE,
NAME VARCHAR(50),
PASS_ID INT,
VISITOR_TYPE VARCHAR(50),
VALIDITY_DATE DATE,
PRIMARY KEY (M_SSN,CHECK_IN),
FOREIGN KEY (M_SSN)REFERENCES MEMBER(SSN)
);

-- Trigger to notify a member about an outstanding overdue book
DELIMITER //
CREATE TRIGGER NOTIFY_OVERDUE_BOOK
AFTER INSERT ON BORROW
FOR EACH ROW
BEGIN
    DECLARE V_DUE_DATE DATE;
    DECLARE V_MESSAGE VARCHAR(255);
    
    -- Get the due date of the book
    SELECT DUE_DATE INTO V_DUE_DATE
    FROM BORROW
    WHERE BOOK_ID = NEW.BOOK_ID AND M_SSN = NEW.M_SSN AND ISSUE_DATE = NEW.ISSUE_DATE;
    
    -- Check if the book was returned after its due date
    IF NEW.RETURN_DATE IS NOT NULL AND NEW.RETURN_DATE > V_DUE_DATE THEN
        -- Set the message
        SET V_MESSAGE = CONCAT('Book due on ', DATE_FORMAT(V_DUE_DATE, '%Y-%m-%d'), '. Returned on ', DATE_FORMAT(NEW.RETURN_DATE, '%Y-%m-%d'), '.');
        -- Raise an exception
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = V_MESSAGE;
    END IF;
END;
//
DELIMITER ;

-- Trigger to notify a member about membership renewal after INSERT
DELIMITER //
CREATE TRIGGER NOTIFY_MEMBERSHIP_RENEWAL_INSERT
AFTER INSERT ON BORROW
FOR EACH ROW
BEGIN
    DECLARE V_EXPIRY_DATE DATE;
    DECLARE V_MEMBER_NAME VARCHAR(50);
    DECLARE V_MESSAGE VARCHAR(255);
    
    -- Get the expiry date of the member's card
    SELECT EXPIRY_DATE INTO V_EXPIRY_DATE
    FROM CARD
    WHERE M_SSN = NEW.M_SSN;
    
    -- Get the name of the member
    SELECT NAME INTO V_MEMBER_NAME
    FROM MEMBER
    WHERE SSN = NEW.M_SSN;
    
    -- Check if the issue date or due date is after the expiry date
    IF NEW.ISSUE_DATE > V_EXPIRY_DATE OR NEW.DUE_DATE > V_EXPIRY_DATE THEN
        -- Set the message
        SET V_MESSAGE = CONCAT('The membership of ', V_MEMBER_NAME, ' must be renewed!');
        -- Raise an exception
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = V_MESSAGE;
    END IF;
END;
//
DELIMITER ;

-- Trigger to notify a member about membership renewal after UPDATE
DELIMITER //
CREATE TRIGGER NOTIFY_MEMBERSHIP_RENEWAL_UPDATE
AFTER UPDATE ON BORROW
FOR EACH ROW
BEGIN
    DECLARE V_EXPIRY_DATE DATE;
    DECLARE V_MEMBER_NAME VARCHAR(50);
    DECLARE V_MESSAGE VARCHAR(255);
    
    -- Get the expiry date of the member's card
    SELECT EXPIRY_DATE INTO V_EXPIRY_DATE
    FROM CARD
    WHERE M_SSN = NEW.M_SSN;
    
    -- Get the name of the member
    SELECT NAME INTO V_MEMBER_NAME
    FROM MEMBER
    WHERE SSN = NEW.M_SSN;
    
    -- Check if the issue date or due date is after the expiry date
    IF NEW.ISSUE_DATE > V_EXPIRY_DATE OR NEW.DUE_DATE > V_EXPIRY_DATE THEN
        -- Set the message
        SET V_MESSAGE = CONCAT('The membership of ', V_MEMBER_NAME, ' must be renewed!');
        -- Raise an exception
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = V_MESSAGE;
    END IF;
END;
//
DELIMITER ;




