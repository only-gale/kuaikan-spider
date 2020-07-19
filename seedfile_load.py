#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2018 yunling.com, Inc. All Rights Reserved
#
########################################################################
"""
Load the seed file as a list.

Authors: Gale
Date:    2020/07/17 14:08
"""

import os


def parse_list_of_urls(url_list_file):
    """
    parse_list_of_urls - parse file as list

    Args:
        url_list_file - the file, one url per line

    Returns:
        list of urls
    """
    tmp = list()
    maxPages = 1 << 16

    if os.path.exists(url_list_file):
        with open(url_list_file, 'r') as file:
            for line in file:
                if line:
                    items = line.strip().split()
                    url = items[0] if len(items) > 0 else ''
                    offset = items[1] if len(items) > 1 else -1
                    try:
                        offset = int(offset)
                        if offset < 0:
                            offset = maxPages
                    except ValueError:
                        offset = maxPages

                    if url:
                        tmp.append((url, offset))
    return tmp
