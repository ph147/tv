#!/usr/bin/python

import sys

from tv import Episode


def print_usage():
    print 'usage: {} <series> <season> [<episode>]'.format(sys.argv[0])


def main():
    episode = 1
    if len(sys.argv) in (3, 4):
        series = sys.argv[1]
        season = int(sys.argv[2])
        if len(sys.argv) == 4:
            episode = int(sys.argv[3])
        epi = Episode(series, season, episode)
        if len(sys.argv) == 4:
            epi.play()
        else:
            epi.print_season()
    else:
        print_usage()


if __name__ == '__main__':
    main()
