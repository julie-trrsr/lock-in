from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import sqlite3
import io
from PIL import Image
import base64
import tools
import jarvis

# buffer last 20 samples
BUFFER_SIZE = 20
latestBrainData = []

app = Flask(__name__)
CORS(app)

# visionAgent = jarvis.AgentCoordinator()
# eegAgent = jarvis.EEGAgent()
# topLevelAgent = jarvis.TopLevelAgent(visionAgent, eegAgent)

# def condense(summaries):
#     condensed = {}
    
#     for summary in summaries:
#         for key, value in summary.items():
#             if key not in condensed:
#                 condensed[key] = []  # Initialize an empty list if key doesn't exist
#             condensed[key].append(value)  # Append the value to the corresponding list
    
#     return condensed

# eeg_data = {
#     "window_length": 10,
#     "sampling_rate": 10,
#     "alpha_waves": [23, 45, 67, 54, 32, 71, 49, 50, 19, 30],
#     "beta_waves": [42, 68, 86, 90, 72, 56, 44, 99, 86, 63],
#     "gamma_waves": [150, 200, 198, 220, 180, 210, 240, 255, 230, 190],
#     "delta_waves": [5, 3, 10, 7, 25, 22, 15, 8, 2, 14],
#     "theta_waves": [10, 20, 35, 40, 25, 45, 30, 38, 12, 27],
#     "attention_levels": [70, 72, 68, 90, 55, 60, 85, 92, 100, 77]
# }

# resp = topLevelAgent.run_analysis(eeg_data, ["./output_image_1.jpg", "./output_image_2.jpg"])
# if resp:
#     print("Got Agent Response: ", resp)
# else:
#     print("Failed to Get Response", resp)
    
@app.route('/')
def home():
    return jsonify({"message": "hello, i'm your brain"})

# returns all past messages for a given user
@app.route('/getPastMessages', methods=['GET'])
def getPastMessages():
    try:
        # Get parameters
        userID = request.args.get('userID')  # Extract 'userID' from the query parameters

        if not userID:
            return jsonify({"response": "failure", "error": "Missing userID parameter"}), 400

        # SQLITE CODE HERE
        response = {}
        return jsonify(response)

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