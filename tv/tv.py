#!/usr/bin/python

import logging
import subprocess

from lxml import etree

from apps import (
    FILEKEY, PARSE_API, APIS,
    get_host_name, get_id, get_embedded_link, get_filekey
)
from url import url_read
from excepts import HostUnavailable


SERIES_PAGE = 'http://www.free-tv-video-online.me/internet/{srs}'
SEASON_PAGE = 'season_{ssn}.html'

HOST_ORDER = ('videoweed', 'movshare', )

DEBUG = False

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def get_tree(url):
    parser = etree.HTMLParser()
    html = url_read(url)
    return etree.parse(html, parser)


def season_page(series, season):
    url = '{base}/{file}'.format(
        base=SERIES_PAGE.format(srs=series),
        file=SEASON_PAGE.format(ssn=season))
    return get_tree(url)


def is_title_row(row):
    return 'class' in row.attrib and row.attrib['class'] == '3'


class Episode(object):
    def __init__(self, series, season, episode=1):
        self.series = series
        self.season = season
        self.host = None
        self._link = None
        self._id = None
        self._name = None
        self._filekey = None
        self._videourl = None
        self._ep_links = None
        self.episode = episode

    def print_season(self):
        print '{} -- Season {}\n'.format(self.series, self.season)
        for epi in self.ep_links:
            print epi['num'], epi['name']

    @property
    def ep_links(self):
        if not self._ep_links:
            self.get_season_ep_links()
        return self._ep_links

    def get_ep_hoster_link(self):
        for host in HOST_ORDER:
            self.host = host
            epi = self.ep_links[self.episode-1]
            if self.host not in epi['ids']:
                continue
            self._name = epi['name']
            self._id = epi['ids'][self.host]
            self._link = get_embedded_link(self.host, self.identifier)
            break
        else:
            raise HostUnavailable(self.host)

    def process_title_row(self, row):
        ep_name = ' '.join(row.xpath(
            'td[@class="episode"]/b')[0].text.split()[1:])
        self._ep_links.append({'name': ep_name,
                               'num': len(self._ep_links)+1,
                               'ids': {}})

    def process_link_row(self, row):
        for link in row.xpath('child::td/a[1]/attribute::href'):
            host = get_host_name(link)
            identifier = get_id(link)
            self._ep_links[-1]['ids'][host] = identifier

    def process_rows(self, rows):
        self._ep_links = []
        for row in rows:
            if is_title_row(row):
                self.process_title_row(row)
            else:
                self.process_link_row(row)

    def get_season_ep_links(self):
        tree = season_page(self.series, self.season)
        rows = tree.xpath('//table[@cellpadding="4"]/tr')
        self.process_rows(rows)

    @property
    def link(self):
        if not self._link:
            self.get_ep_hoster_link()
        return self._link

    @property
    def identifier(self):
        if not self._id:
            self.get_ep_hoster_link()
        return self._id

    @property
    def name(self):
        if not self._name:
            self.get_ep_hoster_link()
        return self._name

    @property
    def filekey(self):
        if not self._filekey:
            tree = get_tree(self.link)
            self._filekey = get_filekey(tree, FILEKEY[self.host])
        return self._filekey

    @property
    def videourl(self):
        if not self._videourl:
            api_url = APIS[self.host].format(
                key=self.filekey, file=self.identifier)
            api_content = url_read(api_url).read()
            self._videourl = PARSE_API[self.host](api_content)
        return self._videourl

    def play(self):
        logging.info('Now playing {} - {}x{} - {}...'.format(
            self.series,
            self.season,
            self.episode,
            self.name
        ))
        devnull = open('/dev/null', 'w')
        print self.videourl
        subprocess.Popen(['mplayer', self.videourl],
                         stdout=devnull,
                         stderr=devnull,
                         )
