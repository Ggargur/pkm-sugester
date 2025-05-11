You can generate the csv file by running:

```
.mode csv
.headers on
.output pkm.csv
SELECT 
  mon.name AS pokemon1,
  mon.usage AS uso_pokemon1, 
  mon.viability_ceiling AS viability_ceiling_pokemon1,
  mon2.name AS pokemon2, 
  mon2.usage AS uso_pokemon2, 
  mon2.viability_ceiling AS viability_ceiling_pokemon2
FROM mon
JOIN team t ON t.mon = mon.name
JOIN mon mon2 ON t.mate = mon2.name;
.output stdout
```
