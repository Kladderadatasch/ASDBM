INSERT INTO SLOPE VALUES(
  1,
  1.1,
  'Contour_a',
  MDSYS.SDO_GEOMETRY(
    2003,  -- 2-dimensional polygon
    NULL,
    NULL,
    MDSYS.SDO_ELEM_INFO_ARRAY(1,1003,4), -- one circle
    MDSYS.SDO_ORDINATE_ARRAY(25,9, 45,27, 25,45)
  )
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
    MDSYS.SDO_ORDINATE_ARRAY(28,16, 35,24, 28,32)
  )
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
    MDSYS.SDO_ORDINATE_ARRAY(29,21, 31,23, 29,25)
  )
);
