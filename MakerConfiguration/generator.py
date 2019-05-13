#/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
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
        if interrupt_flag is True:
            return {"status": False, "message": "Interrupted"}
    return {"status": True}
