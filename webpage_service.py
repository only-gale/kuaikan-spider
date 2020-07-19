#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2018 yunling.com, Inc. All Rights Reserved
#
########################################################################
"""
The webpage service.

Authors: Gale
Date:    2020/07/17 14:08
"""
import os
import bs4
import logging
import retrying


def parse(html, encoding='utf-8'):
    """
    parse - parse raw html by using BeautifulSoup

    Args:
        html - the raw html

    Returns:
        BeautifulSoup
    """
    if isinstance(html, unicode):
        return bs4.BeautifulSoup(html, 'html.parser')

    return bs4.BeautifulSoup(html, 'html.parser', from_encoding=encoding)


def find_all(html, tag, encoding, **kwargs):
    """
    find_all - find all tag from the raw html

    Args:
        html - the raw html
        tag  - the tag to find

    Returns:
        List of tags
    """
    soup = parse(html, encoding)
    return soup.find_all(tag, **kwargs)


@retrying.retry(wait_exponential_multiplier=1000, wait_exponential_max=5000, wrap_exception=True,
                stop_max_attempt_number=3)
def save(dest, content, encoding='utf-8'):
    """
    save - Save content to the file specified by dest.

    Args:
        dest    - the destination path
        content - the content to save

    Returns:
        None
    """
    #with open(dest, "w") as f:
    #    f.write(content.encode(encoding))

    f = None
    try:
        head, tail = os.path.split(dest)
        if not os.path.exists(head):
            os.makedirs(head)
        f = open(dest, "wb")
        logging.info("Saving file: %s", dest)
        f.write(content)
    except Exception as e:
        logging.error("Something nasty happend during wrote to %s, retrying" % dest)
        logging.error(e)
        raise e
    finally:
        if f:
            f.close()
