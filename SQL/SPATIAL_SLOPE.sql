ALTER TABLE SLOPE       -- check table name
ADD(GEOM MDSYS.SDO_GEOMETRY);

UPDATE SLOPE SET GEOM =       -- check table name
MDSYS.SDO_GEOMETRY(2003,NULL,NULL,
MDSYS.SDO_ELEM_INFO_ARRAY(1,2,1),
MDSYS.SDO_ORDINATE_ARRAY(STARTX,STARTY,ENDX,ENDY)); -- check column names

INSERT INTO USER_SDO_GEOM_METADATA
VALUES (
'SLOPE',                          -- check table name
'GEOM',
MDSYS.SDO_DIM_ARRAY(
MDSYS.SDO_DIM_ELEMENT('X', 0, 50, 0.005),
MDSYS.SDO_DIM_ELEMENT('Y', 0, 50, 0.005)),
NULL);