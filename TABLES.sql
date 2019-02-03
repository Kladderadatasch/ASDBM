CREATE TABLE GROUND (GROUND_ID NUMBER NOT NULL, NAME VARCHAR2(15) NOT NULL, SCORE_INFL NUMBER(3,2) NOT NULL, PRIMARY KEY (GROUND_ID));

CREATE TABLE PFIELDS (FIELD_ID NUMBER NOT NULL, LOWX NUMBER(2) CHECK (LOWX>=0) NOT NULL, LOWY NUMBER(2) CHECK (LOWY>=0) NOT NULL, HIX NUMBER(2) CHECK (HIX<=16) NOT NULL, HIY NUMBER(2) CHECK (HIY<=16) NOT NULL, MAP NUMBER NOT NULL, GROUND_ID NUMBER(1) NOT NULL, PRIMARY KEY (FIELD_ID), FOREIGN KEY (GROUND_ID) REFERENCES GROUND(GROUND_ID));

CREATE TABLE PATHS (PATH_ID NUMBER NOT NULL, STARTX NUMBER(2) NOT NULL, ENDX NUMBER(2) NOT NULL, STARTY NUMBER(2) NOT NULL, ENDY NUMBER(2) NOT NULL, PRIMARY KEY (PATH_ID));

CREATE TABLE STYPE (TYPE_ID NUMBER(1) NOT NULL, NAME VARCHAR2(15) NOT NULL, SCORE_INFL NUMBER(3,2) NOT NULL, PRIMARY KEY (TYPE_ID));

CREATE TABLE BOOTS (BOOT_ID NUMBER(1) NOT NULL, NAME VARCHAR2(20) NOT NULL, SCORE_INFL NUMBER(3,2) NOT NULL, PRIMARY KEY (BOOT_ID));

CREATE TABLE SCORE (SCORE_ID NUMBER(2) NOT NULL, PLAYER VARCHAR2(15) NOT NULL, SCORE NUMBER(7,2) NOT NULL, DISTANCE NUMBER(10) NOT NULL, BOOTS NUMBER(1) NOT NULL, PRIMARY KEY (SCORE_ID), FOREIGN KEY (BOOTS) REFERENCES BOOTS(BOOT_ID));

CREATE TABLE SPAWN (SPAWN_ID NUMBER NOT NULL, X NUMBER(2) NOT NULL, Y NUMBER(2) NOT NULL, TYPE_ID NUMBER(1) NOT NULL, PRIMARY KEY (SPAWN_ID), FOREIGN KEY (TYPE_ID) REFERENCES STYPE(TYPE_ID));

CREATE TABLE SLOPE (SLOPE_ID NUMBER NOT NULL, NAME VARCHAR2(20), SCORE_INFL NUMBER(3,2) NOT NULL, PRIMARY KEY (SLOPE_ID));

--LINK TO COMPLEX POLYGON INSERT: https://docs.oracle.com/cd/E11882_01/appdev.112/e11830/sdo_objrelschema.htm#SPATL486
