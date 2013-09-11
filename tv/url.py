#!/usr/bin/python

import urllib2
import logging


#logging.basicConfig(level=logging.DEBUG)


CHROME_HEADER = {
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/28.0.1500.71 Chrome/28.0.1500.71 Safari/537.36',
    #'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4',
}


def url_read(url):
    logging.debug('Loading url "{}"...'.format(url))
    headers = CHROME_HEADER
    req = urllib2.Request(url, None, headers)
    return urllib2.urlopen(req)
