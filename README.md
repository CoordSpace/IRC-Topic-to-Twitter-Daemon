IRC Topic-to-Twitter Daemon
====================================

A lightweight python daemon used push formatted IRC topic changes from 1+ channels to a central twitter account.

Used by IRC-based video gaming/hacking communities to alert their users of events in real time without needing to continually lurk in the channel(s). Additionally, the twitter feed also functions as an independent log of past topics which can be used for a variety of historical contexts.

Dependencies
====

 * [IRC - Internet Relay Chat (IRC) protocol client library](https://bitbucket.org/jaraco/irc)
>$ pip install irc

 * [Python Twitter: A Python wrapper around the Twitter API](https://code.google.com/p/python-twitter/)
>$ pip install python-twitter

Usage
====

    topic2twitter.py serverURL nickname OAuth join [join ...]
                        [-h] [--prependchan] [-p PORT] [--username USERNAME]
                        [--realname REALNAME] [--password PASSWORD]
                        [--infocmd INFOCMD] [--timestamp]

required arguments:

    serverURL             The IRC server to connect to
    nickname              The nickname of the bot upon connection
    OAuth                 The twitter app OAuth info in this format: 
                          consumer_key:consumer_secret:access_token_key:access_token_secret
                          Note: This information is available on your app info page at dev.twitter.com
    join                  Channel(s) to join and monitor, separated by spaces.
                          Remember to escape hashes in *nix systems. e.g. \#chan

optional arguments:

    -h, --help            Show this help message and exit
    --prependchan         Prepend the channel name to topics posted to twitter.
                          Useful when watching multiple channels
    -p PORT, --port PORT  The IRC server port (defaults to 6667)
    --username USERNAME   bot username
    --realname REALNAME   bot realname
    --password PASSWORD   IRC server password (if needed)
    --infocmd INFOCMD     The text command that any user in watched channels can
                          type to recieve the twitter accountt link.
                          Make this unique so it doesn't spam the channel during normal conversation (e.g. !twitter)
    --timestamp           Prepend a formatted [HH:MM] timestamp before the channel name (if enabled) and topic message.

                        
 
Notes
====
This daemon will automatically attempt to reconnect to the IRC server after a timeout of 10 minutes. If you have a flaky net connection, be warned that the repeated ping-outs/joins from the daemon might be considered spam and cause a ban from overzealous channel operators.

Any long topic messages will be truncated to 140 character before being sent to twitter. This may cause a loss of valuable information. 

License
-------

IRC Topic-to-Twitter Daemon is licensed under the MIT License (see `LICENSE` for details).
