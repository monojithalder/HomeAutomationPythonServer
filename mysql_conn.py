import MySQLdb

def conn():
    db = MySQLdb.connect("localhost","root","-eyeSu28yuwu","door_lock") 
    return db