INSERT INTO PEND VALUES(
  1,
  1,
  9,
  23,
  MDSYS.SDO_GEOMETRY(
  2001,
  NULL,
  MDSYS.SDO_POINT_TYPE(9, 23, NULL),
  NULL,
  NULL)
);
INSERT INTO PFIELDS VALUES(
  1,
  0,
  21,
  10,
  25,
  1,
  3,
  MDSYS.SDO_GEOMETRY(
    2003,
    NULL,
    NULL,
    MDSYS.SDO_ELEM_INFO_ARRAY(1,1003,3),
    MDSYS.SDO_ORDINATE_ARRAY(0,21,11,25)
  )
);
INSERT INTO PATHS VALUES(
  1,
  2,
  23,
  9,
  23,
  MDSYS.SDO_GEOMETRY(
    2002,
    NULL,
    NULL,
    MDSYS.SDO_ELEM_INFO_ARRAY(1,2,1),
    MDSYS.SDO_ORDINATE_ARRAY(2,23,9,23)
  )
);
INSERT INTO GROUND VALUES(
  1,
  Rocky,
  1.15
);