from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import sqlite3
import io
from PIL import Image
import base64
import tools

# buffer last 20 samples
BUFFER_SIZE = 20
latestBrainData = []

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "hello, i'm your brain"})

# returns all past messages for a given user
@app.route('/getPastMessages', methods=['GET'])
def getPastMessages():
    try:
        # Get parameters
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        data = request.get_json(force=True)
        userID = data["userID"]

        response = tools.get_all_messages_per_user(userID, cur)
        return jsonify({"messages": response})

    except Exception as e:
        return jsonify({"response": "failure", "error": str(e)}), 500
    
# returns all log ids for a given user
@app.route('/getAllLogsPerUser', methods=['GET'])
def getAllLogsPerUser():
    try:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        data = request.get_json(force=True)
        userID = data["userID"]

        logsID = tools.get_log_id_per_user(userID, cur)
        return jsonify({"logsID": logsID})

    except Exception as e:
        return jsonify({"response": "failure", "error": str(e)}), 500

# get latest brain data
@app.route('/getLatestBrainData', methods=['GET'])
def getLatestBrainData():
    try:
        return jsonify(latestBrainData[-1])

    except Exception as e:
        return jsonify({"response": "failure", "error": str(e)}), 500

# upload image of distractions
@app.route('/uploadImage', methods=['POST'])
def uploadImage():
    
    image_file_1 = request.files['current_image']
    image_file_2 = request.files['past_image']
    image_blob_1 = image_file_1.read()  # Read the binary data of the image
    image_blob_2 = image_file_2.read()  # Read the binary data of the image

    with open("current_image.jpg", "wb") as f:
        f.write(image_blob_1)

    with open("past_image.jpg", "wb") as f:
        f.write(image_blob_2)

    # CALL BONS CV HERE

    return jsonify({"response": "success"})

# upload brain data
@app.route('/uploadBrainData', methods=['POST'])
def uploadBrainData():
    try:
        brainData = request.json

        if len(latestBrainData) < BUFFER_SIZE:
            latestBrainData.append(brainData)
        else:
            latestBrainData.pop(0)
            latestBrainData.append(brainData)

        print(brainData)

        #latestBrainData[userID] = brainData
        return jsonify({"response": "success"})

    except Exception as e:
        return jsonify({"response": "failure", "error": str(e)}), 500

# upload new user
@app.route('/addNewUser', methods=['POST'])
def addNewUser():
    try:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        data = request.get_json(force=True)

        username = data["username"]
        password = data["password"]
        print("ADD NEW USER")
        print(username)
        print(password)

        doesExist = tools.does_username_already_exist(username, cur)
        print(doesExist)
        if doesExist:
            userID = None
        else:
            userID = tools.add_user(username, password, cur)
        # send to database

        return jsonify({"userID": userID})

    except Exception as e:
        return jsonify({"response": "failure", "error": str(e)}), 500
    
# upload new user
@app.route('/tryLogin', methods=['POST'])
def tryLogin():
    try:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        data = request.get_json(force=True)

        username_try = data["username"]
        password_try = data["password"]

        user_info = tools.get_user_infos_from_username(username_try, cur)
        print(user_info)
        user_id = user_info[0]
        password_real = user_info[1]

        if password_real == password_try:
            userID = user_id
        else:
            userID =  None

        return jsonify({"userID": userID})

    except Exception as e:
        return jsonify({"response": "failure", "error": str(e)}), 500
    
# upload new user
@app.route('/doesUserExist', methods=['POST'])
def doesUserExist():
    try:
        username = request.args.get('username')  # Extract 'userID' from the query parameters

        # check user in database
        userExist = False

        return jsonify({"userExist": userExist})

    except Exception as e:
        return jsonify({"response": "failure", "error": str(e)}), 500
    
# upload new user
@app.route('/newLog', methods=['POST'])
def newLog():
    try:
        username = request.args.get('username')  # Extract 'userID' from the query parameters
        timestamp = 100 # need to get this live

        # add record to log table

        return jsonify({"response": "success"})

    except Exception as e:
        return jsonify({"response": "failure", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)