#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2018 yunling.com, Inc. All Rights Reserved
#
########################################################################
"""
The task class.

Authors: Gale
Date:    2020/07/17 14:08
"""
try:
    import urlparse
except (ModuleNotFoundError, ImportError):
    import urllib.parse as urlparse


class Task:
    """
    The task of scraching a webpage

    Attributes:
        url    - the url of this task
        depth  - the depth of this url, the depth of seed urls is 0
        base   - the base url of this task's webpage
        parent - the parent webpage of this task
    """

    def __init__(self, url, offset=0, base=None, parent=None):
        """
        Inits Task with url, optional base and parent.

        """
        self.offset = offset
        self.base = base
        self.parent = parent

        parsed = urlparse.urlparse(url)

        if parsed and not parsed.scheme:
            if base and base.get('href'):
                self.url = urlparse.urljoin(base.get('href'), url)
            elif parent:
                self.url = urlparse.urljoin(parent.url, url)
        else:
            self.url = url
        
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

    def __getitem__(self, item):
        return self.__dict__.get(item, None)

    def __setitem__(self, item, value):
        """
        Enable users could add new attributes to the instance of Task
        """
        self.__dict__[item] = value
