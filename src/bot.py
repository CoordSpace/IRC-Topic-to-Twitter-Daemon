#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Chris Earley <cw.earley@gmail.com>
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
from time import gmtime, strftime, sleep
import random
# app specific packages
from twitterhelper import TwitAPI
from configuration import SystemConf
from infoextraction import ExtractInfo

# Bot logic definition class. Only covers action callbacks.
class TopicBot(irc.IRCClient, TimeoutMixin):
   
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
      self.msg('Q@CServe.quakenet.org', 'AUTH TwitterBot ***REMOVED***')
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
      if msg == SystemConf.config.get('irc','infocmd'):
         log.msg('Recieved !infocmd from %s in %s' % (user, channel))
         self.msg(channel, 'Follow me on twitter for up-to-the-second stream notifications and events at https://twitter.com/%s <3' % (str(TwitAPI.get_screen_name())))
         return
      if msg[0:9].lower() == '!readthis':
         words = msg.split()
         if len(words) > 1:
            self.msg(channel, words[1] + ': Please read the channel rules: http://dopelives.com/newfriend.html')
         else:
            self.msg(channel, 'Please read the channel rules: http://dopelives.com/newfriend.html')
         return
      if msg.lower() == '!next':
         log.msg('Recieved !roulette from %s in %s' % (user, channel))
         # if some times has elapsed since last roll...
         if time() - self.tout > 2700:
            log.msg('The timeout has expired! tout = ' + str(self.tout))
            self.msg(channel, self.makeRoulette())
            # update the last time
            self.tout = time()
      return

   def makeRoulette(self):
      s = ['arch', 'Dopefish__lives', 'Fgw_wolf' , 'GreenMiscreant', 'LewishM', 'Ramstrong', 'Hitman_Spike', 'I-H', 'Lunki', 'Qeird', 'Qipz', 'Ratix', 'Ska', 'Yadde', 'weevil']
      m = ['Lets all kindly ask %s to stream!', 'How about we tell %s just how much we like their streams?', "I think ... %s should stream!", 'It\'s been a while since %s last streamed.', 'The magic conch shell has spoken! %s shall stream!', '%s!', 'I just asked Larry and he said that %s should stream!', 'If only %s would stream some videogames on the internet...', 'Maybe if we wish really hard %s will stream!', 'Lets all clap our hands together and cheer \"Lets go %s!\"', '%s?', '%s.', 'I have fond memories of %s streams.', 'I\'m holding an entire family of snails hostage till %s streams!', 'The world will end in 24 hours if %s doesn\'t stream!', 'Maybe if someone sold their soul to Satan, %s would stream some games?', 'You have been greeted by the spirit of streams! Glorious livelive will be bestowed upon you only if you post \"I love %s streams!\" right now!', 'Lets all get comfy and wait for %s to stream. I bet he\'s setting up right as I type!', 'Lets all ask %s who should stream!', 'I gazed into the abyss and %s gazed back.' , 'The Pope has ordained that %s stream a holy game on this blessed day!', 'How about ... %s? :3c', 'I hacked into the streamer channel and it looks like %s is getting ready to stream!', 'What if %s streamed some videogames?', 'Maybe if %s is around, he could stream?', 'It\'s [Current Year]! %s should be streaming!', 'Don\'t let your %s streams be dreams.', 'Believe in yourself and maybe one day %s will stream!', 'Lets e-bully %s till he streams for us!', 'Yo %s, where the videogames at?', 'Lets all focus our positive energy towards %s.', 'I hear that %s knows who will be streaming next.', 'Everyone stare at %s till he streams!', '%s. Streams. Yes.']
      random.seed(time())
      return random.choice(m) % random.choice(s)
      
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
      if newTopic == None:
         log.msg("Topic is not unique. Not posting!")
         return
      
      message = '' # init the topic string
      
      if SystemConf.getboolean('formatting', 'timestamp'):
         # [00:00] GMT timestamp. Used for giving old postimes more 
         # definition even after twitter only lists the day of the post
         # also defeats the duplicate tweet filter
         message = strftime("[%H:%M]", gmtime()) + ' '
         
      if SystemConf.getboolean('formatting', 'prependchannel'):
         message += channel + ': ' # prepend the topic string with the source channel
         
      message += newTopic # tack on the topic itself
      # replace any off-encided symbols before the twitter API can choke on them
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
      return p
      
   def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

   def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                         reason)
