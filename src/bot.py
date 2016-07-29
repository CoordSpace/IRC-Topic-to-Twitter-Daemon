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

# generic imports
from twisted.words.protocols import irc
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.policies import TimeoutMixin
from twisted.internet import reactor
from twisted.python import log
from time import gmtime, strftime, sleep, time
import random
# app specific packages
from twitterhelper import TwitAPI
from configuration import SystemConf
from infoextraction import ExtractInfo


def greek_string(s):
    '''
        Replaces the first standard vowel in a string with an accented
        unicode vowel. Useful to prevent annoying pings on IRC.
    '''
    log.msg("Greeking string: " + s)
    before = u'aeiouyAEIOUY'
    after = u'àèìòùÿÄÉÍÒÙÝ'
    # our dict of normal to greeked vowels
    trans = {i: j for i, j in zip(before, after)}
    # convert name to unicode
    s = unicode(s)

    for i, c in enumerate(s):
        if c in before:
            # rebuild the string with our new greeked vowel
            # taking the place of the first vowel found
            greeked = s[:i] + trans[c] + s[i + 1:]
            log.msg("Greeked: " + greeked)
            return greeked
    log.msg("No greeking needed!")
    # return the string untouched if there's nothing to change
    return s


def loop_names():
    names = [
        'arch',
        'Booom3',
        'Dopefish_lives',
        'Fgw_wolf',
        'FlippinKamikaze',
        'Fateweaver',
        'GreenMiscreant',
        'Hitman_Spike',
        'I-H',
        'Lunki',
        'Meryl',
        'Nooya',
        'Qipz',
        'Ramstrong',
        'Ratix',
        'Rumia',
        'Ska',
        'weevil',
        'Yadde',
        'Po_',
        'Sauze']
    i = 0
    while True:
        # every time we finish listing all the names, reshuffle
        if i % len(names) == 0:
            random.shuffle(names)
        # grab our name
        name = names[i % len(names)]
        # greek it so we don't get banned
        greeked = greek_string(name)
        yield greeked
        i += 1


