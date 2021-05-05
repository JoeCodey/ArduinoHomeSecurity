import datetime
import uuid #great tool for generating unique IDs 
from cassandra.cluster import Cluster 


def getUniqueId():
    return str(uuid.uuid4().fields[-1])[:5] 

def insertTestRow():
    return "INSERT INTO EventTable(event_id,packedId,dataType,timeStart,timeEnd) \
        VALUES("+getUniqueId()+",0,'text','15:30:12:532','15:30:18:532');"

def createEventTable():
    return ("""CREATE TABLE EventTable(
   event_id int PRIMARY KEY,
   packedId int,
   dataType text,
   location text,
   timeStart text,
   timeEnd text
   );""")

#session.execute(createEventTable()) // Table already exists in database 

cluster = Cluster(['0.0.0.0'],port=9042)
session = cluster.connect()
session.execute('USE ahs_event_database')

session.execute(insertTestRow())
session.execute(insertTestRow())


rows = session.execute('SELECT * FROM eventtable')


for row in rows:
    print(row.event_id,row.datatype,row.timeend)



