#!/usr/bin/env python3

import sys
import json
import cgi
import cgitb

import innerScripts as iScr

cgitb.enable(format='text')

'''
Creates and retrieves Scores
'''

#Parse submitted parameters from jQuery
inp = cgi.FieldStorage()

#Write JSON header
sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")

#Calls inner_score.py instance which writes and retrieves the scores
#addHighScore also returns the current top 10
scoretable = aScr.inner_score(inp)
scoretable.addHSretrieveRank()

#Writes scoretable position to the jQuery response
sys.stdout.write(str(scoretable))
sys.stdout.write("\n")

#Close the jQuery connection
sys.stdout.close()
