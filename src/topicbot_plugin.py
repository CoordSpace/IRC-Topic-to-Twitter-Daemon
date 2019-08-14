# -*- coding: utf-8 -*-
from irc3.plugins.command import command
import irc3
from random import choice
from time import time, gmtime, strftime
from infoextraction import ExtractInfo

@irc3.plugin
class Plugin:

    def __init__(self, bot):
        self.bot = bot
        # a dict to use for tracking cooldowns
        # each function will add a key:value in the form of
        # {name: time_cmd_was_run}
        self.times = {}
        # Seconds between successful command executions
        self.cooldown = 300
        # topic string parsing and tweet text generator
        self.extractor = ExtractInfo(self.bot.log)

    def cooldown_warning(self, nick):
        """
            Send a formatted notice to the given user's nick informing them
            of the command cooldown.
        """
        self.bot.log.info("Cooldown warning sent to {0}".format(nick))
        self.bot.notice(nick, "That command is on cooldown. Please wait before trying again.")

    def is_cooled_down(self, func_name):
        """
            Given a function name in string form, return whether or not the
            cooldown time has been met for the respective function.
            If the cooldown time is met, also update the tracking dict.
        """
        if func_name in self.times:
            if time() - self.times[func_name] > self.cooldown:
                self.times[func_name] = time()
                self.bot.log.info("Function {0}, not in cooldown!".format(func_name))
                return True
            else:
                self.bot.log.info("Function {0}, is in cooldown!".format(func_name))
                return False
        else:
            self.bot.log.info("Function {0}, not in cooldown!".format(func_name))
            self.times[func_name] = time()
            return True

    @command(permission='everyone', quiet=True)
    def notifications(self, mask, target, args):
        """notifications: Posts a link to the bot's twitter account.

            %%notifications
        """
        self.bot.log.info("Recieved !notification from {0}".format(mask.nick))
        if self.is_cooled_down('notification'):
            # Get the current handle of the twitter account the bot is using
            username = self.bot.get_social_connection().account\
                .settings()['screen_name']
            # create the formatted message to be sent out as privmsg to the chan
            yield 'Follow http://twitter.com/{0} to know when the stream is live!'\
                .format(username)
        else:
            self.cooldown_warning(mask.nick)

    @irc3.event(irc3.rfc.TOPIC)
    def topic_change(self, mask, channel, data):
        """
        Upon a channel topic change, send out a formatted tweet informing users
        of the current stream.
        """

        self.bot.log.info('Topic changed! Current topic: ' + data)

        # generate the formatted message
        newTopic = self.extractor.generateMessage(data)

        if newTopic is None:
            # dupe topic, ignore
            return
        else:
            # Start the message to be tweeted with the current time stamp
            final_message = strftime("[%H:%M]", gmtime()) + ' '
            # tack on the topic itself
            final_message += newTopic
            self.bot.log.info('Final message: ' + final_message)
            for name, status in self.bot.send_tweet(final_message):
                self.bot.log.info('Tweet to {0}: status - {1}'.format(name, status))
            self.bot.log.info('Tweet sent!')
