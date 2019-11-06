#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser

import os
import sys
import time


# noinspection PyUnresolvedReferences, PyCompatibility
from urllib.request import urlopen, Request, HTTPError
# noinspection PyUnresolvedReferences, PyCompatibility
from urllib.parse import quote

def decode(s):
    return s


class YumlRequest(object):
    """Represents a single request to the yUML web service."""

    def __init__(self):
        self.fmt = 'png'
        self.out = 'image' + self.fmt
        self.style = "scruffy"
        self.scale = ''
        self.dir = ''
        self.type = "class"
        self.body = "[test]"

    API_BASE = "http://yuml.me/diagram"

    def log(self, msg):
        """
        Optionally log an informative message.
        @param msg: The message to log.
        """
        if self.opts.v:
            print("[yuml] %s" % msg)

    def loadbody(self):
        """Load the yUML text from stdin or a file."""
        infile = self.opts.infile
        self.log('Reading from %s' % ('stdin' if infile == '-' else infile))

        if infile == '-':
            source = decode(sys.stdin.read())
        elif os.path.exists(infile):
            source = decode(open(infile, 'r').read())
        else:
            raise IOError("File %s not found" % infile)

        self.body = [x.strip() for x in source.splitlines() if x.strip()]
        self.log('Done reading.')

    def prepout(self):
        """Open the output file."""
        if self.opts.outfile:
            self.out = open(self.opts.outfile, 'wb')
        else:
            print("Usage: yuml [-i FILE] -o FILE")
            sys.exit(1)

    def run(self):
        """Execute the request."""
        start = time.time()


        opts = self.style

        if self.scale:
            opts += ";scale:" + str(self.scale)

        if self.dir:
            opts += ";dir:" + str(self.dir)

        dsl_text = self.body
        url = "%s/%s/%s/%s.%s" % (self.API_BASE, opts, self.type, quote(dsl_text), self.opts.fmt)

        self.log('Requesting %s' % url)

        try:
            req = Request(url, headers={'User-Agent': 'wandernauta/yuml v0.2'})
            response = urlopen(req).read()

            self.out.write(response)
            self.log('Done after %f seconds' % (time.time() - start))
        except HTTPError as exception:
            if exception.code == 500:
                self.log("Service returned 500: probably malformed input.")
                sys.exit(1)
            else:
                raise


def main():
    """Entry point for the command-line tool."""

    parser = OptionParser(usage="%prog [-i FILE] -o FILE", version="%prog 0.1")

    parser.add_option("-i", "--in", dest="infile", metavar="FILE", default="-",
                      help="read yuml from FILE instead of stdin")
    parser.add_option("-o", "--out", dest="outfile", metavar="FILE",
                      help="store output in FILE")

    parser.add_option("-f", "--format", dest="fmt", metavar="FMT",
                      choices=['png', 'pdf', 'jpg', 'svg'],
                      help="use format FMT")
    parser.add_option("-t", "--type", dest="type", metavar="TYPE",
                      choices=['class', 'activity', 'usecase'],
                      help="draw a TYPE diagram")
    parser.add_option("-s", "--style", dest="style", metavar="STY",
                      choices=['scruffy', 'nofunky', 'plain'],
                      help="use style STY")

    parser.add_option("--scale", dest="scale", metavar="PERCENT", type="int",
                      help="scale output to percentage")
    parser.add_option("--dir", dest="dir", choices=['LR', 'RL', 'TD'],
                      help="direction of the diagram LR RL TD")

    parser.add_option("-v", "--verbose", dest="v", action="store_true",
                      help="print some debug info")

    parser.set_defaults(v=False, fmt="png", type="class", style="scruffy")

    (options, _) = parser.parse_args()

    request = YumlRequest()
    request.opts = options
    request.run()

if __name__ == "__main__":
    main()