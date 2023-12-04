import curses
import json
import threading
import time

import requests
from time import sleep
from arduino_connector import Uno

api_url = "https://w1fyv4m4j3.execute-api.us-west-2.amazonaws.com/prod/"

cur_state = {
    "aT": "Dodgers",
    "hT": "Padres",
    "aS": 0,
    "hS": 0,
    "in": 1,
    "iH": "bottom",
    "outs": 0,
    "count": [0, 0],
    "on_base": "000",
    "last-play": "",
}


def call_get_request():
    try:
        # make a GET request to the API
        response = requests.get(api_url)

        # check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"API request failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


def load_score():
    data = call_get_request()
    cur_state["aT"] = data["away-team"]
    cur_state["hT"] = data["home-team"]
    cur_state["aS"] = data["away-score"]
    cur_state["hS"] = data["home-score"]
    cur_state["in"] = data["inning"]
    cur_state["iH"] = data["inning-half"]
    cur_state["outs"] = data["outs"]
    cur_state["cnt"] = data["count"]
    cur_state["bases"] = data["on_base"]
    cur_state["lP"] = data["last-play"]


# Define the Arduino-related operations in a separate function
def arduino_operations():
    arduino = Uno('/dev/cu.usbmodem1401', 9600)
    time.sleep(2)

    while True:
        load_score()
        arduino.send_data(json.dumps(cur_state))
        time.sleep(3)


def main():
    arduino_operations()


if __name__ == "__main__":
    main()