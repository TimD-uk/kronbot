import discord
import json
import sys
import time
import multiprocessing
import signal
import asyncio
import os
#################################
##### Import my own modules #####
#################################
import util

from events import onReady
from events import onMemberUpdate

from modules.message import message as msg
from modules.server import server as srv
from modules.mysql import mysql
#################################
######## Get config file ########
#################################
config = util.getConfig() 
#################################
# This code was build by hybrid #
### https://vk.me/hybrid.only ###
###### Copyright 2017-2018 ######
#################################

bot = discord.Client()

util.logger(util.colors.OKGREEN + "Bot started" + util.colors.ENDC, True, True)
conn = mysql.connection(config)

class statics:
    startTime = time.time()
    
    def countMemb(bot):
        summ = 0
        for server in bot.servers:
            for member in server.members:
                summ += 1
        
        return str(summ)
            
#################################
#### Other useful functions #####
#################################
        
async def getQuery():
    util.logger("Started to connect")
    while True:
        await asyncio.sleep(1)
        mysql.select(conn, "*", "servers_settings")

#################################
######### Bot's events ##########
#################################

@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name="{} users".format(statics.countMemb(bot))))
    onReady.ready(bot)
    bot.loop.create_task(getQuery())
    
@bot.event
async def on_message(message):
    MSG = msg(bot, message, conn)
    bot.loop.create_task(MSG.run())

@bot.event
async def on_message_edit(before, after):
    MSG = msg(bot, after, conn)
    bot.loop.create_task(MSG.run())

@bot.event
async def on_server_join(server):
    srvr = srv(bot, server, conn)
    srvr.join()
    
@bot.event
async def on_member_join(member):
    await bot.change_presence(game=discord.Game(name="{} users".format(statics.countMemb(bot))))

@bot.event
async def on_member_remove(member):
    await bot.change_presence(game=discord.Game(name="{} users".format(statics.countMemb(bot))))
    
@bot.event
async def on_member_update(memBefore, memAfter):
    upd = onMemberUpdate.update(memBefore, memAfter, conn, bot)
    await upd.update()
#################################
###### При нажатии Ctrl + C #####
#################################
def signal_handler(signum, frame):
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    print(ERASE_LINE + CURSOR_UP_ONE)
    if time.time() - statics.startTime >= 5:
        mysql.close(conn,config)
        
        util.logger(util.colors.OKGREEN + "Bot stopped" + util.colors.ENDC, True, True)
        os.rename("logs/latest.log", "logs/{}.log".format(time.strftime("%Y-%m-%d_%H:%M:%S")))
        sys.exit(0)
    else:
        util.logger(util.colors.WARNING + "Too early stop" + util.colors.ENDC)
        
signal.signal(signal.SIGINT, signal_handler)



bot.run(config['Settings']['token'])
        
