from flask import Flask, request
import cx_Oracle
import json
from flask import jsonify

app = Flask(__name__)

class DataBase():
    
    #score needs to be passed in correctly
    def addHSretrieveRank(self, name, score):
        with open('./db/dbpwd.txt','r') as file:
            pwd = file.readline().replace('\n','')
        conn = cx_Oracle.connect(pwd)
        c = conn.cursor()

        #Get rank
        query = "SELECT COUNT(*) FROM S1893502.SCORE WHERE SCORE >= :score"
        c.execute(query, score=score)
        pos = 0
        for row in c:
            pos = row[0]+1

        #Add the new score
        query = "INSERT INTO S1893502.SCORE VALUES(:name, :score, 1)"
        c.execute(query,name=name,score=score)
        self.conn.commit()

        return json.dumps(result)



if __name__ == '__main__':
    Test_Class.get()
