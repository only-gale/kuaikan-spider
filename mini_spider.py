#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2018 yunling.com, Inc. All Rights Reserved
#
########################################################################
"""
The mini spider.

Authors: Gale
Date:    2020/07/17 14:08
"""

import argparse
import logging
import os
import threading
try:
       import ConfigParser
except (ModuleNotFoundError, ImportError):
       import configparser as ConfigParser
try:
       import queue
except (ModuleNotFoundError, ImportError):
       import Queue as queue

import seedfile_load as sl
import Config
import Spider
import Task


tasks = queue.Queue()
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(threadName)s - %(levelname)s: %(message)s')

def worker(config, verbose=False):
    """
    worker - start the spider

    Args:
        config      - the Config object
        verbose     - should the verbosity logs should be printed

    Returns:
        None
    """
    # All spiders consume the global common queue of tasks
    spider = Spider.Spider(config.max_depth,
                           config.crawl_interval,
                           config.crawl_timeout,
                           config.target_url,
                           config.output_directory,
                           tasks,
                           verbose)
    spider.start()


def init(config_file, verbose=False):
    """
    init - initialize the global common queue of tasks with the list of seed urls

    Args:
        list_of_urls - the list of seed urls

    Returns:
        None
    """
    # Load the spider configuration
    config = Config.Config(config_file, 'spider')

    # Initialize the seed urls
    for (url, offset) in sl.parse_list_of_urls(config.url_list_file):
        tasks.put(Task.Task(url, offset))

    # Start the mini spider
        start(config, verbose)


def start(config, verbose=False):
    """
    start - start to work

    """
    if not config:
        return

    # Create the output directory if it hasn't existed yet.
    if not os.path.exists(config.output_directory):
        os.makedirs(config.output_directory)

    for i in range(config.thread_count):
        t = threading.Thread(target=worker,
                             args=[config, verbose],
                             name="spider_%d" % i)
        t.daemon = True
        t.start()

    # Only exit after all tasks haven been excuted
    tasks.join()
    logging.info("All urls have been scratched, the mini spider exits now.")


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-V",
                        "--verbose",
                        help="print the verbose log",
                        action="store_true",
                        default=False)
    parser.add_argument("-v", "--version", help="print the version", action="store_true")
    parser.add_argument("-c", "--config", help="configuration file", default="spider.conf")
    args = parser.parse_args()
    
    if args.version:
        logging.info("1.0")
    else:
        init(args.config, args.verbose)
