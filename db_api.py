from flask import Flask, request
#from flask_restful import Rescource, Api
import cx_Oracle
import json
from flask import jsonify

app = Flask(__name__)

class Test_Class():
    def get():
        with open('./db/dbpwd.txt','r') as file:
            pwd = file.readline().replace('\n','')
        conn = cx_Oracle.connect(pwd)
        c = conn.cursor()
        query = c.execute("SELECT FIELD_ID, LOWX, LOWY, HIX, HIY FROM S1893502.PFIELDS")
        columns = [i[0] for i in query.description]
        result = [dict(zip(columns, row)) for row in query]
#        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return json.dumps(result)
    
#https://www.codementor.io/sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
#query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
#result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
#return jsonify(result)


if __name__ == '__main__':
    Test_Class.get() 
        
