#!/usr/bin/env python3
import cx_Oracle
import cgitb
import numpy as np
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from pandas import DataFrame as df
import random

class getData():
    
    def __init__(self,maxXinput = 0, maxYinput = 0):
        #Exactly one value of True must be passed into this function
        with open('./db/dbpwd.txt','r') as file:
            pwd = file.readline().replace('\n','')
        conn = cx_Oracle.connect(pwd)
        pwd = None
        self.c = conn.cursor()
        self.maxXinput, self.maxYinput, temp = getData.fields(self)
        temp = None
        self.maxX = maxXinput
        self.maxY = maxYinput

        self.rand_int = random.radint(1,1)

    def fields(self):
            if self.rand_int == 1:
                self.c.execute("SELECT FIELD_ID, LOWX, LOWY, HIX, HIY FROM PFIELDS")
            else:
                self.c.execute("SELECT FIELD_ID, LOWX, LOWY, HIX, HIY FROM PFIELDS2")

            list = []
            dict = {'FieldID':[],'LowX':[],'LowY':[],'HiX':[],'HiY':[], 'MaxCoordX':[],'MaxCoordY':[]}
            for row in self.c:
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
    
    def paths(self):
            self.c.execute("SELECT PATH_ID, STARTX, STARTY, ENDX, ENDY FROM PATHS")
            listpath = []
            dictpath = {'PathID':[],'StartX':[],'StartY':[],'EndX':[],'EndY':[], 'MaxCoordX':[],'MaxCoordY':[], 'Distance':[]}
            for row in self.c:
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
            maxX = self.maxXinput
            maxY = self.maxYinput
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
    
    #############################################################################
    ##############################################################################
    ###############################################################################
    
    def waypointcoords(self):
            self.c.execute('''
    SELECT POINT_ID, S_X, S_Y FROM PEND
    ''')
            listpoint = []
            dictpoint = {'PointID':[],'X':[],'Y':[]}
            for row in self.c:
                listpoint.append(row)
    
    #Appending
            for row in range(len(listpoint)):
                dictpoint['PointID'].append(listpoint[row][0])
                dictpoint['X'].append(listpoint[row][1])
                dictpoint['Y'].append(listpoint[row][2])
                
        #Relativating Coordinates
       
            maxX = self.maxXinput
            maxY = self.maxYinput
    
            for row in range(len(listpoint)):
                dictpoint['X'][row]= ((dictpoint['X'][row]/maxX))*100
                dictpoint['Y'][row]= (1-(dictpoint['Y'][row]/maxY))*100
    
            return dictpoint
    
    ############################################################################
    #############################################################################
    ##############################################################################
    
    def waypointrefs(self):
            self.c.execute('''
    SELECT C.PATH_ID, D.POINT_ID, E.POINT_ID
    FROM PATHS C, PEND D, PEND E
    WHERE SDO_TOUCH(C.GEOM, D.GEOM) = 'TRUE' AND SDO_TOUCH(C.GEOM, E.GEOM) = 'TRUE'
    AND D.POINT_ID < E.POINT_ID
    ORDER BY C.PATH_ID              
    ''')
            listpoint = []
            dictref = {'PathID':[],'PointID1':[],'PointID2':[]}
            for row in self.c:
                listpoint.append(row)
    
    #Appending
            for row in range(len(listpoint)):
                dictref['PathID'].append(listpoint[row][0])
                dictref['PointID1'].append(listpoint[row][1])
                dictref['PointID2'].append(listpoint[row][2])
            
            return dictref
            
            
    ##############################################################################
    #############################################################################
    ##############################################################################
    
    def score(self):
            self.c.execute('''SELECT A.PATH_ID, C.FIELD_ID, SDO_GEOM.SDO_LENGTH(SDO_GEOM.SDO_INTERSECTION(A.GEOM, C.GEOM, 0.005), M.DIMINFO) \
    AS "DISTANCE", C.GROUND_ID, D.SCORE_INFL AS "GROUNDMULTIPLIER", SDO_GEOM.SDO_LENGTH(SDO_GEOM.SDO_INTERSECTION(A.GEOM, C.GEOM, 0.005), M.DIMINFO)*D.SCORE_INFL AS "SCORE" \
    FROM PATHS A, PFIELDS C, USER_SDO_GEOM_METADATA M, GROUND D WHERE M.TABLE_NAME = 'PATHS' AND M.COLUMN_NAME = 'GEOM' AND SDO_GEOM.SDO_LENGTH(SDO_GEOM.SDO_INTERSECTION(A.GEOM, C.GEOM, 0.005), M.DIMINFO) > 0 AND C.GROUND_ID = D.GROUND_ID ORDER BY A.PATH_ID''')
    
            listscore = []
            dictscore = {'PathID':[],'FieldID':[],'Distance':[],'GroundID':[],'GroundMultiplier':[],'Score':[]}
            for row in self.c:
                listscore.append(row)
                
            for row in range(len(listscore)):
                dictscore['PathID'].append(listscore[row][0])
                dictscore['FieldID'].append(listscore[row][1])
                dictscore['Distance'].append(listscore[row][2])
                dictscore['GroundID'].append(listscore[row][3])
                dictscore['GroundMultiplier'].append(listscore[row][4])
                dictscore['Score'].append(listscore[row][5])
    
