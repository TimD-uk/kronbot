from .mysql import mysql as mysql_

import mysql.connector

class server:
    def __init__(self, bot, server, conn):
        self.bot = bot 
        self.server = server
        self.conn = conn
    def join(self):
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES")
        
        tables = cursor.fetchall()
        
        
        self.found = False
        
        for each in tables:
            if each[0] == "server_" + self.server.id:
                self.found = True
        
        if not self.found:
            mysql_.create(self.conn, "server_"+self.server.id, "`channel_id` varchar(18), `matoff` boolean NOT NULL DEFAULT 0")
        
        self.found = False
            
            
        cursor.execute("SELECT * FROM servers_settings")
        servers = cursor.fetchall()
        cursor.close()
                
        for each in servers:
            if each[0] == server.id:
                self.found = True
        
        if not self.found:
            mysql_.insert(self.conn, 'servers_settings', 'server_id', self.server.id)
            