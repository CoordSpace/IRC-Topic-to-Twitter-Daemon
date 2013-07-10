#!/usr/bin/python

# This script needs to:
#	* connect to a specified IRC server
#		- Feature: argument that forces the connection to automatically reconnect upon DC. (-reconnect/-r)
#	* DONE - verify twitter OAuth info to be valid, print an error and quit otherwise.
#	* listen for topic changes and post the new topic to twitter.
#		- if the user specifies more then one channel to watch, append the channel name to the twitter messages.
# Usage: 
#			topic2twitter.py irc.network.url nickname OAuthInfo [additional args]

import argparse
import twitter
import irc.client
import sys

# The Twitter API object that will allow us to communicate with the service
twitAPI = None

# Initialize the twitter API object and verify the connection.
def setuptwitter(OAuth):
	# Split formatted OAuth string into a list
	OAuthlist = OAuth.split(':')
	
	# Do a quick formatting sanity check on the number of OAuth bits given.
	if len(OAuthlist) != 4:
		print "ERROR: Please verify OAuth info and specify in the format shown - consumer_key:consumer_secret:access_token_key:access_token_secret"
		raise SystemExit(1)
	
	# create the API object using the supplied credentials
	api = twitter.Api(OAuthlist[0], OAuthlist[1], OAuthlist[2], OAuthlist[3])
	
	# Verify that we have access to the account, throw error if invalid credentials are given.
	try:
		api.VerifyCredentials()
	except twitter.TwitterError:
		print "ERROR: Please verify OAuth info and specify in the format shown - consumer_key:consumer_secret:access_token_key:access_token_secret"
		raise SystemExit(1)
	return api

# Setup the CLI arguments and create the parser object
def get_args():
	parser = argparse.ArgumentParser(description="IRC daemon that posts channel topics to twitter")
	parser.add_argument('server', help='the IRC server to connect to')
	parser.add_argument('nickname', default='topicBot', help='the nickname of the bot upon connection')
	parser.add_argument('OAuth', help='the twitter app OAuth info in this format: consumer_key:consumer_secret:access_token_key:access_token_secret')
	parser.add_argument('join', nargs='+', help='channel(s) to join and monitor, separated by spaces. remember to escape hashes in *nix systems. e.g. \#chan')
	parser.add_argument('--prependname', help='prepend the channel name to topics posted to twitter. Useful when watching multiple channels')
	parser.add_argument('-p', '--port', default=6667, type=int)
	parser.add_argument('--username', help='bot username')
	parser.add_argument('--realname', help='bot realname')
	return parser.parse_args()
	
# Take the new topic message and send it to twitter.    
def on_topic(self, connection, event):
	main_loop(connection)

# Read lines from channels and if they contain a !command
def on_pubmsg(self, connection, event):
	main_loop(connection)
	
# Join all given channels when welcome message is delivered
def on_welcome(self, connection, event):
	for channel in args.join:
		if irc.client.is_channel(channel):
			connection.join(channel)

# DC from server by killing the process and issuing a quit command
def on_disconnect(self, connection, event):
	raise SystemExit()
    
def main():
	print "Hello!"
	
	args = get_args()
	
	twitAPI = setuptwitter(args.OAuth)

if __name__ == "__main__":
	main()
