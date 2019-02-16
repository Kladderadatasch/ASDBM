SET LINESIZE 150;
SET PAGESIZE 25;
SELECT A.PATH_ID, B.POINT_ID AS "START_POINT_ID", C.POINT_ID AS "END_POINT_ID", B.S_X, B.S_Y, C.S_X AS "E_X", C.S_Y AS "E_Y"
FROM PATHS A, PSTART B, PEND C
WHERE A.PATH_ID = B.PATH_ID AND A.PATH_ID = C.PATH_ID
ORDER BY A.PATH_ID;
