#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2018 yunling.com, Inc. All Rights Reserved
#
########################################################################
"""
The url filter.

Authors: Gale
Date:    2020/07/17 14:08
"""

import logging
import threading


deduplicated = []

lock = threading.Lock()


def filter(url, verbose=False):
    """
    filter - check if the url need to be filtered

    Args:
        url - the url would be checked

    Returns:
        True if the url need to be filtered, or False
    """
    with lock:
        if verbose:
            logging.info( \
            "{} acquired the lock {}".format(threading.currentThread().getName(), lock))
        if not url in deduplicated:
            deduplicated.append(url)
            return False

        if verbose:
            logging.info("%s has been scratched, skip" % url)
        return True


