import requests
import sys
import json
import threading
import io
import time
from picamera2 import Picamera2
from brain_py import Brain

picam2 = Picamera2()
imageBuf = [io.BytesIO(), io.BytesIO()]
imageBuf_lock = threading.Lock()

def main():
    brain = Brain()
    address = "http://"+sys.argv[1]
    print("Starting camera...")
    picam2.start()
    camThread = threading.Thread(target=camera_loop, args=(address,))
    camThread.start()
    while True:
        brain_data = brain.read()
        response = requests.post(address+"/uploadBrainData", json=json.dumps(brain_data))
        # with imageBuf_lock:
        print(brain_data)
    camThread.join()

def camera_loop(address):
    while True:
        with imageBuf_lock:
            del imageBuf[0]
            imageBuf.append(io.BytesIO())
            print("Taking image")
            picam2.capture_file(imageBuf[1], format='jpeg')
            imageBuf[1].seek(0,0)
        time.sleep(30)
        response = requests.post(address+"/uploadImage", files={'past_image': imageBuf[0], 'current_image': imageBuf[1]})


if __name__ == "__main__":
    if(len(sys.argv) == 2):
        main()
    else:
        print("Please provide an IP address and userID")
