#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: finish task manager

import os
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
        self._db_path = path if path.endswith(".db") else \
                        os.path.join(path, DB_NAME)
        self._running_task = []

        self._db_conn = sqlite3.connect(self._db_path)
        c = self._db_conn.cursor()
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
        self._db_conn.commit()


    def create_task(self, input_set):
        pass

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
