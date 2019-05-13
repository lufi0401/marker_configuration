#/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import logging

#TODO: FInish the generate
def generate(*args, **kwargs):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("generate PASS THROUGH: Doing Nothing")

    for i in range(10):
        time.sleep(3)
        print("Time passed:", i)
    return {"status": True}
