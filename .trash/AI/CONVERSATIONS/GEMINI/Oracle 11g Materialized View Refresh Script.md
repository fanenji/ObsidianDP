---
type: conversation
topic: data-platform
created: 2026-02-13
tags:
  - oracle
  - materialized-view
---
**Source:** https://aistudio.google.com/u/1/prompts/19wRhLWe5iM1gzVB6SGUzcUofGUEryFQ6

## System Instructions

Optional tone and style instructions for the model

---

### User

A oracle 11g statement to create a materialized view that refresh every day at 10pm

---

### Model

Okay, here is an Oracle 11g SQL statement to create a materialized view that refreshes automatically every day at 10 PM (22:00).

code
SQL
download
content_copy
expand_less
CREATE MATERIALIZED VIEW my_materialized_view_name
BUILD IMMEDIATE
REFRESH FORCE ON
    START WITH TRUNC(SYSDATE) + (22/24) + CASE WHEN SYSDATE > TRUNC(SYSDATE) + (22/24) THEN 1 ELSE 0 END
    NEXT TRUNC(SYSDATE) + 1 + (22/24)
AS
SELECT
    -- Your select statement goes here
    column1,
    column2,
    COUNT(*) as row_count
FROM
    your_source_table
WHERE
    -- Optional filter conditions
    some_column > 100
GROUP BY
    -- Your group by columns if needed
    column1,
    column2;

Explanation:

CREATE MATERIALIZED VIEW my_materialized_view_name: This specifies the name of your materialized view. Replace my_materialized_view_name with your desired name.

BUILD IMMEDIATE: This means the materialized view will be populated with data immediately upon creation.

REFRESH FORCE ON: This sets up automatic refreshing using a scheduled job.

FORCE: This tells Oracle to try a FAST refresh first (if a materialized view log exists and is valid for the source table), otherwise perform a COMPLETE refresh (rebuild the MV entirely). FORCE is a good default for robustness.

ON: Indicates a scheduled refresh.

START WITH TRUNC(SYSDATE) + (22/24) + CASE WHEN SYSDATE > TRUNC(SYSDATE) + (22/24) THEN 1 ELSE 0 END: This calculates the date and time of the first refresh.

TRUNC(SYSDATE): Gets the current date with the time set to midnight (00:00).

+ (22/24): Adds 22 hours (22 out of 24 hours in a day) to get to 10 PM on that date.

CASE WHEN SYSDATE > TRUNC(SYSDATE) + (22/24) THEN 1 ELSE 0 END: This checks if the current time (SYSDATE) is already past 10 PM today.

If it's past 10 PM today, it adds 1 day to the calculated time, setting the first refresh for 10 PM tomorrow.

If it's before or exactly 10 PM today, it adds 0 days, setting the first refresh for 10 PM today.

This whole START WITH expression ensures that the first scheduled refresh will happen at the next occurrence of 10 PM after you create the materialized view.

NEXT TRUNC(SYSDATE) + 1 + (22/24): This is the crucial part that defines the interval and time for subsequent refreshes.

TRUNC(SYSDATE): Gets the date part of when the NEXT expression is evaluated by the job scheduler.

+ 1: Adds one day.

+ (22/24): Adds 22 hours (10 PM).

This expression effectively calculates "tomorrow at 10 PM" relative to the day the refresh is currently running. This ensures the materialized view refreshes at 10 PM every day.

AS SELECT ... FROM ...: This is the standard query that defines the data for your materialized view. Replace the example SELECT statement with your actual query.

Prerequisites:

You need the CREATE MATERIALIZED VIEW or CREATE ANY MATERIALIZED VIEW system privilege.

You need SELECT privileges on the source table(s).

The database parameter JOB_QUEUE_PROCESSES must be set to a value greater than 0 to enable scheduled jobs.

If you intend for REFRESH FAST to be possible (for performance), you will need to create a MATERIALIZED VIEW LOG on the source table(s) before creating the materialized view. Example: CREATE MATERIALIZED VIEW LOG ON your_source_table WITH ROWID INCLUDING NEW VALUES; (Check Oracle documentation for specific MV log options based on your query and refresh needs).

Remember to replace the placeholder names and the SELECT query with your actual requirements.

You can get the SELECT statement used to create a materialized view from the Oracle data dictionary view ALL_MVIEWS.

