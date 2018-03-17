import mysql.connector as db
import util.logger as logger

class mysql:
    def close(conn, config):
        conn.close()
        logger("Connection closed with database " + config['DataBase']['DB'] + '.', True, True)
        
    def connection(config):
        try:
            conn = db.connect(user=config['DataBase']['login'], 
                                        password=config['DataBase']['pass'],
                                        host=config['DataBase']['host'],
                                        database=config['DataBase']['DB'])
        
            util.logger("Connected to database " + config['DataBase']['DB'] + " as " + config['DataBase']['login'] + '.', True, True)
        
        except Error as e:
            print(e)
        
        finally:
            return conn
        
    def create(conn, tablename, columns):
        cursor = conn.cursor()
    
        SQL = "CREATE TABLE {} ({})".format(tablename, columns)
        
        try:
            cursor.execute(SQL)
            
        except Error as e:
            print(e)
            
        finally:
            cursor.close()
        
    def delete(conn, table, where):
        try:
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM {} WHERE {}".format())
                
        except Error as e:
            print(e)
            
        finally:
            cursor.close()
        
    def insert(conn, places, columns, values):
        try:
            cursor = conn.cursor()
            
            SQL = "INSERT INTO {} ({}) VALUES({})".format(places, columns, values)
            
            cursor.execute(SQL)
            conn.commit() #Сохранение изменений       
             
        except Error as e:
            print(e)
    
        finally:
            cursor.close()
        
    def select(conn, data, dataTable, whereHave = ""):
        try:            
            if whereHave == "":
                SQL = "SELECT " + data + " FROM " + dataTable
            else:
                SQL = "SELECT " + data + " FROM " + dataTable + " WHERE " + whereHave
            cursor = conn.cursor()
            cursor.execute(SQL)
            row = cursor.fetchone()    
            text = []
            while row is not None:
                text.append(row)
                row = cursor.fetchone()
        
            cursor.close()
            
        except Error as e:
            print(e)
        
        return text
        
    def update(conn, table, set, where):
        try:
            cursor = conn.cursor()
        
            cursor.execute("UPDATE {} SET {} WHERE {}".format(table, set, where))
            conn.commit()
            
        except Error as e:
            print(e)
            
        finally:
            cursor.close()
            
    def custom(conn, SQL):
        try:
            cursor = conn.cursor()
            cursor.execute(SQL)
            result = cursor.fetchall()
        
        except Error as e:
            print(e)
        
        finally:
            cursor.close()
            return result