from flask import Flask, render_template, request,Markup
import psycopg2
import os
from datetime import *
import json

username = os.environ['USER']
password = os.environ['PASS']
database = os.environ['DB']
hostname = os.environ['HOST']
thresholdWaterLevel = int(os.environ['threshold_manhole_water_level'])
tf = int(os.environ['threshold_flourine'])
ta = int(os.environ['threshold_arsenic'])
ti = int(os.environ['threshold_iron'])
tn = int(os.environ['threshold_nitrate'])

with open('data_out.txt') as f:
  data = json.load(f)
  
# Simple routine to run a query on a database and print the results:

def doQuery1( conn ) :
    main=0
    tot=0
    down=0
    allval=[]
    cur = conn.cursor()
    cur.execute( "SELECT * FROM maintainance;" )
    for sensor_node, last_date,status in cur.fetchall() :
        tot+=1
        l=[sensor_node,last_date,status]
        allval.append(l)
        if last_date > datetime.now():
            main+=1
        if status != 'up':
            down+=1
    return allval,tot,(tot-main),main,down

def doQuery2( conn ) :
    f=0
    a=0
    i=0
    n=0
    pollutant=[]
    cur = conn.cursor()
    cur.execute( "SELECT * FROM threshold;" )
    for sensor_node,pin, Flouride,Arsenic,Iron,Nitrate in cur.fetchall() :
        l=[sensor_node,pin,Flouride,Arsenic,Iron,Nitrate]
        pollutant.append(l)
        if Flouride>tf :
            f+=1
        if Arsenic>ta :
            a+=1
        if Iron>ti :
            i+=1
        if Nitrate>tn :
            n+=1
    return pollutant,f,a,i,n
            
def doQuery( conn ) :
    keys=[]
    overflow=0
    count=0
    almost=0
    cur = conn.cursor()
    cur.execute( "SELECT * FROM level;" )
    for sensor_node,pin, waterlevel in cur.fetchall() :
        count+=1
        l=[sensor_node,pin, waterlevel]
        keys.append(l)
        if waterlevel>thresholdWaterLevel :
            overflow+=1
        if waterlevel>thresholdWaterLevel-2:
            almost+=1    
    ok=count-overflow       
    return keys,overflow,count,ok,(almost-overflow)

app = Flask(__name__)
@app.route('/chamber')
def index():
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    keys,overflow,count,ok,almost=doQuery( myConnection)
    myConnection.close()
    return render_template('chamber.html',output=keys,overflow=overflow,count=count,ok=ok,almost=almost)
    
@app.route('/pollutants')
def maintainance():
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    main,f,a,i,n=doQuery2( myConnection)
    myConnection.close()
    return render_template('pollutants.html',main=main,f=f,a=a,i=i,n=n)
    
@app.route('/maintain')
def maintain():
    myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)
    main,tot,ok,notok,down=doQuery1( myConnection)
    myConnection.close()
    return render_template('maintain.html',main=main,tot=tot,ok=ok,notok=notok,down=down)    

@app.route('/allindia')
def allindia():
    return render_template('allindia.html')     

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')        
    
@app.route('/analytics/karnataka')
def karnataka():
    return render_template('state.html', title='Pollutant Trends',max=max(data['KARNATAKA'][1])+1000,labels=data['KARNATAKA'][0], values=data['KARNATAKA'][1])
    
@app.route('/analytics/ap')
def ap():
    return render_template('state.html', title='Pollutant Trends',max=max(data['ANDHRA PRADESH'][1])+1000,labels=data['ANDHRA PRADESH'][0], values=data['ANDHRA PRADESH'][1])

@app.route('/analytics/assam')
def assam():
    return render_template('state.html', title='Pollutant Trends',max=max(data['ASSAM'][1])+1000,labels=data['ASSAM'][0], values=data['ASSAM'][1])

@app.route('/analytics/arp')
def arp():
    return render_template('state.html', title='Pollutant Trends',max=max(data['ARUNACHAL PRADESH'][1])+1000,labels=data['ARUNACHAL PRADESH'][0], values=data['ARUNACHAL PRADESH'][1])

@app.route('/analytics/bihar')
def bihar():
    return render_template('state.html', title='Pollutant Trends',max=max(data['BIHAR'][1])+1000,labels=data['BIHAR'][0], values=data['BIHAR'][1])

@app.route('/analytics/hp')
def hp():
    return render_template('state.html', title='Pollutant Trends',max=max(data['HIMACHAL PRADESH'][1])+1000,labels=data['HIMACHAL PRADESH'][0], values=data['HIMACHAL PRADESH'][1])

