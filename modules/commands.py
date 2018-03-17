from .mysql import mysql

import util

class commands:    
    def __init__(self, message, settings, conn):
        self.message = message
        self.guildSettings = settings
        self.conn = conn
        
        self.mats = mysql.select(self.conn, '*', 'mat_regex')
        
        self.back = []
            
        self.alphabet = {
            "а" : ["a","ya","@","а","е","e","о","o"],
            "б" : ["б","6","b"],
            "в" : ["в","v","w"],
            "г" : ["г","g","к","k"],
            "д" : ["д","d","т","t"],
            "е" : ["е","e","и","u","yo","ye"],
            "ё" : ["е","e","yo","ye"],
            "ж" : ["ж","zh","g","j","z","ш","sh"],
            "з" : ["з","z","3","с","c"],
            "и" : ["и","u","i","е","e","l","1"],
            "й" : ["й","y","i"],
            "к" : ["к","q","k","г","g"],
            "л" : ["л","l","1","i"],
            "м" : ["м","m"],
            "н" : ["н","n"],
            "о" : ["о","o","а","a","@","е","e"],
            "п" : ["п","p","р"],
            "р" : ["р","r","p"],
            "с" : ["с","c","s","$","з","z"],
            "т" : ["т","t","д","d"],
            "у" : ["у","u","y","ю"],
            "ф" : ["ф","f","ph"],
            "х" : ["х","h","kh","ch", "x"],
            "ц" : ["ц","c","cz","ts"],
            "ч" : ["ч","ch","c","4"],
            "ш" : ["ш","sh","sch","w"],
            "щ" : ["щ","sh","shch","sc","w"],
            "ъ" : ["ъ"],
            "ы" : ["ы","y","i"],
            "ь" : ["ь"],
            "э" : ["э","е","e"],
            "ю" : ["ю","у","y","u","yu","ju","iu"],
            "я" : ["я","а","е","a","e","ya","ia","ja"]
            }
        self.channelCmd = [
            '366450919543406594',
            '366625847479894026',
            '397813193214394371',
            '382135434966466560'
            ]
                
                
    def matoff(self):
        srvs = mysql.select(self.conn, "*", "server_" + self.message.server.id)
        
        self.f = False
        
        if srvs == []:
            mysql.insert(self.conn, "server_" + self.message.server.id, "channel_id, matoff", self.message.channel.id + ', 1')
            self.back.append(["sendMessage", "Мат-фильтр `выключен` в этом канале"])
            self.f = True
        else:
            for each in srvs:
                if each[0] == str(self.message.channel.id) and each[1] == 0:
                    mysql.update(self.conn, "server_" + self.message.server.id, "matoff = 1", "channel_id={}".format(self.message.channel.id))
                    self.f = True
                    self.back.append(["sendMessage", "Мат-фильтр `выключен` в этом канале"]) 
                    break
                elif each[0] == str(self.message.channel.id) and each[1] == 1:
                    mysql.update(self.conn, "server_" + self.message.server.id, "matoff = 0", "channel_id={}".format(self.message.channel.id))
                    self.f = True
                    self.back.append(["sendMessage", "Мат-фильтр `включен` в этом канале"])
                    break
        
        if not self.f:
            mysql.insert(self.conn, "server_" + self.message.server.id, "channel_id, matoff", self.message.channel.id + ', 1')
            self.back.append(["sendMessage", "Мат-фильтр `выключен` в этом канале"])
        
        self.back.append(["deleteMessage", self.message])
        
    def set_allow_to_games(self):
        self.found = False
        for each in mysql.custom(self.conn, "SHOW TABLES"):
            if each[0] == "userData_" + self.message.server.id and not self.found:
                self.found = True
        
        if self.found:
            self.done = False
            self.usGame = mysql.select(self.conn, '*', 'userData_' + self.message.server.id)
            if self.usGame == []:
                mysql.insert(self.conn, 'userData_' + self.message.server.id, 'user_id', self.message.author.id)
                self.back.append(["sendMessage", "`Больше не добавляем Вам игры`"])
                self.back.append(["deleteMessage", self.message])
            else:
                for each in self.usGame:
                    if each[0] == self.message.author.id and each[1] == True:
                        self.done = True
                        mysql.update(self.conn, 'userData_' + self.message.server.id, 'allow_games = 0', "user_id = {}".format(self.message.author.id))
                        self.back.append(["sendMessage", "`Больше не добавляем Вам игры`"])
                        self.back.append(["deleteMessage", self.message])
                    elif each[0] == self.message.author.id and each[1] == False:
                        self.done = True
                        mysql.update(self.conn, 'userData_' + self.message.server.id, 'allow_games = 1', "user_id = {}".format(self.message.author.id))
                        self.back.append(["sendMessage", "`Теперь добавляем группы игр`"])
                        self.back.append(["deleteMessage", self.message])
                if not self.done: 
                    mysql.insert(self.conn, 'userData_' + self.message.server.id, 'user_id', self.message.author.id)
                    self.back.append(["sendMessage", "`Больше не добавляем Вам игры`"])
                    self.back.append(["deleteMessage", self.message])
        else:
            mysql.create(self.conn, 'userData_' + self.message.server.id, '`user_id` varchar(18), `allow_games` boolean NOT NULL DEFAULT 0')
            mysql.insert(self.conn, 'userData_' + self.message.server.id, 'user_id', self.message.author.id)
            self.back.append(["sendMessage", "`Больше не добавляем Вам игры`"])
            self.back.append(["deleteMessage", self.message])
        
    def clearGames(self):
        if self.message.channel.id in self.channelCmd:
            self.back.append(["clearGames", ""])
            self.back.append(["deleteMessage", self.message])
            self.back.append(["sendMessage", "`Ваши игры очищены`"])
            
    
    def checkCmdPerms(self):
        if self.message.channel.permissions_for(self.message.author).manage_messages or str(self.message.author.id) == '210516579778166787':
            return True
        else:
            return False
    
    def run(self):
        self.lenPrefix = len(self.guildSettings[1])
        self.msg = self.message.content[self.lenPrefix:]
        
        self.msg = self.msg.split(" ") 
        
        self.cmd = self.msg[0].lower()
        self.msg.pop(0)
        self.args = self.msg
        #Команда для сброса игр
        #Команда для отключения выставления игр
        if self.cmd == "matoff":
            if self.checkCmdPerms():
                self.matoff()
            else:
                self.back.append(["sendMessage", "`У Вас недостаточно прав для выполнения команды`"])
                self.back.append(["deleteMessage", self.message])
        elif self.cmd == "gameoff":
            self.set_allow_to_games()
        elif self.cmd == "cleargames":
            self.clearGames()
        return self.back
    
    