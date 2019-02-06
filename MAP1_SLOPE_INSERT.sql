INSERT INTO SLOPE VALUES(
  1,
  1.1,
  'Contour_a',
  MDSYS.SDO_GEOMETRY(
    2003,  -- 2-dimensional polygon
    NULL,
    NULL,
    MDSYS.SDO_ELEM_INFO_ARRAY(1,1003,4), -- one circle
    MDSYS.SDO_ORDINATE_ARRAY(11,10, 14,13, 17,10)
  ),
  200
);
INSERT INTO SLOPE VALUES(
  2,
  1.15,
  'Contour_b',
  MDSYS.SDO_GEOMETRY(
    2003,  -- 2-dimensional polygon
    NULL,
    NULL,
    MDSYS.SDO_ELEM_INFO_ARRAY(1,1003,4), -- one circle
    MDSYS.SDO_ORDINATE_ARRAY(11,7, 17,13, 23,7)
  ),
  150
);
INSERT INTO SLOPE VALUES(
  3,
  1.2,
  'Contour_c',
  MDSYS.SDO_GEOMETRY(
    2003,  -- 2-dimensional polygon
    NULL,
    NULL,
    MDSYS.SDO_ELEM_INFO_ARRAY(1,1003,4), -- one circle
    MDSYS.SDO_ORDINATE_ARRAY(11,4, 20,13, 11,22)
  ),
  100
);
