#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Chris Earley <chris@coord.space>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# generic packages
from twisted.python import log
import sys
from os.path import dirname, join, abspath
import codecs
# app specific packages
from twitterhelper import TwitAPI
from bot import BotFactory
from twisted.internet import reactor
from configuration import SystemConf as c


def main():

    # for those cases where the user supplies more than just the
    # conf location  or none at all
    numargs = len(sys.argv[1:])

    print(sys.argv)

    if numargs < 1:
        confname = "topic2twitter.conf"
    else:
        confname = sys.argv[1]

    c.get_config(confname)

    logfilepath = join(
        dirname(
            abspath(__file__)), c.get(
            'debug', 'loggingfile'))
    log.startLogging(codecs.open(logfilepath, "a", 'utf-8'))

    # create twitter API connection
    TwitAPI.init_twitter(c.get('twitter', 'consumer_key'),
                         c.get('twitter', 'consumer_secret'),
                         c.get('twitter', 'access_token_key'),
                         c.get('twitter', 'access_token_secret'))

    # create factory protocol and application
    f = BotFactory(c.get('irc', 'nickname'),
                   c.get('irc', 'realname'),
                   c.get('irc', 'username'),
                   c.get('irc', 'password'),
                   c.get('irc', 'channels').split(' '))

    # connect factory to this host and port
    reactor.connectTCP(c.get('irc', 'serverURL'),
                       c.getint('irc', 'port'), f)

    # start the bot
    reactor.run()

    return 0

if __name__ == '__main__':
    main()
