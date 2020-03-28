import psycopg2
import time
import os

username = os.environ['USER']
password = os.environ['PASS']
database = os.environ['DB']
hostname = os.environ['HOST']

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
cur = myConnection.cursor()

while(1):
    cur.execute( "update threshold set Nitrate=67 where sensor_node=113432;" )
    myConnection.commit()
    cur.execute( "update maintainance set status='down' where sensor_node=1387423;" )
    myConnection.commit()
    cur.execute( "update level set sewerWater_Level=26 where sensor_node=1387423;" )
    myConnection.commit()
    print("Updated 1")
    time.sleep(15)

    cur.execute( "update  threshold set Nitrate=1.1 where sensor_node=113432;" )
    myConnection.commit()
    cur.execute( "update  maintainance set status='up' where sensor_node=1387423;" )
    myConnection.commit()
    cur.execute( "update  level set sewerWater_Level=1.2 where sensor_node=1387423;" )
    myConnection.commit()
    print("Updated 2")
    time.sleep(15)