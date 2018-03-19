import re
from datetime import datetime
from dateutil.parser import parse

p1 = 0
p2 = 0
p3 = 0
v = 0
i = 0

match = 0

p1time = 0
p2time = 0
p3time = 0

prescp_p1 = 3
prescp_p2 = 3
prescp_p3 = 3

def readpilltiming():
    global p1,p2,p3,v,i,match,p1time,p2time,p3time
    with open('datatime.txt', 'r') as f:
        
        while True:
            if(i==3):
                i = 0
            if(i<3):
                v = f.readline()
                if not v: break

                if("lm : " in v):
                    match = parse(v, fuzzy=True)
                    p1time = str(match.hour)+':'+str(match.minute)+':'+str(match.second)


                elif("mm : " in v):
                    match = parse(v, fuzzy=True)
                    p2time = str(match.hour)+':'+str(match.minute)+':'+str(match.second)
                 
                elif("rm : " in v):
                    match = parse(v, fuzzy=True)
                    p2time = str(match.hour)+':'+str(match.minute)+':'+str(match.second)
                    
                
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

                if("lm : " in v):
                    [int(s) for s in v.split() if s.isdigit()]
                    p1 = int(s)

                elif("mm : " in v):
                    [int(s) for s in v.split() if s.isdigit()]
                    p2 = int(s)

                elif("rm : " in v):
                    [int(s) for s in v.split() if s.isdigit()]
                    p3 = int(s)
    
def pilltiming():
    readpilltiming()
    global p1time,p2time,p3time
    print('you had pill 1 at {} , pill 2 at {} and pill 3 at {}'.format(p1time,p2time,p3time))

pilltiming()