Here's the SQL query:

code
SQL
download
content_copy
expand_less
SELECT
    owner,
    mview_name,
    query
FROM
    all_mviews
WHERE
    mview_name = 'YOUR_MATERIALIZED_VIEW_NAME'; -- Replace with your MV name

Explanation:

all_mviews: This is a data dictionary view that contains information about all materialized views that are accessible to the current user.

owner: The schema owner of the materialized view.

mview_name: The name of the materialized view.

query: This column stores the text of the SELECT statement that defines the materialized view.

WHERE mview_name = 'YOUR_MATERIALIZED_VIEW_NAME': This filters the results to show only the information for your specific materialized view. Replace 'YOUR_MATERIALIZED_VIEW_NAME' with the actual name of your materialized view (it's case-sensitive if the name was created with double quotes, otherwise it's typically uppercase).

You might also want to filter by owner if you know the schema the MV is in and want to be specific, especially if different schemas could have MVs with the same name:

code
SQL
download
content_copy
expand_less
SELECT
    owner,
    mview_name,
    query
FROM
    all_mviews
WHERE
    owner = 'SCHEMA_NAME'           -- Replace with the schema owner
    AND mview_name = 'YOUR_MATERIALIZED_VIEW_NAME'; -- Replace with your MV name

Important Notes:

The query column is of data type LONG. When querying LONG columns in SQL*Plus or other command-line tools, you might need to adjust your session settings to see the entire text. For example:

code
SQL
download
content_copy
expand_less
SET LONG 10000  -- Sets the maximum width for LONG columns
SET PAGESIZE 0  -- Prevents pagination
SET LINESIZE 150 -- Adjust line width

You need the necessary privileges (SELECT on ALL_MVIEWS) to query this view.

For getting the full DDL (CREATE MATERIALIZED VIEW ... statement including storage clauses, refresh options, etc.), the DBMS_METADATA.GET_DDL function is generally preferred:

code
SQL
download
content_copy
expand_less
SELECT dbms_metadata.get_ddl('MATERIALIZED_VIEW', 'YOUR_MATERIALIZED_VIEW_NAME', 'SCHEMA_NAME') FROM dual;

This gives you the complete CREATE statement. Remember to replace the placeholders.

Okay, the error ORA-00922: opzione mancante o non valida ("missing or invalid option") at that position (line 21, near the INNER JOIN) is being caused by a syntax error earlier in your statement, specifically in the REFRESH clause.

You have:
REFRESH COMPLETE ON DEMAND START WITH sysdate+0 NEXT trunc(SYSDATE) + (22 / 24)

The problem is that you specified ON DEMAND. ON DEMAND means the materialized view is refreshed manually (e.g., using DBMS_MVIEW.REFRESH). When you specify ON DEMAND, you cannot include START WITH and NEXT clauses, because those are used for automatic scheduled refreshes.

Since you want it to refresh every day at 10 PM, you need an automatic scheduled refresh. The options for automatic refresh are ON COMMIT (not applicable here) or ON followed by START WITH and NEXT.

You should change ON DEMAND to ON FORCE or just ON (since COMPLETE implies ON). ON FORCE is generally recommended as it tries FAST first if possible, then falls back to COMPLETE. Given your query involves a join, you'd need MV logs on both base tables (V_STAZ_ELENCO_OSS_SPECIE_A_PUB and lobg05_specie_p) and specific MV capabilities for joins if you wanted FAST refresh. Without them, it will default to COMPLETE. Let's use REFRESH COMPLETE ON as you specified COMPLETE.

Also, the START WITH clause sysdate+0 isn't the best way to define the first refresh at the next occurrence of 10 PM. The START WITH needs to calculate the exact date and time of the first scheduled run.

Here is the corrected statement, designed to refresh COMPLETEly every day at 10 PM (22:00):

