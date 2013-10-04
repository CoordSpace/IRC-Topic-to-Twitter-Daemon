#!/usr/bin/python

# topic2twitter.py
# A lightweight python daemon used push formatted IRC topic changes from 1+ channels to a central twitter account.

# The MIT License (MIT)
#
# Copyright (c) 2013 Chris Earley <bearddough+topic2twitter@gmail.com>
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

import argparse
import twitter
import irc.bot
import irc.client
import sys
import time
from time import gmtime, strftime

# The global twitter API object to push posts to
TwitAccount = None

class twitterAPI:
	def __init__ (self, OAuthString):
		# Split formatted OAuth string into a list
		OAuthlist = OAuthString.split(':')
		
		# Do a quick formatting sanity check on the number of OAuth bits given.
		if len(OAuthlist) != 4:
			print "ERROR: Please verify OAuth info and specify in the format shown - consumer_key:consumer_secret:access_token_key:access_token_secret"
			raise SystemExit(1)
		
		# create the API object using the supplied credentials
		self.api = twitter.Api(OAuthlist[0], OAuthlist[1], OAuthlist[2], OAuthlist[3])
		
		# Verify that we have access to the account, throw error if invalid credentials are given.
		# also use this time-heavy API call to nab the screen name for later use.
		try:
			self.User = self.api.VerifyCredentials()
		except twitter.TwitterError:
			print "ERROR: Please verify OAuth info and specify in the format shown - consumer_key:consumer_secret:access_token_key:access_token_secret"
			raise SystemExit(1)
	
	# Post 140 characters of the given text to twitter. 
	def makepost (self, msg):
		# truncate message to 125 characters. This limit is a quick fix until I can make a workaround for twitter-text BS.
		msg = msg[:125]
		#push the message to twitter, checking for any errors from the service
		try:
			self.api.PostUpdate(msg)
		except twitter.TwitterError:
		# Just swallow the exception and move on
		# otherwise twitter's strict spam/duplicate restrictions will constantly crash the daemon.
		# There's nothing serious that can happen other than a lost post. 
			pass
	
	# Get the screen name of the auth'ed twitter account from the User object and return the string.
	def get_screen_name(self):
		return self.User.GetScreenName()

class TopicBot(irc.bot.SingleServerIRCBot):
	def __init__(self, args):
	
		# Begin the mass setting of self varibles
		self.serverURL = args.serverURL
		self.port = args.port
		self.nickname = args.nickname
		self.join = args.join
		self.prependchan = args.prependchan
		self.username = args.username
		self.realname = args.realname
		self.password = args.password
		self.infocmd = args.infocmd
		self.timestamp = args.timestamp
		
		# check for no realname specified
		if self.realname == None:
			self.realname = self.nickname
		
		# set the input buffer to a non-decoding line buffer to prevent UTF-8 crashes
		irc.client.ServerConnection.buffer_class = irc.buffer.LineBuffer
	
		# create IRC bot objects
		irc.bot.SingleServerIRCBot.__init__(self, [(self.serverURL, self.port, self.password)], self.nickname, self.realname, username=self.username)

	# Take the new topic message and send it to twitter.    
	def on_topic (self, connection, event):
		global TwitAccount
		
		topic = '' # init the topic string
		
		if self.timestamp:
			# [00:00] GMT timestamp. Used for giving old postimes more definition even after twitter only lists the day of the post.
			topic = strftime("[%H:%M]", gmtime()) + ' ' 
		
		if self.prependchan:
			topic += event.target + ': ' # start the topic string with the source channel
			
		topic += event.arguments[0] # tack on the topic itself
		# post to twitter!
		TwitAccount.makepost(topic)
		return
	
	# Read lines from channels and if they contain a !command
	def on_pubmsg (self, connection, event):
		global TwitAccount
		
		msg = event.arguments[0]
		if msg == self.infocmd:
			connection.privmsg(event.target, 'https://twitter.com/' + TwitAccount.get_screen_name())
		return
		
	# Join all given channels when welcome message is delivered
	def on_welcome (self, connection, event):
		for channel in self.join:
			connection.join(channel)

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

# Setup the CLI arguments and create the parser object
def get_args ():
	parser = argparse.ArgumentParser(description="IRC daemon that posts channel topics to twitter")
	parser.add_argument('serverURL', help='the IRC server to connect to')
	parser.add_argument('nickname', default='topicBot', help='the nickname of the bot upon connection')
	parser.add_argument('OAuth', help='the twitter app OAuth info in this format: consumer_key:consumer_secret:access_token_key:access_token_secret')
	parser.add_argument('join', nargs='+', help='channel(s) to join and monitor, separated by spaces. remember to escape hashes in *nix systems. e.g. \#chan')
	parser.add_argument('--prependchan', action='store_true', help='prepend the channel name to topics posted to twitter. Useful when watching multiple channels')
	parser.add_argument('-p', '--port', default=6667, type=int)
	# None is default since the username, password, and realname fields are all optional in client.server.connect()
	parser.add_argument('--username', default = None, help='bot username') 
	parser.add_argument('--realname', default = None, help='bot realname')
	parser.add_argument('--password', default = None, help='IRC server password (if needed)')
	parser.add_argument('--infocmd', default = '', help="the text command that any user in watched channels can type to recieve the twitter account link")
	parser.add_argument('--timestamp', action='store_true', help='Prepend a formatted [HH:MM] timestamp before the topic message.')
	return parser.parse_args()
		
def main ():
	global TwitAccount

	# parse all the CLI arguments
	arguments = get_args()
	
	# init and verify the twitter connection
	TwitAccount = twitterAPI(arguments.OAuth)
	
	# init the bot client with the given arguments
	bot = TopicBot(arguments)
	
	bot.start()

if __name__ == "__main__":
	main()
