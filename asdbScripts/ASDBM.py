#!/usr/bin/env python3
import cx_Oracle
import cgitb
import numpy as np
from jinja2 import Environment, FileSystemLoader

#Connection
def dataHtml(fields = True, paths = False, maxXinput = 0, maxYinput = 0):
    #Exactly one value of True must be passed into this function
    with open('./db/dbpwd.txt','r') as file:
        pwd = file.readline().replace('\n','')
    conn = cx_Oracle.connect(pwd)
    c = conn.cursor()
    if fields == True:
        c.execute("SELECT FIELD_ID, LOWX, LOWY, HIX, HIY FROM S1893502.PFIELDS")
        list = []
        dict = {'FieldID':[],'LowX':[],'LowY':[],'HiX':[],'HiY':[], 'MaxCoordX':[],'MaxCoordY':[]}
        replace = ['Owner','Crop']
        for row in c:
            list.append(row)

#Appending
        for row in range(len(list)):
            dict['FieldID'].append(list[row][0])
            dict['LowX'].append(list[row][1])
            dict['LowY'].append(list[row][2])
            dict['HiX'].append(list[row][3])
            dict['HiY'].append(list[row][4])

    #Relativating Coordinates
        maxX = max(dict['HiX'])
        maxY = max(dict['HiY'])

        dict['MaxCoordX'].append(maxX)
        maximumX = maxX
        dict['MaxCoordY'].append(maxY)
        maximumY = maxY

        for row in range(len(list)):
            dict['LowX'][row]= ((dict['LowX'][row]/maximumX))*100
            dict['LowY'][row]= (1-(dict['LowY'][row]/maximumY))*100
            dict['HiX'][row]= ((dict['HiX'][row]/maximumX))*100
            dict['HiY'][row]= (1-(dict['HiY'][row]/maximumY))*100

        return maxX, maxY, dict


###################################################################################################################################
#################################################################################################################################
###############################################################################################################################

    if paths == True:
        c.execute("SELECT PATH_ID, STARTX, STARTY, ENDX, ENDY FROM S1893502.PATHS")
        listpath = []
        dictpath = {'PathID':[],'StartX':[],'StartY':[],'EndX':[],'EndY':[], 'MaxCoordX':[],'MaxCoordY':[], 'Distance':[]}
        for row in c:
            listpath.append(row)

#Appending
        for row in range(len(listpath)):
            dictpath['PathID'].append(listpath[row][0])
            dictpath['StartX'].append(listpath[row][1])
            dictpath['StartY'].append(listpath[row][2])
            dictpath['EndX'].append(listpath[row][3])
            dictpath['EndY'].append(listpath[row][4])

    #Relativating Coordinates
    #This could be a big problem with the maximum and relativeness
        maxX = maxXinput
        maxY = maxYinput
    #This could be a big problem with the maximum and relativeness
        dictpath['MaxCoordX'].append(maxX)
        maximumX = maxX
        dictpath['MaxCoordY'].append(maxY)
        maximumY = maxY

        for row in range(len(listpath)):
            dictpath['StartX'][row]= ((dictpath['StartX'][row]/maximumX))*100
            dictpath['StartY'][row]= (1-(dictpath['StartY'][row]/maximumY))*100
            dictpath['EndX'][row]= ((dictpath['EndX'][row]/maximumX))*100
            dictpath['EndY'][row]= (1-(dictpath['EndY'][row]/maximumY))*100

        return dictpath


#####
def dataHtmlsq(pathsSQ = True):
    #Exactly one value of True must be passed into this function
    with open('./db/dbpwd.txt','r') as file:
        pwd = file.readline().replace('\n','')
    conn = cx_Oracle.connect(pwd)
    c = conn.cursor()

    if pathssq == True:
        c.execute("SELECT FIELD_ID, LOWX, LOWY, HIX, HIY FROM S1893502.PFIELDS")
        listsq = []
        dictsq = {'FieldID':[],'PathID':[],'Distance':[],'GroundID':[],'Groundmultiplier':[],'Score':[]}
        for row in c:
            listsq.append(row)

#Appending
        for row in range(len(listsq)):
            dictsq['FieldID'].append(listsq[row][0])
            dictsq['PathID'].append(listsq[row][1])
            dictsq['Distance'].append(listsq[row][2])
            dictsq['GroundID'].append(listsq[row][3])
            dictsq['Groundmultiplier'].append(listsq[row][4])
            dictsq['Score'].append(listsq[row][5])



    return dictsq