code
SQL
download
content_copy
expand_less
CREATE OR REPLACE MATERIALIZED VIEW "LIBIOSS_ETRF89"."MV_LOBG05_SPECIE_P_A_PUB" ("COD_STAZ", "TIPO_SITO", "DESCR_SITO", "COORD_X", "COORD_Y", "DATA_STAZ", "DATA_STAZ_END", "MOTIVO_STAZ_END", "COD_TIPO_SITO", "NOME_TIPO_SITO", "COD_BIOGEO", "NOME_BIOGEO", "COD_SIC", "DESCR_SIC", "COD_ZPS", "DESCR_ZPS", "COD_AREA_PROT", "NOME_AREA_PROT", "COD_TOPO", "NOME_TOPO", "COD_ZONUM", "NOME_ZONUM", "NOME_TOPO_OLD", "ELENCO_OSSERVAZIONI", "ELENCO_SPECIE", "OGR_FID", "ORA_GEOMETRY")
BUILD IMMEDIATE
REFRESH COMPLETE ON -- Changed from ON DEMAND
    START WITH TRUNC(SYSDATE) + (22/24) + CASE WHEN SYSDATE > TRUNC(SYSDATE) + (22/24) THEN 1 ELSE 0 END -- Calculate next 10 PM
    NEXT TRUNC(SYSDATE+1) + (22/24) -- Calculate 10 PM on the next day
AS SELECT so.COD_STAZ,
       so.TIPO_sito,
       so.descr_sito,
       so.coord_x,
       so.coord_y,
       so.data_staz,
       so.data_staz_end,
       so.motivo_staz_end,
       so.cod_tipo_sito,
       so.nome_tipo_sito,
       so.cod_biogeo,
       so.nome_biogeo,
       so.cod_sic,
       so.descr_sic,
       so.cod_zps,
       so.descr_zps,
       so.cod_area_prot,
       so.nome_area_prot,
       so.cod_topo,
       so.nome_topo,
       so.cod_zonum,
       so.nome_zonum,
       so.nome_topo_old,
       so.ELENCO_OSSERVAZIONI,
       so.ELENCO_SPECIE,
       geo.ogr_fid,
       geo.ora_geometry
  FROM V_STAZ_ELENCO_OSS_SPECIE_A_PUB  so
       INNER JOIN lobg05_specie_p geo ON so.cod_staz = geo.id_staz; -- This line is fine now

Explanation of Changes:

REFRESH COMPLETE ON: Removed ON DEMAND. This enables the scheduled refresh using START WITH and NEXT.

START WITH TRUNC(SYSDATE) + (22/24) + CASE WHEN SYSDATE > TRUNC(SYSDATE) + (22/24) THEN 1 ELSE 0 END: This calculates the date and time for the first refresh. It finds 10 PM today (TRUNC(SYSDATE) + (22/24)) and if the current time is already past 10 PM today, it adds one day to set the first refresh for 10 PM tomorrow.

NEXT TRUNC(SYSDATE+1) + (22/24): This is the standard way to express "every day at 10 PM" for subsequent refreshes. TRUNC(SYSDATE+1) calculates tomorrow's date at midnight, and +(22/24) adds 22 hours to get 10 PM. This expression is evaluated each time the refresh job runs to determine the time of the next run.

This corrected statement should create the materialized view with the desired daily 10 PM refresh schedule.

Yes, you absolutely can "replace" a materialized view in Oracle. The most common and straightforward way to do this is using the CREATE OR REPLACE MATERIALIZED VIEW statement.

Using CREATE OR REPLACE MATERIALIZED VIEW

This statement will:

If the materialized view already exists: Drop the existing materialized view and then create it again with the new definition you provide.

If the materialized view does not exist: Create it as specified.

Syntax:

code
SQL
download
content_copy
expand_less
CREATE OR REPLACE MATERIALIZED VIEW schema_name.mview_name
   [ (column_alias [, column_alias]...) ] -- Optional: to rename columns
   [ OF [schema.]object_type ] -- For object materialized views
   [ DEFAULT COLLATION collation_name ] -- If needed
   [ USING INDEX (index_options) ] -- To control the backing index
   [ USING NO INDEX ]
   [ storage_clause ] -- TABLESPACE, PCTFREE, etc.
   [ BUILD {IMMEDIATE | DEFERRED | PREBUILT} ]
   [ REFRESH [FAST | COMPLETE | FORCE]
       [ ON [COMMIT | DEMAND] ]
       [ START WITH date_expression ]
       [ NEXT date_expression ]
       [ WITH {PRIMARY KEY | ROWID} ]
       [ USING DEFAULT {MASTER | LOCAL} ROLLBACK SEGMENT ]
       [ USING {MASTER | LOCAL} ROLLBACK SEGMENT segment_name ]
       [ NEVER REFRESH ]
   ]
   [ FOR UPDATE ] -- If the MV is updatable
   [ {ENABLE | DISABLE} QUERY REWRITE ]
