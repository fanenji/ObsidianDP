
# POSTGIS_CACHE_MNGR



Da **geoserver/postgis_cache_manager** a **dp/ora_to_pg**

## **PROMPT**

```other
Convert this groovy script to a python script with the same name.
Read the SMTP_MAIL_SERVER var not from configuration.properties file but from .env file.
Use load_dotenv to read the .env file
Create a .py.bat and a .sh file to launch the script in Windows and Ubuntu
Move the vars definition to .env file and read it
```

## ARGPARSE

```other
Use argparse to read input params

Change the management of scheduled using the flags:
-sp --sched-prod
-st --sched-test

You can now run the script using the new argument style, for example:
- python postgis_cache_mngr.py --sched-prod or python postgis_cache_mngr.py -sp
- python postgis_cache_mngr.py --sched-test or python postgis_cache_mngr.py -st
- python postgis_cache_mngr.py --id 56 --update-flag
- python postgis_cache_mngr.py --id L789

WINDOWS
REM Run scheduled task for Production
f:\Geoscripts\geoserver\postgis_cache_mngr.py.bat -sp

REM Run scheduled task for Test (using long flag)
f:\Geoscripts\geoserver\postgis_cache_mngr.py.bat --sched-test

REM Run manually for Map IDs 123 and 456, and update the flag in Oracle
f:\Geoscripts\geoserver\postgis_cache_mngr.py.bat --id 123,456 --update-flag

REM Run manually for Layer ID L789 (update flag is ignored)
f:\Geoscripts\geoserver\postgis_cache_mngr.py.bat --id L789

LINUX
# Run scheduled task for Production (assuming you are in the geoserver directory)
./postgis_cache_mngr.sh -sp

# Run scheduled task for Test (using full path and long flag)
/f/Geoscripts/geoserver/postgis_cache_mngr.sh --sched-test

# Run manually for Map IDs 123 and 456, and update the flag in Oracle
./postgis_cache_mngr.sh --id 123,456 --update-flag

# Run manually for Layer ID L789
./postgis_cache_mngr.sh --id L789
```

## TEST

- Creato dir tests

PROMPT

```other
I created the test dir inside geoserver dir implement a base test suite using pytest

Complete the test suite writing test for all individual functions
```

TEST IN F:\Geoscripts\geoserver\tests\test_postgis_cache_mngr.py

REQUISITI

```other
pip install pytest pytest-mock
```

ESECUZIONE

```other
cd f:\Geoscripts
pytest
```

PROMPT

```other
Best way to make integration tests for some peculiar cases without mocking
```

