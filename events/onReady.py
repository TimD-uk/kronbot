import util 
import discord

def countMemb(bot):
    summ = 0
    for server in bot.servers:
        for member in server.members:
            summ += 1
        
    return str(summ)

def ready(bot):
    util.logger('----', False)
    util.logger('Logged in as ' + util.colors.WARNING + bot.user.name + util.colors.ENDC +'(ID:' + util.colors.WARNING + bot.user.id + util.colors.ENDC + ') | Connected to ' + util.colors.WARNING + str(len(bot.servers))+ util.colors.ENDC +' servers | Connected to ' + util.colors.WARNING + countMemb(bot) + util.colors.ENDC +' users', True, True)
    util.logger(util.colors.WARNING + 'Discord bot is running on discord.py(ver. ' + discord.__version__ + ')' + util.colors.ENDC, False)
    util.logger('Bot version: 2.0.15') 
    util.logger('----', False)