AS
   subquery; -- Your new SELECT statement defining the MV

Example:

Let's say you have MV_MY_DATA and you want to change its underlying query or refresh schedule.

Original (simplified):

code
SQL
download
content_copy
expand_less
CREATE MATERIALIZED VIEW MV_MY_DATA
REFRESH COMPLETE ON DEMAND
AS SELECT col1, COUNT(*) AS c FROM my_table GROUP BY col1;

Now you want to change it to refresh daily at 2 AM and add another column:

code
SQL
download
content_copy
expand_less
CREATE OR REPLACE MATERIALIZED VIEW MV_MY_DATA
BUILD IMMEDIATE
REFRESH COMPLETE ON
    START WITH TRUNC(SYSDATE) + (2/24) + CASE WHEN SYSDATE > TRUNC(SYSDATE) + (2/24) THEN 1 ELSE 0 END
    NEXT TRUNC(SYSDATE+1) + (2/24)
ENABLE QUERY REWRITE
AS
SELECT
    col1,
    col2,  -- Added a new column
    COUNT(*) AS c
FROM
    my_table
GROUP BY
    col1, col2; -- Changed group by

Important Considerations When Using CREATE OR REPLACE MATERIALIZED VIEW:

Data Loss (Temporary): The old MV is dropped, and then the new one is built. If BUILD IMMEDIATE is used, it will be repopulated. During the drop and recreate phase, the MV is unavailable.

Privileges: Any GRANTs made directly on the materialized view will be lost. You will need to re-grant them after the CREATE OR REPLACE statement.

Indexes: Any custom indexes you created on the materialized view (other than the default one Oracle creates) will be dropped. You'll need to recreate them.

Constraints: If you had defined constraints (like a primary key for a prebuilt MV), they would be lost and might need redefinition.

Dependent Objects: Other objects (views, procedures, functions, other MVs) that depend on the materialized view will be invalidated. They will typically recompile automatically upon next access, but it's something to be aware of.

Refresh Job: The underlying DBMS_JOB or Scheduler job that handles automatic refreshes will be dropped and recreated based on the new REFRESH clause.

Alternative: ALTER MATERIALIZED VIEW

If you only want to change certain attributes of the materialized view (like its refresh method, schedule, or query rewrite eligibility) but not its defining query, you can use ALTER MATERIALIZED VIEW.

Example: Changing refresh schedule of an existing MV (without changing the query)

code
SQL
download
content_copy
expand_less
ALTER MATERIALIZED VIEW MV_MY_DATA
REFRESH COMPLETE ON
    START WITH TRUNC(SYSDATE) + (3/24) -- Change to 3 AM
    NEXT TRUNC(SYSDATE+1) + (3/24);
code
SQL
download
content_copy
expand_less
ALTER MATERIALIZED VIEW MV_MY_DATA DISABLE QUERY REWRITE;

You cannot use ALTER MATERIALIZED VIEW to change the AS SELECT ... part (the subquery). For that, you must use CREATE OR REPLACE MATERIALIZED VIEW.

In summary:

Use CREATE OR REPLACE MATERIALIZED VIEW to change the defining query or make multiple changes at once. Be mindful of lost grants and indexes.

Use ALTER MATERIALIZED VIEW to modify refresh options, scheduling, or query rewrite behavior without changing the underlying query.

You're very close! The ORA-00905: parola chiave mancante (missing keyword) in this context with ALTER MATERIALIZED VIEW usually means that the ON keyword after REFRESH COMPLETE is the issue when you are altering an existing scheduled refresh.

When you CREATE a materialized view with a schedule, you use REFRESH [type] ON START WITH ... NEXT ....
However, when you ALTER an existing materialized view that already has a schedule and you just want to change the START WITH and NEXT times, you generally omit the ON.

Try this corrected statement:

code
SQL
download
content_copy
expand_less
ALTER MATERIALIZED VIEW "LIBIOSS_ETRF89"."MV_LOBG05_SPECIE_P_A_PUB"
REFRESH COMPLETE -- Removed the "ON" keyword
    START WITH TRUNC(SYSDATE) + (23/24) + CASE WHEN SYSDATE > TRUNC(SYSDATE) + (23/24) THEN 1 ELSE 0 END -- Changed to 11 PM and made robust
    NEXT TRUNC(SYSDATE+1) + (23/24);

