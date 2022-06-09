#!/usr/bin/python3.9
import re
import gitlab
from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
#from lib get_projects

print(dir(gitlab))
git = gitlab.GitLab(host='gitlab.com')

def main():
    bot = Bot()
    bot.run()


@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply('i understand HI or hi')
    message.react('+1')


if __name__ == "__main__":
    main()
