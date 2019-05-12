#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)

from TaskManager import TaskManager

def pass_through(*args, **kwargs):
    """ pass through function for debug """
    return True

tm = TaskManager(validate_func=pass_through, execute_func=pass_through)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/input_set/upload')
def upload_input_set():
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)