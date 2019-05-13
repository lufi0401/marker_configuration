#/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
import logging

import operator as op
import functools
import itertools
import numpy as np

#TODO: FInish the generate
def generate(sockets, constraints, similarity_function, 
             interrupt_flag, update_func, update_param):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("generate")

    coords, vecs = [], []
    for pt in sockets:
        coords.append([pt[k] for k in ("x", "y", "z")])
        vecs.append([pt[k] for k in ("vx", "vy", "vz")])
    coords = np.array(coords)
    vecs = np.array(vecs)
    n_sockets = coords.shape[0]

    markers = np.array(list(set(constraints["n_markers"])), dtype=np.int)
    stick_lengths = np.array(list(set(constraints["stick_lengths"])))
    n_stick_len = stick_lengths.shape[0]

    n_combin = 0  # Total number of possible configurations
    for r_mark in markers:
        r = min(r_mark, n_sockets-r_mark)
        numer = functools.reduce(op.mul, range(n_sockets, n_sockets-r, -1), 1)
        denom = functools.reduce(op.mul, range(1, r+1), 1)
        nCr = numer // denom
        
        sticks = np.power(n_stick_len, r_mark)
        n_combin += sticks*nCr

    logging.info("Total possible combinations: {}".format(n_combin))


    unique_configs = []    
    for r_mark in markers:
        for socket_idx in itertools.combinations(range(n_sockets), int(r_mark)):
            for stick_idxs in itertools.product(range(n_stick_len), repeat=r_mark):
                # Stop at any point
                if interrupt_flag.value is True:
                    update_func(update_type="progress", content="Interrupted",
                                **update_param)
                    return {"status": False, "message": "Interrupted"}
                
                print(np.array(socket_idx), np.array(stick_idxs))

                i_coords = np.take(coords, socket_idx, axis=0) 
                i_vecs = np.take(vecs, socket_idx, axis=0)
                i_sticks = np.take(stick_lengths, stick_idxs, axis=0).reshape(-1, 1)

                marker_coords = i_coords + i_vecs * i_sticks
                import ipdb; ipdb.set_trace()
                
    # TODO: Finish this part
    # import ipdb; ipdb.set_trace()




    # for i in range(10):
    #     time.sleep(2)
    #     print("Time passed:", i)
    #     update_func(update_type="progress", content="Time {}".format(i), 
    #                 **update_param)
    #     if interrupt_flag.value is True:
    #         update_func(update_type="progress", content="Interrupted",
    #                     **update_param)
    #         return {"status": False, "message": "Interrupted"}

    update_func(update_type="progress", content="Completed.",
                **update_param)
    update_func(update_type="result_json", content=json.dumps({"tasks": 123}),
                **update_param)

    return {"status": True}


if __name__ == "__main__":
    from multiprocessing import Value
    d = json.loads("""
        {
        "sockets": [
            {"x": 0.0, "y": 0.0, "z": 0.0,  "vx": 1.0, "vy": 0.0, "vz": 0.0},
            {"x": 0.0, "y": 0.0, "z": 0.0,  "vx": -1.0, "vy": 0.0, "vz": 0.0},
            {"x": 0.0, "y": 0.0, "z": 0.0,  "vx": 0.0, "vy": 0.0, "vz": 1.0},
            {"x": 0.0, "y": 1.0, "z": 0.0,  "vx": 1.0, "vy": 0.0, "vz": 0.0},
            {"x": 0.0, "y": 1.0, "z": 0.0,  "vx": -1.0, "vy": 0.0, "vz": 0.0},
            {"x": 0.0, "y": 1.0, "z": 0.0,  "vx": 0.0, "vy": 0.0, "vz": 1.0}

        ],
        "constraints": {
            "n_markers": [4, 5, 5],
            "stick_lengths": [ 3.0, 4.0 ]
        },
        "similarity_function": {
            "name": "l2_point_norm",
            "threshold": 2.0
        } 
    }""")
    def do_nothing(content=None, *args, **kwargs):
        print(content)
    generate(interrupt_flag=Value('b', False), update_func=do_nothing, update_param={}, **d)
    import ipdb; ipdb.set_trace()
