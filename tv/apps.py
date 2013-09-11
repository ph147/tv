#!/usr/bin/python


import re

from excepts import UnknownHost


def movshare_parse_api(string):
    return re.sub(r'(^url=|&title=.*$)', '', string)


def get_host_name(link):
    return re.sub(r'(^.*/player/|\.php.*$)', '', link)


def get_id(link):
    return re.sub(r'^.*\.php\?id=', '', link)


def get_embedded_link(host, identifier):
    try:
        return EMBED_LINKS[host].format(id=identifier)
    except KeyError:
        raise UnknownHost(host)


def get_filekey(tree, num):
    script = tree.xpath('//script')[num].text.split('\n')
    for line in script:
        if 'flashvars.filekey' in line:
            return re.sub(r'(^[^"]+"|";.*$)', '', line)


FILEKEY = {
    'movshare': 5,
    'videoweed': 7,
}

PARSE_API = {
    'movshare': movshare_parse_api,
    'videoweed': movshare_parse_api,
}

APIS = {
    'movshare': 'http://www.movshare.net/api/player.api.php?key={key}&file={file}',
    'videoweed': 'http://www.videoweed.es/api/player.api.php?key={key}&file={file}',
}

EMBED_LINKS = {
    'movshare': 'http://www.movshare.net/embed/{id}/?width=655&height=362',
    'videoweed': 'http://embed.videoweed.es/embed.php?v={id}&width=600&height=480',
}