Explanation of Changes:

Removed ON: The primary change is removing the ON keyword after REFRESH COMPLETE. When altering an existing schedule, you typically don't re-specify ON.

Robust START WITH: I've also adjusted your START WITH clause to be more robust, similar to the CREATE statement.

TRUNC(SYSDATE) + (23/24): Gets 11 PM today.

+ CASE WHEN SYSDATE > TRUNC(SYSDATE) + (23/24) THEN 1 ELSE 0 END: This part ensures that if it's already past 11 PM today when you run this ALTER statement, the first rescheduled refresh will be at 11 PM tomorrow. If it's before 11 PM today, the first rescheduled refresh will be 11 PM today.

NEXT clause: NEXT TRUNC(SYSDATE+1) + (23/24) remains correct for "every day at 11 PM (23:00)".

This should allow you to alter the refresh schedule of your existing materialized view.

Why the error?

The parser expects a certain sequence of keywords. When you use ALTER MATERIALIZED VIEW ... REFRESH ..., if the MV is already set for a scheduled refresh, providing ON again can confuse it, making it look for other keywords associated with defining the type of refresh (like COMMIT or DEMAND) rather than just updating the schedule parameters.

You've hit the same subtle syntax point again, but this time in the CREATE OR REPLACE MATERIALIZED VIEW statement.

The error ORA-00922: opzione mancante o non valida at line: 3 pos: 18 is because of the ON keyword after REFRESH COMPLETE when you are specifying a START WITH ... NEXT ... schedule.

Incorrect:
REFRESH COMPLETE ON START WITH ...

Correct for scheduled refresh:
REFRESH COMPLETE START WITH ...

The ON keyword is used in the REFRESH clause only for ON COMMIT or ON DEMAND types of refresh. When you're defining a schedule using START WITH and NEXT, you don't use ON directly after the refresh method (COMPLETE, FAST, FORCE).

Here's the corrected statement:

code
SQL
download
content_copy
expand_less
CREATE OR REPLACE MATERIALIZED VIEW MV_LOBG05_SPECIE_P_PUB
BUILD IMMEDIATE
REFRESH COMPLETE -- Removed "ON" from here
    START WITH TRUNC(SYSDATE) + (2/24) + CASE WHEN SYSDATE > TRUNC(SYSDATE) + (2/24) THEN 1 ELSE 0 END
    NEXT TRUNC(SYSDATE+1) + (2/24)
ENABLE QUERY REWRITE
AS SELECT so.COD_STAZ,
       so.TIPO_sito,
       so.descr_sito,
       so.coord_x,
       so.coord_y,
       so.data_staz,
       so.data_staz_end,
       so.motivo_staz_end,
       so.cod_tipo_sito,
       so.nome_tipo_sito,
       so.cod_biogeo,
       so.nome_biogeo,
       so.cod_sic,
       so.descr_sic,
       so.cod_zps,
       so.descr_zps,
       so.cod_area_prot,
       so.nome_area_prot,
       so.cod_topo,
       so.nome_topo,
       so.cod_zonum,
       so.nome_zonum,
       so.nome_topo_old,
       so.ELENCO_OSSERVAZIONI,
       so.ELENCO_SPECIE,
       geo.ogr_fid,
       geo.ora_geometry
  FROM V_STAZ_ELENCO_OSS_SPECIE_PUB so
       INNER JOIN lobg05_specie_p geo ON so.cod_staz = geo.id_staz ;

Key Change:

Line 3 changed from REFRESH COMPLETE ON to REFRESH COMPLETE

By removing the ON keyword before START WITH, the syntax will be correct for defining an automatically scheduled refresh for the materialized view.

Okay, this ORA-00922: opzione mancante o non valida on line: 5 pos: 18 (which is the NEXT clause) strongly suggests that the parser is getting confused by the complexity of your START WITH date expression.

When a date_expression for START WITH (or NEXT) becomes complex, especially involving CASE statements mixed with arithmetic, it's crucial to ensure the parser sees it as a single, unified expression. The most common way to do this is to enclose the entire date calculation for START WITH in parentheses.

