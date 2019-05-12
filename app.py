#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging

from flask import Flask, Request, request, jsonify
app = Flask(__name__)

class custom_request(Request):
    def on_json_loading_failed(self, e):
        return {
            "status": False,
            "message": "Failed to decode JSON object: {0}".format(e)
        }
app.request_class = custom_request

from TaskManager import TaskManager

def pass_through(*args, **kwargs):
    """ pass through function for debug """
    return {"status": True}


tm = TaskManager(validate_func=pass_through, execute_func=pass_through)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload_input_set', methods=['POST'])
def upload_input_set():
    content = request.get_json()
    if content.get("status") is False:
        return jsonify(content), 400
    logging.debug("upload_input_set, json: "+json.dumps(content))
    ret = tm.create_task(content)
    return jsonify(ret)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", port="5000", debug=True)
