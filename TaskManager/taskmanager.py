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
            progress TEXT,
            result_json TEXT,
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

        query = "INSERT INTO input_sets (input_json) VALUES (?)"
        conn = sqlite3.connect(self.db_path)
        try:
            c = conn.execute(query, (json.dumps(input_set),))
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

    def start_task(self, input_id):
        # input_id and task_id is same for now, but maybe changed to 
        # have multiple running tasks
        task_id = input_id
        if self.running_tasks.get(task_id) is not None:
            if self.running_tasks.get(task_id).process.is_alive():
                return {
                    "status": False,
                    "message": "input_id {} is already running.".format(input_id)
                }
        logging.debug("start_task, input_id: {}".format(input_id))

        task_data, task_id = self.get_task_and_allocate_tid(input_id)
        if task_data.get("status") is False:
            return task_data

        interrupt_flag = Value(ctypes.c_bool)
        params_dict = {
            "interrupt_flag": interrupt_flag,
            "update_func": TaskManager.update_task,
            "update_param": {
                "db_path": self.db_path,
                "task_id": task_id,
            }
        }
        params_dict.update(task_data)
        p = Process(target=self.__execute, kwargs=params_dict) 
        p.start()
        t = Task(p, interrupt_flag)
        self.running_tasks[task_id] = t
        return {
            "status": True,
            "task_id": task_id
        }

    def stop_task(self, task_id): 
        if self.running_tasks.get(task_id) is not None:
            t = self.running_tasks.get(task_id)
            if t.process.is_alive():
                t.interrupt_flag = True
                return {
                    "status": True,
                    "message": "interrupting task_id {}.".format(task_id)
                }
        return {
            "status": True,
            "message": "task_id {} not running".format(task_id)
        }

    def list_available_tasks(self, ):
        pass

    def list_running_tasks(self, ):
        pass

    def get_task_and_allocate_tid(self, input_id):
        logging.debug("get_task, input_id: {}".format(input_id))

        try:
            # Retrieve Data
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            query = """SELECT input_json FROM input_sets WHERE input_id = ?"""
            c.execute(query, (input_id,))
            row = c.fetchone()
            if row is None:
                raise IndexError("input_id {} not found".format(input_id))
            input_set = json.loads(row[0])
        
            query = """REPLACE INTO results
                       (input_id, result_id, progress, result_json)
                       VALUES (?, ?, "Initializing...", "")"""
            c.execute(query, (input_id, input_id))
            conn.commit()
            ret_id = input_id
        except Exception as e:
            logging.debug("Error get_task: {}".format(e))
            conn.close()
            return {
                "status": False,
                "message": repr(e)
            }, -1

        conn.close()
        return input_set, ret_id

    @staticmethod
    def update_task(update_type, content, db_path, task_id):
        """ update the task with update type and content"""
        if update_type not in ["progress", "result_json"]:
            return False
        
        logging.debug("update_task, task_id: {}; type: {}; data: {}".format(
            task_id, update_type, content))
        try:
            # Update Data Data
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            query = """UPDATE results
                       SET {} = ?
                       WHERE result_id = ?""".format(update_type)
            c.execute(query, (content, task_id))
            conn.commit()
            conn.close()
        except Exception as e:
            logging.debug("Error get_task: {}".format(e))
            conn.close()
            return False
        return True
