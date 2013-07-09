IRC Topic-to-Twitter Daemon
====================================

This is a lightweight python daemon used push IRC topic changes from 1+ channels to a twitter account. Used by IRC-based video gaming communities to alert their viewers of streams in real time without needing to stay on IRC.

Dependances
====

 * [KitnIRC - A Python IRC Bot Framework](https://github.com/ayust/kitnirc)
>$ pip install kitnirc

 * [Python Twitter: A Python wrapper around the Twitter API](https://code.google.com/p/python-twitter/)
>$ pip install python-twitter

Usage
====

    topic2twitter.py irc.network.url nickname OAuthInfo [additional args]

Arguments:
    
    irc.network.url     : The URL of the IRC network server (e.g. irc.quakenet.org)
	nickname			: The nick to give the daemon on the server
	OAuthInfo			: The consumer and access token info needed to communicate with twitter specified in this format: 
                          consumer_key:consumer_secret:access_token_key:access_token_secret
                        
    Note: This information is available on your app info page at dev.twitter.com

Additional Arguments:
    
    --port [value] 		: IRC server port [default is 6667]
    --username [string]	: Client username
    --realname [string]	: Client realname
    --password [string]	: Server password (if needed)
    --join [string]		: Comma-separated list of channels to join 
    
License
-------

IRC Topic-to-Twitter Daemon is licensed under the MIT License (see `LICENSE` for details).

Other Resources
---------------

 * [KitnIRC - A Python IRC Bot Framework](https://github.com/ayust/kitnirc)
 * [Python Twitter: A Python wrapper around the Twitter API](https://code.google.com/p/python-twitter/)
