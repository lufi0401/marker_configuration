#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging

from flask import Flask, Request, request, jsonify

from TaskManager import TaskManager
from MakerConfiguration import generate, validate

app = Flask(__name__)

class custom_request(Request):
    def on_json_loading_failed(self, e):
        return {
            "status": False,
            "message": "Failed to decode JSON object: {0}".format(e)
        }
app.request_class = custom_request


# TO BE DELETED
# def pass_through(*args, **kwargs):
#     """ pass through function for debug """
#     logging.debug("PASS THROUGH: Doing Nothing")
#     return {"status": True}


tm = TaskManager(validate_func=validate, execute_func=generate)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/input_set/upload', methods=['POST'])
def upload_input_set():
    content = request.get_json()
    if content is None:
        return jsonify({"status": False, "message": "There is no json."}), 400
    if content.get("status") is False:
        return jsonify(content), 400
    logging.debug("input_set/upload, json: "+json.dumps(content))
    ret = tm.create_task(content)
    return jsonify(ret)

@app.route('/input_set/<int:input_id>/', methods=['GET'])
def get_task(input_id):
    logging.debug("input_set/, id: {}".format(input_id))
    ret = tm.get_task_info(input_id)
    return jsonify(ret)

@app.route('/input_set/<int:input_id>/start', methods=['POST'])
def start_task(input_id):
    logging.debug("input_set/start, id: {}".format(input_id))
    ret = tm.start_task(input_id)
    return jsonify(ret)

@app.route('/input_set/<int:input_id>/stop', methods=['POST'])
def stop_task(input_id):
    logging.debug("input_set/stop, id: {}".format(input_id))
    ret = tm.stop_task(input_id)
    return jsonify(ret)

@app.route('/input_set/list', methods=['GET'])
def list_tasks():
    logging.debug("input_set/list")
    ret = tm.list_tasks()
    return jsonify(ret)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0", port="5000", debug=True)
