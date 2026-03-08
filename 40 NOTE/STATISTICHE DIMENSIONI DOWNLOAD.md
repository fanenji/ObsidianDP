---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - sql
  - statistiche
---

```other
WITH y_stat as
(
    select to_char( data_inserimento,'yyyy' ) anno,to_char(sum(dimensione_mb) / (1024*1024),'99.99') dimensione_tb
    from sit_richieste_download
    where stato_richiesta=2
    and cod_cliente is not null
    group by to_char( data_inserimento,'yyyy' )
)
select * FROM y_stat WHERE dimensione_tb IS NOT NULL
AND ANNO > '2012'
order by 1

SELECT to_char(avg(dimensione_tb),'9.99') AVG, to_char(sum(dimensione_tb),'99.99') SUM FROM
(
	WITH y_stat as
	(
	    select to_char( data_inserimento,'yyyy' ) anno,sum(dimensione_mb) / (1024*1024) dimensione_tb
	    from sit_richieste_download
	    where stato_richiesta=2
	    and cod_cliente is not null
	    group by to_char( data_inserimento,'yyyy' )
	)
	select * FROM y_stat WHERE dimensione_tb IS NOT NULL
	AND ANNO > '2012'
)
```

| **ANNO** | **DIMENSIONE_TB** |
| -------- | ----------------- |
| 2013     | .52               |
| 2014     | 1.05              |
| 2015     | 1.06              |
| 2016     | 1.06              |
| 2017     | 1.46              |
| 2018     | 6.19              |
| 2019     | 7.67              |
| 2020     | 2.12              |
| 2021     | 2.71              |
| 2022     | 3.61              |
| 2023     | 2.94              |

| **AVG** | **SUM** |
| ------- | ------- |
| 2.76    | 30.39   |

