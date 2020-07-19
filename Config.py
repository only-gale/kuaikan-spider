#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2018 yunling.com, Inc. All Rights Reserved
#
########################################################################
"""
The spider configuration class.

Authors: Gale
Date:    2020/07/17 14:08
"""

import logging
import ConfigParser


required = ['url_list_file',
            'output_directory',
            'max_depth',
            'crawl_interval',
            'crawl_timeout',
            'target_url',
            'thread_count']

class Config:
    """Configuration object
    
    Attributes:
        section - the section name
    """

    def __init__(self, path, section):
        """
        Inits Config with file path and section name
        """
        self.section = section
        self.parse(path)

    def __getitem__(self, item):
        return self.__dict__.get(item, None)

    def __setitem__(self, item, value):
        """
        Enable users could add new attributes to the instance of Config
        """
        self.__dict__[item] = value

    def parse(self, path):
        """
        parse - try to parse the configuration file specified path

        Args:
            path - the configuration file path

        Returns:
            None
        """
        logging.info("Reading the config file: {}".format(path))
        parser = ConfigParser.RawConfigParser()
        try:
            parser.read(path)
            logging.info("Loaded configurations:")
            for (name, value) in parser.items(self.section):
                logging.info("\t{}: {}".format(name, value))

            self.get_with_default(parser, 'url_list_file', None, './urls')
            self.get_with_default(parser, 'output_directory', None, './ourput')
            self.get_with_default(parser, 'max_depth', 'int', 1)
            self.get_with_default(parser, 'crawl_interval', 'int', 1)
            self.get_with_default(parser, 'crawl_timeout', 'int', 5)
            self.get_with_default(parser, 'target_url', None, '.*.(htm|html)$')
            self.get_with_default(parser, 'thread_count', 'int', 1)
        except Exception as e:
            logging.error(e)


    def get_with_default(self, parser, option, category, default):
        """
        get_with_default - try to get option's value, default value would be used if any exception
                           rised

        Args:
            parser    - the ConfigParser object
            option    - the option name
            category  - 'int', 'float' or 'bool'
            default   - option's default value

        Returns:
            None
        """
        try:
            if 'int' == category:
                self[option] = parser.getint(self.section, option)
            elif 'float' == category:
                self[option] = parser.getfloat(self.section, option)
            elif 'bool' == category:
                self[option] = parser.getbool(self.section, option)
            else:
                self[option] = parser.get(self.section, option)
        except Exception as e:
            logging.error("Something nasty happend, defaults %s to %s" % (option, default))
            self[option] = default