# Bot logic definition class. Only covers action callbacks.
class TopicBot(irc.IRCClient, TimeoutMixin):

    # streamer name generator
    name = loop_names()

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.setTimeout(600)
        log.msg("[connected!]")

    def connectionLost(self, reason):
        log.msg("Disconnected! " + reason.getErrorMessage())
        irc.IRCClient.connectionLost(self, reason)

    def timeoutConnection(self):
        self.transport.abortConnection()
        irc.IRCClient.connectionLost(self, '[Restarting connection..]')

    # callbacks for events #

    def dataReceived(self, data):
        self.resetTimeout()
        # pass on date to the normal event callbacks
        irc.IRCClient.dataReceived(self, data)

    def signedOn(self):
        log.msg('Signed on to server.')
        # reset the counter for topic msgs encounted upon channel joins
        # since this method will get called again upon reconnection
        self.numjointopics = 0
        log.msg('Authing with Q')
        self.msg('Q@CServe.quakenet.org', 'AUTH TwitterBot CcA3NGSxDT')
        self.mode(self.nickname, True, 'x')

    def joined(self, channel):
        log.msg('Joined ' + channel)

    def modeChanged(self, user, channel, set, modes, args):
        log.msg("Mode changed - " + modes)
        if modes == 'x':
            # separate the channels and cut off any whitespace
            for channel in self.factory.channels:
                log.msg('Attempting to join %s.' % (channel))
                self.join(channel)

    def privmsg(self, user, channel, msg):
        if msg == SystemConf.config.get('irc', 'infocmd'):
            log.msg('Recieved !infocmd from %s in %s' % (user, channel))
            self.msg(
                channel,
                'Follow me on twitter for up-to-the-second stream notifications and events at https://twitter.com/%s <3' %
                (str(
                    TwitAPI.get_screen_name())))
            return
        if msg[0:9].lower() == '!readthis':
            words = msg.split()
            if len(words) > 1:
                self.msg(
                    channel,
                    words[1] +
                    ': Please read the channel rules: http://dopelives.com/newfriend.html')
            else:
                self.msg(
                    channel,
                    'Please read the channel rules: http://dopelives.com/newfriend.html')
            return
        if msg.lower() == '!next':
            log.msg('Recieved !next from %s in %s' % (user, channel))
            # if some times has elapsed since last roll...
            if time() - self.tout > 1800:
                log.msg('The timeout has expired! tout = ' + str(self.tout))
                self.msg(channel, self.makeRoulette().encode('utf-8'))
                # update the last time
                self.tout = time()
        if msg.lower() == '!quotes':
            self.msg(
                channel,
                'Shit people say in >this chat - https://twitter.com/Dopefish_Quotes')
        return

    def makeRoulette(self):
        m = [
            'Lets all kindly ask %s to stream!',
            'I think ... %s should stream!',
            'It\'s been a while since %s last streamed.',
            '%s!',
            'I just asked !larry and he said that %s should stream!',
            'If only %s would stream some videogames on the internet.',
            'Maybe if we focus really hard %s will stream!',
            '%s?',
            '%s.',
            'I have fond memories of %s streams.',
            'I\'m holding an entire family of snails hostage till %s streams!',
            'Lets all get comfy and wait for %s to stream.',
            'I bet %s is setting up to stream as I type!',
            'Lets all ask %s who should stream!',
            'How about ... %s? :3c',
            'I hacked into the streamer channel and it looks like %s is getting ready to stream!',
            'What if %s streamed some videogames?',
            'Maybe if %s is around, they could stream?',
            'Don\'t let your %s streams be dreams.',
            'Believe in yourself and maybe one day %s will stream!',
            'Yo %s, where the vidja at?',
            'Lets all focus our positive energy towards %s.',
            'I hear that %s knows who will be streaming next.',
            'Everyone stare at %s till they stream!',
            '%s. Streams. Yes!',
            '%s should stream!',
            'I can never get enough of %s streams!',
            '!nextplayed whatever %s wants to stream!',
            'There\'s no such thing as too much %s livelive!',
            'The world would be a better place if only %s would stream.',
            'I\'ll give 20 dopecoins to %s if they stream.',
            'Let\'s mix it up. How about if %s streams a movie instead?',
            '!p1ayed %s',
            '%s streams are so comfy, I could go for one right now!']
        message = random.choice(m) % next(self.name)
        log.msg("Roulette message: " + message)
        return message

    # Ignore the topic messages generated upon joining channels then
    # pass every topic after that to the twitter helper.
    def topicUpdated(self, user, channel, newTopic):
        if self.numjointopics < len(self.factory.channels):
            self.numjointopics += 1
            return

        log.msg("Raw Topic: " + newTopic)

        # generate the formatted message
        newTopic = self.processor.generateMessage(newTopic)

        # if the message is empty don't post anything
        if newTopic is None:
            log.msg("Topic is not unique. Not posting!")
            return

        message = ''  # init the topic string

        if SystemConf.getboolean('formatting', 'timestamp'):
            # [00:00] GMT timestamp. Used for giving old postimes more
            # definition even after twitter only lists the day of the post
            # also defeats the duplicate tweet filter
            message = strftime("[%H:%M]", gmtime()) + ' '

        if SystemConf.getboolean('formatting', 'prependchannel'):
            message += channel + ': '  # prepend the topic string with the source channel

        message += newTopic  # tack on the topic itself
        # replace any off-encided symbols before the twitter API can choke on
        # them
        message = message.decode('utf-8', 'ignore')
        log.msg('Posting final message: %s' % (message))
        TwitAPI.makepost(message)


# Covers connection logic and instantiation
class BotFactory(ReconnectingClientFactory):

    # set all the relevant instance vars for TopicBot
    # Some are used automagically (like nickname)
    def __init__(self, nickname, realname, username, password, channels):
        self.nickname = nickname
        self.realname = realname
        self.username = username
        self.password = password
        self.channels = channels

    def buildProtocol(self, addr):
        self.resetDelay()
        p = TopicBot()
        p.factory = self
        p.nickname = self.nickname
        p.username = self.username
        p.realname = self.realname
        p.password = self.password
        p.processor = ExtractInfo()
        # !next cooldown timer val
        p.tout = 0
        return p

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)
