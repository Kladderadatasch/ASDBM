INSERT INTO SLOPE VALUES(
  1,
  1.2,
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