#           Insert here a new dict which joins the values of the scores together
            sumscore = {'PathID':[], 'Score':[]}
            sumscore['PathID'] = dictscore['PathID']
            sumscore['Score'] = dictscore['Score']
            dfscore = sumscore      
#            Add the influence of slopes to belonging lines
            slopes = getData.slopeadding(self)
            slopes['PathID'].pop(2)
            slopes['ScoreInfluence'].pop(2) 
            for i in range(len(dfscore)):
                for j in range(len(slopes)):
                    if slopes['PathID'][j] == dfscore['PathID'][i]:
                        dfscore['Score'][i] = dfscore['Score'][i] * slopes['ScoreInfluence'][i]

            dfscore = df(dfscore).groupby(['PathID']).sum().to_dict()['Score']
            
            return dfscore
    
    ##############################################################################
    #############################################################################
    ##############################################################################
    
    def grounds(self):
        self.c.execute('''
    SELECT * FROM GROUND      
    ''')
    
        listgrounds = []
        dictgrounds = {'GroundID':[],'Name':[],'GroundInfluence':[]}
        for row in self.c:
            listgrounds.append(row)

        for row in range(len(listgrounds)):
            dictgrounds['GroundID'].append(listgrounds[row][0])
            dictgrounds['Name'].append(listgrounds[row][1])
            dictgrounds['GroundInfluence'].append(listgrounds[row][2])
        
        self.c.execute('''
SELECT FIELD_ID, GROUND_ID FROM PFIELDS ORDER BY FIELD_ID ''')
        listgrounds = []
        dictgroundfields = {'FieldID':[],'GroundID':[]}
        for row in self.c:
            listgrounds.append(row)
        for row in range(len(listgrounds)):
            dictgroundfields['FieldID'].append(listgrounds[row][0])
            dictgroundfields['GroundID'].append(listgrounds[row][1])
                 
        return dictgrounds, dictgroundfields

##############################################################################
#############################################################################
##############################################################################

    ''' Slope Overlay Query'''
    def slopeadding(self):
        self.c.execute('''SELECT A.PATH_ID, C.SLOPE_ID, C.SCORE_INFL \
FROM PATHS A, SLOPES C, USER_SDO_GEOM_METADATA M \
WHERE M.TABLE_NAME = 'PATHS' AND M.COLUMN_NAME = 'GEOM' \
AND SDO_RELATE(A.GEOM, C.GEOM, 'mask=overlapbdydisjoint+inside') = 'TRUE' ORDER BY A.PATH_ID''')

        listslope = []
        dictslope = {'PathID':[], 'ScoreInfluence':[]}
        for row in self.c:
            listslope.append(row)

        for row in range(len(listslope)):
            dictslope['PathID'].append(listslope[row][0])
            dictslope['ScoreInfluence'].append(listslope[row][1])
         
        return dictslope

################################################################################
###############################################################################

def print_html():
    env = Environment(loader = FileSystemLoader('../'))
    temp = env.get_template('SVG.html')
    con = getData()
    maxXfields, maxYfields, fields = con.fields()
    paths = con.paths()
    points= con.waypointcoords()
    pointref = con.waypointrefs()
    scoredic = con.score()
    grounds, groundfields = con.grounds()
  

    print('''Content-Type: text/html\n\n\
<!DOCTYPE html>\n\
<head>\n\
<title> Turnipator the Game </title>\n\
<link href="../styling.css" rel="stylesheet" type="text/css" >\n\
<link href="../turnip_popup.css" rel="stylesheet" type="text/css" >\n\
<style type="text/css" media="screen">\n''')

    '''Dynamic InLine CSS'''
