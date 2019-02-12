#!/usr/bin/env python3

import cx_Oracle


__all__ = ['DataBase']


#name = "Max"
#score = 200

class DataBase():

    def __init__(self):

        self._conn = None
        
    def openConnection(self):
        """Open Connection"""

        with open('./db/dbpwd.txt','r') as file:
            self.pwd = file.readline().replace('\n','')
  
        self._conn = cx_Oracle.connect(self.pwd)
        self.pwd = None #Keep Pwd in memory for a short as possible
            
    def closeConnection(self):
        """Close Connection"""

        assert self._conn != None #Check connection open
        self._conn.close
        self._conn = None      
        
    #score needs to be passed in correctly
    def addHSretrieveRank(self, name, score):

        self.username = name
        self.highscore = score
        c = self.conn.cursor()

        #Add the new score
#        query = "INSERT INTO S1893502.SCORE VALUES (3,1,:name, :score, 10)"
        query = "INSERT INTO JQSCORE VALUES (1,:name,:score)"
        c.execute(query,name=self.username,score=self.highscore)
        self._conn.commit()

        #Get rank
#        query = "SELECT COUNT(*) FROM S1893502.SCORE WHERE SCORE >= :score"
        query = "SELECT COUNT(*) FROM JQSCORE WHERE SCORE >= :score"
        c.execute(query, score=self.highscore)
        pos = 0
        for row in c:
#            pos = row[0]+1
            pos = row[0]

        return str(pos)

