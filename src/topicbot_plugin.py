# -*- coding: utf-8 -*-
from irc3.plugins.command import command
import irc3
from random import choice
from time import time, gmtime, strftime
from infoextraction import ExtractInfo


def greek_string(s):
    '''
        Replaces the first standard vowel in a string with an accented
        unicode vowel. Useful to prevent annoying pings on IRC.
    '''
    before = u'aeiouyAEIOUY'
    after = u'àèìòùÿÄÉÍÒÙÝ'
    # our dict of normal to greeked vowels
    trans = {i: j for i, j in zip(before, after)}

    for i, c in enumerate(s):
        if c in before:
            # rebuild the string with our new greeked vowel
            # taking the place of the first vowel found
            greeked = s[:i] + trans[c] + s[i + 1:]
            return greeked
    # return the string untouched if there's nothing to change
    return s


def makeRoulette(nickname):
    m = [
        'Lets all kindly ask {0} to stream!',
        'I think ... {0} should stream!',
        'It\'s been a while since {0} last streamed.',
        '{0}!',
        'I just asked !larry and he said that {0} should stream!',
        'If only {0} would stream some videogames on the internet.',
        'Maybe if we focus really hard {0} will stream!',
        '{0}?',
        '{0}.',
        'I have fond memories of {0} streams.',
        'Lets all get comfy and wait for {0} to stream.',
        'I bet {0} is setting up to stream as I type!',
        'How about ... {0}? :3c',
        'I hacked into the streamer channel and it looks like {0} is getting ready to stream!',
        'What if {0} streamed some videogames?',
        'Maybe if {0} is around, they could stream?',
        'Don\'t let your {0} streams be dreams.',
        'Believe in yourself and maybe one day {0} will stream!',
        'Yo {0}, where the vidja at?',
        'Lets all focus our positive energy towards {0}.',
        'I hear that {0} knows who will be streaming next.',
        '{0}. Streams. Yes!',
        '{0} should stream!',
        'I can never get enough of {0} streams!',
        'There\'s no such thing as too much {0} livelive!',
        'The world would be a better place if only {0} would stream.',
        'I\'ll give 20 dopecoins to {0} if they stream.',
        'Let\'s mix it up. How about if {0} streams a movie instead?',
        '!p1ayed {0}',
        '{0} streams are so comfy, I could go for one right now!',
        'Maybe you should stream!',
        'Lets put our heads to together and think of who should stream.',
        'You know what, no. How about YOU say who will stream next!',
        '>implying someone will stream',
        '(Pssst, {0} will be streaming next)',
        'The streaming gods demand an offering! Decide amongst youselves who should be sacrificed.',
        'Maybe we should just play videogames instead.',
        'How about we all go read a book instead?',
        'When was the last time you went outside?',
        'Hey, remember when Po_ used to stream?',
        'http://i.imgur.com/y7GDSmh.png']
    return choice(m).format(nickname)


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

    @irc3.event(irc3.rfc.JOIN)
    def say_hi(self, mask, channel, **kw):
        if mask.nick == self.bot.nick:
            self.bot.log.info("Joined channel {0}".format(channel))
            self.bot.notice('birdo', 'Twitter bot, ready for service!')

    @command(permission='admin')
    def echo(self, mask, target, args):
        """Echo

            %%echo <message>...
        """
        self.bot.log.info("Recieved !echo from {0}".format(mask.nick))
        yield ' '.join(args['<message>'])

    @command(permission='everyone')
    def quotes(self, mask, target, args):
        """Echo

            %%quotes
        """
        self.bot.log.info("Recieved !quotes from {0}".format(mask.nick))
        yield "Shit people say in >this chat - https://twitter.com/Dopefish_Quotes"

    @command(permission='everyone')
    def next(self, mask, target, args):
        """next: Ask the bot who will stream next.

            %%next
        """
        self.bot.log.info("Recieved !next from {0}".format(mask.nick))
        if self.is_cooled_down('next'):
            # parse the channel list for OP users and pick a random one
            nick = choice(list(self.bot.channels[target].modes['@']))
            # greek it by mutating any vowels and sent it to the channel
            yield makeRoulette(greek_string(nick))
        else:
            self.cooldown_warning(mask.nick)

    @command(permission='everyone')
    def readthis(self, mask, target, args):
        """readthis: Inform users of the channel rules.

            %%readthis [<username>]
        """
        self.bot.log.info("Recieved !readthis from {0}".format(mask.nick))
        if self.is_cooled_down('readthis'):
            if args['<username>']:
                yield "{0}: Please read the channel rules - http://dopelives.com/newfriend.html".format(args['<username>'])
            else:
                yield "Please read the channel rules: http://dopelives.com/newfriend.html"
        else:
            self.cooldown_warning(mask.nick)

    @command(permission='everyone')
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
