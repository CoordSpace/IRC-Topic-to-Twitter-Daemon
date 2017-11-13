# -*- coding: utf-8 -*-
"""
    This class is dedicated to the extraction of information from specially
    formatted IRC topic strings and the creation of concise messages
    It is inherently single use and relies on a specific set of unwritten
    topic formatting standards that only exist on the #dopefish_lives IRC channel
    Due to this inflexible nature, I do not recommend using this fork of the
    twitter daemon unless you can adopt some conventions:

    In the original usage, this script extracts the first two elements from
    a topic string formatted as shown:
        Streamer: <item one> | Game: <item 2> | Useless information that
        gets removed -> <item one> is playing <item two>! Come watch @ Dopelives.com
     or
        Movienight: Stream info here | Any | number | of | segments ->
        Movienight: Stream info here | Any | number | of | segments
"""
import time
from random import choice


class ExtractInfo():

    def __init__(self, log):
        # The tuple containing a list of information Strings used to generate
        # twitter posts and seconds from the epoc upon creation
        self.prevInfo = ([], 0)
        self.timeout = 10  # seconds before a topic change is considered unique
        # python logger instance used by IRC3
        self.log = log

    # Take a raw topic String and return a tuple with either:
    #  - A List of two Strings for the current streamer and game followed by a time() value
    #  - A List containing one String for the current event (movie, cue, etc) followed by a time() value
    def extract(self, s):

        # Movie night links are special in their lack of constant formatting. Just send the entire topic off.
        # if "Movie" in s:
        #   return ([s.strip()], time.time())

        items = s.split('|')

        # If there's only one element in the topic, trim of whitespace and
        # return
        if len(items) == 1:
            items[0] = items[0].strip()
            return (items[:1], time.time())

        # trim off everything past the : in 'streamer:' and 'Game:' and strip
        # off any whitespace
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

        self.log.info("Time since last topic: " +
                str(currentInfo[1] - self.prevInfo[1]) + " sec")
        # kick out topic changes that happen before the timeout period lapses
        if currentInfo[1] - self.prevInfo[1] < self.timeout:
            self.log.info("Topic change before timeout period.")
            return False

        currentItems, prevItems = currentInfo[0], self.prevInfo[0]

        # If the info arrays differ in length (say, prev was a movie night link
        # and current is a game) ...
        if len(currentItems) != len(prevItems):
            # print ' LENGTHS - ' + str(len(currentItems)) + ', ' +
            # str(len(prevItems))
            self.log.info("New topic format.")
            return True

        # if there are two Strings in the List, check for sameness on both
        if len(currentItems) == 2:

            if currentItems[1] != prevItems[1]:
                self.log.info("Updated game.")
                return True

            if currentItems[0] != prevItems[0]:
                self.log.info("Updated streamer.")
                return True

        # in the case of only one String (movie link)
        else:
            if currentItems[0] != prevItems[0]:
                self.log.info("Updated movie night topic.")
                return True

        # if all else fails, default to sameness. False negatives are preferred
        # in this situation.
        self.log.info("Topic information not unique.")
        return False

    # Take in the raw topic String and generate a corresponding String message to post on twitter
    # Possibilities include:
    #  - (streamer) is currently playing (game)! Watch @ www.dopelives.com
    #  - Stream over. Thanks for watching everyone!
    #  - (raw entry if only one element is in the List, like movie night links)
    #  - None (in the case of a duplicate message)
    def generateMessage(self, topic):

        verb = ["playing",
                "streaming"]

        outro = ["Thanks for watching!",
                 "Stream over!"]

        # extract that informations!
        info = self.extract(topic)
        extracted = info[0]

        # is this new topic information unique?
        if self.uniqueTest(info):

            # if there's just one String in the information array (movie link)
            # Empty topics are disregarded by twitter upon submission so those
            # can pass
            if len(info[0]) == 1:
                self.prevInfo = info

                # if the topic is entirely empty, print a message about it!
                if extracted[0] == '':
                    self.log.info("Empty topic string.")
                    return "The chat topic is empty! Someone messed up..."

                # return the raw string
                self.log.info("Movie night topic.")
                return extracted[0]

            # is it an empty topic?
            if (extracted[0] == '') & (extracted[1] == ''):
                self.log.info("Empty topic. e.g. Streamer | Game |")
                self.prevInfo = info
                return choice(outro)

            # Fantastic! A real new stream!
            else:
                # replace any empty fields with placeholders
                for i in range(2):
                    if extracted[i] == '':
                        extracted[i] = '???'
                self.log.info("New populated topic.")
                self.prevInfo = info
                return extracted[0] + ' is ' + choice(verb) + ' ' + \
                    extracted[1] + ' @ DopeLives.com!'
        else:
            return None

