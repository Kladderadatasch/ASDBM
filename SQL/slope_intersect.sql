SELECT A.PATH_ID, C.SLOPE_ID, C.SCORE_INFL
FROM PATHS A, SLOPES C, USER_SDO_GEOM_METADATA M
WHERE M.TABLE_NAME = 'PATHS' AND M.COLUMN_NAME = 'GEOM' AND SDO_RELATE(A.GEOM, C.GEOM, 'mask=overlapbdydisjoint+inside') = 'TRUE'
ORDER BY A.PATH_ID;
