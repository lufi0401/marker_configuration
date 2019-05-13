#/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
import logging

#TODO: FInish the generate
def generate(mount_points, constraints, similarity_function, 
             interrupt_flag, update_func, update_param):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("generate PASS THROUGH: Doing Nothing")

    for i in range(10):
        time.sleep(2)
        print("Time passed:", i)
        update_func(update_type="progress", content="Time {}".format(i), 
                    **update_param)
        if interrupt_flag.value is True:
            update_func(update_type="progress", content="Interrupted",
                        **update_param)
            return {"status": False, "message": "Interrupted"}

    update_func(update_type="progress", content="Completed.",
                **update_param)
    update_func(update_type="result_json", content=json.dumps({"tasks": 123}),
                **update_param)

    return {"status": True}