The parser likely consumes TRUNC(SYSDATE) + (22/24) as the potential date_expression for START WITH. Then, it sees + CASE WHEN SYSDATE > TRUNC(SYSDATE) + (22/24) THEN 1 ELSE 0 END as trailing, unexpected tokens. Because the START WITH clause isn't "cleanly" finished in the parser's view, the subsequent NEXT keyword appears out of place, leading to the "missing or invalid option" error pointing to the NEXT line.

Try this corrected version:

code
SQL
download
content_copy
expand_less
CREATE OR REPLACE MATERIALIZED VIEW MV_LOBG05_SPECIE_P_PUB
BUILD IMMEDIATE
REFRESH COMPLETE
    START WITH (TRUNC(SYSDATE) + (22/24) + CASE WHEN SYSDATE > TRUNC(SYSDATE) + (22/24) THEN 1 ELSE 0 END) -- Entire expression for START WITH is parenthesized
    NEXT TRUNC(SYSDATE+1) + (22/24)
ENABLE QUERY REWRITE
AS SELECT so.COD_STAZ,
       so.TIPO_sito,
       so.descr_sito,
       so.coord_x,
       so.coord_y,
       so.data_staz,
       so.data_staz_end,
       so.motivo_staz_end,
       so.cod_tipo_sito,
       so.nome_tipo_sito,
       so.cod_biogeo,
       so.nome_biogeo,
       so.cod_sic,
       so.descr_sic,
       so.cod_zps,
       so.descr_zps,
       so.cod_area_prot,
       so.nome_area_prot,
       so.cod_topo,
       so.nome_topo,
       so.cod_zonum,
       so.nome_zonum,
       so.nome_topo_old,
       so.ELENCO_OSSERVAZIONI,
       so.ELENCO_SPECIE,
       geo.ogr_fid,
       geo.ora_geometry
  FROM V_STAZ_ELENCO_OSS_SPECIE_PUB so
       INNER JOIN lobg05_specie_p geo ON so.cod_staz = geo.id_staz ;

Key Change:

The entire date calculation for the START WITH clause is now enclosed in parentheses:
START WITH (TRUNC(SYSDATE) + (22/24) + CASE WHEN SYSDATE > TRUNC(SYSDATE) + (22/24) THEN 1 ELSE 0 END)

This tells the Oracle parser to evaluate everything inside the parentheses as a single date expression for the START WITH parameter. This should resolve the parsing ambiguity.

You could also write the START WITH logic slightly differently using a CASE expression that directly returns the target date (which also should be parenthesized if used directly):

code
SQL
download
content_copy
expand_less
-- Alternative START WITH logic (also parenthesized)
START WITH (CASE
              WHEN SYSDATE >= TRUNC(SYSDATE) + (22/24) -- If current time is 10 PM or later today
              THEN TRUNC(SYSDATE + 1) + (22/24)     -- Schedule for 10 PM tomorrow
              ELSE TRUNC(SYSDATE) + (22/24)         -- Schedule for 10 PM today
            END)

But the version you had, once parenthesized correctly as shown in the main corrected script above, should work fine.

---

### User

how can i get the select statement of an existing materialized view from the oracle system table

CREATE OR REPLACE MATERIALIZED VIEW "LIBIOSS_ETRF89"."MV_LOBG05_SPECIE_P_A_PUB" ("COD_STAZ", "TIPO_SITO", "DESCR_SITO", "COORD_X", "COORD_Y", "DATA_STAZ", "DATA_STAZ_END", "MOTIVO_STAZ_END", "COD_TIPO_SITO", "NOME_TIPO_SITO", "COD_BIOGEO", "NOME_BIOGEO", "COD_SIC", "DESCR_SIC", "COD_ZPS", "DESCR_ZPS", "COD_AREA_PROT", "NOME_AREA_PROT", "COD_TOPO", "NOME_TOPO", "COD_ZONUM", "NOME_ZONUM", "NOME_TOPO_OLD", "ELENCO_OSSERVAZIONI", "ELENCO_SPECIE", "OGR_FID", "ORA_GEOMETRY")
BUILD IMMEDIATE
REFRESH COMPLETE ON DEMAND START WITH sysdate+0 NEXT trunc(SYSDATE) + (22 / 24)
AS SELECT so.COD_STAZ,
so.TIPO_sito,
so.descr_sito,
so.coord_x,
so.coord_y,
so.data_staz,
so.data_staz_end,
so.motivo_staz_end,
so.cod_tipo_sito,
so.nome_tipo_sito,
so.cod_biogeo,
so.nome_biogeo,
so.cod_sic,
so.descr_sic,
so.cod_zps,
so.descr_zps,
so.cod_area_prot,
so.nome_area_prot,
so.cod_topo,
so.nome_topo,
so.cod_zonum,
so.nome_zonum,
so.nome_topo_old,
so.ELENCO_OSSERVAZIONI,
so.ELENCO_SPECIE,
geo.ogr_fid,
geo.ora_geometry
FROM V_STAZ_ELENCO_OSS_SPECIE_A_PUB  so
INNER JOIN lobg05_specie_p geo ON so.cod_staz = geo.id_staz;