#####

########################################

def print_html():
    env = Environment(loader = FileSystemLoader('../'))
    temp = env.get_template('SVG.html')
    maxXfields, maxYfields, fields = dataHtml(fields = True, paths = False)
    paths = dataHtml(fields = False, paths = True, maxXinput = maxXfields, maxYinput = maxYfields)


    print('''Content-Type: text/html\n\n\
<!DOCTYPE html>\n\
<head>\n\
<title>Devour The Turnip </title>\n\
<link href="../styling.css" rel="stylesheet" type="text/css" >\n\
<style type="text/css" media="screen">\n''')

    '''Dynamic InLine CSS'''
#   Add CSS above
    colorramp = ["F0F8FF","FAEBD7","00FFFF","7FFFD4","F0FFFF","F5F5DC","FFE4C4",
                 0,"FFEBCD","0000FF","8A2BE2","A52A2A","DEB887","5F9EA0",
                 "7FFF00","D2691E","FF7F50","6495ED","FFF8DC","DC143C",
                 "00FFFF","00008B","008B8B","B8860B","A9A9A9","A9A9A9",
                 6400,"BDB76B","8B008B","556B2F","FF8C00","9932CC","8B0000",
                 "E9967A","8FBC8F","483D8B","2F4F4F","2F4F4F","00CED1",
                 "9400D3","FF1493","00BFFF",696969,696969,"1E90FF",
                 "B22222","FFFAF0","228B22","FF00FF","DCDCDC","F8F8FF",
                 "FFD700","DAA520",808080,808080,8000,"ADFF2F","F0FFF0",
                 "FF69B4","CD5C5C","4B0082","FFFFF0","F0E68C","E6E6FA",
                 "FFF0F5","7CFC00","FFFACD","ADD8E6","F08080","E0FFFF",
                 "FAFAD2","D3D3D3","D3D3D3","90EE90","FFB6C1","FFA07A",
                 "20B2AA","87CEFA",778899,778899,"B0C4DE","FFFFE0","00FF00",
                 "32CD32","FAF0E6","FF00FF",800000,"66CDAA","0000CD","BA55D3",
                 "9370DB","3CB371","7B68EE","00FA9A","48D1CC","C71585",191970,
                 "F5FFFA","FFE4E1","FFE4B5","FFDEAD",80,"FDF5E6",808000,
                 "6B8E23","FFA500","FF4500","DA70D6","EEE8AA","98FB98",
                 "AFEEEE","DB7093","FFEFD5","FFDAB9","CD853F","FFC0CB",
                 "DDA0DD","B0E0E6",800080,663399,"FF0000","BC8F8F",41690,
                 "8B4513","FA8072","F4A460","2E8B57","FFF5EE","A0522D",
                 "C0C0C0","87CEEB","6A5ACD",708090,708090,"FFFAFA","00FF7F",
                 "4682B4","D2B48C",8080,"D8BFD8","FF6347","40E0D0","EE82EE",
                 "F5DEB3","FFFFFF","F5F5F5","FFFF00","9ACD32"]

    for row in range(len(fields['FieldID'])):
        print('''#r'''+str(row)+''' {
fill: #'''+str(colorramp[row+np.random.randint(low = 0, high = 50)])+''';}\n''')


    print('''</style>\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n\
<script src="../counter.js"></script>\n\
<script src="jQuery.js"></script>\n\
</head>\n<body>''')


    print('''<svg viewBox="-5 -4 110 110" >\n\
<g class="grid">''')

    '''Grid Labelling'''
    '''Static Values for neat positioning'''
    '''Y Axis Inverted'''

    i = -1
    j = -1

    while True:
        i = i + 1
        xticks = float((i/fields['MaxCoordX'][0])*100)
        print('''<text font-size="2" x="'''+str(xticks -0.5)+'''" y="103">'''+str(i)+'''</text>''')
        if i == fields['MaxCoordX'][0]:
            break


    while True:
        j = j + 1
        yticks = float((j/fields['MaxCoordY'][0])*100)
        print('''<text font-size="2" x="-3" y="'''+str(yticks +0.5)+'''" >'''+str(-1*(j-fields['MaxCoordY'][0]))+'''</text>''')
        if j == fields['MaxCoordY'][0]:
            break

    '''Grid Computing'''
    i = 0
    j = 0

    while True:
        i = i + 1
        xticks = str(float((i/fields['MaxCoordX'][0])*100))
        print('''<line x1='''+xticks+''' y1=0 x2='''+xticks+''' y2=100 class = "line" /> ''')
        if i == fields['MaxCoordX'][0] - 1:
            break

    while True:
        j = j + 1
        yticks = str(float((j/fields['MaxCoordY'][0])*100))
        print('''<line x1=0 y1='''+yticks+''' x2=100 y2='''+yticks+''' class = "line"/> ''')
        if j == fields['MaxCoordY'][0] - 1:
            break

    print('''</g>''')

    '''Path Computing'''
    print('''<g class="paths">''')
    i = -1

    while True:
        i = i + 1
        xstartticks = str(float(paths['StartX'][i]))
        ystartticks = str(float(paths['StartY'][i]))
        xendticks = str(float(paths['EndX'][i]))
        yendticks = str(float(paths['EndY'][i]))
        print('''<line x1='''+xstartticks+''' y1='''+ystartticks+''' x2='''+xendticks+''' y2='''+yendticks+''' /> ''')
        if i == len(paths['PathID']) - 1:
            break

    print('''</g>''')

    '''Rectangle Computing'''

    print('''<g class="rectangles">''')
    for row in range(len(fields['FieldID'])):

        lowX = fields['LowX'][row]
        lowY = fields['LowY'][row]
        highX = fields['HiX'][row]
        highY = fields['HiY'][row]

        idX = (highX-((highX-lowX)/2))-2.5
        idY = (highY-((highY-lowY)/2))-2.5
        idW = 5
        idH = 5
        idTX = idX +1.8
        idTY = idY +3.5

        print('''<rect x="'''+str(idX)+'''" y="'''+str(idY)+'''" width="'''+str(idW)+'''" height="'''+str(idH)+'''" class="field_ids" />''')
        print('''<text x="'''+str(idTX)+'''" y="'''+str(idTY)+'''" class="field_id_text">'''+str(fields['FieldID'][row])+'''</text>''' )

        print ('''\n<polygon points="'''+str(lowX)+''' '''+str(lowY)+''', '''+str(highX)+''' '''+str(lowY)+''', \
'''+str(highX)+''' '''+str(highY)+''', '''+str(lowX)+''' '''+str(highY)+'''" class="fields" id="r'''+str(row)+'''" />''')
    print('''</g>\n''')

    '''Waypoint Computing'''
    print('''<g class="Waypoints">''')
    print('''<circle cx="'''+str(paths['EndX'][1])+'''" cy="'''+str(paths['EndY'][1])+'''" r="3" stroke="black" stroke-width="1" fill="red" id="counter_test" />''')
    print('''</g>''')

    # print('''<g class = "AJAX"><text id="demo" class="field_id_text x="'''+str((14/16)*100)+'''" y="'''+str((1/16)*100)+'''" onclick="loadDoc()">Test</text></g>\n''')

    print('''<text id="demo" x="'''+str((14/16)*100)+'''" y="'''+str((1/16)*100)+'''" class="field_id_text" onclick="loadDoc()">Test</text>''' )

    print('''</svg>''')

    print('''<script>\n\
//insert Event Listener for Classes
//if Statements in this function

      var totalScore = 100; \n\
      var scoreLine0 = -15; \n\
      var scoreLine1 = -20; \n\
      var scoreLine2 = -30; \n\

      var pointReference0 = scoreLine0,scoreLine1; \n\
      var pointReference1 = scoreLine1,scoreLine2; \n\
      var pointReference2 = scoreLine1,scoreLine3; \n\

      var fromCounter = pointReference0; \n\
      var toCounter = null; \n\

      function clickCounter () { \n\
        // set onlick the clicked pointReference as \n\
        // toCounter if the point is connected \n\
        // by a line from the fromCounter \n\
      } \n\

      if (fromCounter == pointReference0 && toCounter == pointReference1) \n\
        totalScore = totalScore + scoreLine0 + scoreLine1; \n\
        return totalScore \n\

    }); \n\
</script>''')

    print('''<script>function loadDoc() {\n\
  var xhttp = new XMLHttpRequest();\n\
  xhttp.onreadystatechange = function() {\n\
    if (this.readyState == 4 && this.status == 200) {\n\
     document.getElementById("demo").innerHTML = this.responseText;\n\
    }\
  };\
  xhttp.open("GET", "ajax_info.txt", true);\
  xhttp.send();}</script></body>\n</html>''')




    print(temp.render())

#run
if __name__ == '__main__':
    print_html()