[https://chatgpt.com/share/680b6d5b-4440-8008-b4e4-5b7a16bb52e0](https://chatgpt.com/share/680b6d5b-4440-8008-b4e4-5b7a16bb52e0)

GEMINI

Okay, let's outline a strategy for creating robust integration tests for your Python script, focusing on peculiar cases *without* mocking the external dependencies (PostgreSQL, Oracle, OGR2OGR, SMTP).

This approach prioritizes testing the *real interactions* but requires significant setup and careful management of the test environment.

**Core Principles:**

1. **Dedicated Test Environment:** Absolutely essential. You need separate, isolated instances of PostgreSQL and Oracle dedicated *only* to running these tests. Never run integration tests against production or shared development databases. Docker is an excellent choice for this (e.g., using `postgres:alpine` and `gvenzl/oracle-xe` images).
2. **Test-Specific Configuration:** Use a separate `.env` file (`.env.test`) pointing to the test databases, a test SMTP server (optional), and potentially a test `GEOSCRIPTS_HOME`. Your test runner should load this configuration.
3. **Controlled Test Data:** Pre-populate your test Oracle database with specific schemas and tables designed to trigger the peculiar cases you want to test. This includes tables that *should* work, tables with invalid geometries, empty tables, tables that don't exist, etc.
4. **State Verification:** Tests will assert conditions by querying the test PostgreSQL database, checking log file contents, and examining the script's exit status or exceptions raised.
5. **Setup and Teardown:** Use a testing framework like `pytest` with fixtures to manage the setup (creating schemas/tables, inserting test data, setting environment vars) and teardown (dropping test objects, cleaning logs) for each test or test suite.
6. **Control External Processes (OGR):** This is the trickiest part without mocking `subprocess`. You might need a *wrapper* script for `ogr2ogr.bat` that you can control during tests.

**Steps and Strategies:**

1. **Test Environment Setup (Docker Preferred):**
    - Use `docker-compose` to define and manage your test PostgreSQL and Oracle containers.
    - Configure them with fixed ports and known credentials.
    - Ensure the Oracle container has the necessary schemas/users available (`VISCARTO`, the users defined in `stringa_conn`, and the main user running the script).
    - Mount volumes if needed for Oracle initialization scripts or data persistence between test runs (though starting fresh is often better).
2. **Test Framework (`pytest`):**
    - Install `pytest`: `pip install pytest psycopg2-binary cx_Oracle python-dotenv`
    - Structure tests in files like `test_integration.py`.
3. **Fixtures for Setup/Teardown (`conftest.py` or test file):**

```python
# conftest.py (or in your test_integration.py)
import pytest
import os
import subprocess
import psycopg2
import cx_Oracle
from dotenv import load_dotenv

# Load test environment variables
load_dotenv(dotenv_path='.env.test', override=True)

# --- Test Database Credentials (Read from .env.test) ---
TEST_PG_HOST = os.getenv("TEST_PG_HOST", "localhost")
TEST_PG_PORT = os.getenv("TEST_PG_PORT", "5433") # Example port
TEST_PG_USER = os.getenv("TEST_PG_USER")
TEST_PG_PWD = os.getenv("TEST_PG_PWD")
TEST_PG_DB_NAME = os.getenv("TEST_PG_DB_NAME")

TEST_ORA_USER = os.getenv("TEST_ORA_USER")
TEST_ORA_PWD = os.getenv("TEST_ORA_PWD")
TEST_ORA_DB_CONN_STR = os.getenv("TEST_ORA_DB_CONN_STR") # e.g., localhost:1521/XE

# --- Test GEOSCRIPTS_HOME ---
# Point to a test-specific directory if needed, e.g., for OGR wrapper
TEST_GEOSCRIPTS_HOME = os.path.join(os.path.dirname(__file__), 'test_geoscripts_home')
os.makedirs(TEST_GEOSCRIPTS_HOME, exist_ok=True)
# Ensure the main script uses this via environment override during tests
os.environ['GEOSCRIPTS_HOME'] = TEST_GEOSCRIPTS_HOME
# Create dummy .env inside test home if needed by script startup logic
with open(os.path.join(TEST_GEOSCRIPTS_HOME, '.env'), 'w') as f:
     # Add *non-sensitive* test config if the script absolutely needs it there
     # Sensitive stuff should still be in .env.test loaded here
     f.write("# Test .env in GEOSCRIPTS_HOME\\n")

@pytest.fixture(scope="session") # Connect once per session
def test_pg_conn():
    print(f"Connecting to TEST PostgreSQL: {TEST_PG_HOST}:{TEST_PG_PORT}/{TEST_PG_DB_NAME}")
    conn = psycopg2.connect(
        host=TEST_PG_HOST, port=TEST_PG_PORT, dbname=TEST_PG_DB_NAME,
        user=TEST_PG_USER, password=TEST_PG_PWD
    )
    conn.autocommit = True
    yield conn
    conn.close()
    print("Closed TEST PostgreSQL connection")

@pytest.fixture(scope="session") # Connect once per session
def test_ora_conn():
    print(f"Connecting to TEST Oracle: {TEST_ORA_DB_CONN_STR}")
    conn = cx_Oracle.connect(
        user=TEST_ORA_USER, password=TEST_ORA_PWD, dsn=TEST_ORA_DB_CONN_STR
    )
    yield conn
    conn.close()
    print("Closed TEST Oracle connection")

@pytest.fixture(scope="function") # Run setup/teardown for each test function
def test_db_setup(test_pg_conn, test_ora_conn):
    # --- SETUP ---
    print("Setting up test schemas and tables...")
    with test_ora_conn.cursor() as ora_cur, test_pg_conn.cursor() as pg_cur:
        # Example: Create PG_CACHE_LAYERS in Oracle
        try:
            ora_cur.execute("""
                CREATE TABLE PG_CACHE_LAYERS (
                    ID_LAYER NUMBER PRIMARY KEY,
                    STRINGA_CONN VARCHAR2(200),
                    TAB_GEOM VARCHAR2(100),
                    EPSG_CODE VARCHAR2(20),
                    PK_FIELD VARCHAR2(100),
                    GEOM_FIELD VARCHAR2(100),
                    POSTGIS_CACHE CHAR(1) DEFAULT 'N',
                    ID_MAP NUMBER, -- Added for map id tests
                    CACHE_SCHEDULATA VARCHAR2(50) -- Added for schedule tests
                )
            """)
        except cx_Oracle.DatabaseError as e:
            if "ORA-00955" in str(e): print("ORA Table PG_CACHE_LAYERS already exists.") # Ignore if exists
            else: raise

        # Example: Create target PG schema
        try:
            pg_cur.execute("CREATE SCHEMA IF NOT EXISTS public") # Ensure public exists
            pg_cur.execute("CREATE SCHEMA IF NOT EXISTS varie") # For post_update test
        except psycopg2.Error as e: print(f"PG Schema setup info: {e}")

        # Example: Create SIT_DB_ISTANZE for get_geom_db testing
        try:
             ora_cur.execute("""
                CREATE TABLE SIT_DB_ISTANZE (
                    ALIAS_NAME VARCHAR2(100) PRIMARY KEY,
                    CONNECTION_STRING VARCHAR2(200)
                )
             """)
             ora_cur.execute("INSERT INTO SIT_DB_ISTANZE (ALIAS_NAME, CONNECTION_STRING) VALUES ('TESTALIAS', :conn_str)", {'conn_str': TEST_ORA_DB_CONN_STR}) # Point to itself for testing
        except cx_Oracle.DatabaseError as e:
            if "ORA-00955" in str(e): print("ORA Table SIT_DB_ISTANZE already exists.")
            else: raise

        # Example: Create LOG_CACHE_PG for write_db_log testing
        try:
             ora_cur.execute("""
                 CREATE TABLE LOG_CACHE_PG (
                    LOG_DATE TIMESTAMP,
                    CONNECTION_STRING VARCHAR2(200),
                    TABLE_NAME VARCHAR2(100),
                    EXEC_TIME_MIN NUMBER,
                    INSTANCE VARCHAR2(10)
                )
             """)
        except cx_Oracle.DatabaseError as e:
             if "ORA-00955" in str(e): print("ORA Table LOG_CACHE_PG already exists.")
             else: raise

        test_ora_conn.commit()

    yield # Test runs here

    # --- TEARDOWN ---
    print("Tearing down test schemas and tables...")
    with test_ora_conn.cursor() as ora_cur, test_pg_conn.cursor() as pg_cur:
        # Drop Oracle test tables (source data) created within tests
        tables_to_drop_ora = ["TEST_GOOD_TABLE", "TEST_INVALID_GEOM", "TEST_EMPTY_TABLE", "V_SIS_INSTAB_PUB"] # Add any other test tables
        for table in tables_to_drop_ora:
            try: ora_cur.execute(f"DROP TABLE {table} PURGE")
            except cx_Oracle.DatabaseError as e:
                if "ORA-00942" not in str(e): print(f"Warn: Could not drop ORA table {table}: {e}")

        # Drop PG tables created by the script
        # Careful: Determine schema and table name dynamically if needed
        tables_to_drop_pg = ["test_user_test_good_table", "test_user_test_invalid_geom", "test_user_test_empty_table", "pgr_grandi_piccole_deriv_idr"] # Add others
        for table in tables_to_drop_pg:
             try: pg_cur.execute(f"DROP TABLE IF EXISTS public.{table} CASCADE")
             except psycopg2.Error as e: print(f"Warn: Could not drop PG table public.{table}: {e}")
        try: pg_cur.execute(f"DROP VIEW IF EXISTS public.pgr_grandi_piccole_deriv_idr CASCADE") # Drop view specifically
        except psycopg2.Error as e: print(f"Warn: Could not drop PG view public.{e}")
        try: pg_cur.execute(f"DROP VIEW IF EXISTS varie.pgr_v_sis_instab_pub CASCADE")
        except psycopg2.Error as e: print(f"Warn: Could not drop PG view varie.{e}")

        # Clear control tables
        ora_cur.execute("DELETE FROM PG_CACHE_LAYERS")
        ora_cur.execute("DELETE FROM LOG_CACHE_PG")
        # Don't drop SIT_DB_ISTANZE here if it's session-scoped fixture setup
        test_ora_conn.commit()

    # Clean up log files (adjust path based on script's logic)
    log_dir = os.path.join(TEST_GEOSCRIPTS_HOME, '_log', 'geoserver')
    if os.path.exists(log_dir):
        for f in os.listdir(log_dir):
            if f.startswith('postgis_cache_mngr_') and f.endswith('.log'):
                os.remove(os.path.join(log_dir, f))
        # Optionally remove main log too, or clear it
        # if os.path.exists(MAIN_LOG_FILE_PATH): os.remove(MAIN_LOG_FILE_PATH)
    print("Teardown complete.")

# Fixture to provide path to a controllable OGR script
@pytest.fixture
def ogr_wrapper_path():
    wrapper_content = """
			@echo off
			REM Simple OGR2OGR Wrapper for testing
			echo Running Test OGR Wrapper with args: %* >> test_ogr_wrapper.log
			
			REM --- SIMULATE SUCCESS (DEFAULT) ---
			REM Simulating ogr2ogr success - replace with actual ogr2ogr if testing real execution
			REM "C:\\path\\to\\real\\ogr2ogr.exe" %*
			echo OGR Simulation: Success >> test_ogr_wrapper.log
			exit /b 0
			
			REM --- EXAMPLE: SIMULATE FAILURE based on input table ---
			REM if "%6"=="OCI:test_user/pwd@test_host:1521/XE:TEST_FAIL_TABLE" (
			REM     echo OGR Simulation: Specific Table Failure! >&2
			REM     echo ORA-12345: Simulated Oracle Error >&2
			REM     exit /b 1
			REM )
			
			REM --- EXAMPLE: SIMULATE ORA-13208 ---
			REM if "%6"=="OCI:test_user/pwd@test_host:1521/XE:TEST_ORA13208_TABLE" (
			REM     echo OGR Simulation: Triggering ORA-13208 >&2
			REM     echo ORA-13208: internal error while evaluating [MDSYS.SDO_AGGR_CENTROID] >&2
			REM     exit /b 1 REM OGR might exit 0 or 1, but script checks stderr
			REM )
			
			REM --- EXAMPLE: SIMULATE TIMEOUT ---
			REM if "%6"=="OCI:test_user/pwd@test_host:1521/XE:TEST_TIMEOUT_TABLE" (
			REM     echo OGR Simulation: Sleeping to cause timeout...
			REM     timeout /t 90 /nobreak > NUL
			REM     echo OGR Simulation: Sleep finished (should have timed out)
			REM     exit /b 0
			REM )
    """
    wrapper_path = os.path.join(TEST_GEOSCRIPTS_HOME, "OGR2OGR.bat")
    with open(wrapper_path, "w") as f:
        f.write(wrapper_content)
    # Clean up log from previous runs
    log_path = os.path.join(os.getcwd(), "test_ogr_wrapper.log") # Log in CWD
    if os.path.exists(log_path): os.remove(log_path)

    yield wrapper_path # Provide the path to the test

    # Optional: cleanup the wrapper log file after test
    # if os.path.exists(log_path): os.remove(log_path)
```

```other

```

1. **Writing Tests for Peculiar Cases (`test_integration.py`):**

```python
# test_integration.py
import pytest
import os
import sys
from datetime import datetime
# Import the script containing the main function (adjust import path)
# e.g., from .. import your_script_name as cache_manager
import postgis_cache_mngr as cache_manager # Assuming the script is named this

# Helper to run the script's main function
def run_script(args):
    # Modify sys.argv temporarily or pass args to main if possible
    original_argv = sys.argv
    # Use test .env automatically via fixture setup / load_dotenv
    # Run main, capturing SystemExit if it occurs
    try:
        print(f"\\n--- Running script with args: {args} ---")
        # Ensure GEOSCRIPTS_HOME is set from fixture
        print(f"GEOSCRIPTS_HOME for script run: {os.getenv('GEOSCRIPTS_HOME')}")
        cache_manager.main(args_list=args) # Pass args directly
        print("--- Script finished normally ---")
        return 0 # Indicate normal exit
    except SystemExit as e:
        print(f"--- Script exited with code: {e.code} ---")
        return e.code # Return exit code
    except Exception as e:
         print(f"--- Script failed with exception: {e} ---")
         pytest.fail(f"Script raised unhandled exception: {e}") # Fail test

# --- Test Case: Successful Run for a Specific Map ID ---
def test_successful_map_id_run(test_db_setup, test_ora_conn, test_pg_conn, ogr_wrapper_path):
    # Arrange: Setup Oracle source table and PG_CACHE_LAYERS entry
    ora_user = os.getenv("TEST_ORA_USER").upper() # Get Oracle user for schema name
    pg_target_table = f"public.{ora_user.lower()}_test_good_table" # Predicted PG table name
    with test_ora_conn.cursor() as ora_cur:
        ora_cur.execute(f"""
            CREATE TABLE TEST_GOOD_TABLE (
                ID NUMBER PRIMARY KEY,
                NAME VARCHAR2(50),
                GEOM SDO_GEOMETRY -- Assuming SDO_GEOMETRY
            )
        """)
        # Insert valid data (adjust geometry creation for your Oracle setup)
        ora_cur.execute("INSERT INTO TEST_GOOD_TABLE (ID, NAME, GEOM) VALUES (1, 'Feature 1', SDO_GEOMETRY(2001, 4326, SDO_POINT_TYPE(10, 20, NULL), NULL, NULL))")
        ora_cur.execute("INSERT INTO PG_CACHE_LAYERS (ID_LAYER, STRINGA_CONN, TAB_GEOM, EPSG_CODE, PK_FIELD, GEOM_FIELD, ID_MAP, POSTGIS_CACHE, CACHE_SCHEDULATA) VALUES (101, :cs, 'TEST_GOOD_TABLE', '4326', 'ID', 'GEOM', 123, 'S', 'P_DAILY')",
                        {'cs': f'{os.getenv("TEST_ORA_USER")}/{os.getenv("TEST_ORA_PWD")}@{os.getenv("TEST_ORA_DB_CONN_STR")}'}) # Use test credentials/DSN
        test_ora_conn.commit()

    # Act: Run the script for map ID 123
    exit_code = run_script(['--id', '123'])

    # Assert
    assert exit_code == 0
    # Check if PG table exists and has data
    with test_pg_conn.cursor() as pg_cur:
        pg_cur.execute(f"SELECT COUNT(*) FROM {pg_target_table}")
        assert pg_cur.fetchone()[0] == 1
        pg_cur.execute(f"SELECT name FROM {pg_target_table} WHERE id = 1")
        assert pg_cur.fetchone()[0] == 'Feature 1'
    # Check Oracle log table
    with test_ora_conn.cursor() as ora_cur:
        ora_cur.execute("SELECT COUNT(*) FROM LOG_CACHE_PG WHERE TABLE_NAME = 'TEST_GOOD_TABLE'")
        assert ora_cur.fetchone()[0] == 1
    # Check log file content (more complex, requires reading the generated log)
    # log_path = find_latest_log_file(...)
    # with open(log_path, 'r') as f: assert "IMPORT OK" in f.read()

# --- Test Case: OGR Failure (Simulated via Wrapper) ---
def test_ogr_failure(test_db_setup, test_ora_conn, ogr_wrapper_path):
     # Arrange: Setup Oracle table, PG_CACHE entry for a table that wrapper will fail
     # Modify ogr_wrapper_path content *before* this test runs if needed,
     # or have wrapper detect table name like "TEST_FAIL_TABLE"
    with test_ora_conn.cursor() as ora_cur:
        ora_cur.execute("CREATE TABLE TEST_FAIL_TABLE (ID NUMBER PRIMARY KEY)") # Dummy table
        ora_cur.execute("INSERT INTO PG_CACHE_LAYERS (ID_LAYER, STRINGA_CONN, TAB_GEOM, EPSG_CODE, PK_FIELD, GEOM_FIELD, ID_MAP) VALUES (102, :cs, 'TEST_FAIL_TABLE', '4326', 'ID', NULL, 456)",
                        {'cs': f'{os.getenv("TEST_ORA_USER")}/{os.getenv("TEST_ORA_PWD")}@{os.getenv("TEST_ORA_DB_CONN_STR")}'})
        test_ora_conn.commit()

     # IMPORTANT: Modify the ogr_wrapper_path content or ensure it's pre-set
     # to fail for 'TEST_FAIL_TABLE'. E.g., uncomment the failure simulation block.
     # This usually requires test parameterization or modifying the fixture dynamically.
     # For simplicity here, assume the wrapper has the fail logic uncommented.

     # Act: Run the script
     exit_code = run_script(['--id', '456'])

     # Assert
     assert exit_code == 1 # Script should exit with error
     # Check that error was logged (requires log file parsing)
     # Check that PG table was NOT created or is empty
     # Check that specific error email *would* be sent (check logs for send_mail call)

# --- Test Case: Invalid Geometry Handling ---
def test_invalid_geometry(test_db_setup, test_ora_conn, test_pg_conn, ogr_wrapper_path):
    # Arrange: Create Oracle table with invalid self-intersecting polygon
    ora_user = os.getenv("TEST_ORA_USER").upper()
    pg_target_table = f"public.{ora_user.lower()}_test_invalid_geom"
    with test_ora_conn.cursor() as ora_cur:
        ora_cur.execute("CREATE TABLE TEST_INVALID_GEOM (ID NUMBER PRIMARY KEY, GEOM SDO_GEOMETRY)")
        # Insert invalid polygon (bow-tie) - Adjust SRID and syntax as needed
        ora_cur.execute("""
            INSERT INTO TEST_INVALID_GEOM (ID, GEOM) VALUES (
                1,
                SDO_GEOMETRY(2003, 4326, NULL, SDO_ELEM_INFO_ARRAY(1, 1003, 1),
                             SDO_ORDINATE_ARRAY(0,0, 10,10, 0,10, 10,0, 0,0))
            )
        """)
        ora_cur.execute("INSERT INTO PG_CACHE_LAYERS (ID_LAYER, STRINGA_CONN, TAB_GEOM, EPSG_CODE, PK_FIELD, GEOM_FIELD, ID_MAP) VALUES (103, :cs, 'TEST_INVALID_GEOM', '4326', 'ID', 'GEOM', 789)",
                         {'cs': f'{os.getenv("TEST_ORA_USER")}/{os.getenv("TEST_ORA_PWD")}@{os.getenv("TEST_ORA_DB_CONN_STR")}'})
        test_ora_conn.commit()

    # Act
    exit_code = run_script(['--id', '789'])

    # Assert
    assert exit_code == 0 # Should succeed after validation
    # Check PG table - query ST_IsValid and ST_GeometryType
    with test_pg_conn.cursor() as pg_cur:
         pg_cur.execute(f"SELECT COUNT(*) FROM {pg_target_table}")
         assert pg_cur.fetchone()[0] == 1
         # Check if geometry is now valid and potentially a MultiPolygon
         pg_cur.execute(f"SELECT ST_IsValid(wkb_geometry), ST_GeometryType(wkb_geometry) FROM {pg_target_table} WHERE id = 1")
         is_valid, geom_type = pg_cur.fetchone()
         assert is_valid is True
         # MakeValid might turn it into a MultiPolygon
         assert geom_type in ('ST_Polygon', 'ST_MultiPolygon')
    # Check logs for "BONIFICA GEOMETRIE" messages

# --- Test Case: Oracle/PG Count Mismatch (Difficult to force reliably) ---
# This might require manually intervening after OGR runs but before the script checks counts,
# or modifying the OGR wrapper to simulate dropping records.
# Test would assert that the WARNING log about mismatch appears.

# --- Test Case: OGR Timeout (Simulated via Wrapper) ---
# Similar to OGR failure, modify wrapper to sleep longer than script timeout.
# Assert exit code 1 and check logs for "timed out" message.

# --- Test Case: Handling Non-Existent Oracle Table ---
def test_missing_oracle_table(test_db_setup, test_ora_conn, ogr_wrapper_path):
    # Arrange: Add entry for a table that *does not* exist in Oracle
    with test_ora_conn.cursor() as ora_cur:
         ora_cur.execute("INSERT INTO PG_CACHE_LAYERS (ID_LAYER, STRINGA_CONN, TAB_GEOM, EPSG_CODE, PK_FIELD, GEOM_FIELD, ID_MAP) VALUES (104, :cs, 'NON_EXISTENT_TABLE', '4326', 'ID', 'GEOM', 111)",
                         {'cs': f'{os.getenv("TEST_ORA_USER")}/{os.getenv("TEST_ORA_PWD")}@{os.getenv("TEST_ORA_DB_CONN_STR")}'})
         test_ora_conn.commit()

    # Act
    exit_code = run_script(['--id', '111'])

    # Assert
    assert exit_code == 1 # Should fail because OGR will error
    # Check logs for OGR errors about table not found.
    # Check that specific error email would be sent.

# --- Test Case: Scheduled Run ---
def test_scheduled_run(test_db_setup, test_ora_conn, test_pg_conn, ogr_wrapper_path):
    # Arrange: Setup like successful run, but use CACHE_SCHEDULATA field
    ora_user = os.getenv("TEST_ORA_USER").upper()
    pg_target_table = f"public.{ora_user.lower()}_test_good_table" # Reusing table name
    with test_ora_conn.cursor() as ora_cur:
        # Recreate or ensure table exists if previous tests dropped it
        try: ora_cur.execute(f"CREATE TABLE TEST_GOOD_TABLE (ID NUMBER PRIMARY KEY, NAME VARCHAR2(50), GEOM SDO_GEOMETRY)")
        except: pass # Ignore if exists
        ora_cur.execute("DELETE FROM TEST_GOOD_TABLE") # Clear previous data
        ora_cur.execute("INSERT INTO TEST_GOOD_TABLE (ID, NAME, GEOM) VALUES (2, 'Scheduled Feature', SDO_GEOMETRY(2001, 4326, SDO_POINT_TYPE(30, 40, NULL), NULL, NULL))")
        ora_cur.execute("UPDATE PG_CACHE_LAYERS SET POSTGIS_CACHE = 'S', CACHE_SCHEDULATA = 'P_DAILY' WHERE ID_LAYER = 101") # Assuming layer 101 exists from previous test setup or create new
        test_ora_conn.commit()

    # Act: Run scheduled for Production ('P')
    exit_code = run_script(['-sp'])

    # Assert
    assert exit_code == 0
    with test_pg_conn.cursor() as pg_cur:
        pg_cur.execute(f"SELECT COUNT(*) FROM {pg_target_table}")
        assert pg_cur.fetchone()[0] == 1 # Should have imported the row
        pg_cur.execute(f"SELECT name FROM {pg_target_table} WHERE id = 2")
        assert pg_cur.fetchone()[0] == 'Scheduled Feature'
    # Check logs for scheduled run messages and email sending intent (OK email)

# --- Test Case: Post Update View Creation ---
def test_post_update(test_db_setup, test_pg_conn, ogr_wrapper_path):
     # Arrange: Create the source tables/views needed for the post_update views in PG
     # These might be imported by a prerequisite test or set up here directly.
     # For simplicity, create empty dummy tables in the correct PG schemas.
     with test_pg_conn.cursor() as pg_cur:
         pg_cur.execute("CREATE TABLE IF NOT EXISTS public.genioweb_rl_s3_punti_de_view_gd (id int, codice_pratica text, denominazione text, wkb_geometry geometry, tipo_uso text, descrizione_stato_prat text)")
         pg_cur.execute("CREATE TABLE IF NOT EXISTS public.genioweb_rl_s3_punti_de_view_pd (id int, codice_pratica text, denominazione text, wkb_geometry geometry, tipo_uso text, descrizione_stato_prat text)")
         pg_cur.execute("CREATE TABLE IF NOT EXISTS varie.v_sis_instab_pub (id int, id_i int, tipo_i int, decodifica text, cod_com text, flag_validazione text, frt text, frr text, il text, disl text, fa text, fv text, ft text, fh0105 text, fh0515 text, fpga text, fa0105 text, fa0408 text, fa0711 text, spettri text, livello text, cat text, amb text, li text, valore_f text, tipo_f text, versione_standard text, wkb_geometry geometry, tipo_i_sempl text)")

     # Act: Run a minimal script execution that triggers post_update
     # (e.g., run with an ID that imports nothing but allows script to finish)
     exit_code = run_script(['--id', '99999']) # Assume ID 99999 doesn't exist in PG_CACHE_LAYERS

     # Assert
     assert exit_code == 0 # Should still succeed overall
     # Check if views exist in PostgreSQL
     with test_pg_conn.cursor() as pg_cur:
         pg_cur.execute("SELECT 1 FROM information_schema.views WHERE table_schema = 'public' AND table_name = 'pgr_grandi_piccole_deriv_idr'")
         assert pg_cur.fetchone() is not None
         pg_cur.execute("SELECT 1 FROM information_schema.views WHERE table_schema = 'varie' AND table_name = 'pgr_v_sis_instab_pub'")
         assert pg_cur.fetchone() is not None

# Add more tests for:
# - Different argument combinations (--id Lxxx, --update-flag)
# - Connection errors (by providing bad credentials in .env.test)
# - get_geom_db failures (invalid stringa_conn format, alias not in SIT_DB_ISTANZE)
# - get_dim failures (missing metadata, invalid geom column)
# - Email sending (less critical if logging is checked, maybe just check logs for "Sending email" / "Failed to send email")
```

**Considerations and Trade-offs:**

- **Complexity:** This is significantly more complex to set up and maintain than unit tests with mocks. Database schema changes require updating test setup.
- **Speed:** Integration tests are slow. Running against real databases and external processes takes time.
- **Fragility:** Tests can fail due to transient issues in the test environment (network glitches, container issues) not related to the script's code.
- **OGR Wrapper:** The dummy `OGR2OGR.bat` wrapper is crucial for controlling OGR's behavior (simulating errors, timeouts) without mocking `subprocess`. You'll need to make it sophisticated enough to handle different test cases, perhaps by checking input arguments or reading a configuration file.
- **Email:** Testing actual email sending is often skipped in CI. You can:
    - Check log messages indicating an attempt to send.
    - Use a local SMTP debugging server (like `python -m smtpd -c DebuggingServer -n localhost:1025`) and configure the script (`.env.test`) to send there, then verify the output.
    - Accept that email sending isn't fully integration-tested without a dedicated test mail server.
- **Resource Intensive:** Requires running two database instances.

This non-mocking approach provides the highest confidence that your script works correctly with its real dependencies, but it comes at the cost of increased complexity and slower execution. Choose the specific "peculiar cases" that provide the most value to test this way.



# RQA


Porting script RQA in python

## SCRIPT

Creato file .env

BAT

F:\geoscripts\rqa\load_postgis_full.bat (schedulazione a ore 1)

\rqa\load_postgis.bat
\rqa\load_postgis_cor_mv.bat
\rqa\download.bat

F:\Geoscripts\rqa\load_postgis_cor.bat (schedulazione a ore 7 e ore 16)

F:\geoscripts\rqa\load_postgis_corsto_aa.bat (1 volta all’anno)

F:\geoscripts\rqa\load_postgis_corsto_gg.bat (1 volta all’anno)

**GROOVY**

- load_postgis.groovy → load_postgis.py
- load_postgis_cor_mv.groovy
- download.groovy
- load_postgis_cor.groovy
- load_postgis_corsto_aa.groovy
- load_postgis_corsto_gg.groovy

**PROMPT**

```other
Convert this groovy script to a python script with the same name.
Read the pg_host var not from input arg but from the pgHost entry 
in configuration.properties file.
Change references to config.properties to the file .env and populate 
the .env file with the required referenced variables from config.properties.
```
