SELECT C.PATH_ID, D.PATH_ID
FROM PATHS C, PATHS D
WHERE SDO_TOUCH(C.GEOM, D.GEOM) = 'TRUE'
ORDER BY C.PATH_ID;
