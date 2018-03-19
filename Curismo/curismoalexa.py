"""

Curismo : A Smart Pill Box Assistant
Developer : Geeve George
External Libraries used : Flask-Ask

"""

import logging
from random import randint
from flask import Flask, render_template #library for building skills using python
from flask_ask import Ask, statement, question, session

from dateutil.parser import parse #parse time corresponding to pill intake logged into datatime.txt file by walabot
import re
from datetime import datetime


p1 = 0
p2 = 0
p3 = 0
v = 0
i =0

match = 0
p1time = 0
p2time = 0
p3time = 0

prescp_p1 = 3
prescp_p2 = 3
prescp_p3 = 3


def readpilltiming():
    global p1,p2,p3,v,i,match,p1time,p2time,p3time
    with open('datatime.txt', 'r') as f: #read file that contains information logged by walabot
        
        while True:
            if(i==3):
                i = 0
            if(i<3):
                v = f.readline() #extract time substring from each line
                if not v: break

                if("lm : " in v):
                    match = parse(v, fuzzy=True)
                    p1time = datetime.strptime(str(match.hour)+':'+str(match.minute), '%H:%M').strftime("%I:%M %p") #convert to 24 hour to 12 hour format


                elif("mm : " in v):
                    match = parse(v, fuzzy=True)
                    p2time = datetime.strptime(str(match.hour)+':'+str(match.minute), '%H:%M').strftime("%I:%M %p")
                 
                elif("rm : " in v):
                    match = parse(v, fuzzy=True)
                    p3time = datetime.strptime(str(match.hour)+':'+str(match.minute), '%H:%M').strftime("%I:%M %p")
                    
                
    f.close()            

def readnupdate():
    global p1,p2,p3,v,i
    with open('data.txt', 'r') as f:
        
        while True:
            if(i==3):
                i = 0
            if(i<3):
                v = f.readline()
                if not v: break

                if("lm : " in v): #extract pill intake count 
                    [int(s) for s in v.split() if s.isdigit()]
                    p1 = int(s)

                elif("mm : " in v):
                    [int(s) for s in v.split() if s.isdigit()]
                    p2 = int(s)

                elif("rm : " in v):
                    [int(s) for s in v.split() if s.isdigit()]
                    p3 = int(s)
                
    f.close()            

    
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def starting():
    readnupdate()
    welcome = render_template('welcome')
    return statement(welcome)

@ask.intent("AllPillIntent")
def allpill():
    readnupdate()
    global p1,p2,p3
    return statement('as of now, you have had {} pill 1, {} pill 2 and {} pill 3'.format(p1,p2,p3))

@ask.intent("DailyPrescpIntent")
def dailypres():
    readnupdate()
    return statement('As per your prescription, you need to have {} pill 1 with food, {} pill 2 and {} pill 3 without daily. As of now you have had {} pill 1, {} pill 2 and {} pill 3'.format(prescp_p1,prescp_p2,prescp_p3,p1,p2,p3))
    
@ask.intent("PillNotTakenIntent")
def pillnothad():
    readnupdate()
    global p1,p2,p3
    if(p1==0 and p2==0 and p3==0):
        return statement('you have not had any pills today')
    elif(p1==0 and p2==0 and p3!=0):
        return statement('you have not had pill 1 and pill 2')
    elif(p1==0 and p2!=0 and p3==0):
        return statement('you have not had pill 1 and pill 3')
    elif(p1!=0 and p2==0 and p3==0):
        return statement('you have not had pill 2 and pill 3')
    elif(p1==0 and p2!=0 and p3!=0):
        return statement('you have not had pill 1 today')
    elif(p1!=0 and p2==0 and p3!=0):
        return statement('you have not had pill 2 today')
    elif(p1!=0 and p2!=0 and p3==0):
        return statement('you have not had pill 3 today')
    else:
        return statement('you have atleast had one of each pill today')
    
@ask.intent("PillTimeIntent")
def pilltiming():
    readpilltiming()
    global p1time,p2time,p3time
    return statement('you had pill 1 at {} , pill 2 at {} and pill 3 at {}'.format(p1time,p2time,p3time))

@ask.intent("PillRemainingIntent")
def pillremaining():
    readnupdate()
    global prescp_p1,prescp_p2,prescp_p3
    r1 = prescp_p1 - p1
    r2 = prescp_p1 - p2
    r3 = prescp_p1 - p3

    return statement('you have {} pill 1, {} pill 2 and {} pill 3 left to be taken today'.format(r1,r2,r3))
    
if __name__ == '__main__':
    app.run(debug=True)
