CREATE TABLE PATHS (PATH_ID NUMBER NOT NULL, STARTX NUMBER(2) NOT NULL, STARTY NUMBER(2) NOT NULL, ENDX NUMBER(2) NOT NULL, ENDY NUMBER(2) NOT NULL, PRIMARY KEY (PATH_ID));
 
ALTER TABLE PATHS       -- check table name
ADD(GEOM MDSYS.SDO_GEOMETRY);

UPDATE PATHS SET GEOM =       -- check table name
MDSYS.SDO_GEOMETRY(2002,NULL,NULL,
MDSYS.SDO_ELEM_INFO_ARRAY(1,2,1),
MDSYS.SDO_ORDINATE_ARRAY(STARTX,STARTY,ENDX,ENDY)); -- check column names

DELETE FROM USER_SDO_GEOM_METADATA
  WHERE TABLE_NAME = 'PATHS' AND COLUMN_NAME = 'GEOM';


INSERT INTO USER_SDO_GEOM_METADATA
VALUES (
'PATHS',                         -- check table name
'GEOM',
MDSYS.SDO_DIM_ARRAY(
MDSYS.SDO_DIM_ELEMENT('X', 0, 50, 0.005),
MDSYS.SDO_DIM_ELEMENT('Y', 0, 50, 0.005)),
NULL);