import irc3


def main():
    # instanciate a bot
    config = irc3.utils.parse_config('bot', 'config.ini')
    bot = irc3.IrcBot.from_config(config)
    bot.run(forever=True)

if __name__ == '__main__':
    main()
