#!/usr/bin/python
# dopewatcher.py - A service daemon that listens to IRC channel(s)
#				   and posts topic changes to a specified twitter account
# Usage: 
#			topic2twitter.py irc.network.url nickname OAuthInfo [additional args]
#
# Arguments:
#			irc.network.url 	: The URL of the IRC network server [e.g. irc.quakenet.org]
#			nickname			: The nick to give the daemon on the server
#			OAuthInfo			: The consumer key and access tokens needed to communicate with twitter
#								  specified in this format - consumer_key:consumer_secret:access_token_key:access_token_secret
#								  Note: This information is available on your app's info page at dev.twitter.com
#
# Additional Arguments:
#			--port [value] 		: IRC server port [default is 6667]
#			--username [string]	: Client's username
#			--realname [string]	: Client's realname
#			--password [string]	: Server password (if needed)
#			--join [string]		: Comma-separated list of channels to join 
#
# Typical usage:
#			Add this service to a cron job that restarts even if the 
#			crashes.
#
#  The MIT License (MIT)
#  Copyright 2013 Chris Earley <bearddough+dopewatcher@gmail.com>
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

import argparse
import kitnirc.client
import twitter

def main():
	# parse command line arguments and setup client object
	parser = argparse.ArgumentParser(description="IRC daemon that posts channel topics to twitter")
	parser.add_argument("host", help="Address of an IRC server")
	parser.add_argument("nick", help="Nickname to use when connecting")
	parser.add_argument("OAuthInfo", help="App OAuth details separated by colons - consumer_key:consumer_secret:access_token_key:access_token_secret")
	parser.add_argument("-p", "--port", type=int, default=6667, help="Port to use when connecting")
	parser.add_argument("--username", help="Username to use. If not set, defaults to nickname.")
	parser.add_argument("--realname", help="Real name to use. If not set, defaults to username.")
	parser.add_argument("--password", help="IRC server password, if any.")
	parser.add_argument("--join", metavar="CHAN[,CHAN...]", help="Comma-separated list of channels to join on connect.")
	args = parser.parse_args()

	c = kitnirc.client.Client(args.host, args.port)
	c.connect(
        args.nick,
        username=args.username or args.nick,
        realname=args.realname or args.username or args.nick,
        password=args.password,
	)
    
    # parse OAuth into into an array
	OAuthInfo = args.OAuthInfo.split(':')
    
	# setup conenction to twitter account using parsed OAuth info
	api = twitter.Api(OAuthInfo[0], OAuthInfo[1], OAuthInfo[2], OAuthInfo[3])
	 
	# Verify that we have access to the account, throw error if invalid credentials are given.
	try:
		api.VerifyCredentials()
	except twitter.TwitterError:
		print "ERROR: Please verify OAuth info and specify in the format shown - consumer_key:consumer_secret:access_token_key:access_token_secret"
		quit()
    
    # define dispatch routine that execute when IRC messages are captured
	try:
		#Welcome message dispatch routine
		@c.handle('WELCOME')
		def join_channels(client, *params):
			if not args.join:
				return
			for chan in args.join.split(","):
				client.join(chan)
                
		#Topic change dispatch routine
		@c.handle('TOPIC')
		def post_topic(client, *params):
			# extract the last element from the event dispatch tuple
			# (the topic string in this case) and post it to twitter
			makepost(params[len(params) - 1], api)
			
	# Connect!
		c.run()
        
    # if the user interrupts the process with ^C, then DC gracefully
	except KeyboardInterrupt:
		c.disconnect()
        
# Post the message to the @DopeLives_bot twitter account!
def makepost(topic, api):
	#shorten string to 140 characters
	message = topic[0:140]
	# post the formatted string to the account
	api.PostUpdate(message)

if __name__ == "__main__":
	main()
