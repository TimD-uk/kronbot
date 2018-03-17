import discord
import util
from modules.mysql import mysql

import re

class update:
    def __init__(self, memBefore, memAfter, conn, bot):
        self.games = util.getGames()
        self.memBefore = memBefore
        self.memAfter = memAfter
        self.conn = conn
        self.bot = bot
        
        self.allowedServerForGames = [
            '344870707882360835',
            '367409060334665730',
            '366615202470297600'
            ]
        
    def get_allow_to_games(self):
        self.found = False
        for each in mysql.custom(self.conn, "SHOW TABLES"):
            if each[0] == "userData_" + self.memAfter.server.id and not self.found:
                self.found = True
                
        if self.found:
            self.table = mysql.select(self.conn, '*', 'userData_' + self.memAfter.server.id)
            if self.table == []:
                return True
            else:
                for each in self.table:
                    if each[0] == self.memAfter.id and each[1] == True:
                        return True
                    elif each[0] == self.memAfter.id and each[1] == False:
                        return False
                return True
        else:
            return True
    
    def get_role(self, role_name):
        for role in self.memAfter.server.roles:
            if role.name == role_name:
                return role
        return None
    
    def check_role(self, role_name):
        for role in self.memAfter.roles:
            if role.name == role_name:
                return True
        return False
    
    async def setGame(self, game):
        if not self.check_role(game):
            gameRole = self.get_role(game)
            if not gameRole == None:
                await self.bot.add_roles(self.memAfter, gameRole)
                util.logger('Пользователю `{}` добавлена группа `{}`.'.format(self.memAfter.id, game), True, False)
        
    async def update(self):
        if self.memBefore.server.id in self.allowedServerForGames:
            if not self.memAfter.game == None and self.get_allow_to_games():
                for gameRegex, gameRole in self.games.items():
                    if not re.search(gameRegex, self.memAfter.game.name) == None:
                        await self.setGame(gameRole)
                        break
                        
                    
                