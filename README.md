You can generate the csv file by running:

```
.headers on
.mode csv
.output pkm.csv
SELECT 
  mon.name AS pokemon1,
  mon2.name AS pokemon2, 
  t.usage AS compatibility, 
  mon2.viability_ceiling AS viability_ceiling_pokemon2
FROM mon
JOIN team t ON t.mon = mon.name
JOIN mon mon2 ON t.mate = mon2.name;
.output stdout
```
