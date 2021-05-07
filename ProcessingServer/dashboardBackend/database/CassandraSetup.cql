
CREATE KEYSPACE AHS_EVENT_DATABASE
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};






CREATE TABLE EventTable(
   event_id int PRIMARY KEY,
   packedId int,
   dataType text,
   location text,
   timeStart text,
   timeEnd text
   );

INSERT INTO EventTable(event_id,packedId,dataType,timeStart,timeEnd) VALUES(0,0,'text','15:30:12:532','15:30:18:532');

INSERT INTO EventTable(event_id,packedId,dataType,timeStart,timeEnd) VALUES(0,0,'video','15:30:12:532','15:30:18:532');

INSERT INTO EventTable(event_id,packedId,dataType,timeStart,timeEnd) VALUES(0,0,'live','15:30:12:532','15:30:18:532');

   CREATE TABLE emp(
   emp_id int PRIMARY KEY,
   emp_name text,
   emp_city text,
   emp_sal varint,
   emp_phone varint
   );