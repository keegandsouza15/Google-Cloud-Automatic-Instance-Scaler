#!/bin/sh

sudo apt-get update
sudo apt-get install -y python-pip
sudo pip install flask

sudo touch /opt/restserver.py 
sudo chmod 777 /opt/restserver.py

echo '
"""
Simple REST API that calculates fibonacci numbers and keeps a counter
of the number of requests received
"""

import json
from flask import Flask, Response, request

app = Flask(__name__)

call_count = 0
fibonacci_numbers = [0, 1]


@app.route("/status")
def status():
    return "'"{{'"'cache_length'"': {},'"'requests'"': {}}}"'".format(
        len(fibonacci_numbers),
        call_count)


@app.route("/fibonacci", methods=["POST", "GET"])
def fibonacci():
    global call_count
    call_count += 1
    number = int(json.dumps(request.get_json()["fibonacci_number"]))
    resp_content = "'"{{'"'fibonacci_number'"': {}, '"'value'"': {}}}"'".format(
        number,
        calc_fibonacci(number))
    return Response(response=resp_content,
                    status=200,
                    mimetype="application/json")


def calc_fibonacci(number):
    """
    Calculates a fibonnaci numbers recursively
    Does not handle calculations that exceed the
    maximum recursion depth
    """
    if number < 0:
        raise ValueError
    if number < len(fibonacci_numbers):
        result = fibonacci_numbers[number]
    else:
        result = calc_fibonacci(number - 2) + calc_fibonacci(number - 1)
        fibonacci_numbers.append(result)
    return result'> /opt/restserver.py

nohup sudo FLASK_APP=/opt/restserver.py flask run --host=0.0.0.0 --port=80 &

