from flask import Flask, request, Response, jsonify
import os
import json
from validate import validate_name, validate_phone
from database import insert, select, delete_name, delete_number
from login import login

import logging

logging.basicConfig(filename="phonebook.log", format='%(asctime)s %(message)s', filemode='a', level=logging.INFO)
logger = logging.getLogger()

app = Flask(__name__)

def generate_response(message, status_code, data=None):
    response_data = {"message": message}
    if data:
        response_data["data"] = data
    json_response = json.dumps(response_data, indent=4)
    return Response(json_response, status=status_code, mimetype='application/json')

@app.route('/PhoneBook/')
def home():
    return "<h1>Please use API calls / Postman to access the API</h1>"

@app.route('/PhoneBook/list', methods=['GET'])
def list_entries():
    data = select()
    return generate_response("Success", 200, data)

@app.route('/PhoneBook/add', methods=['POST'])
def add_entry():
    data = request.get_json()
    cred_flag, ret_login = login(data)
    if not cred_flag:
        return ret_login
    
    name = data.get('name')
    phone = data.get('phonenumber')
    username = data.get("username")

    if not name or not phone:
        return generate_response("Name or phone number missing!", 400)

    if validate_name(name) and validate_phone(phone):
        message, status_code = insert(username, name, phone)
        return generate_response(message, status_code)
    else:
        return generate_response("Invalid Name or Phone Format", 400)

@app.route('/PhoneBook/deleteByName', methods=['PUT'])
def delete_entry_by_name():
    data = request.get_json()
    cred_flag, ret_login = login(data)
    if not cred_flag:
        return ret_login
    
    name = data.get('name')
    username = data.get("username")

    if not name:
        return generate_response("Name missing!", 400)

    if validate_name(name):
        message, status_code = delete_name(username, name)
        return generate_response(message, status_code)
    else:
        return generate_response("Invalid Name Format", 400)

@app.route('/PhoneBook/deleteByNumber', methods=['PUT'])
def delete_entry_by_number():
    data = request.get_json()
    cred_flag, ret_login = login(data)
    if not cred_flag:
        return ret_login

    phone = data.get('phonenumber')
    username = data.get("username")

    if not phone:
        return generate_response("Phone number missing!", 400)

    if validate_phone(phone):
        message, status_code = delete_number(username, phone)
        return generate_response(message, status_code)
    else:
        return generate_response("Invalid Phone Format", 400)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=True, host='0.0.0.0', port=port)
