import json
import time
import config

import requests
from arduino_connector import Uno

api_url = config.api_key

cur_state = {
    "aT": "Dodgers",
    "aA": "LAD",
    "hT": "Padres",
    "hA": "SD",
    "aS": 0,
    "hS": 0,
    "in": 1,
    "iH": "t",
    "outs": 0,
    "count": [0, 0],
    "bases": "100",
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


def set_bases(bases):
    res = []
    for i in range(len(bases) - 1):
        res.append(f"{i + 1 if bases[i] else 0}")
    return "".join(res)


def set_inning_half(inning_half):
    if inning_half == "top":
        return "t"
    else:
        return "b"


def load_score():
    data = call_get_request()
    cur_state["aT"] = data["away-team"]
    cur_state["aA"] = data["away-abrv"]
    cur_state["hT"] = data["home-team"]
    cur_state["hA"] = data["home-abrv"]
    cur_state["aS"] = data["away-score"]
    cur_state["hS"] = data["home-score"]
    cur_state["in"] = data["inning"]
    cur_state["iH"] = set_inning_half(data["inning-half"])
    cur_state["outs"] = data["outs"]
    cur_state["cnt"] = data["count"]
    cur_state["bases"] = set_bases(data["on_base"])
    cur_state["lP"] = data["last-play"]


# Define the Arduino-related operations in a separate function
def arduino_operations():
    arduino = Uno('/dev/cu.usbmodem211401', 9600)
    time.sleep(2)

    while True:
        load_score()
        json_data = json.dumps(cur_state)
        arduino.send_data(json_data)
        print(json_data)
        time.sleep(3)


def main():
    arduino_operations()


if __name__ == "__main__":
    main()
