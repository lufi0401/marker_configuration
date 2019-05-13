#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Set of Simiarity functions that return True if similar and False otherwise
"""
import functools
import logging
import numpy as np


class l2_point_norm(object):
    """
    this function:
    1. return False if number of points are different across configurations
    2. map points so that overall distance is minimum
    3. return True if their avarege distance is below avg_threshold
    4. return True if the pair with max distance is below max_threshold
    """
    def __init__(self, avg_threshold, max_threshold, name=None):
        self.avg_threshold = avg_threshold
        self.max_threshold = max_threshold
    
    def __call__(self, lhs, rhs):
        if (lhs.shape[0] != rhs.shape[0]):
            return False
        dist_mat = np.linalg.norm(lhs.reshape(-1,1,3)-rhs.reshape(1,-1,3), 
                                  axis=-1)
        argsorted = np.unravel_index(np.argsort(dist_mat.ravel()), dist_mat.shape)
        argsorted_pairs = np.stack(argsorted, axis=1)

        lhs_taken = np.zeros((lhs.shape[0],), dtype=np.bool)
        rhs_taken = np.zeros((rhs.shape[0],), dtype=np.bool)

        pairs = []
        distances = []
        for p in argsorted_pairs:
            pl, pr = p
            if (not lhs_taken[pl]) and (not rhs_taken[pr]):
                pairs.append(p)
                distances.append(dist_mat[pl, pr])
                lhs_taken[pl] = True
                rhs_taken[pr] = True
                if np.all(lhs_taken*rhs_taken):
                    break
        pairs = np.array(pairs)
        distances = np.array(distances)

        dist_mean = np.mean(distances)
        dist_max = np.max(distances)
        # logging.debug("lhs:\n{}".format(lhs))
        # logging.debug("rhs:\n{}".format(rhs))
        logging.debug("distances(mean, max, all): {}, {}, {}".format(
            dist_mean, dist_max, distances))

        if dist_mean <= self.avg_threshold:
            return True
        elif dist_max <= self.max_threshold:
            return True
        else:
            return False

        
SimilarityFunctions = {
    "l2_point_norm": l2_point_norm
}


def create_similarity_function(param):
    name = param.get("name")
    ret_cls = SimilarityFunctions.get(name)
    return ret_cls(**param)