#   Add CSS above
    colorramp = ["443f3b","135111","77e874"]
    
    for row in range(len(groundfields['FieldID'])):
        if groundfields['GroundID'][row] == 1:
            i = 0
        elif groundfields['GroundID'][row] == 2:
            i = 1
        elif groundfields['GroundID'][row] == 3:
            i = 2
        print('''#r'''+str(row)+''' {
fill: #'''+str(colorramp[i])+''';}\n''')

    print('''</style>\n<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>\n\
</head>\n<body>''')


    print('''
<div class = "colum left"><svg viewBox="-5 -4 110 110" xmlns="http://www.w3.org/2000/svg" class = "svg">\n\
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

    for row in range(len(points['PointID'])):

        print('''\n\
<circle cx="'''+str(points['X'][row])+'''" \
cy="'''+str(points['Y'][row])+'''" r="1.5" stroke="black" \
stroke-width="0.5" fill="red" id="waypoint'''+str(row + 1)+'''" class="waypoint" />\n\
''')

    print('''</g>''')
    
    '''The golden Turnip'''
    print(''' <div id="popup_default" class="popup">
  <div class="popup-overlay"></div>
  <div class="popup-content">
    <a href="#" class="close-popup" data-id="popup_default">&times;</a>
    <h1>Popup 1</h1>
    <img src="../the-golden-turnip.svg"></img>
  </div>
</div>
''')
    
    
    
    print('''</svg></div><div class= "column right">''')
    
    print('''\n\
<script>
//insert Event Listener for Classes \n\
//if Statements in this function \n\

    var totalScore = 100;\n''')
          
    for row in range(len(scoredic)):
        index = row+1
        print('''var scoreLine'''+str(index)+'''= '''+str(-1*(scoredic[index]))+'''\n''')
      

    print('''
     
      var fromCounter = "waypoint16";
      var toCounter = null;
      $("#waypoint16").attr({"r" : "3"});
      $("#waypoint16").attr({"class" : "waypoint waypointpulse"});
      $("circle.waypoint").click(clickCounter);
     
     
        // jQuery extend functions for popup
        
    (function($) {
      $.fn.openPopup = function( settings ) {
        var elem = $(this);
        // Establish our default settings
        var settings = $.extend({
          anim: 'fade'
        }, settings);
        elem.show();
        elem.find('.popup-content').addClass(settings.anim+'In');
      }
      
      $.fn.closePopup = function( settings ) {
        var elem = $(this);
        // Establish our default settings
        var settings = $.extend({
          anim: 'fade'
        }, settings);
        elem.find('.popup-content').removeClass(settings.anim+'In').addClass(settings.anim+'Out');
        
        setTimeout(function(){
            elem.hide();
            elem.find('.popup-content').removeClass(settings.anim+'Out')
          }, 500);
      }
        
    }(jQuery));
    
    // Click functions for popup
    function openPopup(){
      $('#'+$(this).data('id')).openPopup({
        anim: (!$(this).attr('data-animation') || $(this).data('animation') == null) ? 'fade' : $(this).data('animation')
      });
    };
    $('.close-popup').click(function(){
      $('#'+$(this).data('id')).closePopup({
        anim: (!$(this).attr('data-animation') || $(this).data('animation') == null) ? 'fade' : $(this).data('animation')
      });
    });
    
    
    // Counter Function
    
      function clickCounter() {
        
        $('#'+fromCounter).attr({"class" : "waypoint", "r" : "1.5"});           
        if(((this.id == "waypoint2")||(this.id == "waypoint4")||(this.id == "waypoint16")) && (fromCounter == "waypoint1")){
        //PointID2 20 - last one
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            
            if((toCounter == "waypoint2")){
            totalScore = totalScore + scoreLine2;
            }
            if((toCounter == "waypoint4")){
            totalScore = totalScore + scoreLine4;
            }
            if((toCounter == "waypoint16")){
            totalScore = totalScore + scoreLine1;
            }
            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint5")||(this.id == "waypoint1")) && (fromCounter == "waypoint2")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint5")){
            totalScore = totalScore + scoreLine5;
            }
            if((toCounter == "waypoint1")){
            totalScore = totalScore + scoreLine2;
            }
            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint6")||(this.id == "waypoint7")||(this.id == "waypoint16")) && (fromCounter == "waypoint3")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint6")){
            totalScore = totalScore + scoreLine5;
            }
            if((toCounter == "waypoint7")){
            totalScore = totalScore + scoreLine2;
            }
            if((toCounter == "waypoint16")){
            totalScore = totalScore + scoreLine2;
            }
            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint7")||(this.id == "waypoint11")||(this.id == "waypoint1")) && (fromCounter == "waypoint4")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint7")){
            totalScore = totalScore + scoreLine8;
            }
            if((toCounter == "waypoint11")){
            totalScore = totalScore + scoreLine13;
            }
            if((toCounter == "waypoint1")){
            totalScore = totalScore + scoreLine4;
            }
            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint13")||(this.id == "waypoint2")) && (fromCounter == "waypoint5")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint13")){
            totalScore = totalScore + scoreLine18;
            }
            if((toCounter == "waypoint2")){
            totalScore = totalScore + scoreLine5;
            }

            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint8")||(this.id == "waypoint3")) && (fromCounter == "waypoint6")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint8")){
            totalScore = totalScore + scoreLine9;
            }
            if((toCounter == "waypoint3")){
            totalScore = totalScore + scoreLine6;
            }

            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint9")||(this.id == "waypoint3")||(this.id == "waypoint4")) && (fromCounter == "waypoint7")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint9")){
            totalScore = totalScore + scoreLine10;
            }
            if((toCounter == "waypoint3")){
            totalScore = totalScore + scoreLine7;
            }
            if((toCounter == "waypoint4")){
            totalScore = totalScore + scoreLine8;
            }
            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint12")||(this.id == "waypoint6")) && (fromCounter == "waypoint8")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint12")){
            totalScore = totalScore + scoreLine14;
            }
            if((toCounter == "waypoint6")){
            totalScore = totalScore + scoreLine9;
            }
            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint7")||(this.id == "waypoint15")) && (fromCounter == "waypoint9")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint7")){
            totalScore = totalScore + scoreLine10;
            }
            if((toCounter == "waypoint15")){
            totalScore = totalScore + scoreLine11;
            }
            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint12")||(this.id == "waypoint15")||(this.id == "waypoint14")) && (fromCounter == "waypoint10")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint12")){
            totalScore = totalScore + scoreLine15;
            }
            if((toCounter == "waypoint15")){
            totalScore = totalScore + scoreLine12;
            }
            if((toCounter == "waypoint14")){
            totalScore = totalScore + scoreLine16;
            $('#waypoint14').click(openPopup()); 
            }
            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint13")||(this.id == "waypoint4")) && (fromCounter == "waypoint11")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint13")){
            totalScore = totalScore + scoreLine17;
            }
            if((toCounter == "waypoint4")){
            totalScore = totalScore + scoreLine13;
            }
            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint8")||(this.id == "waypoint10")) && (fromCounter == "waypoint12")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint8")){
            totalScore = totalScore + scoreLine14;
            }
            if((toCounter == "waypoint10")){
            totalScore = totalScore + scoreLine15;
            }
            fromCounter = this.id;
            alert(totalScore);       
        } 
        if(((this.id == "waypoint14")||(this.id == "waypoint11")||(this.id == "waypoint5")) && (fromCounter == "waypoint13")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint14")){
            totalScore = totalScore + scoreLine19;
            $('#waypoint14').click(openPopup()); 
            }
            if((toCounter == "waypoint11")){
            totalScore = totalScore + scoreLine13;
            }
            if((toCounter == "waypoint5")){
            totalScore = totalScore + scoreLine18;
            }
            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint10")||(this.id == "waypoint13")) && (fromCounter == "waypoint14")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint10")){
            totalScore = totalScore + scoreLine16;
            }
            if((toCounter == "waypoint17")){
            totalScore = totalScore + scoreLine19;
            }
            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint10")||(this.id == "waypoint9")) && (fromCounter == "waypoint15")){
           
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint10")){
            totalScore = totalScore + scoreLine12;
            }
            if((toCounter == "waypoint9")){
            totalScore = totalScore + scoreLine11;
            }
            fromCounter = this.id;
            alert(totalScore);       
        }
        if(((this.id == "waypoint1")||(this.id == "waypoint3")) && (fromCounter == "waypoint16")){  
        
            toCounter = this.id;
            $(this).attr({"r" : "3"});
            $(this).attr({"class" : "waypoint waypointpulse"});
            if((toCounter == "waypoint1")){
            totalScore = totalScore + scoreLine1;
            }
            if((toCounter == "waypoint3")){
            totalScore = totalScore + scoreLine3;
            }
            fromCounter = this.id;
            alert(totalScore);
        }     
      }

      
</script></body>\n</html>''')

    # print('''function loadDoc() {\n\
    # var xhttp = new XMLHttpRequest();\n\
    # xhttp.onreadystatechange = function() {\n\
    # if (this.readyState == 4 && this.status == 200) {\n\
    #  document.getElementById("demo").innerHTML = this.responseText;\n\
    # }\
    # };\
    #
    # xhttp.open("GET", "ajax_info.txt", true);\
    # xhttp.send();}</script></body>\n</html>''')




    print(temp.render())

#run
if __name__ == '__main__':
    print_html()
