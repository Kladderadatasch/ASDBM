SELECT C.POINT_ID, SDO_GEOM.SDO_DISTANCE(C.GEOM, B.GEOM, 0.005) AS "SP DISTANCE FROM END"
   FROM SPAWN B, PSTART C
   WHERE B.SPAWN_ID = 2
   ORDER BY C.POINT_ID;
