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
import ConfigParser
from os.path import dirname, join, abspath

class SystemConf:
   
   # user config values for module level access (e.g. config.port)
   config = None

   # Generate the populated parser and relevent documentation needed to 
   # create the application's conf file.
   @staticmethod
   def build_config():
      config = ConfigParser.RawConfigParser()
      # dict of option:descriptions to make the configwriter more friendly
      description = dict()
         
      config.add_section('twitter')
      description['twitter'] = 'Twitter Settings - Get these from your API key settings at apps.twitter.com'
      config.set('twitter', 'consumer_key')
      config.set('twitter', 'consumer_secret')
      config.set('twitter', 'access_token_key')
      config.set('twitter', 'access_token_secret')
      
      description['irc'] = 'IRC Settings - Chat settings to define watched channels and commands.'
      config.add_section('irc')
      config.set('irc', 'serverURL', 'irc.quakenet.org')
      config.set('irc', 'port', '6667')
      config.set('irc', 'nickname', 'TopicBot')
      description['channels'] = 'A space-separated list of channels '
      config.set('irc', 'channels')
      description['infocmd'] = '!cmd to post the twitter link in chat '
      config.set('irc', 'infocmd', '!twitter')
      config.set('irc', 'password', '')
      config.set('irc', 'realname', 'http://hex.io/irc2twit')
      config.set('irc', 'username', 'bot')
      
      description['formatting'] = 'Formatting Settings - Optional additions to the generated topic message.'
      config.add_section('formatting')
      description['prependchannel'] = 'Prepend the chan name? '
      config.set('formatting', 'prependchannel', 'false')
      description['timestamp'] = 'Prepend a [HH:MM] timestamp? '
      config.set('formatting', 'timestamp', 'true')
      
      description['debug'] = 'Debug Settings - Logging settings to finetune bookkeeping.'
      config.add_section('debug')
      config.set('debug', 'loggingfile', 'irc2twitter.log')
      
      # we're returning the configparse dict since it makes bulk searching
      # so much more easier for the wizard and there's no need for cross-
      # module access
      return config, description
      
   @classmethod
   def get_config (cls, filename):
      config = ConfigParser.ConfigParser()
      filepath = join(dirname(abspath(__file__)), filename)
      fp = open(filepath)
      config.readfp(fp)
      fp.close()
      cls.config = config
      return config
      
   # Creating wrapper methods to expose the dict variable is much cleaner
   # than extending the ConfigParser class and using that since we need something 
   @classmethod
   def get (cls, section, option):
      return cls.config.get(section, option)
      
   @classmethod
   def getint (cls, section, option):
      return cls.config.getint(section, option)

   @classmethod
   def getboolean (cls, section, option):
      return cls.config.getboolean(section, option)

