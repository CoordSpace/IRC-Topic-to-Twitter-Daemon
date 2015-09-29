#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This class is dedicated to the extraction of information from specially 
# formatted IRC topic strings and the creation of concise messages
# It is inherently single use and relies on a specific set of unwritten 
# topic formatting standards that only exist on the #dopefish_lives IRC channel
# Due to this inflexible nature, I do not recommend using this fork of the 
# twitter daemon unless you can adopt some conventions:

# In the original usage, this script extracts the first two elements from 
# a topic string formatted as shown:
#     Streamer: <item one> | Game: <item 2> | Useless information that 
#     gets removed -> <item one> is playing <item two>! Come watch @ Dopelives.com
#  or
#     Movienight: Stream info here | Any | number | of | segments -> 
#     Movienight: Stream info here | Any | number | of | segments 

# If you stick to those conventions and change any specifics to the 
# Dopelives community, this fork will work out just fine for your uses. :)
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

import time
from twisted.python import log

class ExtractInfo():

   def __init__(self):
      # The tuple containing a list of information Strings used to generate twitter posts and seconds from the epoc upon creation
      self.prevInfo = ([], 0)
      self.timeout = 20 # seconds before a topic change is considered unique
   
   # Take a raw topic String and return a tuple with either:
   #  - A List of two Strings for the current streamer and game followed by a time() value
   #  - A List containing one String for the current event (movie, cue, etc) followed by a time() value
   def extract(self, s):
   
      # Movie night links are special in their lack of constant formatting. Just send the entire topic off.
      #if "Movie" in s:
      #   return ([s.strip()], time.time())
   
      items = s.split('|')
      
      # If there's only one element in the topic, trim of whitespace and return
      if len(items) == 1:
         items[0] = items[0].strip()
         return (items[:1], time.time())
      
      # trim off everything past the : in 'streamer:' and 'Game:' and strip off any whitespace
      for i in range(2):
         semicolonindex = items[i].find(':')
         items[i] = items[i][semicolonindex + 1:]
         items[i] = items[i].strip()
         
      return (items[:2], time.time())
   
   # Take in a List of 1+ String(s) and a timestamp (seconds from epoch) and return a Boolean if it is unique based on the previous List in self.prevInfo
   # Unique is defined as:
   #  - Containing different content in the game section
   #  - Occurring after a reasonable timeout (to prevent any double posting during cheeky mod humor)
   def uniqueTest(self, currentInfo):
   
      log.msg("Time since last topic: " + str(currentInfo[1] - self.prevInfo[1]) + " sec")
      # kick out topic changes that happen before the timeout period lapses
      if currentInfo[1] - self.prevInfo[1] < self.timeout:
         log.msg("Topic change before timeout period.")
         return False
         
      currentItems, prevItems = currentInfo[0], self.prevInfo[0]
         
      # If the info arrays differ in length (say, prev was a movie night link and current is a game) ...
      if len(currentItems) != len(prevItems):
         #print ' LENGTHS - ' + str(len(currentItems)) + ', ' + str(len(prevItems))
         log.msg("New topic format.")
         return True
         
      # if there are two Strings in the List, check for sameness on both
      if len(currentItems) == 2:
         
         if currentItems[1] != prevItems[1]:
            log.msg("Updated game.")
            return True
            
         if currentItems[0] != prevItems[0]:
            log.msg("Updated streamer.")
            return True
         
      # in the case of only one String (movie link)
      else:
         if currentItems[0] != prevItems[0]:
            log.msg("Updated movie night topic.")
            return True
            
      # if all else fails, default to sameness. False negatives are preferred in this situation.   
      log.msg("Topic information not unique.")
      return False
         
   
   # Take in the raw topic String and generate a corresponding String message to post on twitter
   # Possibilities include:
   #  - (streamer) is currently playing (game)! Watch @ www.dopelives.com
   #  - Stream over. Thanks for watching everyone!
   #  - (raw entry if only one element is in the List, like movie night links)
   #  - None (in the case of a duplicate message)
   def generateMessage(self, topic):
   
      # extract that informations!
      info = self.extract(topic)
      extracted = info[0]
      
      # is this new topic information unique?
      if self.uniqueTest(info):
      
         # if there's just one String in the information array (movie link)
         # Empty topics are disregarded by twitter upon submission so those can pass
         if len(info[0]) == 1:
            self.prevInfo = info
            
            # if the topic is entirely empty, print a message about it!
            if extracted[0] == '':
               log.msg("Empty topic string.")
               return "No community messages. If only there were streams..."
               
            # return the raw string
            log.msg("Movie night topic.")
            return extracted[0]
   
         # is it an empty topic?
         if (extracted[0] == '') & (extracted[1] == ''):
            log.msg("Empty topic. e.g. Streamer | Game |")
            self.prevInfo = info
            return "Stream over. Thanks for watching everyone!"
                        
         # Fantastic! A real new stream!
         else:
            # replace any empty fields with placeholders
            for i in range(2): 
               if extracted[i] == '':
                  extracted[i] = '???'
            log.msg("New populated topic.")
            self.prevInfo = info
            return extracted[0] + ' is playing ' + extracted[1] + ' @ dopelives.com!'
      
      return None

