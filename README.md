IRC Topic-to-Twitter Daemon
====================================

A lightweight python daemon used push formatted IRC topic changes from 1+ channels to a central twitter account.

Used by IRC-based video gaming/hacking communities to alert their users of chatroom events in real time without needing to continually lurk in the channel(s). Additionally, the twitter feed also functions as an independent log of past topics which can be used for a variety of historical contexts.

Dependencies
====

 * Python 3.3+

 * [IRC3](https://pypi.python.org/pypi/irc3/)

 * [Twitter](https://pypi.python.org/pypi/twitter) with a [Twitter app](https://apps.twitter.com/) made on an account in your control.


Usage
====

Note: It's recommended to run the daemon from within a [virtual environment](https://docs.python.org/3/library/venv.html).

First install all the requirements using:

`pip install -r /path/to/requirements.txt`

Then copy the config.ini.sample to config.ini and edit it to your needs.

Make sure to input all the keys and access tokens supplied by twitter for your app so the bot can post to the service!

Then launch the bot with helpful debug using:

`irc3 -v -r config.ini`


A sample systemd unit file available in /src though you will need to change the ExecStart and WorkingDirectory paths to match your setup.

License
====

IRC Topic-to-Twitter Daemon is licensed under the MIT License (see `LICENSE` for details).
