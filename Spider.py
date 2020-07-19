#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) 2018 yunling.com, Inc. All Rights Reserved
#
########################################################################
"""
The spider class.

Authors: Gale
Date:    2020/07/17 14:08
"""

import logging
import os
import re
import sys
import time
try:
    import urllib2
except (ModuleNotFoundError, ImportError):
    import urllib.request as urllib2

from urllib.parse import urlparse

import bs4
import retrying

import url_table
import webpage_service as ws
import Task

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


if sys.version_info[0] >= 3:
    unicode = str


class Spider:
    """
    The spider logic

    Attributes:
        maxDepth      - how deep the spider can go
        interval      - how often the spider scratch, in seconds
        timeout       - how patient the spider be for one task, in seconds
        regex         - what kind of urls the spider can scratch
        output        - where to store the webpages
        verbose       - should the verbosity logs should be printed
    """

    def __init__(self,
                 maxDepth,
                 interval,
                 timeout,
                 regex,
                 output,
                 tasks=None,
                 verbose=False):
        """
        Inits Spider with attributes and a list of tasks
        """
        self.maxDepth = maxDepth
        self.interval = interval
        self.timeout = timeout
        self.regex = re.compile(regex)
        self.verbose = verbose

        if not output:
            self.output = os.path.join(os.getcwd(), "output")
        else:
            self.output = output

        # Queue of tasks
        self.tasks = tasks


    def __getitem__(self, item):
        return self.__dict__.get(item, None)


    def __setitem__(self, item, value):
        self.__dict__[item] = value


    def digger(self, html, encoding='utf-8', parent=None):
        """
        digger - proceed to dig the raw webpage

        Args:
            html    - the raw webpage
            paren   - parent task
        """
        soup = bs4.BeautifulSoup(html, 'html.parser')
        titleDiv = soup.select_one("div.titleBox.cls > h3.title")
        titleText = titleDiv.text
        titleTextItems = titleText.replace("\n", "").split("-")
        comicName = titleTextItems[1].strip() if len(titleTextItems) > 1 else ""
        chapterName = titleTextItems[2].strip() if len(titleTextItems) > 2 else ""
        chapterNameItems = chapterName.split(" ")
        chapterNumText = chapterNameItems[0].strip() if len(chapterNameItems) > 0 else ""
        chapterNameText = chapterNameItems[1].strip() if len(chapterNameItems) > 1 else ""
        m = re.match(r".*?(?P<chapter_num>\d+)", chapterNumText)

        chapterNum = int(m.group("chapter_num")) if m else -1
        logging.debug("chapterNum = %d, chapterNumText = %s, typem = %s, self.domain = %s", chapterNum, chapterNumText, type(m), self.domain)
        navDiv = soup.select("div.AdjacentChapters.topNav > ul.cls a")
        if len(navDiv) == 0:
            logging.info("No more pages")
            return
        nextPageUrl = navDiv[-1]["href"]
        nextPageUrl = os.path.join(self.domain, os.path.relpath(nextPageUrl, "/"))
        logging.debug("next page url: %s", nextPageUrl)
        if nextPageUrl and self.offset > 0:
            nextPageTask = Task.Task(nextPageUrl, max(self.offset - 1, 0))
            logging.info("Adding next page task, url = %s, offset = %d", nextPageTask.url, nextPageTask.offset)
            self.tasks.put(nextPageTask)
        imgsDiv = soup.select("div.imgList img")
        imgUrls = []
        index = 1
        for imgDiv in imgsDiv:
            imgUrl = imgDiv['data-src']
            request = urllib2.Request(imgUrl)
            response = urllib2.urlopen(request, timeout=2)
            ws.save(os.path.join(self.output, comicName, chapterNameText, str(chapterNum), str(index) + '.jpg'), response.read())
            index += 1
            imgUrls.append(imgUrl)

        logging.debug("titleDiv: %s" % titleTextItems)
        logging.debug("navDiv: %s" % navDiv)
        logging.debug("nextPage: %s" % nextPageUrl)
        logging.debug("imgsDiv: %s" % imgUrls)


    def guess_encoding(self, resinfo, rescontent):
        """
        guess_encoding - guess the webpage's encoding

        Args:
            resinfo      - response.info()
            rescontent   - response.read()

        Returns:
            encoding
        """
        encoding = None

        # try to get encoding from headers
        if resinfo:
            try:
                encoding = resinfo.getparam('charset')
            except:
                pass

            # try to get encoding from meta tag
            if not encoding and rescontent:
                soup = bs4.BeautifulSoup(rescontent, 'html.parser')
                meta = soup.find_all('meta',
                                     {'http-equiv': lambda v: v and v.lower() == 'content-type'})
                content0 = meta[0].get('content') if len(meta) > 0 else None
                if content0:
                    encoding = content0.split('charset=')[-1]
        return encoding


    @retrying.retry(wait_exponential_multiplier=1000, wait_exponential_max=5000,
                    wrap_exception=True, stop_max_attempt_number=1)
    def getPage(self, task, timeout=1):
        """
        getPage - download the webpage

        Args:
            task    - the Task object
            timeout - the timeout of accessing url, in seconds

        Returns:
            the raw webpage string if access the url successfully within timeout, else None
        """
        if not task:
            return None

        url = task.url

        try:
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(chrome_options=options)
            logging.debug("driver = %s", driver.name)
            driver.get(url)
            #assert "Python" in driver.title
            logging.info("Trying to scroll the page(%s)'s body to the end", url)
            body = driver.find_element_by_tag_name("body")
            SCROLL_PAUSE_TIME = 0.5
            last_height = driver.execute_script("return document.body.scrollHeight")
            logging.debug("last_height = %d", last_height)
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            if body:
                #rescontent = response.read()
                rescontent = driver.page_source
                logging.debug("type_rescontent = %s", type(rescontent))

                #encoding = self.guess_encoding(response.info(), rescontent)
                encoding = 'utf-8'
                if self.verbose:
                    logging.info("I guess webpage(%s)'s encoding is %s" % (url, encoding))
                task.encoding = encoding
                #return rescontent.decode(encoding)
                return rescontent
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                logging.error( \
                "Request {} failed, the reason is: {}, retrying".format(url, e.reason))
            raise e
        
        return None


    def scratch(self, task):
        """
        scratch - scratch the webpage specified by task

        Args:
            task - the Task object

        Returns:
            None
        """
        if not task or task.depth > self.maxDepth or url_table.filter(task.url, self.verbose):
            return

        if self.verbose:
            logging.info("Trying to scratch: %s, depth = %d, parent url: %s" % \
                   (task.url, task.depth, task.parent.url if task.parent else task.parent))

        html = self.getPage(task, self.timeout)

        if not task.encoding:
            task.encoding = 'utf-8'

        if html:
            if self.verbose:
                logging.info("Recieved %d bytes from %s" % (len(html), task.url))

            self.digger(html, task.encoding, task)


    def start(self):
        """
        start - try to process all tasks
        """
        if not self.tasks:
            return

        while True:
            time.sleep(self.interval)
            t = self.tasks.get()
            logging.debug("taks url: %s, task offset: %d", t.url, t.offset)
            self.offset = t.offset
            parsed_uri = urlparse(t.url)
            self.domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            logging.debug("domain: %s", self.domain)
            
            try:
                self.scratch(t)
            except Exception as e:
                logging.error(e)
            finally:
                # one task has been done
                self.tasks.task_done()
