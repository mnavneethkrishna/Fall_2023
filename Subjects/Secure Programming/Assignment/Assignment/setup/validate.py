import re
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def validate_phone(phone):
    phone_patterns = [
        "^[0-9]{5}( [0-9]{5})?$",
        "^[0-9]{5}\\.[0-9]{5}$",
        "(^\\+[1-9]{1,2}[ ]?\\(|^[1][ ]?\\(|^[0][1][1][ ][1]?[ ]?\\(?|^\\(?)"
        "([1-9][0-9]{1,2})?\\)?[- ]?([0-9]{3})[-| ]([0-9]{4})$",
        "^(\\+[0-9]{2} )?([0-9]{2} ){3}[0-9]{2}$",
        "^1?(\\([0-9]{3}\\)|[ ]?[0-9]{3} |\\.?[0-9]{3}\\.|-?[0-9]{3}-)[0-9]{3}[ .-]?[0-9]{4}$"
    ]

    for pattern in phone_patterns:
        if re.match(pattern, phone):
            logger.info(f"VALIDATE: Pattern: {pattern}, Phone: {phone}")
            return True

    return False

def validate_name(name):
    name_patterns = [
        "^[A-Za-z]+[’\'-]?[A-Za-z]+[.]?( [A-Za-z]+([’\'-]?[A-Za-z]+[.]?){0,2}){0,2}$",
        "^[A-Za-z]+[’\'-]?[A-Za-z]+[.]?,( [A-Za-z]+([’\'-]?[A-Za-z]+[.]?){0,2}){0,2}$",
        "^[A-Za-z]+[’\'-]?[A-Za-z]+[.]?( [A-Za-z]+[.]?){0,2}$",
        "^[A-Za-z]+[’\'-]?[A-Za-z]+[.]?,( [A-Za-z]+[.]?){1,2}$"
    ]

    for pattern in name_patterns:
        if re.match(pattern, name):
            logger.info(f"VALIDATE: Pattern: {pattern}, Name: {name}")
            return True

    return False

def validate_username(username):
    username_patterns = ["^[A-Za-z0-9._]{6,24}$"]

    for pattern in username_patterns:
        if re.match(pattern, username):
            logger.info(f"VALIDATE: Pattern: {pattern}, Username: {username}")
            return True

    return False

def validate_password(password):
    password_patterns = ["^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@]{8,20}$"]

    for pattern in password_patterns:
        if re.match(pattern, password):
            return True

    return False
