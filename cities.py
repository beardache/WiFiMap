__author__ = 'R'
__project__ = 'Wifimap Downloader'

import hashlib
import requests
import time
import random
import json
from os import path

# Config
user_agent = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1; Google Nexus 6 - 5.1.0 - API 22 - '
                  '1440x2560 Build/LMY47D) WiFiMap/2.2.0',
    'Content-type': 'application/json',
    'Accept': 'text/plain'
}

sign_in = {
    "email": "",
    "password": ""
}


def format_string(value):
    return "{{{}}}".format(','.join('"{}":"{}"'.format(key, val) for (key, val) in sorted(value.items())))


def key():
    random.seed(time.time())
    return random.randrange(0, 1000)


def linuxTimestamp(string):
    salt = "MoKXE8Z84hkHOIXNWw6XIJli2Sl-pqE-rryygRBj"
    sha = hashlib.sha1()
    sha.update("{}".format(string + salt))
    return sha.hexdigest().lower()[2:25]


def load_token():
    if not path.exists('session.txt'):
        data = '{}'.format(format_string(sign_in))
        token = requests.post("http://wifimap.io/users/sign_in?timestamp={}".format(linuxTimestamp(data)),
                              data=data, headers=user_agent)
        with open("session.txt", "w") as line:
            line.write(token.text)
        return json.loads(token.text)

    else:
        with open("session.txt", "r") as line:
            return json.loads(line.read())


if __name__ == "__main__":
    token = load_token()["session_token"]

    with open("city.csv", "r") as f:
        for i in f:
            split = i.split(",")
            print '{} - {}'.format(split[2].translate(None, '"\n\r'), split[1].translate(None, '"\n'))

            x = requests.get("http://wifimap.io//user/purchased_cities/"
                             "{}?srv_id={}&sub_srv_id={}&timestamp={}&session_token={}".format(
                split[0], key(), key(), linuxTimestamp(str(split[0] + token)), token), headers=user_agent)

            with open('data/{} - {}'.format(split[2].translate(None, '"\n\r'),
                                            split[1].translate(None, '"\n')).strip(), 'w') as z:
                z.write(x.text.encode('utf-8'))
