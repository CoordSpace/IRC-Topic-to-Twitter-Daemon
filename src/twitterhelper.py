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

import twitter
from twisted.python import log


class TwitAPI:

    # The twitter lib object containing information regarding the
    # current twitter user
    user = None
    # The twitter lib object containing the current session data
    # needed to make REST API calls to the twitter service
    api = None

    @classmethod
    def init_twitter(
            cls,
            consumer_key,
            consumer_secret,
            access_token_key,
            access_token_secret):

        # create the API object using the supplied credentials
        cls.api = twitter.Api(
            consumer_key,
            consumer_secret,
            access_token_key,
            access_token_secret)

        # Verify that we have access to the account,
        # throw error if invalid credentials are given.
        # also use this time-heavy API call to nab the user obj for later use.
        try:
            cls.user = cls.api.VerifyCredentials()
        except twitter.TwitterError as e:
            print "ERROR: Please verify OAuth info and specify in the format shown - consumer_key:consumer_secret:access_token_key:access_token_secret"
            log.err(e)
            raise SystemExit(1)

    # Post 140 characters of the given text to twitter.
    @classmethod
    def makepost(cls, msg):

        for tweet in tweets:
            # push the message to twitter, checking for any errors from the service
            # now we don't have to worry about length as postupdates will
            # magically split the message into multiple tweets for us
            try:
                cls.api.PostUpdates(tweet)
            except twitter.TwitterError as e:
                # Just swallow the exception and move on
                # otherwise twitter's strict spam/duplicate restrictions
                # will constantly crash the daemon.
                # There's nothing serious that can happen other than a lost post.
                log.err(e)
                pass

    # Get the screen name of the auth'ed twitter account from the
    # User object and return the string.
    @classmethod
    def get_screen_name(cls):
        return cls.user.screen_name
