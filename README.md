IRC Topic-to-Twitter Daemon
====================================

A lightweight python daemon used push formatted IRC topic changes from 1+ channels to a central twitter account.

Used by IRC-based video gaming/hacking communities to alert their users of chatroom events in real time without needing to continually lurk in the channel(s). Additionally, the twitter feed also functions as an independent log of past topics which can be used for a variety of historical contexts.

Dependencies
====

 * Python 2.7

 * [Twisted](twistedmatrix.com)
>$ pip install twisted

 * [Python Twitter: A Python wrapper around the Twitter API](https://code.google.com/p/python-twitter/)
>$ pip install python-twitter

Usage
====

    First create the configuration file using the handy wizard:
        
        `python src/makeconfig.py`

    Then launch the bot:

        `python2.7 /path/to/main.py /path/to/topic2twitter.conf &`

    A sample systemd unit file and wrapper bash script are available in /src though you will need to change the ExecStart and bash paths.

 
Notes
====

Any long topic messages will be truncated to 125 characters before being sent to twitter. This may cause a loss of valuable information so format your topics accordingly. 

To Do
====

 * Make the system aware of twitter's t.co 'URL lengthener' when formatting the message string. Sometimes short URLs in a topic can cause the message to become too large to post after twitter expands them into 20+ character t.co links. 

License
====

IRC Topic-to-Twitter Daemon is licensed under the MIT License (see `LICENSE` for details).
