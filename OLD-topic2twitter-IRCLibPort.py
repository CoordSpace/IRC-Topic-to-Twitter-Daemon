# This script needs to:
#	* connect to a specified IRC server
#		- Feature: argument that forces the connection to automatically reconnect upon DC. (-reconnect/-r)
#	* verify twitter OAuth info to be valid, print an error and quit otherwise.
#	* listen for topic changes and post the new topic to twitter.
#		- if the user specifies more then one channel to watch, append the channel name to the twitter messages.
# Usage: 
#			topic2twitter.py irc.network.url nickname OAuthInfo [additional args]
#
# Arguments:
#			irc.network.url 	: The URL of the IRC network server [e.g. irc.quakenet.org]
#			nickname			: The nick to give the daemon on the server
#			OAuthInfo			: The consumer key and access tokens needed to communicate with twitter
#								  specified in this format - consumer_key:consumer_secret:access_token_key:access_token_secret
#								  Note: This information is available on your app info page at dev.twitter.com
#
# Additional Arguments:
#			--port [value] 		: IRC server port [default is 6667]
#			--username [string]	: Client username
#			--realname [string]	: Client realname
#			--password [string]	: Server password (if needed)
#			--join #C1 #C2 ...	: Space separated list of channels to join

def main():
	#global twitAPI
	
	#global args
	
	#args = getargs()
	
	#bot = IRCBot()
	
	#bot.start()
	
	# setup IRC event handlers 
	#bot.add_global_handler("welcome", on_connect)
   # bot.add_global_handler("join", on_join)
   # bot.add_global_handler("disconnect", on_disconnect)
   # bot.add_global_handler("topic", on_topic)
    
    #bot.process_forever()
    print "Hello"
    print "Hello"

## The Twitter API object that will allow us to communicate with the service
#twitAPI = None
## the 
#args = None

## Take the new topic message and send it to twitter.    
#def on_topic(self, connection, event):

## Read lines from channels and if they contain a !command
#def on_pubmsg(self, connection, event):
	
## Join all given channels when welcome message is delivered
#def on_welcome(self, connection, event):
	#for channel in args.join:
		#if irc.client.is_channel(channel):
			#connection.join(channel)

## DC from server by killing the process and issuing a quit command
#def on_disconnect(self, connection, event):
    #raise SystemExit()

# Initialize the twitter API oject and verify the connection.
def setuptwitter(OAuth):
	# Split formatted OAuth string into a list
	OAuthlist = OAuth.split(':')
	
	# create the API object using the supplied credentials
	twitAPI = twitter.Api(OAuthlist[0], OAuthlist[1], OAuthlist[2], OAuthlist[3])
	
	# Verify that we have access to the account, throw error if invalid credentials are given.
	try:
		api.VerifyCredentials()
	except twitter.TwitterError:
		print "ERROR: Please verify OAuth info and specify in the format shown - consumer_key:consumer_secret:access_token_key:access_token_secret" + sys.exc_info()[1]
		raise SystemExit(1)

# Setup the CLI arguments and create the parser object
def getargs():
	parser = argparse.ArgumentParser()
    parser.add_argument('server', required=True)
    parser.add_argument('nickname', default='TopicBot')
    parser.add_argument('OAuth', required=True, help='The consumer key and access tokens needed to communicate with twitter', epilog='Specified in this format - consumer_key:consumer_secret:access_token_key:access_token_secret')
    parser.add_argument('-j', '--join' nargs='+', required=True, help='Channel(s) to join and monitor, separated by spaces.')
    parser.add_argument('--prependname', help='Prepend the channel name to any topics posted to twitter. Useful when watching multiple channels.')
    parser.add_argument('-p', '--port', default=6667, type=int)
    parser.add_argument('-u', '--username', help='Bot username.')
    parser.add_argument('-r', '--realname', help='Bot realname.')
    parser.add_argument('-p', '--password', help='Server password (if needed)')
    irc.logging.add_arguments(parser)
    return parser.parse_args()
    
if __name__ == "__main__":
	main()
