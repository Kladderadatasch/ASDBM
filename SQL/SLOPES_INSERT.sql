INSERT INTO SLOPES VALUES(
  1,
  1.1,
  100,
  MDSYS.SDO_GEOMETRY(
    2003,  -- two-dimensional polygon
    NULL,
    NULL,
    MDSYS.SDO_ELEM_INFO_ARRAY(1,1003,1, 15,2003,1), -- polygon with hole
    MDSYS.SDO_ORDINATE_ARRAY(8,17, 8,24, 17,24, 19,20, 17,12, 13,12, 8,17,
      14,17, 14,20, 17,20, 17,17, 14,17)
    )
);
INSERT INTO SLOPES VALUES(
  2,
  1.2,
  150,
  MDSYS.SDO_GEOMETRY(
    2003,  -- two-dimensional polygon
    NULL,
    NULL,
    MDSYS.SDO_ELEM_INFO_ARRAY(1,1003,1, 11,2003,1), -- polygon with hole
    MDSYS.SDO_ORDINATE_ARRAY(14,17, 14,20, 17,20, 17,17, 14,17,
      15,18, 15,19, 16,19, 16,18, 15,18)
    )
);
