#!/usr/bin/env python3
# -*- coding: utf-8

import logging

import numpy as np

def validate(input_set):
    # TODO: Finish validte config input set
    SKTS = "sockets"
    CONS = "constraints"
    SIMF = "similarity_function"

    logging.debug("validate")

    ret = validate_keys(input_set, [SKTS, CONS, SIMF])
    if ret.get("status") is False:
        return ret

    func_key_list = [
        (validate_sockets, SKTS),
        (validate_constraints, CONS)
    ]

    for f, k in func_key_list:
        ret = f(input_set.get(k))
        if ret.get("status") is False:
            ret["message"] = "In {}: ".format(key) + ret["message"]
            return ret

    return { "status": True }


def validate_keys(d, keys):
    missing_keys = set(keys)
    for k in d:
        try:
            missing_keys.remove(k)
        except KeyError as e:
            return {
                "status": False,
                "message": "Invalid Key: {}".format(k)
            }

    if len(missing_keys) > 0:
        return {
            "status": False,
            "message": "Missing Key(s): {}".format(missing_keys)
        }

    return { "status": True }


def validate_sockets(sockets):
    keys = ["x", "y", "z", "vx", "vy", "vz"]
    for i, pt in enumerate(sockets):
        ret = validate_keys(pt, keys)
        if ret.get("status") is False:
            ret["message"] = "at point {}: ".format(i) + ret["message"]
            return ret
        for k in keys:
            if not isinstance(pt[k], float) and not isinstance(pt[k], int):
                return {
                    "status": False,
                    "message": "at point {}: {} is not float({})".format(
                        i, k, type(pt[k]))
                }
            if not np.allclose(1., np.linalg.norm([pt["vx"], pt["vy"], pt["vz"]])):
                return {
                    "status": False,
                    "message": "at point {}: {} is not unit vector.".format(
                        i, pt)
                }

    return { "status": True}


def validate_constraints(constraints):
    keys = ["n_markers", "stick_lengths"]
    ret = validate_keys(constraints, keys)
    if ret.get("status") is False:
        ret["message"] = "at constraints: " + ret["message"]
        return ret

    for i, v in enumerate(constraints["n_markers"]):
        if not isinstance(v, int):
            return {
                "status": False,
                "message": "at {}th value: {} is not int({})".format(
                    i, k, type(v))
            }

    for i, v in enumerate(constraints["stick_lengths"]):
        if not isinstance(v, float):
            return {
                "status": False,
                "message": "at {}th value: {} is not float({})".format(
                    i, k, type(v))
            }

    return { "status": True}