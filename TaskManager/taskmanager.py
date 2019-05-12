#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: finish task manager

import os
import json
import sqlite3

DB_NAME = "data.db"
DEFAULT_DATA_PATH = "./data/data.db"


class TaskManager(object):
    """
    manage tasks given input validation and execution functions
    
    """

    def __init__(self, validate_func, execute_func, path=DEFAULT_DATA_PATH):
        self.__validate = validate_func
        self.__execute = TaskManager.execute_wrap(execute_func)
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
        c = conn.cursor()
        try:
            c.execute("INSERT INTO input_sets (input_json) VALUES (?)", 
                      (json.dumps(input_set),)
            )
            conn.commit()
            ret_dict = { 
                "status": True,
                "input_set_id": c.lastrowid,
            }
            return ret_dict
        except Exception as e:
            return {
                "status": False,
                "message": repr(e)
            }


    def start_task(self, task_name):
        pass

    def list_tasks(self, ):
        pass

    def list_running_tasks(self, ):
        pass
    
    @staticmethod
    def execute_wrap(execute_func):
        def func(input_id, *args, **kwargs):
            # TODO: get something from input id
            ret = execute_func(*args, **kwargs)
            # TODO: save something to output
            return ret
        return func
