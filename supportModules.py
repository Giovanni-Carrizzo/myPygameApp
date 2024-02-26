import pygame as pg
import sqlite3 as sq

font_name = pg.font.match_font('arial')

def draw_text(surf,text,size,x,y,cir):
    #create a font object
    try:
        font = pg.font.Font(font_name,size)#this will create text
        text_surface = font.render(text,True,cir) #True is for anti aliasing
        text_rect = text_surface.get_rect()#get the rectangle for the text
        text_rect.midtop = (x,y) #put x,y at the midtop of the rectangle
        surf.blit(text_surface, text_rect)
    except pg.error as e:
        print(f'Pygame error: {e}')

def dbConnector():
    '''Connect to database and return a connection object'''
    try:
        conn = sq.connect("Garley.db")
        cur = conn.cursor()
        return conn, cur
    except sq.Error as e:
        print(f'Database connection error: {e}')
print(dbConnector())

def writeNewtoDatabase(playerName, score):
    '''Writes to the database'''
    conn,cur = dbConnector()
    id = primaryKeyGen()
    query = f'''INSERT INTO Leaderboard VALUES(?,?,?,?,?)'''
    cur.execute(query, (id, playerName, 0,0,score))
    conn.commit()
    conn.close()
    print('Success')

def readDatabaseRecords():
    '''Reads data from a database'''
    conn,cur = dbConnector()
    query = '''SELECT * FROM Leaderboard'''
    cur.execute(query)
    results = cur.fetchall()
    print(results)
    conn.close()
readDatabaseRecords()

def writetoSpecific(playerName,score):
    '''Writes a value to a specific record'''
    #query record to be written to
    conn,cur = dbConnector()
    query = '''SELECT COUNT(*)
    FROM Leaderboard
    WHERE Username = ?'''
    cur.execute(query,(playerName,))
    results = cur.fetchall()
    if results[0][0] == 1:
        print('call append method')
    else:
        writeNewtoDatabase(playerName,score)
    #query record to be written to
    #prepare data to be written 
    #open connection, write data, close connection
        
def primaryKeyGen():
    '''Generates a new PK for a new record using last PK'''
    conn, cur = dbConnector()
    query = '''SELECT ID from Leaderboard '''
    cur.execute(query,)
    results = cur.fetchall()
    print(results)
    newID = results[-1][0]+1
    conn.close()
    return newID

def updateExisting(playerName, score):
    '''Reads existing records and updates the score
    shuffling out the oldest score and adding new
    '''
    conn,cur = dbConnector()
    query = '''SELECT score1, score2, score3 FROM Leaderboard WHERE username =?'''
    cur.execute(query,(playerName,))
    results = cur.fetchall
    updateQuery ='''UPDATE Leaderboard SET score1=?, score2=?, scores3=? WHERE username=?'''
    score1, score2, score3 = results[0][1], results[0][2], score
    cur.execute(updateQuery,(score1,score2,score3))
    conn.commit()
    conn.close()