Errore SQL [922] [42000]: ORA-00922: opzione mancante o non valida
Error position: line: 21 pos: 18

can i replace a materialized view?

ALTER MATERIALIZED VIEW MV_LOBG05_SPECIE_P_A_PUB
REFRESH COMPLETE ON
START WITH TRUNC(SYSDATE) + (23/24) -- Change to 3 AM
NEXT TRUNC(SYSDATE+1) + (23/24);

Errore SQL [905] [42000]: ORA-00905: parola chiave mancante
Error position: line: 23 pos: 73

i'm on oracle 11g

CREATE OR REPLACE MATERIALIZED VIEW MV_LOBG05_SPECIE_P_PUB
BUILD IMMEDIATE
REFRESH COMPLETE ON
START WITH TRUNC(SYSDATE) + (2/24) + CASE WHEN SYSDATE > TRUNC(SYSDATE) + (2/24) THEN 1 ELSE 0 END
NEXT TRUNC(SYSDATE+1) + (2/24)
ENABLE QUERY REWRITE
AS SELECT so.COD_STAZ,
so.TIPO_sito,
so.descr_sito,
so.coord_x,
so.coord_y,
so.data_staz,
so.data_staz_end,
so.motivo_staz_end,
so.cod_tipo_sito,
so.nome_tipo_sito,
so.cod_biogeo,
so.nome_biogeo,
so.cod_sic,
so.descr_sic,
so.cod_zps,
so.descr_zps,
so.cod_area_prot,
so.nome_area_prot,
so.cod_topo,
so.nome_topo,
so.cod_zonum,
so.nome_zonum,
so.nome_topo_old,
so.ELENCO_OSSERVAZIONI,
so.ELENCO_SPECIE,
geo.ogr_fid,
geo.ora_geometry
FROM V_STAZ_ELENCO_OSS_SPECIE_PUB so
INNER JOIN lobg05_specie_p geo ON so.cod_staz = geo.id_staz ;

gives this error
Errore SQL [922] [42000]: ORA-00922: opzione mancante o non valida
Error position: line: 3 pos: 18

CREATE OR REPLACE MATERIALIZED VIEW MV_LOBG05_SPECIE_P_PUB
BUILD IMMEDIATE
REFRESH COMPLETE
START WITH TRUNC(SYSDATE) + (22/24) + CASE WHEN SYSDATE > TRUNC(SYSDATE) + (22/24) THEN 1 ELSE 0 END
NEXT TRUNC(SYSDATE+1) + (22/24)
ENABLE QUERY REWRITE
AS SELECT so.COD_STAZ,
so.TIPO_sito,
so.descr_sito,
so.coord_x,
so.coord_y,
so.data_staz,
so.data_staz_end,
so.motivo_staz_end,
so.cod_tipo_sito,
so.nome_tipo_sito,
so.cod_biogeo,
so.nome_biogeo,
so.cod_sic,
so.descr_sic,
so.cod_zps,
so.descr_zps,
so.cod_area_prot,
so.nome_area_prot,
so.cod_topo,
so.nome_topo,
so.cod_zonum,
so.nome_zonum,
so.nome_topo_old,
so.ELENCO_OSSERVAZIONI,
so.ELENCO_SPECIE,
geo.ogr_fid,
geo.ora_geometry
FROM V_STAZ_ELENCO_OSS_SPECIE_PUB so
INNER JOIN lobg05_specie_p geo ON so.cod_staz = geo.id_staz ;

Errore SQL [922] [42000]: ORA-00922: opzione mancante o non valida

Error position: line: 5 pos: 18

---
