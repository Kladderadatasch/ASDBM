SELECT A.PATH_ID, C.FIELD_ID, SDO_GEOM.SDO_LENGTH(SDO_GEOM.SDO_INTERSECTION(A.GEOM, C.GEOM, 0.005), M.DIMINFO) AS "DISTANCE", C.GROUND_ID, D.SCORE_INFL AS "GROUNDMULTIPLIER", SDO_GEOM.SDO_LENGTH(SDO_GEOM.SDO_INTERSECTION(A.GEOM, C.GEOM, 0.005), M.DIMINFO)*D.SCORE_INFL AS "SCORE"
FROM PATHS A, PFIELDS C, USER_SDO_GEOM_METADATA M, GROUND D
WHERE M.TABLE_NAME = 'PATHS' AND M.COLUMN_NAME = 'GEOM' AND SDO_GEOM.SDO_LENGTH(SDO_GEOM.SDO_INTERSECTION(A.GEOM, C.GEOM, 0.005), M.DIMINFO) > 0 AND C.GROUND_ID = D.GROUND_ID
ORDER BY A.PATH_ID;
