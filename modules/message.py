import discord
import time

from .mysql import mysql
from .commands import commands
from .matCheck import check as matCheck

import util


class message:
    def __init__(self, bot, message, conn):
        self.bot = bot
        self.message = message
        self.conn = conn
        
        self.settings = []
        
        self.guildSettings = mysql.select(self.conn, '*', 'servers_settings')
        self.checkable = True
        
    '''
        1. Запрет ЛС на антимата
        2. Команда для запрета в определённом канале по определённой группе, по стандарту - управление только администратором 
        3. Команда смены префикса сервера. Так же, по умолчанию только администратором
        4. Добавить команду для разрешения команд каким-то пользователям
        5. Разрабатывать индивидуальный словарь
    '''
           
    def getSettings(self):        
        for setting in self.guildSettings:
            if int(self.message.server.id) == int(setting[0]):
                self.settings = setting
                break
        if self.settings == None:
            mysql.insert(self.conn, 'servers_settings', 'server_id', self.message.server.id)
        
        tables = mysql.custom(self.conn, 'SHOW TABLES')    
        self.found = False
        for each in tables:
            if each[0] == "server_" + self.message.server.id:
                self.found = True
        if not self.found:
            mysql.create(self.conn, "server_" + self.message.server.id, "`channel_id` varchar(18), `matoff` boolean NOT NULL DEFAULT 0")
            
        self.channelSettings = mysql.select(self.conn, '*', 'server_'+self.message.server.id)
            
    
    def checkMatChannel(self):
        for each in self.channelSettings:
            if self.message.channel.id == each[0] and each[1]:
                return True
                break
        return False
    
    def checkPrefix(self):
        if self.pm:
            self.withPrefix = False
            return False
        self.withPrefix = False
        if self.message.content.startswith(self.settings[1]):
            self.withPrefix = True
    
    async def run(self):        
        #Проверка на то, что сообщение создал не сам бот            
        if self.message.author.bot:
            self.checkable = False
            await self.getMsg(self.message.channel, self.message.id)
            
        #Проверка на личное сообщение и занесение этого в переменную self.pm
        if self.message.server == None:
            self.pm = True
        else:
            self.pm = False
        #Получаем индивидуальные настройки сервера
        if not self.pm:
            self.getSettings()
        else:
            self.settings = None
            self.channelSettings = None
            
        
        #Дальше идёт, если это не бот писал
        if self.checkable:
            self.checkPrefix()
            if not self.withPrefix:
                #Подключаем класс matCheck
                self.check = matCheck(self.conn, self.message, self.settings)
                
                #Проверка на мат в сообщении
                if self.check.run() and not self.checkMatChannel():
                    util.logger("Deleted message from '{}' in '{}' channel at '{}' server; msg contained '{}'".format(self.message.author.id, self.message.channel.id, self.message.server.id, self.message.content), True, False)
                    await self.delMsg()
                
            #Если же это команда, то делаем следующее    
            elif self.withPrefix:
                self.cmd = commands(self.message, self.settings, self.conn)
                self.callBack = self.cmd.run()
                
                for each in self.callBack:
                    if each[0] == "sendMessage":
                        await self.sendMsg(each[1])
                    elif each[0] == "deleteMessage":
                        await self.delMsg(each[1])
                    elif each[0] == "clearGames":
                        await self.clearGames()

    async def clearGames(self):
        for gameName, gameRole in util.getGames().items():
            for role in self.message.author.roles:
                if role.name == gameRole:
                    await self.bot.remove_roles(self.message.author, role)
    
    
    async def sendMsg(self, msgCont, msgChannel = None):
        if msgChannel == None:
            msgChannel = self.message.channel
        await self.bot.send_message(msgChannel, msgCont)
        
    async def delMsg(self, msg = None):
        if msg == None:
            msg = self.message
        await self.bot.delete_message(msg)
#    
    async def sendTyping(self):
        await self.bot.send_typing(self.message.channel)
#        
    async def delMsgs(self, messages):
        await self.bot.delete_messages(messages)
#        
    async def purgeFrom(self, channel = None , none = None, limit=100, check=None, before=None, after=None, around=None):
        if channel == None:
            channel = self.message.channel
        await self.bot.purge_from(channel, none, limit, check, before, after, around)
#        
    async def editMsg(self, msg, new_content = None, none = None, embed = None):
        await self.bot.edit_message(msg, new_content, none, embed)
#    
    async def getMsg(self, channel, id):
        await self.bot.get_message(channel, id)
#        
    async def pinMsg(self, msg):
        await self.bot.pin_message(msg)
#        
    async def uppinMsg(self, msg):
        await self.bot.uppin_message(msg)
#        
    async def pinsFrom(self, channel = None):
        if channel == None:
            channel = self.message.channel
        await self.bot.pins_from(channel)
#        
    async def logsFrom(self, channel = None, limit = 100, none = None, before=None, after=None, around=None, reverse=False):
        if channel == None:
            channel = self.message.channel
        await self.bot.logs_from(channel, limit, none, before, after, around)
    