@app.route('/analytics/gj')
def gj():
    return render_template('state.html', title='Pollutant Trends',max=max(data['GUJARAT'][1])+1000,labels=data['GUJARAT'][0], values=data['GUJARAT'][1])

@app.route('/analytics/hr')
def hr():
    return render_template('state.html', title='Pollutant Trends',max=max(data['HARYANA'][1])+1000,labels=data['HARYANA'][0], values=data['HARYANA'][1])

@app.route('/analytics/jk')
def jk():
    return render_template('state.html', title='Pollutant Trends',max=max(data['JAMMU AND KASHMIR'][1])+100,labels=data['JAMMU AND KASHMIR'][0], values=data['JAMMU AND KASHMIR'][1])

@app.route('/analytics/kl')
def kl():
    return render_template('state.html', title='Pollutant Trends',max=max(data['KERALA'][1])+1000,labels=data['KERALA'][0], values=data['KERALA'][1])

@app.route('/analytics/mp')
def mp():
    return render_template('state.html', title='Pollutant Trends',max=max(data['MADHYA PRADESH'][1])+1000,labels=data['MADHYA PRADESH'][0], values=data['MADHYA PRADESH'][1])

@app.route('/analytics/mh')
def mh():
    return render_template('state.html', title='Pollutant Trends',max=max(data['MAHARASHTRA'][1])+1000,labels=data['MAHARASHTRA'][0], values=data['MAHARASHTRA'][1])

@app.route('/analytics/mg')
def mg():
    return render_template('state.html', title='Pollutant Trends',max=max(data['MEGHALAYA'][1])+1000,labels=data['MEGHALAYA'][0], values=data['MEGHALAYA'][1])

@app.route('/analytics/nl')
def nl():
    return render_template('state.html', title='Pollutant Trends',max=max(data['NAGALAND'][1])+1000,labels=data['NAGALAND'][0], values=data['NAGALAND'][1])

@app.route('/analytics/rj')
def rj():
    return render_template('state.html', title='Pollutant Trends',max=max(data['RAJASTHAN'][1])+1000,labels=data['RAJASTHAN'][0], values=data['RAJASTHAN'][1])    
    
@app.route('/analytics/ori')
def ori():
    return render_template('state.html', title='Pollutant Trends',max=max(data['ORISSA'][1])+1000,labels=data['ORISSA'][0], values=data['ORISSA'][1])    
@app.route('/analytics/pd')
def pd():
    return render_template('state.html', title='Pollutant Trends',max=max(data['PUDUCHERRY'][1])+50,labels=data['PUDUCHERRY'][0], values=data['PUDUCHERRY'][1])    
@app.route('/analytics/pj')
def pj():
    return render_template('state.html', title='Pollutant Trends',max=max(data['PUNJAB'][1])+1000,labels=data['PUNJAB'][0], values=data['PUNJAB'][1])    
@app.route('/analytics/tp')
def tp():
    return render_template('state.html', title='Pollutant Trends',max=max(data['TRIPURA'][1])+1000,labels=data['TRIPURA'][0], values=data['TRIPURA'][1])    
@app.route('/analytics/up')
def up():
    return render_template('state.html', title='Pollutant Trends',max=max(data['UTTAR PRADESH'][1])+1000,labels=data['UTTAR PRADESH'][0], values=data['UTTAR PRADESH'][1])        
@app.route('/analytics/wb')
def wb():
    return render_template('state.html', title='Pollutant Trends',max=max(data['WEST BENGAL'][1])+1000,labels=data['WEST BENGAL'][0], values=data['WEST BENGAL'][1])        
@app.route('/analytics/ch')
def ch():
    return render_template('state.html', title='Pollutant Trends',max=max(data['CHATTISGARH'][1])+1000,labels=data['CHATTISGARH'][0], values=data['CHATTISGARH'][1])    
@app.route('/analytics/jh')    
def jh():
    return render_template('state.html', title='Pollutant Trends',max=max(data['JHARKHAND'][1])+1000,labels=data['JHARKHAND'][0], values=data['JHARKHAND'][1])    
@app.route('/analytics/uk')    
def uk():

    return render_template('state.html', title='Pollutant Trends',max=max(data['UTTARAKHAND'][1])+1000,labels=data['UTTARAKHAND'][0], values=data['UTTARAKHAND'][1])    
@app.route('/analytics/manipur')    
def manipur():
    return render_template('state.html', title='Pollutant Trends',max=max(data['MANIPUR'][1])+100,labels=data['MANIPUR'][0], values=data['MANIPUR'][1])     
if __name__ == '__main__':
    app.run(host='0.0.0.0')

