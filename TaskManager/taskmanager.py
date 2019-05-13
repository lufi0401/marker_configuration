#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: finish task manager

import os
import json
import logging
import sqlite3
import ctypes
from multiprocessing import Process, Value
from collections import namedtuple

DB_NAME = "data.db"
DEFAULT_DATA_PATH = "./data/data.db"

Task = namedtuple('Task', ['process', 'interrupt_flag'])

class TaskManager(object):
    """
    manage tasks given input validation and execution functions

    """

    def __init__(self, validate_func, execute_func, path=DEFAULT_DATA_PATH):
        self.__validate = validate_func
        self.__execute = execute_func
        self.db_path = path if path.endswith(".db") else \
                        os.path.join(path, DB_NAME)
        self.running_tasks = {}

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS input_sets(
            input_id INTEGER PRIMARY KEY,
            input_json TEXT NOT NULL
        );''')
        c.execute('''CREATE TABLE IF NOT EXISTS results(
            result_id INTEGER PRIMARY KEY,          
            result_json TEXT NOT NULL,
            input_id INTEGER NOT NULL,
                FOREIGN KEY (input_id)  REFERENCES input_sets(input_id)
        );''')
        conn.commit()
        conn.close()


    def create_task(self, input_set):
        ret_validate = self.__validate(input_set)
        if ret_validate.get("status") is not True: # input_set invalid
            return ret_validate
        # TODO insert tasks and commit

        conn = sqlite3.connect(self.db_path)
        try:
            c = conn.execute("INSERT INTO input_sets (input_json) VALUES (?)",
                             (json.dumps(input_set),)
            )
            conn.commit()
            ret_dict = {
                "status": True,
                "input_set_id": c.lastrowid,
            }
            conn.close()
            return ret_dict
        except Exception as e:
            return {
                "status": False,
                "message": repr(e)
            }

    def start_task(self, task_id):
        tid = str(task_id)
        if self.running_tasks.get(tid) is not None:
            if self.running_tasks.get(tid).process.is_alive():
                return {
                    "status": False,
                    "message": "task_id {} is already running.".format(task_id)
                }
        logging.debug("start_task, task_id: {}".format(task_id))
        task_data = self.get_task(task_id)
        interrupt_flag = Value(ctypes.c_bool)
        params_dict = {
            "interrupt_flag": interrupt_flag,
            "save_func": TaskManager.save_result,
            "save_param": {
                "db_path": self.db_path,
                "task_id": task_id,
            }
        }
        params_dict.update(task_data)
        p = Process(target=self.__execute, kwargs=params_dict) 
        p.start()
        t = Task(p, interrupt_flag)
        self.running_tasks[tid] = t
        return {
            "status": True,
            "task_id": tid
        }

    def stop_task(self, task_id): 
        pass

    def list_available_tasks(self, ):
        pass

    def list_running_tasks(self, ):
        pass

    def get_task(self, task_id):
        # TODO: Finish this
        logging.debug("get_task, task_id: {}".format(task_id))
        return {"data": 0}

    @staticmethod
    def save_result(result, db_path, task_id):
        # TODO: FInish this
        logging.debug("save_result, task_id: {};  result: {}".format(
            task_id, result))
        return True
