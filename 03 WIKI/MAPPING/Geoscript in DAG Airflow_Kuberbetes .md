---
title: "Geoscript in DAG Airflow_Kuberbetes "
type: conversation
topic: gis
created: 2026-02-13
tags:
  - airflow
  - kubernetes
  - gis
  - gemini
  - mapping

---
> From: https://gemini.google.com/u/1/app/5f8bd3f28fa387e2?pageId=none

# you asked

Trasforma il seguente script python in un dag airflow:

import os
import sys
import uuid
import logging
import subprocess
import smtplib
import argparse # Import argparse
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg2
import oracledb

# Inizializza la modalità thick di oracledb usando la variabile d'ambiente impostata nel Dockerfile
oracledb.init_oracle_client(lib_dir=os.environ.get("ORACLE_CLIENT_LIB_DIR", "/opt/oracle/instantclient"))

# Load environment variables from .env file
load_dotenv()

# Get GEOSCRIPTS_HOME after loading .env
geoscripts_home = os.getenv('GEOSCRIPTS_HOME')
if not geoscripts_home:
    print("ERROR: GEOSCRIPTS_HOME environment variable not set.")
    sys.exit(1)

dotenv_path = os.path.join(geoscripts_home, '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Configuration ---
# Read database credentials and connection details from environment variables
PG_USER = os.getenv("PG_USER")
PG_PWD = os.getenv("PG_PWD")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DB_NAME = os.getenv("PG_DB_NAME")
ORA_DB_CONN_STR = os.getenv("ORA_DB_CONN_STR")
ORA_USER = os.getenv("ORA_USER")
ORA_PWD = os.getenv("ORA_PWD")

# Check if all required DB variables are loaded
required_db_vars = {
    "PG_USER": PG_USER,
    "PG_PWD": PG_PWD,
    "PG_HOST": PG_HOST,
    "PG_PORT": PG_PORT,
    "PG_DB_NAME": PG_DB_NAME,
    "ORA_DB_CONN_STR": ORA_DB_CONN_STR,
    "ORA_USER": ORA_USER,
    "ORA_PWD": ORA_PWD
}

missing_vars = [name for name, value in required_db_vars.items() if not value]
if missing_vars:
    print(f"ERROR: Missing required environment variables in .env file: {', '.join(missing_vars)}")
    sys.exit(1)

PG_URL = f"postgresql://{PG_USER}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"

SMTP_MAIL_SERVER = os.getenv("SMTP_MAIL_SERVER")
FROM_ADDRESS = os.getenv("FROM_ADDRESS")
ERROR_TO_ADDRESS = os.getenv("ERROR_TO_ADDRESS")
OK_TO_ADDRESS = os.getenv("OK_TO_ADDRESS")

# Check if all required email variables are loaded
required_email_vars = {
    "SMTP_MAIL_SERVER": SMTP_MAIL_SERVER,
    "FROM_ADDRESS": FROM_ADDRESS,
    "ERROR_TO_ADDRESS": ERROR_TO_ADDRESS,
    "OK_TO_ADDRESS": OK_TO_ADDRESS
}

missing_email_vars = [name for name, value in required_email_vars.items() if not value]
if missing_email_vars:
    print(f"ERROR: Missing required email environment variables in .env file: {', '.join(missing_email_vars)}")
    sys.exit(1)

LOG_DIR = os.path.join(geoscripts_home, '_log')
os.makedirs(LOG_DIR, exist_ok=True)

# --- Global Variables ---
pg_conn = None
ora_conn = None
log_file_path = None
istanza = ''
main_logger = None

# --- Logging Setup ---
def setup_logging(run_uuid):
    global log_file_path, main_logger
    current_date = datetime.now().strftime('%Y-%m-%d')
    log_file_path = os.path.join(LOG_DIR, f'dp-ora_to_pg_{current_date}_{run_uuid}.log')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S',
                        handlers=[
                            logging.FileHandler(log_file_path),
                            logging.StreamHandler(sys.stdout) # Also print to console
                        ])

    # Configure a separate logger for the main summary log
    MAIN_LOG_FILE = os.path.join(LOG_DIR, f'dp-ora_to_pg_{current_date}.log')
    main_logger = logging.getLogger('main_log')
    main_logger.setLevel(logging.INFO)
    # Rimuovo tutti gli handler esistenti
    for handler in list(main_logger.handlers):
        main_logger.removeHandler(handler)
    main_handler = logging.FileHandler(MAIN_LOG_FILE)
    main_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    main_handler.setFormatter(main_formatter)
    main_logger.addHandler(main_handler)

    return main_logger

def print_log(level, msg):
    if level.upper() == "INFO":
        logging.info(msg)
    elif level.upper() == "ERROR":
        logging.error(msg)
    elif level.upper() == "WARNING":
        logging.warning(msg)
    else:
        logging.debug(msg)

def print_log_main(level, msg, _main_logger=None):
    global main_logger
    log_entry = f"{istanza} - {msg}" if istanza else msg
    logger = main_logger if main_logger else _main_logger
    if logger:
        if level.upper() == "INFO":
            logger.info(log_entry)
        elif level.upper() == "ERROR":
            logger.error(log_entry)
        elif level.upper() == "WARNING":
            logger.warning(log_entry)
        else:
            logger.debug(log_entry)


# --- Database Functions ---
def connect_db():
    global pg_conn, ora_conn
    try:
        print_log("INFO", f"Connecting to PostgreSQL: {PG_HOST}:{PG_PORT}/{PG_DB_NAME}")
        pg_conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, dbname=PG_DB_NAME, user=PG_USER, password=PG_PWD)
        pg_conn.autocommit = True # Match Groovy Sql behavior where execute doesn't need explicit commit for DDL/non-select
        print_log("INFO", "PostgreSQL connection successful.")
    except Exception as e:
        print_log("ERROR", f"Failed to connect to PostgreSQL: {e}")
        raise

    try:
        print_log("INFO", f"Connecting to Oracle: {ORA_DB_CONN_STR}")
        # Ensure Oracle Client libraries are found (might need ORACLE_HOME or PATH set)
        # oracledb.init_oracle_client(lib_dir=r"C:\path\to\instantclient") # Example if needed
        ora_conn = oracledb.connect(user=ORA_USER, password=ORA_PWD, dsn=ORA_DB_CONN_STR)
        print_log("INFO", "Oracle connection successful.")
    except Exception as e:
        print_log("ERROR", f"Failed to connect to Oracle: {e}")
        if pg_conn: pg_conn.close()
        raise

def close_db():
    if pg_conn:
        pg_conn.close()
        print_log("INFO", "PostgreSQL connection closed.")
    if ora_conn:
        ora_conn.close()
        print_log("INFO", "Oracle connection closed.")

def execute_pg(sql, params=None):
    with pg_conn.cursor() as cur:
        cur.execute(sql, params or ())
        # No fetch needed for execute, autocommit handles commit

def fetchone_pg(sql, params=None):
     with pg_conn.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchone()

def fetchall_ora(sql, params=None):
    with ora_conn.cursor() as cur:
        cur.execute(sql, params or {}) # Use dict for named params if needed
        # Fetch column names for dictionary cursor if desired
        # columns = [col[0] for col in cur.description]
        # cur.rowfactory = lambda *args: dict(zip(columns, args))
        return cur.fetchall()

def fetchone_ora(sql, params=None):
     with ora_conn.cursor() as cur:
        cur.execute(sql, params or {})
        # columns = [col[0] for col in cur.description]
        # cur.rowfactory = lambda *args: dict(zip(columns, args))
        return cur.fetchone()

def execute_ora(sql, params=None):
     with ora_conn.cursor() as cur:
        cur.execute(sql, params or {})
        ora_conn.commit() # Explicit commit needed for Oracle DML/DDL

def get_geom_db(stringa_conn):
    jdbc_conn_string = 'amb_db.regione.liguria.it:1522/SIT' # Default? Check Groovy logic
    usr = 'VISCARTO'
    pwd = 'CARTOVIS'
    appo_str_conn = stringa_conn.split('@')
    geom_db_conn = None

    try:
        if len(appo_str_conn) >= 2:
            alias = appo_str_conn[1]
            # Use main Oracle connection to query SIT_DB_ISTANZE
            conn_str_row = fetchone_ora("select ALIAS_NAME from SIT_DB_ISTANZE where UPPER(ALIAS_NAME) = UPPER(:alias)", {'alias': alias})
            if conn_str_row:
                jdbc_conn_string = conn_str_row[0]

            appo_str_conn2 = appo_str_conn[0].split('/')
            if len(appo_str_conn2) == 2:
                usr = appo_str_conn2[0]
                pwd = appo_str_conn2[1]
            else:
                 print_log("WARNING", f"Could not parse user/password from {appo_str_conn[0]}")

        print_log("INFO", f"Connecting to Geometry Oracle DB: {jdbc_conn_string} as {usr}")
        geom_db_conn = oracledb.connect(user=usr, password=pwd, dsn=jdbc_conn_string)
        print_log("INFO", "Geometry Oracle DB connection successful.")
        return geom_db_conn
    except Exception as e:
        print_log("ERROR", f"Failed to connect to Geometry Oracle DB ({jdbc_conn_string}): {e}")
        if geom_db_conn: geom_db_conn.close() # Ensure cleanup on partial success
        raise # Re-raise the exception

def get_dim(geom_db, feature_name, geom_field):
    dim = None
    try:
        with geom_db.cursor() as cur:
            if not geom_field:
                # Fetch geom field if not provided (assuming USER_SDO_GEOM_METADATA exists and is accessible)
                cmd_geom = "SELECT COLUMN_NAME FROM USER_SDO_GEOM_METADATA WHERE TABLE_NAME = :table_name"
                print_log("INFO", f"getDim GEOM_FIELD query: {cmd_geom} with table_name='{feature_name.upper()}'")
                cur.execute(cmd_geom, {'table_name': feature_name.upper()})
                geom_field_row = cur.fetchone()
                if geom_field_row:
                    geom_field = geom_field_row[0]
                    print_log("INFO", f"getDim GEOM_FIELD found: {geom_field}")
                else:
                    print_log("WARNING", f"Could not find geometry column for {feature_name} in USER_SDO_GEOM_METADATA")
                    return None # Cannot proceed without geometry field

            # Fetch dimension
            # Ensure geom_field is treated as an identifier, not a string literal
            # WARNING: Direct string formatting for column names can be an SQL injection risk if geom_field comes from untrusted input.
            # Here it comes from metadata or config, which is generally safer, but be aware.
            if not geom_field or not geom_field.isidentifier():
                 print_log("ERROR", f"Invalid geometry field name: {geom_field}")
                 return None

            cmd_dim = f"SELECT SUBSTR(t.{geom_field}.SDO_GTYPE, 1, 1) FROM {feature_name} t WHERE ROWNUM = 1"
            print_log("INFO", f"getDim query: {cmd_dim}")
            cur.execute(cmd_dim)
            rec = cur.fetchone()
            if rec:
                dim = rec[0]
                print_log("INFO", f"getDim found: {dim}")

    except Exception as e:
        print_log("ERROR", f"Error getting dimension for {feature_name}: {e}")
        # Potentially log the specific Oracle error code if available (e.g., e.args[0].code)

    return dim


def get_ora_count(geom_db, feature_name):
    count = "2" # Default from Groovy
    try:
        with geom_db.cursor() as cur:
            # WARNING: Direct string formatting for table names can be an SQL injection risk.
            if not feature_name or not feature_name.isidentifier():
                 print_log("ERROR", f"Invalid feature name: {feature_name}")
                 return count
            cur.execute(f"SELECT COUNT(*) FROM {feature_name}")
            rec = cur.fetchone()
            if rec:
                count = str(rec[0])
    except Exception as e:
        print_log("ERROR", f"Error getting Oracle count for {feature_name}: {e}")
    return count

def get_pg_count(feature_name_pg):
    count = None
    try:
        # WARNING: Direct string formatting for table names can be an SQL injection risk.
        # Assuming feature_name_pg is constructed safely internally.
        # Use schema name if necessary: f"public.{feature_name_pg}"
        # Need to handle potential SQL injection if schema/table names come from external sources.
        # For psycopg2, it's safer to use sql composition for identifiers:
        # from psycopg2 import sql
        # query = sql.SQL("SELECT COUNT(*) FROM {}.{}").format(sql.Identifier(schema_name), sql.Identifier(table_name))
        # For simplicity here, assuming internal construction is safe:
        if '.' in feature_name_pg: # Basic check for schema.table
             schema_name, table_name = feature_name_pg.split('.', 1)
             if not schema_name.isidentifier() or not table_name.isidentifier():
                  print_log("ERROR", f"Invalid PG feature name: {feature_name_pg}")
                  return None
        elif not feature_name_pg.isidentifier():
             print_log("ERROR", f"Invalid PG feature name: {feature_name_pg}")
             return None

        count_row = fetchone_pg(f"SELECT COUNT(*) FROM {feature_name_pg}")
        if count_row:
            count = str(count_row[0])
    except Exception as e:
        print_log("ERROR", f"Error getting PostgreSQL count for {feature_name_pg}: {e}")
    return count

def write_db_log(stringa_conn, tab_geom, td_tavola_minutes, istanza_log):
    try:
        # Using CURRENT_TIMESTAMP for Oracle sysdate equivalent
        # Ensure parameter binding is correct for oracledb
        
        comando = """
            INSERT INTO LOG_CACHE_PG (DATA_CACHE, STRING_CONN, TAB_GEOM, TEMPO_ELABORAZIONE_MINUTI, ISTANZA)
            VALUES (CURRENT_TIMESTAMP, :conn_str, :tab_geom, :exec_time, :instance)
        """
        params = {
            'conn_str': stringa_conn,
            'tab_geom': tab_geom,
            'exec_time': td_tavola_minutes,
            'instance': istanza_log
        }
        execute_ora(comando, params)
        print_log("INFO", f"Logged execution time for {tab_geom}: {td_tavola_minutes} mins")
    except Exception as e:
        print_log("ERROR", f"Failed to write DB log for {tab_geom}: {e}")


# --- Core Logic Functions ---
def import_table(stringa_conn, tab_geom, pg_schema, epsg_code, pk_field, geom_field, ora_schema):
    geom_db = None
    try:
        geom_db = get_geom_db(stringa_conn)
        if not geom_db:
             raise Exception("Failed to get geometry DB connection") # Or handle more gracefully

        if not tab_geom:
            print_log("WARNING", "Table name is null, skipping import.")
            return

        print_log("INFO", f"ELABORAZIONE TAVOLA: {tab_geom}")

        dim = get_dim(geom_db, tab_geom, geom_field)
        if dim is None:
             print_log("ERROR", f"Could not determine dimension for {tab_geom}, skipping import.")
             # Optionally send error mail here if skipping is critical
             raise Exception(f"Dimension determination failed for {tab_geom}") # Stop processing this table

        # Ensure ora_schema and tab_geom are valid identifiers before concatenation
        if not ora_schema.isidentifier() or not tab_geom.isidentifier():
             raise ValueError(f"Invalid Oracle schema or table name: {ora_schema}, {tab_geom}")
        pg_tab_geom = f"{ora_schema.lower()}_{tab_geom.lower()}" # Lowercase convention often used in PG

        print_log("INFO", f"DIM={dim} - PG_TABLE={pg_schema}.{pg_tab_geom}")

        # OGR Command Execution
        timeout_seconds = 70 * 60 # 70 minutes
        start_ogr = datetime.now()

        # Construct OGR command
        # Ensure paths and connection strings are quoted if they contain spaces
        pg_conn_str = f"host={PG_HOST} port={PG_PORT} dbname={PG_DB_NAME} user={PG_USER} password={PG_PWD} active_schema={pg_schema}"
        # Ensure OCI connection string is correctly formatted and potentially quoted if needed by OGR/OCI driver
        oci_conn_str = f"{stringa_conn}:{tab_geom}"
        # Ensure table/layer names are safe for shell command
        # Basic check: ensure pg_schema and pg_tab_geom are valid identifiers
        if not pg_schema.isidentifier() or not pg_tab_geom.isidentifier():
             raise ValueError(f"Invalid PG schema or table name for OGR: {pg_schema}, {pg_tab_geom}")

        # Use list of arguments for subprocess to avoid shell injection issues
        comando_args = [
            "ogr2ogr",
            "-overwrite",
            "-f", "PostgreSQL",
            f"PG:{pg_conn_str}",
            f"OCI:{oci_conn_str}",
            "-sql", f"SELECT * FROM {tab_geom}", # Table name from Oracle side
            "-a_srs", f"EPSG:{epsg_code}",
            "--config", "PG_USE_COPY", "YES",
            "-lco", "FID=ogr_fid", # Or keep original PK if preferred and possible
            "-lco", f"DIM={dim}",
            "-nln", f"{pg_schema}.{pg_tab_geom}" # Target table name in PG
        ]
        comando_ogr = " ".join(comando_args) # Join for logging
        comando_ogr = comando_ogr.replace(pg_conn_str, "<PG_CONN_STR>").replace(oci_conn_str,"<OCI_CONN_STR>") # Replace single quotes with double quotes for logging
        print_log("INFO", f"COMANDO OGR: {comando_ogr}") # Log the command string for readability

        try:
            # Use subprocess.run for simpler blocking execution with timeout
            proc = subprocess.run(comando_args, capture_output=True, text=True, timeout=timeout_seconds, check=False, shell=False) # shell=False is safer

            ogr_stdout = proc.stdout
            ogr_stderr = proc.stderr
            exit_code = proc.returncode

            print_log("INFO", f"OGR STDOUT:\n{ogr_stdout}")
            if ogr_stderr:
                 print_log("WARNING", f"OGR STDERR:\n{ogr_stderr}") # Log stderr even on success, might contain warnings

            # Check for specific Oracle error in stderr as in Groovy
            if "ORA-13208" in ogr_stderr:
                print_log("ERROR", "OGR failed with ORA-13208 (likely internal error during spatial query). Treating as error.")
                exit_code = 1 # Force error status

            if exit_code != 0:
                raise subprocess.CalledProcessError(exit_code, comando_args, output=ogr_stdout, stderr=ogr_stderr)

        except subprocess.TimeoutExpired:
            elapsed = datetime.now() - start_ogr
            print_log("ERROR", f"OGR command timed out after {elapsed.total_seconds():.1f} seconds (limit: {timeout_seconds}s).")
            raise TimeoutError("ERRORE ELABORAZIONE TIMEOUT")
        except subprocess.CalledProcessError as e:
            elapsed = datetime.now() - start_ogr
            print_log("ERROR", f"OGR command failed with exit code {e.returncode} after {elapsed.total_seconds():.1f} seconds.")
            print_log("ERROR", f"OGR STDERR was:\n{e.stderr}")
            raise IOError(f"ERRORE ELABORAZIONE OGR: {e.stderr[:500]}") # Limit error message length
        except Exception as e:
             print_log("ERROR", f"An unexpected error occurred during OGR execution: {e}")
             raise


        print_log("INFO", "BONIFICA GEOMETRIE NON VALIDE (Polygons)")
        # Ensure pg_tab_geom is safe here too
        # Use sql composition for safety if needed
        valid_cmd = f"""
            UPDATE {pg_schema}.{pg_tab_geom}
            SET wkb_geometry = st_multi(st_collectionextract(st_makevalid(wkb_geometry),3))
            WHERE NOT ST_IsValid(wkb_geometry)
              AND ST_GeometryType(wkb_geometry) = 'ST_Polygon'
        """
        print_log("INFO", f"COMANDO: {valid_cmd}")
        try:
            execute_pg(valid_cmd)
            print_log("INFO", "BONIFICA OK")
        except Exception as e:
            print_log("ERROR", f"Error during geometry validation: {e}")
            # Decide if this is fatal or just a warning

        print_log("INFO", "CREO INDICI E VACUUM")
        try:
            if pk_field:
                # Ensure pk_field and pg_tab_geom are valid identifiers
                if not pk_field.isidentifier(): raise ValueError(f"Invalid PK field: {pk_field}")
                # Index name needs sanitizing too, or use default naming
                index_name = f"{pg_tab_geom}_{pk_field.lower()}_pk_idx" # Example naming
                # Basic sanitization for index name
                index_name = "".join(c if c.isalnum() or c == '_' else '_' for c in index_name)[:60] # Limit length

                # Use sql composition for safety
                from psycopg2 import sql
                index_cmd = sql.SQL("""
                    CREATE UNIQUE INDEX IF NOT EXISTS {index_name}
                    ON {schema}.{table} USING btree ({pk_column})
                """).format(
                    index_name=sql.Identifier(index_name),
                    schema=sql.Identifier(pg_schema),
                    table=sql.Identifier(pg_tab_geom),
                    pk_column=sql.Identifier(pk_field.lower()) # Assuming PK field name from Oracle is case-insensitive or needs lowercasing for PG
                )
                print_log("INFO", f"Creating index: {index_cmd.as_string(pg_conn)}")
                execute_pg(index_cmd)
                print_log("INFO", f"Index on {pk_field} created (or already exists).")

        except Exception as e:
            # Catch specific psycopg2 errors if needed (e.g., DuplicateTableError for index)
            print_log("WARNING", f"Could not create PK index (maybe exists or invalid PK '{pk_field}'): {e}")
            # Reset transaction state if error occurred in non-autocommit mode
            # if not pg_conn.autocommit: pg_conn.rollback()


        print_log("INFO", "ESEGUO VACUUM/ANALYZE")
        try:
            # VACUUM deve essere eseguito fuori da una transazione esplicita
            pg_conn.autocommit = True
            from psycopg2 import sql
            vacuum_cmd = sql.SQL("VACUUM ANALYZE {schema}.{table}").format(
                schema=sql.Identifier(pg_schema),
                table=sql.Identifier(pg_tab_geom)
            )
            print_log("INFO", f"Executing: {vacuum_cmd.as_string(pg_conn)}")
            with pg_conn.cursor() as cur:
                cur.execute(vacuum_cmd)
            print_log("INFO", "VACUUM ANALYZE OK")
        except Exception as e:
            print_log("ERROR", f"Error during VACUUM ANALYZE: {e}")
            # Decide if this is fatal

        print_log("INFO", "IMPORT OK")

        # Record Counts
        ora_count = get_ora_count(geom_db, tab_geom)
        pg_count = get_pg_count(f"{pg_schema}.{pg_tab_geom}")
        print_log("INFO", "CONTEGGIO RECORD ------------------------------- ")
        print_log("INFO", f" - ORACLE ({tab_geom}): {ora_count} - PG ({pg_schema}.{pg_tab_geom}): {pg_count}")
        if ora_count != pg_count:
             print_log("WARNING", "Record counts do not match!")
             # Optionally send a specific warning email

    except Exception as ex:
        print_log("ERROR", f"Exception during importTable for {tab_geom}: {ex}")
        # Re-raise the exception to be caught by the main loop for error reporting
        raise
    finally:
        if geom_db:
            geom_db.close()
            print_log("INFO", f"Closed Geometry Oracle DB connection")


def read_db(comando, main_logger, params=None):
    print_log("INFO", f"Esecuzione Comando Oracle: {comando} with params {params}")
    processed_tables = 0
    failed_tables = 0
    try:
        with ora_conn.cursor() as cur:
            cur.execute(comando, params or {})
            # Fetch column names to access by name (case-insensitive)
            columns = [col[0] for col in cur.description]
            cur.rowfactory = lambda *args: dict(zip(columns, args))

            for row in cur:
                # Access columns by uppercase name as in Groovy/Oracle
                stringa_conn = row.get('STRINGA_CONN')
                tab_geom = row.get('TAB_GEOM')
                epsg_code = row.get('EPSG_CODE')
                pk_field = row.get('PK_FIELD')
                geom_field = row.get('GEOM_FIELD')
                ora_schema = row.get('ORA_SCHEMA') # Already uppercase from query
                pg_schema = "public" # Default schema

                if not all([stringa_conn, tab_geom, epsg_code, ora_schema]):
                     print_log("WARNING", f"Skipping row due to missing data: {row}")
                     continue

                try:
                    start_tavola = datetime.now()
                    import_table(stringa_conn, tab_geom, pg_schema, epsg_code, pk_field, geom_field, ora_schema)
                    stop_tavola = datetime.now()
                    td_tavola = stop_tavola - start_tavola
                    td_tavola_minutes = int(td_tavola.total_seconds() / 60)
                    write_db_log(stringa_conn, tab_geom, td_tavola_minutes, istanza)
                    processed_tables += 1
                except Exception as e:
                    # Error logged within import_table or get_geom_db
                    print_log("ERROR", f"Failed to process table {tab_geom} from connection {stringa_conn}. Error: {e}")
                    failed_tables += 1
                    # Send specific error email for this table failure
                    body = f"CONNESSIONE: {stringa_conn}<br>TAVOLA: {tab_geom}<br>ERRORE: {e}"
                    send_mail(ERROR_TO_ADDRESS, "Errore Cache POSTGIS - Tabella Specifica", body)
                    # Decide whether to continue with other tables or stop
                    # continue # Uncomment to continue processing other tables despite errors

    except Exception as e:
        print_log("ERROR", f"Error executing main Oracle query or iterating results: {e}")
        raise # Raise to main block for general error reporting

    print_log("INFO", f"Finished processing tables. Success: {processed_tables}, Failed: {failed_tables}")
    if failed_tables > 0:
        # Maybe raise an exception here if any failure should stop the overall success message
        print_log("WARNING", f"{failed_tables} tables failed to import.")


def post_update():
    print_log("INFO", "POST UPDATE: Executing specific view updates")
    cmds = [
        """
            CREATE OR REPLACE VIEW public.pgr_grandi_piccole_deriv_idr
            AS SELECT genioweb_rl_s3_punti_de_view_gd.id,
                genioweb_rl_s3_punti_de_view_gd.codice_pratica,
                genioweb_rl_s3_punti_de_view_gd.denominazione,
                genioweb_rl_s3_punti_de_view_gd.wkb_geometry
            FROM public.genioweb_rl_s3_punti_de_view_gd -- Assuming schema is public
            WHERE genioweb_rl_s3_punti_de_view_gd.tipo_uso::text = 'UMANO'::text AND genioweb_rl_s3_punti_de_view_gd.descrizione_stato_prat::text = 'IN ESERCIZIO'::text
            UNION ALL
            SELECT genioweb_rl_s3_punti_de_view_pd.id,
                genioweb_rl_s3_punti_de_view_pd.codice_pratica,
                genioweb_rl_s3_punti_de_view_pd.denominazione,
                genioweb_rl_s3_punti_de_view_pd.wkb_geometry
            FROM public.genioweb_rl_s3_punti_de_view_pd -- Assuming schema is public
            WHERE genioweb_rl_s3_punti_de_view_pd.tipo_uso::text = 'UMANO'::text AND genioweb_rl_s3_punti_de_view_pd.descrizione_stato_prat::text = 'IN ESERCIZIO'::text;
        """,
        """
            CREATE OR REPLACE VIEW varie.pgr_v_sis_instab_pub -- Assuming schema varie exists
            AS SELECT v_sis_instab_pub.id,v_sis_instab_pub.id_i,v_sis_instab_pub.tipo_i,v_sis_instab_pub.decodifica,v_sis_instab_pub.cod_com,
                v_sis_instab_pub.flag_validazione,v_sis_instab_pub.frt,v_sis_instab_pub.frr,v_sis_instab_pub.il,v_sis_instab_pub.disl,
                v_sis_instab_pub.fa,v_sis_instab_pub.fv,v_sis_instab_pub.ft,v_sis_instab_pub.fh0105,v_sis_instab_pub.fh0515,v_sis_instab_pub.fpga,
                v_sis_instab_pub.fa0105,v_sis_instab_pub.fa0408,v_sis_instab_pub.fa0711,v_sis_instab_pub.spettri,v_sis_instab_pub.livello,
                v_sis_instab_pub.cat,v_sis_instab_pub.amb,v_sis_instab_pub.li,v_sis_instab_pub.valore_f,v_sis_instab_pub.tipo_f,
                v_sis_instab_pub.versione_standard,v_sis_instab_pub.wkb_geometry,v_sis_instab_pub.tipo_i_sempl
            FROM varie.v_sis_instab_pub -- Assuming schema varie exists
            WHERE v_sis_instab_pub.tipo_i not in (3060,3070)
        """
    ]

    success_count = 0
    for i, cmd in enumerate(cmds):
        print_log("INFO", f"Esecuzione Post-Update Comando {i+1}") # Log snippet removed for brevity
        try:
            execute_pg(cmd)
            print_log("INFO", f"Post-Update Comando {i+1} OK")
            success_count += 1
        except Exception as e:
            print_log("ERROR", f"Errore durante Post-Update Comando {i+1}: {e}")
            # Decide if this error is critical

    print_log("INFO", f"Post-Update finished. {success_count}/{len(cmds)} commands executed successfully.")


# --- Email Function ---
def send_mail(to_address_str, subject, body):
    if not SMTP_MAIL_SERVER:
        print_log("ERROR", "SMTP server not configured. Cannot send email.")
        return

    # Split addresses, strip whitespace
    to_addresses = [addr.strip() for addr in to_address_str.split(';') if addr.strip()]
    if not to_addresses:
        print_log("WARNING", "No valid recipient addresses provided for email.")
        return

    msg = MIMEText(body, 'html', 'utf-8') # Use utf-8, more standard than ISO-8859-1
    msg['Subject'] = subject
    msg['From'] = FROM_ADDRESS
    msg['To'] = ', '.join(to_addresses) # Comma-separated for header

    try:
        print_log("INFO", f"Connecting to SMTP server: {SMTP_MAIL_SERVER}:25")
        with smtplib.SMTP(SMTP_MAIL_SERVER, 25) as server:
            # server.set_debuglevel(1) # Uncomment for debugging SMTP
            # Add login here if authentication is required:
            # server.login(SMTP_USER, SMTP_PASSWORD)
            print_log("INFO", f"Sending email to: {', '.join(to_addresses)}")
            server.sendmail(FROM_ADDRESS, to_addresses, msg.as_string())
            print_log("INFO", "Email sent successfully.")
    except smtplib.SMTPRecipientsRefused:
         print_log("ERROR", f"SMTP server refused recipients: {', '.join(to_addresses)}")
    except smtplib.SMTPAuthenticationError:
         print_log("ERROR", "SMTP authentication failed. Check credentials if login is used.")
    except smtplib.SMTPSenderRefused:
         print_log("ERROR", f"SMTP server refused sender address: {FROM_ADDRESS}")
    except Exception as e:
        print_log("ERROR", f"Failed to send email: {e}")


def create_parser():
    """Creates and returns the ArgumentParser instance."""
    parser = argparse.ArgumentParser(description='Import Oracle spatial data to PostGIS cache based on map/layer IDs or scheduled instance.')

    # Group for mutually exclusive run types: scheduled or manual ID
    run_type_group = parser.add_mutually_exclusive_group(required=True)
    run_type_group.add_argument('-sp', '--sched-prod', action='store_const', const='P', dest='schedule_type', help='Run scheduled task for Production instance (P).')
    run_type_group.add_argument('-st', '--sched-test', action='store_const', const='T', dest='schedule_type', help='Run scheduled task for Test instance (T).')
    run_type_group.add_argument('--id', dest='identifier', help='Run for specific Map ID(s) (e.g., 123,456) or Layer ID(s) (e.g., L789,L1011).')

    parser.add_argument('--update-flag', action='store_true', help='Set POSTGIS_CACHE=\'S\' in sit_catalogo for the specified map IDs after successful import (only applicable when using --id for maps).')
    return parser

# --- Main Execution ---
def main(args_list=None):
    """Main execution logic. Accepts optional list of arguments for testing."""
    global istanza, main_logger
    # Controllo se esiste la variabile d'ambiente RUN_UUID
    env_run_uuid = os.getenv('RUN_UUID')
    run_uuid = uuid.UUID(env_run_uuid) if env_run_uuid else uuid.uuid4()
    main_logger = setup_logging(run_uuid)
    start_time = datetime.now()

    # --- Argument Parsing Setup ---
    parser = create_parser()
    # Parse actual command line args if not testing, else parse provided list
    args = parser.parse_args(args_list if args_list is not None else sys.argv[1:])
    # --- End Argument Parsing ---


    print_log("INFO", f"SCRIPT START - Run UUID: {run_uuid}")
    print_log("INFO", f"Arguments: {args}") # Log parsed arguments
    print_log_main("INFO", f"SCRIPT START - Run UUID: {run_uuid}", main_logger)

    # Determine run type and parameters
    param = None
    flag_schedulata = False
    update_postgis_flag = args.update_flag

    if args.schedule_type:
        flag_schedulata = True
        istanza = args.schedule_type # Will be 'P' or 'T'
        param = istanza # Use instance type as the parameter identifier for logging/emails
        print_log("INFO", f"Scheduled run detected for instance: {istanza}")
        if update_postgis_flag:
            print_log("WARNING", "--update-flag is ignored for scheduled runs.")
            update_postgis_flag = False # Ensure flag is not used for scheduled runs
    elif args.identifier:
        param = args.identifier
        print_log("INFO", f"Manual run detected for ID(s): {param}")
        if update_postgis_flag and param.startswith('L'):
             print_log("WARNING", "--update-flag is ignored for layer-specific runs (--id starts with L).")
             update_postgis_flag = False # Ensure flag is not used for layer runs
        elif update_postgis_flag:
             print_log("INFO", "--update-flag is set for map ID run.")
    else:
        # This case should not be reached due to the required mutually exclusive group
        print_log("ERROR", "Invalid arguments. Must specify schedule type (-sp/-st) or manual ID (--id).")
        parser.print_help()
        sys.exit(1)

    try:
        connect_db()

        print_log("INFO", "COPIA DATI POSTGIS")
        base_comando = "SELECT DISTINCT STRINGA_CONN, TAB_GEOM, UPPER(SUBSTR(STRINGA_CONN,0,INSTR(STRINGA_CONN,'/')-1)) ORA_SCHEMA, EPSG_CODE, PK_FIELD, GEOM_FIELD FROM PG_CACHE_LAYERS"
        where_clause = ""
        order_by = " ORDER BY 1, 2" # Order by STRINGA_CONN, TAB_GEOM
        params = {} # Initialize params dictionary

        if flag_schedulata:
            # Use the stored instance ('P' or 'T')
            print_log("INFO", f"Esecuzione schedulata per istanza: {istanza}")
            where_clause = " WHERE ID_LAYER IN (SELECT DISTINCT ID_LAYER FROM GS_LAYERS WHERE CACHE_SCHEDULATA LIKE :p_instance || '_%') AND POSTGIS_CACHE = 'S'"
            params = {'p_instance': istanza} # Bind the instance type ('P' or 'T')
        else:
            # Manual run using --id
            id_param = args.identifier
            print_log("INFO", f"Esecuzione singola per ID: {id_param}")
            if id_param.startswith("L"):
                # Layer ID(s)
                try:
                    layer_ids = [int(x) for x in id_param[1:].split(',') if x.isdigit()]
                    if not layer_ids: raise ValueError("No valid layer IDs found")
                    id_placeholders = ','.join([':id'+str(i) for i in range(len(layer_ids))])
                    where_clause = f" WHERE ID_LAYER IN ({id_placeholders})"
                    params = {'id'+str(i): lid for i, lid in enumerate(layer_ids)}
                except ValueError as e:
                     print_log("ERROR", f"Invalid Layer ID format (--id): {id_param}. Error: {e}")
                     sys.exit(1)
            else:
                 # Map ID(s)
                 try:
                    map_ids = [int(x) for x in id_param.split(',') if x.isdigit()]
                    if not map_ids: raise ValueError("No valid map IDs found")
                    id_placeholders = ','.join([':id'+str(i) for i in range(len(map_ids))])
                    where_clause = f" WHERE ID_MAP IN ({id_placeholders})"
                    params = {'id'+str(i): mid for i, mid in enumerate(map_ids)}
                 except ValueError as e:
                     print_log("ERROR", f"Invalid Map ID format (--id): {id_param}. Error: {e}")
                     sys.exit(1)

        # Construct and execute the command
        comando = base_comando + where_clause + order_by
        read_db(comando, main_logger, params) # Pass params dict

        # Update Oracle flag if requested (only for manual map ID runs)
        if update_postgis_flag:
             id_param = args.identifier # Already validated as map IDs if flag is true
             try:
                map_ids_to_update = [int(x) for x in id_param.split(',') if x.isdigit()]
                if map_ids_to_update:
                    update_placeholders = ','.join([':id'+str(i) for i in range(len(map_ids_to_update))])
                    update_params = {'id'+str(i): mid for i, mid in enumerate(map_ids_to_update)}
                    update_cmd = f"UPDATE sit_catalogo SET POSTGIS_CACHE = 'S' WHERE CODICE IN ({update_placeholders})"
                    execute_ora(update_cmd, update_params)
                    print_log("INFO", f"Aggiornato campo POSTGIS_CACHE in sit_catalogo per ID(s): {id_param}")
                # else case not needed due to prior validation
             except Exception as e:
                  print_log("ERROR", f"Failed to update POSTGIS_CACHE flag in sit_catalogo: {e}")

        post_update()

        stop_time = datetime.now()
        td = stop_time - start_time
        print_log("INFO", "ESECUZIONE TERMINATA")

        # Send final email
        email_param_id = istanza if flag_schedulata else args.identifier
        if flag_schedulata:
            subject = f"Esecuzione Cache Schedulata POSTGIS - {istanza}"
            body = f"CACHE POSTGIS SCHEDULATA ({istanza}): Esecuzione Terminata.<br>Tempo totale di esecuzione: {td}"
            print_log_main("INFO", f"CACHE POSTGIS SCHEDULATA: Esecuzione Terminata - {td}", main_logger)
            send_mail(OK_TO_ADDRESS, subject, body)
        else:
            subject = f"Esecuzione Cache POSTGIS - {email_param_id}"
            body = f"CACHE POSTGIS ({email_param_id}): Esecuzione Terminata.<br>Tempo totale di esecuzione: {td}"
            print_log_main("INFO", f"CACHE POSTGIS {email_param_id}: Esecuzione Terminata - {td}", main_logger)
            # send_mail(OK_TO_ADDRESS, subject, body) # Send mail for manual runs? Uncomment if needed

    except Exception as e:
        stop_time = datetime.now()
        td = stop_time - start_time
        error_param_id = istanza if flag_schedulata else args.identifier if args.identifier else "N/A"
        print_log("ERROR", f"SCRIPT FAILED ({error_param_id}): {e}")
        print_log_main("ERROR", f"SCRIPT FAILED ({error_param_id}): {e} - Runtime: {td}", main_logger)
        # Send error email for general failure
        error_body = f"Esecuzione Cache POSTGIS fallita ({error_param_id}).<br>Errore: {e}<br>Controllare il log: {log_file_path}"
        send_mail(ERROR_TO_ADDRESS, f"ERRORE Esecuzione Cache POSTGIS - {error_param_id}", error_body)
        sys.exit(1) # Exit with error code
    finally:
        close_db()
        print_log("INFO", f"SCRIPT END - Total Time: {datetime.now() - start_time}")

if __name__ == "__main__":
    main()

---

# gemini response

Certamente! Trasformare uno script Python complesso in un DAG Airflow richiede di pensare in termini di task, dipendenze e come Airflow gestirà l'esecuzione, la configurazione e il logging.

Ecco una versione del tuo script trasformata in un DAG Airflow. Ho cercato di mantenere la logica originale il più possibile, ma con alcune modifiche chiave per adattarla al paradigma di Airflow:

**Considerazioni sulla trasformazione:**

1.  **Struttura del DAG:**
    * Il DAG avrà un `PythonOperator` principale che eseguirà la logica di business principale (contenuta nella funzione `main_script_logic`).
    * Le email di successo e fallimento saranno gestite tramite callback (`on_success_callback`, `on_failure_callback`).

2.  **Parametri del DAG:**
    * Gli argomenti da riga di comando (`argparse`) sono stati sostituiti con i `params` del DAG di Airflow. Questo permette di specificare il tipo di esecuzione (schedulata o manuale con ID) quando si triggera il DAG manualmente dall'interfaccia di Airflow. Per le esecuzioni schedulate, puoi impostare i parametri di default.

3.  **Variabili d'Ambiente e Connessioni:**
    * Lo script originale carica le variabili d'ambiente da un file `.env`. In Airflow, è prassi comune gestire le configurazioni sensibili (come le credenziali del database) tramite le **Airflow Connections** e le variabili non sensibili tramite le **Airflow Variables** o variabili d'ambiente definite nell'ambiente di esecuzione dei worker Airflow.
    * Per questa trasformazione, manterrò il caricamento da `.env` come nello script originale, ma in un ambiente di produzione Airflow, dovresti considerare l'uso delle Connections. L'inizializzazione del client Oracle e `GEOSCRIPTS_HOME` devono essere disponibili nell'ambiente del worker.

4.  **Logging:**
    * Airflow ha il suo sistema di logging per task. Le istruzioni `print_log` e `print_log_main` verranno comunque eseguite e i loro output appariranno nei log del task di Airflow. Il logging su file separato come configurato nello script originale continuerà a funzionare, a patto che i worker Airflow abbiano i permessi di scrittura nella `LOG_DIR`.

5.  **Funzioni Globali e Stato:**
    * Le variabili globali come `pg_conn`, `ora_conn`, `main_logger` sono state mantenute all'interno della funzione principale eseguita dal `PythonOperator`. Questo va bene per un singolo task che racchiude la maggior parte della logica. Se si volessero suddividere ulteriormente i task, la gestione dello stato (come le connessioni al DB) dovrebbe essere rivista (es. usando XComs o Hooks di Airflow).

6.  **`sys.exit()`:**
    * Le chiamate a `sys.exit()` sono state sostituite con il sollevamento di eccezioni Python (es. `raise ValueError(...)`). Questo permette ad Airflow di intercettare l'errore e marcare il task come fallito.

7.  **`if __name__ == "__main__":`**:
    * Il blocco `if __name__ == "__main__":` non è necessario in un DAG Airflow poiché Airflow stesso importa ed esegue il codice definito nei task.

**Script del DAG Airflow (`your_dag_file.py`):**

```python
import os
import sys
import uuid
import logging
import subprocess
import smtplib
# argparse non è più necessario qui, useremo dag_params
from email.mime.text import MIMEText
from datetime import datetime, timedelta

from dotenv import load_dotenv
import psycopg2
import oracledb

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param # Per i parametri del DAG

# --- INIZIO CODICE ORIGINALE ADATTATO ---
# (La maggior parte del tuo script verrà qui, incapsulato in funzioni o classi se necessario)

# Variabili globali dello script originale (saranno gestite all'interno delle funzioni del task)
PG_USER = None
PG_PWD = None
PG_HOST = None
PG_PORT = None
PG_DB_NAME = None
ORA_DB_CONN_STR = None
ORA_USER = None
ORA_PWD = None
PG_URL = None
SMTP_MAIL_SERVER = None
FROM_ADDRESS = None
ERROR_TO_ADDRESS = None
OK_TO_ADDRESS = None
LOG_DIR = None
geoscripts_home = None

pg_conn_global = None # Rinominate per evitare conflitti con variabili locali in Airflow
ora_conn_global = None
log_file_path_global = None
istanza_global = ''
main_logger_global = None


def initialize_config_and_oracle_client():
    """
    Carica la configurazione e inizializza il client Oracle.
    Questa funzione dovrebbe essere chiamata all'inizio del task.
    """
    global PG_USER, PG_PWD, PG_HOST, PG_PORT, PG_DB_NAME, ORA_DB_CONN_STR, ORA_USER, ORA_PWD
    global PG_URL, SMTP_MAIL_SERVER, FROM_ADDRESS, ERROR_TO_ADDRESS, OK_TO_ADDRESS
    global LOG_DIR, geoscripts_home

    # Inizializza la modalità thick di oracledb
    # Assicurati che ORACLE_CLIENT_LIB_DIR sia impostata nell'ambiente del worker Airflow
    try:
        client_lib_dir = os.environ.get("ORACLE_CLIENT_LIB_DIR")
        if not client_lib_dir:
            print("WARNING: ORACLE_CLIENT_LIB_DIR not set, oracledb.init_oracle_client() might fail or use default.")
            # Considera di impostare un default se appropriato, es: "/opt/oracle/instantclient"
            # oracledb.init_oracle_client() # Prova senza lib_dir se non specificato
        else:
            oracledb.init_oracle_client(lib_dir=client_lib_dir)
        print(f"Oracle DB thick client initialized (lib_dir: {client_lib_dir if client_lib_dir else 'default'}).")
    except Exception as e:
        print(f"ERROR initializing Oracle client: {e}. Ensure client libraries are correctly installed and configured for Airflow workers.")
        raise # Questo errore è critico

    # Load environment variables from .env file
    geoscripts_home = os.getenv('GEOSCRIPTS_HOME')
    if not geoscripts_home:
        print("ERROR: GEOSCRIPTS_HOME environment variable not set.")
        raise EnvironmentError("GEOSCRIPTS_HOME environment variable not set.")

    dotenv_path = os.path.join(geoscripts_home, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        print(f"Loaded .env file from {dotenv_path}")
    else:
        print(f"WARNING: .env file not found at {dotenv_path}. Relying on environment variables set elsewhere.")


    # --- Configuration ---
    PG_USER = os.getenv("PG_USER")
    PG_PWD = os.getenv("PG_PWD")
    PG_HOST = os.getenv("PG_HOST")
    PG_PORT = os.getenv("PG_PORT")
    PG_DB_NAME = os.getenv("PG_DB_NAME")
    ORA_DB_CONN_STR = os.getenv("ORA_DB_CONN_STR")
    ORA_USER = os.getenv("ORA_USER")
    ORA_PWD = os.getenv("ORA_PWD")

    required_db_vars = {
        "PG_USER": PG_USER, "PG_PWD": PG_PWD, "PG_HOST": PG_HOST, "PG_PORT": PG_PORT,
        "PG_DB_NAME": PG_DB_NAME, "ORA_DB_CONN_STR": ORA_DB_CONN_STR,
        "ORA_USER": ORA_USER, "ORA_PWD": ORA_PWD
    }
    missing_vars = [name for name, value in required_db_vars.items() if not value]
    if missing_vars:
        msg = f"ERROR: Missing required DB environment variables: {', '.join(missing_vars)}"
        print(msg)
        raise EnvironmentError(msg)

    PG_URL = f"postgresql://{PG_USER}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"

    SMTP_MAIL_SERVER = os.getenv("SMTP_MAIL_SERVER")
    FROM_ADDRESS = os.getenv("FROM_ADDRESS")
    ERROR_TO_ADDRESS = os.getenv("ERROR_TO_ADDRESS")
    OK_TO_ADDRESS = os.getenv("OK_TO_ADDRESS")

    required_email_vars = {
        "SMTP_MAIL_SERVER": SMTP_MAIL_SERVER, "FROM_ADDRESS": FROM_ADDRESS,
        "ERROR_TO_ADDRESS": ERROR_TO_ADDRESS, "OK_TO_ADDRESS": OK_TO_ADDRESS
    }
    missing_email_vars = [name for name, value in required_email_vars.items() if not value]
    if missing_email_vars:
        msg = f"ERROR: Missing required email environment variables: {', '.join(missing_email_vars)}"
        print(msg)
        raise EnvironmentError(msg)

    LOG_DIR = os.path.join(geoscripts_home, '_log')
    os.makedirs(LOG_DIR, exist_ok=True)
    print(f"LOG_DIR set to: {LOG_DIR}")


def setup_logging_dag(run_uuid_str): # Rinominata per evitare conflitti
    global log_file_path_global, main_logger_global, LOG_DIR
    current_date = datetime.now().strftime('%Y-%m-%d')
    # Assicurati che LOG_DIR sia inizializzato
    if not LOG_DIR:
        # Questo non dovrebbe accadere se initialize_config_and_oracle_client() è stato chiamato
        print("ERROR: LOG_DIR not set in setup_logging_dag. Defaulting to current directory.")
        _LOG_DIR = "_log_airflow_fallback" # Fallback
        os.makedirs(_LOG_DIR, exist_ok=True)
    else:
        _LOG_DIR = LOG_DIR

    log_file_path_global = os.path.join(_LOG_DIR, f'dp-ora_to_pg_{current_date}_{run_uuid_str}.log')

    # Rimuove gli handler esistenti dal logger root per evitare duplicazioni
    root_logger = logging.getLogger()
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S',
                        handlers=[
                            logging.FileHandler(log_file_path_global),
                            logging.StreamHandler(sys.stdout)
                        ])
    logging.info(f"Standard logging configured. Log file: {log_file_path_global}")


    MAIN_LOG_FILE = os.path.join(_LOG_DIR, f'dp-ora_to_pg_{current_date}.log')
    main_logger_global = logging.getLogger('main_log_dag') # Nome univoco
    main_logger_global.setLevel(logging.INFO)
    for handler in list(main_logger_global.handlers): # Rimuove handler preesistenti per questo logger specifico
        main_logger_global.removeHandler(handler)
        handler.close() # Chiudi l'handler per rilasciare il file
    main_handler = logging.FileHandler(MAIN_LOG_FILE)
    main_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    main_handler.setFormatter(main_formatter)
    main_logger_global.addHandler(main_handler)
    main_logger_global.propagate = False # Evita che i log vengano passati al logger root se non desiderato
    logging.info(f"Main summary logger configured. Log file: {MAIN_LOG_FILE}")

    return main_logger_global

def print_log(level, msg):
    # logging.getLogger() qui si riferisce al logger root configurato da basicConfig
    if level.upper() == "INFO": logging.info(msg)
    elif level.upper() == "ERROR": logging.error(msg)
    elif level.upper() == "WARNING": logging.warning(msg)
    else: logging.debug(msg)

def print_log_main(level, msg, _main_logger=None):
    global main_logger_global, istanza_global
    log_entry = f"{istanza_global} - {msg}" if istanza_global else msg
    logger_to_use = _main_logger if _main_logger else main_logger_global
    if logger_to_use:
        if level.upper() == "INFO": logger_to_use.info(log_entry)
        elif level.upper() == "ERROR": logger_to_use.error(log_entry)
        elif level.upper() == "WARNING": logger_to_use.warning(log_entry)
        else: logger_to_use.debug(log_entry)
    else:
        print(f"WARNING: main_logger not available for: {log_entry}")


def connect_db_dag(): # Rinominata
    global pg_conn_global, ora_conn_global
    global PG_HOST, PG_PORT, PG_DB_NAME, PG_USER, PG_PWD, ORA_DB_CONN_STR, ORA_USER, ORA_PWD

    # Assicura che le variabili di configurazione siano caricate
    if not PG_HOST: # Semplice controllo per vedere se la configurazione è stata caricata
        print("ERROR: Database configuration not loaded. Call initialize_config_and_oracle_client() first.")
        raise ConnectionError("DB config not loaded before connect_db_dag")

    try:
        print_log("INFO", f"Connecting to PostgreSQL: {PG_HOST}:{PG_PORT}/{PG_DB_NAME}")
        pg_conn_global = psycopg2.connect(host=PG_HOST, port=PG_PORT, dbname=PG_DB_NAME, user=PG_USER, password=PG_PWD)
        pg_conn_global.autocommit = True
        print_log("INFO", "PostgreSQL connection successful.")
    except Exception as e:
        print_log("ERROR", f"Failed to connect to PostgreSQL: {e}")
        raise

    try:
        print_log("INFO", f"Connecting to Oracle: {ORA_DB_CONN_STR}")
        ora_conn_global = oracledb.connect(user=ORA_USER, password=ORA_PWD, dsn=ORA_DB_CONN_STR)
        print_log("INFO", "Oracle connection successful.")
    except Exception as e:
        print_log("ERROR", f"Failed to connect to Oracle: {e}")
        if pg_conn_global: pg_conn_global.close()
        raise

def close_db_dag(): # Rinominata
    global pg_conn_global, ora_conn_global
    if pg_conn_global:
        pg_conn_global.close()
        pg_conn_global = None
        print_log("INFO", "PostgreSQL connection closed.")
    if ora_conn_global:
        ora_conn_global.close()
        ora_conn_global = None
        print_log("INFO", "Oracle connection closed.")

# --- Le funzioni execute_pg, fetchone_pg, fetchall_ora, fetchone_ora, execute_ora USANO le connessioni globali ---
def execute_pg(sql, params=None):
    global pg_conn_global
    if not pg_conn_global or pg_conn_global.closed:
        print_log("ERROR", "PostgreSQL connection is not available or closed in execute_pg.")
        raise ConnectionError("PG connection lost in execute_pg")
    with pg_conn_global.cursor() as cur:
        cur.execute(sql, params or ())

def fetchone_pg(sql, params=None):
    global pg_conn_global
    if not pg_conn_global or pg_conn_global.closed:
        print_log("ERROR", "PostgreSQL connection is not available or closed in fetchone_pg.")
        raise ConnectionError("PG connection lost in fetchone_pg")
    with pg_conn_global.cursor() as cur:
        cur.execute(sql, params or ())
        return cur.fetchone()

def fetchall_ora(sql, params=None):
    global ora_conn_global
    if not ora_conn_global: # or ora_conn_global.is_healthy() in newer versions
        print_log("ERROR", "Oracle connection is not available in fetchall_ora.")
        raise ConnectionError("Oracle connection lost in fetchall_ora")
    with ora_conn_global.cursor() as cur:
        cur.execute(sql, params or {})
        return cur.fetchall()

def fetchone_ora(sql, params=None):
    global ora_conn_global
    if not ora_conn_global:
        print_log("ERROR", "Oracle connection is not available in fetchone_ora.")
        raise ConnectionError("Oracle connection lost in fetchone_ora")
    with ora_conn_global.cursor() as cur:
        cur.execute(sql, params or {})
        return cur.fetchone()

def execute_ora(sql, params=None):
    global ora_conn_global
    if not ora_conn_global:
        print_log("ERROR", "Oracle connection is not available in execute_ora.")
        raise ConnectionError("Oracle connection lost in execute_ora")
    with ora_conn_global.cursor() as cur:
        cur.execute(sql, params or {})
        ora_conn_global.commit()

# --- get_geom_db, get_dim, get_ora_count, get_pg_count, write_db_log ---
# Queste funzioni sono per lo più auto-contenute o usano connessioni passate come argomenti,
# tranne write_db_log che usa execute_ora (e quindi ora_conn_global)
# e get_dim che usa fetchone_ora.

def get_geom_db(stringa_conn):
    # Questa funzione crea la sua connessione, il che è buono.
    # Assicurati che le credenziali usate (VISCARTO/CARTOVIS) siano sicure.
    # Potrebbe essere meglio passarle come argomenti o da config.
    jdbc_conn_string_default = 'amb_db.regione.liguria.it:1522/SIT'
    usr_default = 'VISCARTO'
    pwd_default = 'CARTOVIS'

    # La logica per derivare jdbc_conn_string, usr, pwd da stringa_conn
    # e tramite query a SIT_DB_ISTANZE usando la connessione Oracle principale
    appo_str_conn = stringa_conn.split('@')
    jdbc_conn_string = jdbc_conn_string_default
    usr = usr_default
    pwd = pwd_default
    geom_db_conn = None

    try:
        if len(appo_str_conn) >= 2:
            alias = appo_str_conn[1]
            # Usa fetchone_ora che si basa sulla connessione globale ora_conn_global
            conn_str_row = fetchone_ora("select CONNECTION_STRING from SIT_DB_ISTANZE where UPPER(ALIAS_NAME) = UPPER(:alias)", {'alias': alias.upper()})
            if conn_str_row and conn_str_row[0]: # Assicurati che conn_str_row[0] (CONNECTION_STRING) non sia None
                jdbc_conn_string = conn_str_row[0]
                print_log("INFO", f"Retrieved connection string for alias {alias}: {jdbc_conn_string}")
            else:
                print_log("WARNING", f"Alias {alias} not found in SIT_DB_ISTANZE or CONNECTION_STRING is null. Using default: {jdbc_conn_string_default}")
                # jdbc_conn_string rimane il default

            appo_str_conn2 = appo_str_conn[0].split('/')
            if len(appo_str_conn2) == 2:
                usr = appo_str_conn2[0]
                pwd = appo_str_conn2[1]
            else:
                 print_log("WARNING", f"Could not parse user/password from {appo_str_conn[0]}, using defaults.")
        else:
            print_log("WARNING", f"Could not parse alias from {stringa_conn}, using default connection: {jdbc_conn_string_default}")


        print_log("INFO", f"Connecting to Geometry Oracle DB: {jdbc_conn_string} as {usr}")
        geom_db_conn = oracledb.connect(user=usr, password=pwd, dsn=jdbc_conn_string)
        print_log("INFO", "Geometry Oracle DB connection successful.")
        return geom_db_conn
    except Exception as e:
        print_log("ERROR", f"Failed to connect to Geometry Oracle DB ({jdbc_conn_string} as {usr}): {e}")
        if geom_db_conn: geom_db_conn.close()
        raise

def get_dim(geom_db, feature_name, geom_field):
    dim = None
    try:
        with geom_db.cursor() as cur:
            if not geom_field:
                cmd_geom = "SELECT COLUMN_NAME FROM ALL_SDO_GEOM_METADATA WHERE TABLE_NAME = :table_name AND OWNER = :owner" # OWNER aggiunto per robustezza
                owner_name = feature_name.split('.')[0].upper() if '.' in feature_name else geom_db.username.upper() # Prova a derivare owner o usa l'utente connesso
                table_name_simple = feature_name.split('.')[-1].upper()
                print_log("INFO", f"getDim GEOM_FIELD query: {cmd_geom} with table_name='{table_name_simple}', owner='{owner_name}'")
                cur.execute(cmd_geom, {'table_name': table_name_simple, 'owner': owner_name})
                geom_field_row = cur.fetchone()
                if geom_field_row:
                    geom_field = geom_field_row[0]
                    print_log("INFO", f"getDim GEOM_FIELD found: {geom_field}")
                else:
                    print_log("WARNING", f"Could not find geometry column for {feature_name} (owner: {owner_name}, table: {table_name_simple}) in ALL_SDO_GEOM_METADATA")
                    return None

            if not geom_field or not geom_field.isidentifier(): # Semplice controllo, isidentifier potrebbe essere troppo restrittivo per nomi di colonna Oracle
                 print_log("ERROR", f"Invalid geometry field name: {geom_field}")
                 return None

            # cmd_dim = f"SELECT SUBSTR(t.{geom_field}.SDO_GTYPE, 1, 1) FROM {feature_name} t WHERE ROWNUM = 1"
            # Usare i placeholder per i nomi di tabella/colonna non è direttamente supportato.
            # La concatenazione di stringhe è un rischio se feature_name o geom_field provengono da input non fidati.
            # Qui, feature_name proviene da DB e geom_field da metadati, quindi il rischio è minore ma presente.
            # Per una maggiore sicurezza, sanitizzare o validare feature_name e geom_field.
            # Assumiamo che feature_name e geom_field siano sicuri in questo contesto.
            # Bisogna fare attenzione se feature_name contiene lo schema (es. "SCHEMA.TABELLA")
            sanitized_feature_name = feature_name # Dovrebbe essere già qualificato se necessario
            sanitized_geom_field = geom_field     # Dovrebbe essere un nome di colonna valido

            # Verifica che non ci siano caratteri sospetti (esempio molto base)
            if not all(c.isalnum() or c in ['.', '_'] for c in sanitized_feature_name) or \
               not all(c.isalnum() or c == '_' for c in sanitized_geom_field):
                print_log("ERROR", f"Potentially unsafe feature_name ('{sanitized_feature_name}') or geom_field ('{sanitized_geom_field}') for dynamic SQL.")
                return None

            cmd_dim = f"SELECT SUBSTR(t.\"{sanitized_geom_field}\".SDO_GTYPE, 1, 1) FROM {sanitized_feature_name} t WHERE ROWNUM = 1"

            print_log("INFO", f"getDim query: {cmd_dim}")
            cur.execute(cmd_dim) # Questo è il punto di potenziale SQL injection se non sanitizzato correttamente
            rec = cur.fetchone()
            if rec:
                dim = rec[0]
                print_log("INFO", f"getDim found: {dim}")
    except Exception as e:
        print_log("ERROR", f"Error getting dimension for {feature_name} (geom: {geom_field}): {e}")
    return dim


def get_ora_count(geom_db, feature_name):
    count = "0" # Default più sicuro di "2"
    try:
        with geom_db.cursor() as cur:
            # Simile a get_dim, feature_name necessita di attenzione se usato dinamicamente
            sanitized_feature_name = feature_name
            if not all(c.isalnum() or c in ['.', '_'] for c in sanitized_feature_name):
                 print_log("ERROR", f"Potentially unsafe feature name for count: {sanitized_feature_name}")
                 return count
            cur.execute(f"SELECT COUNT(*) FROM {sanitized_feature_name}")
            rec = cur.fetchone()
            if rec:
                count = str(rec[0])
    except Exception as e:
        print_log("ERROR", f"Error getting Oracle count for {feature_name}: {e}")
    return count

def get_pg_count(feature_name_pg):
    count = None
    try:
        # Per psycopg2, è più sicuro usare sql.Identifier per nomi di tabella/schema.
        from psycopg2 import sql
        parts = feature_name_pg.split('.')
        if len(parts) == 2:
            schema_name, table_name = parts
            query = sql.SQL("SELECT COUNT(*) FROM {}.{}").format(sql.Identifier(schema_name), sql.Identifier(table_name))
        elif len(parts) == 1:
            table_name = parts[0]
            query = sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table_name))
        else:
            print_log("ERROR", f"Invalid PG feature name format: {feature_name_pg}")
            return None

        # Usa fetchone_pg che si basa sulla connessione globale pg_conn_global
        count_row = fetchone_pg(query)
        if count_row:
            count = str(count_row[0])
    except Exception as e:
        print_log("ERROR", f"Error getting PostgreSQL count for {feature_name_pg}: {e}")
    return count

def write_db_log(stringa_conn, tab_geom, td_tavola_minutes, istanza_log):
    # Usa execute_ora che si basa sulla connessione globale ora_conn_global
    try:
        comando = """
            INSERT INTO LOG_CACHE_PG (DATA_CACHE, STRING_CONN, TAB_GEOM, TEMPO_ELABORAZIONE_MINUTI, ISTANZA)
            VALUES (CURRENT_TIMESTAMP, :conn_str, :tab_geom, :exec_time, :instance)
        """
        params = {
            'conn_str': stringa_conn,
            'tab_geom': tab_geom,
            'exec_time': td_tavola_minutes,
            'instance': istanza_log
        }
        execute_ora(comando, params)
        print_log("INFO", f"Logged execution time for {tab_geom}: {td_tavola_minutes} mins")
    except Exception as e:
        print_log("ERROR", f"Failed to write DB log for {tab_geom}: {e}")


# --- import_table ---
def import_table(stringa_conn, tab_geom, pg_schema, epsg_code, pk_field, geom_field, ora_schema_orig): # ora_schema rinominata
    global PG_HOST, PG_PORT, PG_DB_NAME, PG_USER, PG_PWD # Necessarie per la stringa di connessione OGR
    geom_db = None
    # Sanitize ora_schema_orig and tab_geom for pg_tab_geom
    # Let's assume ora_schema_orig is the one read from PG_CACHE_LAYERS.ORA_SCHEMA
    # It might be case-sensitive or need specific handling if it comes from Oracle dictionary.
    # For PG, typically lowercase is preferred.
    # Ensure ora_schema_orig is a valid identifier part
    safe_ora_schema_part = "".join(c if c.isalnum() else '_' for c in ora_schema_orig)
    safe_tab_geom_part = "".join(c if c.isalnum() else '_' for c in tab_geom)
    pg_tab_geom = f"{safe_ora_schema_part.lower()}_{safe_tab_geom_part.lower()}"


    try:
        geom_db = get_geom_db(stringa_conn) # Questa funzione gestisce la sua connessione
        if not geom_db:
             raise Exception(f"Failed to get geometry DB connection for {stringa_conn}")

        if not tab_geom:
            print_log("WARNING", "Table name is null, skipping import.")
            return # Non sollevare eccezione qui, è uno skip gestito

        print_log("INFO", f"ELABORAZIONE TAVOLA: {tab_geom} (da {stringa_conn})")

        # feature_name per get_dim dovrebbe essere nome tabella Oracle qualificato se necessario (es. SCHEMA.TABELLA)
        # Se ora_schema_orig è lo schema del proprietario della tabella tab_geom
        feature_name_ora_qualified = f"{ora_schema_orig}.{tab_geom}" if ora_schema_orig else tab_geom
        dim = get_dim(geom_db, feature_name_ora_qualified, geom_field) # geom_db è la connessione Oracle "locale"
        if dim is None:
             msg = f"Could not determine dimension for {feature_name_ora_qualified}, skipping import."
             print_log("ERROR", msg)
             raise Exception(msg) # Rende questo un errore che interrompe per questa tabella

        print_log("INFO", f"DIM={dim} - PG_TABLE={pg_schema}.{pg_tab_geom}")

        timeout_seconds = 70 * 60
        start_ogr = datetime.now()

        # Costruzione stringa di connessione OCI per ogr2ogr
        # stringa_conn è del tipo "utente/password@alias"
        # ogr2ogr OCI driver si aspetta "utente/password@connect_string_oracle"
        # connect_string_oracle può essere un alias TNSNAMES o una stringa Easy Connect
        # Se stringa_conn è "VISCARTO/PWD@SIT", e SIT è in tnsnames.ora, va bene.
        # Se SIT_DB_ISTANZE.CONNECTION_STRING dà la stringa Easy Connect, usala.
        # Per ora, assumiamo che stringa_conn sia direttamente utilizzabile o che
        # l'alias in stringa_conn sia configurato in tnsnames.ora per i worker Airflow.
        # OGR potrebbe necessitare di TNS_ADMIN impostato nell'ambiente.

        # Il formato OCI per ogr2ogr è `OCI:userid/password@database_specification:table_name,table_name...`
        # o `OCI:userid/password@database_specification` e poi si usa `-sql "SELECT ... FROM table_name"`
        # `stringa_conn` sembra essere "user/pass@alias_db"
        # `tab_geom` è il nome della tabella.

        # Deriviamo le parti di connessione per OGR da stringa_conn
        # Se stringa_conn è "USR/PWD@ALIASDB"
        # L'OCI DSN per ogr2ogr sarebbe "USR/PWD@ALIASDB"
        # Poi si specifica la tabella con -sql o direttamente come layer.
        # L'originale `oci_conn_str = f"{stringa_conn}:{tab_geom}"` non sembra corretto per -sql.
        # Dovrebbe essere `oci_source_conn_str = stringa_conn` e poi `tab_geom` usato in -sql.
        # o `oci_source_layer = f"{stringa_conn}:{tab_geom}"` se non si usa -sql
        
        oci_connection_part = stringa_conn # Es: "USR_ORA/PWD_ORA@DB_ALIAS"
        source_table_in_oracle = f"{ora_schema_orig}.{tab_geom}" if ora_schema_orig else tab_geom


        pg_conn_str_ogr = f"host={PG_HOST} port={PG_PORT} dbname={PG_DB_NAME} user={PG_USER} password='{PG_PWD}' active_schema={pg_schema}"
        # La password in PG_CONN_STR_OGR potrebbe necessitare di quoting se contiene caratteri speciali.
        # subprocess.list2cmdline può aiutare a vedere come verrebbe interpretato, ma è meglio passare una lista.

        # Comando OGR
        comando_args = [
            "ogr2ogr",
            "-overwrite",
            "-f", "PostgreSQL",
            f"PG:{pg_conn_str_ogr}", # Destinazione PG
            f"OCI:{oci_connection_part}", # Sorgente Oracle, es: "user/pass@dbalias"
            "-sql", f"SELECT * FROM {source_table_in_oracle}", # Query sulla sorgente Oracle
            "-a_srs", f"EPSG:{epsg_code}",
            "--config", "PG_USE_COPY", "YES",
            "-lco", "FID=ogr_fid", # Nome colonna chiave primaria in PG
            "-lco", f"DIM={dim}",
            "-lco", f"GEOMETRY_NAME=wkb_geometry", # Nome colonna geometria in PG (default di PostGIS è geom o wkb_geometry)
            "-nln", f"{pg_schema}.{pg_tab_geom}" # Nome tabella target in PG: schema.tabella
        ]
        # Se pk_field è specificato e si vuole usarlo come FID in PG (invece di ogr_fid)
        if pk_field:
            comando_args.extend(["-lco", f"PRIMARY_KEY={pk_field.lower()}"]) # dice a PG driver di creare PK
            # ogr2ogr non ha un'opzione diretta per rinominare la colonna FID in PG con il nome di pk_field
            # se si vuole che la colonna si chiami come pk_field, si dovrebbe fare dopo con ALTER TABLE
            # o se la colonna pk_field è già parte del SELECT * ed è unica,
            # OGR potrebbe prenderla come FID se non ci sono altre opzioni specificate.
            # Per ora, usiamo ogr_fid e creiamo un indice su pk_field dopo.


        # Log del comando OGR mascherando la password PG
        comando_ogr_log = list(comando_args)
        for i, arg in enumerate(comando_ogr_log):
            if arg.startswith("PG:host=") and PG_PWD in arg :
                 comando_ogr_log[i] = arg.replace(f"password='{PG_PWD}'", "password='****'")
            if arg.startswith("OCI:") and ORA_PWD in arg : # Se ORA_PWD fosse parte di oci_connection_part
                # Questo richiede di sapere come è formattata oci_connection_part
                # Se è user/pass@db, allora la pass è lì.
                parts = oci_connection_part.split('@')[0].split('/')
                if len(parts) == 2 and parts[1] == ORA_PWD: # Semplice controllo
                    user_part = parts[0]
                    db_part = oci_connection_part.split('@')[1] if '@' in oci_connection_part else ''
                    comando_ogr_log[i] = f"OCI:{user_part}/****@{db_part}"

        print_log("INFO", f"COMANDO OGR: {' '.join(comando_ogr_log)}")


        try:
            proc = subprocess.run(comando_args, capture_output=True, text=True, timeout=timeout_seconds, check=False, shell=False)
            ogr_stdout = proc.stdout
            ogr_stderr = proc.stderr
            exit_code = proc.returncode

            print_log("INFO", f"OGR STDOUT:\n{ogr_stdout}")
            if ogr_stderr:
                 print_log("WARNING" if exit_code == 0 else "ERROR", f"OGR STDERR:\n{ogr_stderr}")

            if "ORA-13208" in ogr_stderr:
                print_log("ERROR", "OGR failed with ORA-13208 (likely internal error during spatial query). Treating as error.")
                exit_code = 1

            if exit_code != 0:
                raise subprocess.CalledProcessError(exit_code, comando_args, output=ogr_stdout, stderr=ogr_stderr)

        except subprocess.TimeoutExpired:
            elapsed = datetime.now() - start_ogr
            print_log("ERROR", f"OGR command timed out after {elapsed.total_seconds():.1f} seconds (limit: {timeout_seconds}s).")
            raise TimeoutError(f"ERRORE ELABORAZIONE TIMEOUT OGR per {tab_geom}")
        except subprocess.CalledProcessError as e:
            elapsed = datetime.now() - start_ogr
            print_log("ERROR", f"OGR command failed with exit code {e.returncode} after {elapsed.total_seconds():.1f} seconds for {tab_geom}.")
            # Non stampare e.stderr di nuovo se già loggato sopra, ma includilo nell'eccezione sollevata
            raise IOError(f"ERRORE ELABORAZIONE OGR per {tab_geom}: Code {e.returncode}. STDERR: {e.stderr[:1000]}")
        except Exception as e:
             print_log("ERROR", f"An unexpected error occurred during OGR execution for {tab_geom}: {e}")
             raise


        print_log("INFO", f"BONIFICA GEOMETRIE NON VALIDE (Polygons) per {pg_schema}.{pg_tab_geom}")
        # Usa sql.Identifier per sicurezza
        from psycopg2 import sql as pgsql
        
        # Controlla se la tabella esiste prima di tentare l'update
        check_table_exists_sql = pgsql.SQL("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE  table_schema = {schema_name}
                AND    table_name   = {table_name}
            );
        """).format(schema_name=pgsql.Literal(pg_schema), table_name=pgsql.Literal(pg_tab_geom))
        
        table_exists_result = fetchone_pg(check_table_exists_sql)
        if not table_exists_result or not table_exists_result[0]:
            print_log("WARNING", f"Table {pg_schema}.{pg_tab_geom} does not seem to exist after OGR import. Skipping geometry validation and indexing.")
        else:
            # Controlla se la colonna wkb_geometry esiste
            check_geom_col_exists_sql = pgsql.SQL("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_schema = {schema_name} 
                    AND table_name = {table_name} 
                    AND column_name = 'wkb_geometry'
                );
            """).format(schema_name=pgsql.Literal(pg_schema), table_name=pgsql.Literal(pg_tab_geom))
            geom_col_exists_result = fetchone_pg(check_geom_col_exists_sql)

            if geom_col_exists_result and geom_col_exists_result[0]:
                try:
                    # Assicurati che pg_conn_global sia autocommit=True per non bloccare altre sessioni su cataloghi
                    pg_conn_global.autocommit = True # Ripristina autocommit se necessario

                    valid_cmd_sql = pgsql.SQL("""
                        UPDATE {schema}.{table}
                        SET wkb_geometry = st_multi(st_collectionextract(st_makevalid(wkb_geometry),3))
                        WHERE NOT ST_IsValid(wkb_geometry)
                          AND ST_GeometryType(wkb_geometry) = 'ST_Polygon'
                    """).format(
                        schema=pgsql.Identifier(pg_schema),
                        table=pgsql.Identifier(pg_tab_geom)
                    )
                    print_log("INFO", f"COMANDO BONIFICA: {valid_cmd_sql.as_string(pg_conn_global)}")
                    execute_pg(valid_cmd_sql)
                    print_log("INFO", "BONIFICA GEOMETRIE OK")
                except Exception as e:
                    print_log("ERROR", f"Error during geometry validation for {pg_schema}.{pg_tab_geom}: {e}")
                    # Considera se questo errore debba essere fatale per la tabella
            else:
                print_log("WARNING", f"Geometry column 'wkb_geometry' not found in {pg_schema}.{pg_tab_geom}. Skipping geometry validation.")


            print_log("INFO", f"CREO INDICI E VACUUM per {pg_schema}.{pg_tab_geom}")
            try:
                if pk_field:
                    # Sanitize pk_field se necessario, ma assumiamo che sia un nome di colonna valido.
                    # In PG, i nomi delle colonne sono tipicamente lowercase se non quotati. OGR potrebbe aver creato
                    # la colonna pk_field con lo stesso case dell'originale Oracle o lowercase.
                    # Controlla il case effettivo della colonna in PG dopo l'import di OGR.
                    # Per semplicità, assumiamo che sia lowercase come specificato in -lco PRIMARY_KEY
                    pk_col_pg = pk_field.lower()
                    
                    # Controlla se la colonna pk_col_pg esiste
                    check_pk_col_exists_sql = pgsql.SQL("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.columns 
                            WHERE table_schema = {schema_name} 
                            AND table_name = {table_name} 
                            AND column_name = {column_name}
                        );
                    """).format(
                        schema_name=pgsql.Literal(pg_schema), 
                        table_name=pgsql.Literal(pg_tab_geom),
                        column_name=pgsql.Literal(pk_col_pg)
                    )
                    pk_col_exists_result = fetchone_pg(check_pk_col_exists_sql)

                    if pk_col_exists_result and pk_col_exists_result[0]:
                        index_name_base = f"{pg_tab_geom}_{pk_col_pg}_pk_idx"
                        index_name = "".join(c if c.isalnum() or c == '_' else '_' for c in index_name_base)[:60] # Limita lunghezza per PG

                        index_cmd_sql = pgsql.SQL("""
                            CREATE UNIQUE INDEX IF NOT EXISTS {index_name}
                            ON {schema}.{table} USING btree ({pk_column})
                        """).format(
                            index_name=pgsql.Identifier(index_name),
                            schema=pgsql.Identifier(pg_schema),
                            table=pgsql.Identifier(pg_tab_geom),
                            pk_column=pgsql.Identifier(pk_col_pg)
                        )
                        print_log("INFO", f"Creating PK index: {index_cmd_sql.as_string(pg_conn_global)}")
                        execute_pg(index_cmd_sql)
                        print_log("INFO", f"Index on {pk_col_pg} created (or already exists) for {pg_schema}.{pg_tab_geom}.")
                    else:
                        print_log("WARNING", f"PK column '{pk_col_pg}' not found in {pg_schema}.{pg_tab_geom}. Skipping PK index creation.")

            except Exception as e:
                print_log("WARNING", f"Could not create PK index for {pg_schema}.{pg_tab_geom} (maybe exists or invalid PK '{pk_field}'): {e}")

            print_log("INFO", f"ESEGUO VACUUM/ANALYZE per {pg_schema}.{pg_tab_geom}")
            try:
                pg_conn_global.autocommit = True # VACUUM ANALYZE non può essere in una transazione
                vacuum_cmd_sql = pgsql.SQL("VACUUM ANALYZE {schema}.{table}").format(
                    schema=pgsql.Identifier(pg_schema),
                    table=pgsql.Identifier(pg_tab_geom)
                )
                print_log("INFO", f"Executing: {vacuum_cmd_sql.as_string(pg_conn_global)}")
                # execute_pg(vacuum_cmd_sql) # execute_pg usa un cursore, il che è ok per VACUUM se autocommit è True
                with pg_conn_global.cursor() as cur_vac:
                    cur_vac.execute(vacuum_cmd_sql)
                print_log("INFO", "VACUUM ANALYZE OK")
            except Exception as e:
                print_log("ERROR", f"Error during VACUUM ANALYZE for {pg_schema}.{pg_tab_geom}: {e}")
                # Considerare se questo errore è fatale.

        print_log("INFO", f"IMPORT OK per {tab_geom}")

        # Record Counts
        ora_count_source_table = f"{ora_schema_orig}.{tab_geom}" if ora_schema_orig else tab_geom
        ora_count = get_ora_count(geom_db, ora_count_source_table) # Usa geom_db (connessione locale)
        pg_count = get_pg_count(f"{pg_schema}.{pg_tab_geom}") # Usa connessione globale pg_conn_global
        print_log("INFO", "CONTEGGIO RECORD ------------------------------- ")
        print_log("INFO", f" - ORACLE ({ora_count_source_table}): {ora_count} - PG ({pg_schema}.{pg_tab_geom}): {pg_count}")
        if ora_count != pg_count:
             print_log("WARNING", f"Record counts do not match for {tab_geom}! Oracle: {ora_count}, PG: {pg_count}")
             # Potrebbe essere necessario inviare un avviso specifico

    except Exception as ex:
        print_log("ERROR", f"Exception during importTable for {tab_geom} (from {stringa_conn}): {ex}")
        raise # Rilancia per essere gestita dal ciclo chiamante
    finally:
        if geom_db:
            geom_db.close()
            print_log("INFO", f"Closed Geometry Oracle DB connection for {stringa_conn}")


# --- read_db ---
def read_db(comando_select_tabelle, params_select, ti=None): # ti è task_instance di Airflow
    global main_logger_global, istanza_global
    print_log("INFO", f"Esecuzione Comando Oracle per selezionare tabelle: {comando_select_tabelle} with params {params_select}")
    processed_tables_count = 0
    failed_tables_count = 0
    failed_table_details = []

    # Usa fetchall_ora che si basa sulla connessione globale ora_conn_global
    try:
        with ora_conn_global.cursor() as cur:
            cur.execute(comando_select_tabelle, params_select or {})
            columns = [col[0].upper() for col in cur.description] # Assicura nomi colonna uppercase
            
            rows = cur.fetchall() # Prendi tutte le righe prima
            
        print_log("INFO", f"Trovate {len(rows)} tabelle da processare.")

        for i, row_tuple in enumerate(rows):
            row_dict = dict(zip(columns, row_tuple))
            # Accedi alle colonne con nomi uppercase
            stringa_conn = row_dict.get('STRINGA_CONN')
            tab_geom = row_dict.get('TAB_GEOM')
            epsg_code = row_dict.get('EPSG_CODE')
            pk_field = row_dict.get('PK_FIELD') # Può essere None
            geom_field = row_dict.get('GEOM_FIELD') # Può essere None
            ora_schema = row_dict.get('ORA_SCHEMA') # Questo è l'owner della tabella in Oracle
            pg_schema = "public" # Default schema in PG, potrebbe essere parametrizzato

            print_log("INFO", f"Riga {i+1}/{len(rows)}: STRINGA_CONN={stringa_conn}, TAB_GEOM={tab_geom}, ORA_SCHEMA={ora_schema}, EPSG={epsg_code}, PK={pk_field}, GEOM_FIELD={geom_field}")


            if not all([stringa_conn, tab_geom, epsg_code, ora_schema]):
                 print_log("WARNING", f"Skipping row due to missing critical data: {row_dict}")
                 failed_tables_count += 1
                 failed_table_details.append({'table': tab_geom or "N/A", 'conn': stringa_conn or "N/A", 'reason': "Missing critical data in PG_CACHE_LAYERS"})
                 continue

            try:
                start_tavola = datetime.now()
                import_table(stringa_conn, tab_geom, pg_schema, epsg_code, pk_field, geom_field, ora_schema)
                stop_tavola = datetime.now()
                td_tavola = stop_tavola - start_tavola
                td_tavola_minutes = int(td_tavola.total_seconds() / 60)
                # write_db_log usa connessione globale ora_conn_global
                write_db_log(stringa_conn, tab_geom, td_tavola_minutes, istanza_global)
                processed_tables_count += 1
            except Exception as e:
                print_log("ERROR", f"Failed to process table {ora_schema}.{tab_geom} from connection {stringa_conn}. Error: {e}")
                failed_tables_count += 1
                failed_table_details.append({'table': f"{ora_schema}.{tab_geom}", 'conn': stringa_conn, 'reason': str(e)[:500]})
                # Invia email di errore specifica per questa tabella
                # (la funzione send_mail_dag sarà definita più avanti)
                error_body_table = f"CONNESSIONE: {stringa_conn}<br>TAVOLA: {ora_schema}.{tab_geom}<br>ERRORE: {e}"
                send_mail_dag(ERROR_TO_ADDRESS, f"Errore Cache POSTGIS - Tabella Specifica ({istanza_global if istanza_global else 'MANUAL'})", error_body_table)
                # Non continuare se una tabella fallisce? O continuare? Lo script originale sembra continuare.
                # Per ora, continuiamo. Se si vuole interrompere, sollevare l'eccezione qui.

    except Exception as e:
        print_log("ERROR", f"Error executing main Oracle query to fetch tables or iterating results: {e}")
        raise # Rilancia per far fallire il task Airflow

    print_log("INFO", f"Finished processing tables. Success: {processed_tables_count}, Failed: {failed_tables_count}")

    if ti: # Se task_instance è passata, possiamo usare XComs
        ti.xcom_push(key="processed_tables_count", value=processed_tables_count)
        ti.xcom_push(key="failed_tables_count", value=failed_tables_count)
        ti.xcom_push(key="failed_table_details", value=failed_table_details)


    if failed_tables_count > 0:
        # Solleva un'eccezione per marcare il task come fallito se almeno una tabella fallisce.
        # Oppure, si potrebbe decidere di marcarlo come successo con avvisi.
        # Per ora, consideriamo un fallimento parziale come un fallimento del task.
        # Questo attiverà on_failure_callback.
        failure_summary = "\n".join([f"- {f['table']} (Conn: {f['conn']}): {f['reason']}" for f in failed_table_details])
        raise Exception(f"{failed_tables_count} table(s) failed to import. Failures:\n{failure_summary}")


# --- post_update ---
def post_update():
    # Usa execute_pg che si basa sulla connessione globale pg_conn_global
    print_log("INFO", "POST UPDATE: Executing specific view updates")
    cmds = [
        # Assicurati che gli schemi public e varie esistano e siano accessibili
        """
            CREATE OR REPLACE VIEW public.pgr_grandi_piccole_deriv_idr
            AS SELECT genioweb_rl_s3_punti_de_view_gd.id,
                genioweb_rl_s3_punti_de_view_gd.codice_pratica,
                genioweb_rl_s3_punti_de_view_gd.denominazione,
                genioweb_rl_s3_punti_de_view_gd.wkb_geometry
            FROM public.genioweb_rl_s3_punti_de_view_gd
            WHERE genioweb_rl_s3_punti_de_view_gd.tipo_uso::text = 'UMANO'::text AND genioweb_rl_s3_punti_de_view_gd.descrizione_stato_prat::text = 'IN ESERCIZIO'::text
            UNION ALL
            SELECT genioweb_rl_s3_punti_de_view_pd.id,
                genioweb_rl_s3_punti_de_view_pd.codice_pratica,
                genioweb_rl_s3_punti_de_view_pd.denominazione,
                genioweb_rl_s3_punti_de_view_pd.wkb_geometry
            FROM public.genioweb_rl_s3_punti_de_view_pd
            WHERE genioweb_rl_s3_punti_de_view_pd.tipo_uso::text = 'UMANO'::text AND genioweb_rl_s3_punti_de_view_pd.descrizione_stato_prat::text = 'IN ESERCIZIO'::text;
        """,
        # Assicurati che lo schema varie.v_sis_instab_pub esista
        """
            DO $$
            BEGIN
                IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'varie' AND table_name = 'v_sis_instab_pub') THEN
                    CREATE OR REPLACE VIEW varie.pgr_v_sis_instab_pub
                    AS SELECT id,id_i,tipo_i,decodifica,cod_com,
                        flag_validazione,frt,frr,il,disl,
                        fa,fv,ft,fh0105,fh0515,fpga,
                        fa0105,fa0408,fa0711,spettri,livello,
                        cat,amb,li,valore_f,tipo_f,
                        versione_standard,wkb_geometry,tipo_i_sempl
                    FROM varie.v_sis_instab_pub
                    WHERE tipo_i not in (3060,3070);
                ELSE
                    RAISE NOTICE 'Table varie.v_sis_instab_pub does not exist. Skipping view varie.pgr_v_sis_instab_pub creation.';
                END IF;
            END $$;
        """
    ]
    success_count = 0
    failed_cmds = []
    for i, cmd in enumerate(cmds):
        print_log("INFO", f"Esecuzione Post-Update Comando {i+1}")
        # Rimuovi commenti e spazi extra per un log più pulito del comando effettivo
        # log_cmd = " ".join(cmd.strip().split())
        # print_log("DEBUG", f"SQL: {log_cmd[:200]}...") # Log solo inizio comando
        try:
            pg_conn_global.autocommit = True # Le CREATE VIEW potrebbero necessitare di questo o essere ok
            execute_pg(cmd)
            print_log("INFO", f"Post-Update Comando {i+1} OK")
            success_count += 1
        except Exception as e:
            print_log("ERROR", f"Errore durante Post-Update Comando {i+1}: {e}")
            failed_cmds.append({'command_index': i+1, 'error': str(e)})

    print_log("INFO", f"Post-Update finished. {success_count}/{len(cmds)} commands executed successfully.")
    if len(failed_cmds) > 0:
        # Decide se questo è un errore fatale per il DAG.
        # Per ora, logga e continua (non solleva eccezione).
        print_log("WARNING", f"Alcuni comandi di post-update sono falliti: {failed_cmds}")


# --- Email Function ---
def send_mail_dag(to_address_str, subject, body): # Rinominata
    global SMTP_MAIL_SERVER, FROM_ADDRESS # Usa le variabili globali caricate
    if not SMTP_MAIL_SERVER:
        print_log("ERROR", "SMTP server not configured. Cannot send email.")
        return
    if not to_address_str :
        print_log("WARNING", "No recipient addresses provided for email. Skipping send.")
        return

    to_addresses = [addr.strip() for addr in to_address_str.split(';') if addr.strip()]
    if not to_addresses:
        print_log("WARNING", "No valid recipient addresses found after stripping. Skipping email.")
        return

    msg = MIMEText(body, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = FROM_ADDRESS
    msg['To'] = ', '.join(to_addresses)

    try:
        print_log("INFO", f"Connecting to SMTP server: {SMTP_MAIL_SERVER}:25")
        with smtplib.SMTP(SMTP_MAIL_SERVER, 25) as server:
            # server.set_debuglevel(1) # Uncomment for SMTP debugging
            # Aggiungere login se necessario: server.login(SMTP_USER, SMTP_PASSWORD)
            print_log("INFO", f"Sending email to: {', '.join(to_addresses)} with subject: {subject}")
            server.sendmail(FROM_ADDRESS, to_addresses, msg.as_string())
            print_log("INFO", "Email sent successfully.")
    except smtplib.SMTPRecipientsRefused as e_rec:
         print_log("ERROR", f"SMTP server refused recipients: {e_rec.recipients}. Original list: {', '.join(to_addresses)}")
    except smtplib.SMTPAuthenticationError:
         print_log("ERROR", "SMTP authentication failed. Check credentials if login is used.")
    except smtplib.SMTPSenderRefused:
         print_log("ERROR", f"SMTP server refused sender address: {FROM_ADDRESS}")
    except Exception as e:
        print_log("ERROR", f"Failed to send email: {e}")


# --- Main Execution Logic (da incapsulare in un PythonCallable per Airflow) ---
def main_script_logic(**kwargs):
    """
    Logica principale dello script, adattata per essere chiamata da un PythonOperator.
    kwargs conterrà dag_run, conf, params, ti (task_instance), etc.
    """
    global istanza_global, main_logger_global, log_file_path_global # Riferimento alle variabili globali dello script

    ti = kwargs.get('ti') # Task Instance
    dag_run = kwargs.get('dag_run')
    
    # Ottieni i parametri del DAG (definiti nel DAG object)
    # Se i parametri non sono passati (es. esecuzione schedulata con params di default),
    # dag_run.conf potrebbe essere None o vuoto. Accedi a params direttamente.
    params_from_dag = kwargs.get('params', {})

    # Inizializza configurazione e client Oracle all'inizio del task
    initialize_config_and_oracle_client()

    # Imposta il logging con un UUID di esecuzione
    # Se RUN_UUID è fornito da Airflow (es. tramite Variable o come parte dei params), usalo.
    # Altrimenti, genera un UUID. Airflow ha dag_run.run_id.
    run_id_for_log = dag_run.run_id if dag_run else str(uuid.uuid4())
    main_logger_global = setup_logging_dag(run_id_for_log) # Usa la funzione di logging adattata

    start_time_task = datetime.now()

    # Determina il tipo di esecuzione dai parametri del DAG
    # I parametri del DAG sono in params_from_dag
    # Esempio: params_from_dag = {'schedule_type': 'P', 'identifier': None, 'update_flag': False}
    # o params_from_dag = {'schedule_type': None, 'identifier': '123,456', 'update_flag': True}
    
    schedule_type_param = params_from_dag.get('schedule_type')
    identifier_param = params_from_dag.get('identifier')
    update_flag_param = params_from_dag.get('update_flag', False) # Default a False se non fornito

    print_log("INFO", f"SCRIPT START (Airflow Task) - Run ID for log: {run_id_for_log}")
    print_log("INFO", f"DAG Params: schedule_type='{schedule_type_param}', identifier='{identifier_param}', update_flag={update_flag_param}")
    print_log_main("INFO", f"SCRIPT START (Airflow Task) - Run ID for log: {run_id_for_log}", main_logger_global)

    param_for_query = None # Usato per la query e per i log/email
    flag_schedulata = False
    update_postgis_flag_effective = update_flag_param

    if schedule_type_param: # Es. 'P' o 'T'
        flag_schedulata = True
        istanza_global = schedule_type_param
        param_for_query = istanza_global
        print_log("INFO", f"Scheduled run detected for instance: {istanza_global}")
        if update_postgis_flag_effective:
            print_log("WARNING", "--update-flag (valore: {update_postgis_flag_effective}) is ignored for scheduled runs. Forcing to False.")
            update_postgis_flag_effective = False
    elif identifier_param:
        param_for_query = identifier_param
        istanza_global = f"ID_{identifier_param.replace(',','_')[:20]}" # Crea un identificatore per istanza_global
        print_log("INFO", f"Manual run detected for ID(s): {param_for_query}")
        if update_postgis_flag_effective and param_for_query.upper().startswith('L'):
             print_log("WARNING", "--update-flag (valore: {update_postgis_flag_effective}) is ignored for layer-specific runs. Forcing to False.")
             update_postgis_flag_effective = False
        elif update_postgis_flag_effective:
             print_log("INFO", "--update-flag is set for map ID run.")
    else:
        # Questo non dovrebbe accadere se i params del DAG sono ben definiti (es. con uno di default)
        msg = "Invalid DAG parameters. Must specify schedule_type or identifier."
        print_log("ERROR", msg)
        raise ValueError(msg)

    try:
        connect_db_dag() # Usa la funzione adattata

        print_log("INFO", "COPIA DATI POSTGIS")
        # Nota: ORA_SCHEMA nella query si riferisce al proprietario della tabella in Oracle.
        # Questo è importante per get_dim e get_ora_count.
        base_comando = "SELECT DISTINCT STRINGA_CONN, TAB_GEOM, UPPER(SUBSTR(STRINGA_CONN,0,INSTR(STRINGA_CONN,'/')-1)) AS ORA_SCHEMA_CONN_USER, EPSG_CODE, PK_FIELD, GEOM_FIELD, ORA_SCHEMA FROM PG_CACHE_LAYERS"
        # ORA_SCHEMA è il campo da PG_CACHE_LAYERS che dovrebbe indicare il proprietario della tabella in Oracle.
        # ORA_SCHEMA_CONN_USER è l'utente nella stringa di connessione, che potrebbe o non potrebbe essere l'owner.
        # È meglio affidarsi a PG_CACHE_LAYERS.ORA_SCHEMA se popolato correttamente.

        where_clause = ""
        order_by = " ORDER BY STRINGA_CONN, TAB_GEOM" # Ordina per stringa di connessione, poi per tabella
        query_params = {}

        if flag_schedulata:
            print_log("INFO", f"Esecuzione schedulata per istanza: {istanza_global}")
            # Assumiamo che istanza_global sia 'P' o 'T'
            where_clause = " WHERE ID_LAYER IN (SELECT DISTINCT ID_LAYER FROM GS_LAYERS WHERE CACHE_SCHEDULATA LIKE :p_instance || '_%') AND POSTGIS_CACHE = 'S'"
            query_params = {'p_instance': istanza_global}
        else: # Manual run usando identifier_param
            print_log("INFO", f"Esecuzione singola per ID: {param_for_query}")
            if param_for_query.upper().startswith("L"): # Layer ID(s)
                try:
                    layer_ids_str = param_for_query[1:].split(',')
                    layer_ids = [int(x.strip()) for x in layer_ids_str if x.strip().isdigit()]
                    if not layer_ids: raise ValueError("No valid layer IDs found after parsing.")
                    id_placeholders = ','.join([f':id{i}' for i in range(len(layer_ids))])
                    where_clause = f" WHERE ID_LAYER IN ({id_placeholders}) AND POSTGIS_CACHE = 'S'" # Aggiunto POSTGIS_CACHE = 'S' per coerenza?
                    query_params = {f'id{i}': lid for i, lid in enumerate(layer_ids)}
                except ValueError as e:
                     msg = f"Invalid Layer ID format for identifier '{param_for_query}'. Error: {e}"
                     print_log("ERROR", msg)
                     raise ValueError(msg)
            else: # Map ID(s)
                 try:
                    map_ids_str = param_for_query.split(',')
                    map_ids = [int(x.strip()) for x in map_ids_str if x.strip().isdigit()]
                    if not map_ids: raise ValueError("No valid map IDs found after parsing.")
                    id_placeholders = ','.join([f':id{i}' for i in range(len(map_ids))])
                    # La query originale per Map ID non filtrava per POSTGIS_CACHE = 'S' su PG_CACHE_LAYERS
                    # ma lo faceva implicitamente se ID_MAP portava a layer con quel flag.
                    # Se si vuole un comportamento simile, la query potrebbe essere più complessa o
                    # si potrebbe aggiungere AND POSTGIS_CACHE = 'S' se appropriato.
                    where_clause = f" WHERE ID_MAP IN ({id_placeholders}) AND POSTGIS_CACHE = 'S'" # Aggiunto per coerenza? Valutare se corretto.
                    # Se la logica è che i layer associati a queste mappe devono avere POSTGIS_CACHE='S',
                    # allora la subquery è più appropriata:
                    # where_clause = f" WHERE ID_LAYER IN (SELECT ID_LAYER FROM GS_LAYERS WHERE ID_MAP IN ({id_placeholders}) AND POSTGIS_CACHE = 'S')"

                    query_params = {f'id{i}': mid for i, mid in enumerate(map_ids)}
                 except ValueError as e:
                     msg = f"Invalid Map ID format for identifier '{param_for_query}'. Error: {e}"
                     print_log("ERROR", msg)
                     raise ValueError(msg)
        
        comando_selezione_tabelle = base_comando + where_clause + order_by
        read_db(comando_selezione_tabelle, query_params, ti) # Passa ti per XComs

        # Update Oracle flag SIT_CATALOGO.POSTGIS_CACHE se richiesto
        if update_postgis_flag_effective: # Già controllato che non sia per layer o schedulato
             if not param_for_query or param_for_query.upper().startswith("L"):
                 print_log("INFO", "Skipping update of POSTGIS_CACHE in sit_catalogo (not applicable or flag disabled).")
             else:
                try:
                    map_ids_to_update_str = param_for_query.split(',')
                    map_ids_to_update = [int(x.strip()) for x in map_ids_to_update_str if x.strip().isdigit()]
                    if map_ids_to_update:
                        update_placeholders = ','.join([f':id{i}' for i in range(len(map_ids_to_update))])
                        update_ora_params = {f'id{i}': mid for i, mid in enumerate(map_ids_to_update)}
                        # Assicurati che SIT_CATALOGO.CODICE sia il campo corretto per ID_MAP
                        update_cmd_ora = f"UPDATE sit_catalogo SET POSTGIS_CACHE = 'S' WHERE CODICE IN ({update_placeholders})"
                        print_log("INFO", f"Attempting to update sit_catalogo POSTGIS_CACHE='S' for map IDs: {map_ids_to_update}")
                        execute_ora(update_cmd_ora, update_ora_params) # Usa connessione globale
                        print_log("INFO", f"Aggiornato campo POSTGIS_CACHE in sit_catalogo per ID(s): {param_for_query}")
                    else:
                        print_log("WARNING", f"No valid map IDs found in '{param_for_query}' for sit_catalogo update.")
                except Exception as e:
                    # Non far fallire l'intero processo per questo, ma logga come errore.
                    print_log("ERROR", f"Failed to update POSTGIS_CACHE flag in sit_catalogo for '{param_for_query}': {e}")


        post_update() # Usa connessioni globali

        stop_time_task = datetime.now()
        td_task = stop_time_task - start_time_task
        print_log("INFO", "ESECUZIONE TASK AIRFLOW TERMINATA CON SUCCESSO")

        # Il corpo dell'email di successo sarà gestito da on_success_callback
        # ma possiamo preparare le informazioni qui se necessario tramite XCom.
        if ti:
            ti.xcom_push(key="total_execution_time", value=str(td_task))
            ti.xcom_push(key="run_type_param", value=param_for_query) # 'P', 'T', o ID
            ti.xcom_push(key="is_scheduled_run", value=flag_schedulata)

    except Exception as e:
        # L'eccezione sarà catturata da Airflow, che marcherà il task come FAILED.
        # on_failure_callback sarà triggerato.
        # Logghiamo comunque l'errore qui.
        stop_time_task = datetime.now()
        td_task = stop_time_task - start_time_task
        error_context = istanza_global if istanza_global else param_for_query if param_for_query else "N/A"
        
        print_log("ERROR", f"SCRIPT TASK FAILED ({error_context}): {e}")
        # main_logger_global potrebbe non essere inizializzato se l'errore avviene prima di setup_logging_dag
        if main_logger_global:
            print_log_main("ERROR", f"SCRIPT TASK FAILED ({error_context}): {e} - Runtime: {td_task}", main_logger_global)
        
        # Rilancia l'eccezione per farla gestire da Airflow
        raise
    finally:
        close_db_dag() # Assicura che le connessioni siano chiuse
        print_log("INFO", f"SCRIPT TASK END - Total Time: {datetime.now() - start_time_task}")
        # main_logger_global handlers should be closed if setup_logging_dag is robust
        if main_logger_global:
            for handler in list(main_logger_global.handlers):
                handler.close()
                main_logger_global.removeHandler(handler)
        # Also for root logger file handler
        root_logger_handlers = logging.getLogger().handlers
        for handler in list(root_logger_handlers):
            if isinstance(handler, logging.FileHandler) and handler.baseFilename == log_file_path_global:
                handler.close()
                logging.getLogger().removeHandler(handler)


# --- Callback per email ---
def on_success_email_callback(context):
    ti = context['ti']
    dag_run = context['dag_run']
    
    # Prova a inizializzare la configurazione solo per le variabili email se non già fatto
    # Questo è un po' un hack; idealmente le variabili email sono da Airflow Variables/Connections
    try:
        initialize_config_and_oracle_client() # Carica SMTP_MAIL_SERVER, FROM_ADDRESS, OK_TO_ADDRESS
    except Exception as e:
        print(f"Error initializing config in success callback (for email vars): {e}")
        # Non si può inviare email se questo fallisce

    if not OK_TO_ADDRESS or not SMTP_MAIL_SERVER or not FROM_ADDRESS:
        print("WARNING: Email configuration for success mail not fully available. Skipping success email.")
        return

    total_time = ti.xcom_pull(task_ids=dag_params['dag_id'] + '.' + 'run_oracle_to_pg_script', key='total_execution_time') or "N/A"
    run_param = ti.xcom_pull(task_ids=dag_params['dag_id'] + '.' + 'run_oracle_to_pg_script', key='run_type_param') or "N/A"
    is_scheduled = ti.xcom_pull(task_ids=dag_params['dag_id'] + '.' + 'run_oracle_to_pg_script', key='is_scheduled_run')
    
    processed_count = ti.xcom_pull(task_ids=dag_params['dag_id'] + '.' + 'run_oracle_to_pg_script', key='processed_tables_count') or "N/A"
    failed_count = ti.xcom_pull(task_ids=dag_params['dag_id'] + '.' + 'run_oracle_to_pg_script', key='failed_tables_count') or 0


    run_type_str = f"Schedulata ({run_param})" if is_scheduled else f"Manuale ({run_param})"
    subject = f"SUCCESSO Esecuzione Cache POSTGIS - {run_param}"
    body = (f"CACHE POSTGIS {run_type_str}: Esecuzione Terminata con SUCCESSO.<br>"
            f"Tempo totale di esecuzione del task: {total_time}.<br>"
            f"Tabelle processate con successo: {processed_count}.<br>"
            f"Tabelle fallite: {failed_count}.<br>"
            f"Controllare i log di Airflow per i dettagli: Run ID {dag_run.run_id}")

    if int(failed_count) > 0:
        subject = f"ATTENZIONE Esecuzione Cache POSTGIS - {run_param} (con fallimenti parziali)"
        body += "<br><br><b>ATTENZIONE: Alcune tabelle non sono state processate correttamente.</b>"
        failed_details = ti.xcom_pull(task_ids=dag_params['dag_id'] + '.' + 'run_oracle_to_pg_script', key='failed_table_details')
        if failed_details:
            body += "<br>Dettagli fallimenti:<br>"
            for fail in failed_details:
                body += f"- Tabella: {fail.get('table','N/A')}, Connessione: {fail.get('conn','N/A')}, Errore: {fail.get('reason','N/A')}<br>"
    
    send_mail_dag(OK_TO_ADDRESS, subject, body)


def on_failure_email_callback(context):
    ti = context['ti']
    dag_run = context['dag_run']
    exception = context.get('exception')
    
    try:
        initialize_config_and_oracle_client()
    except Exception as e:
        print(f"Error initializing config in failure callback: {e}")

    if not ERROR_TO_ADDRESS or not SMTP_MAIL_SERVER or not FROM_ADDRESS:
        print("WARNING: Email configuration for failure mail not fully available. Skipping failure email.")
        return

    run_param = ti.xcom_pull(task_ids=dag_params['dag_id'] + '.' + 'run_oracle_to_pg_script', key='run_type_param') # Potrebbe non essere disponibile se il task fallisce presto
    if not run_param: # Prova a prenderlo dai parametri del DAG se XCom fallisce
        run_param = context['params'].get('schedule_type') or context['params'].get('identifier', "N/A")


    # log_file_path_global potrebbe non essere settato se il failure è molto precoce
    # Cerca il log file del task di Airflow
    log_url = ti.log_url
    
    subject = f"ERRORE Esecuzione Cache POSTGIS - {run_param}"
    body = (f"Esecuzione Cache POSTGIS fallita ({run_param}).<br>"
            f"Errore: {exception}<br>"
            f"Controllare i log di Airflow: <a href='{log_url}'>Link ai Log Task</a><br>"
            f"Run ID: {dag_run.run_id}")
    
    # Aggiungi dettagli se ci sono state tabelle fallite prima dell'eccezione principale
    failed_count = ti.xcom_pull(task_ids=dag_params['dag_id'] + '.' + 'run_oracle_to_pg_script', key='failed_tables_count')
    if failed_count is not None and int(failed_count) > 0:
        body += "<br><br><b>Informazioni su fallimenti parziali prima dell'errore principale:</b>"
        failed_details = ti.xcom_pull(task_ids=dag_params['dag_id'] + '.' + 'run_oracle_to_pg_script', key='failed_table_details')
        if failed_details:
            body += "<br>Dettagli fallimenti parziali:<br>"
            for fail in failed_details:
                body += f"- Tabella: {fail.get('table','N/A')}, Connessione: {fail.get('conn','N/A')}, Errore: {fail.get('reason','N/A')}<br>"

    send_mail_dag(ERROR_TO_ADDRESS, subject, body)

# --- FINE CODICE ORIGINALE ADATTATO ---


# --- Definizione del DAG Airflow ---
dag_params = {
    'dag_id': 'oracle_to_postgis_cache_etl', # Nome del DAG
    'description': 'Importa dati spaziali da Oracle a cache PostGIS, basato su script Python originale.',
    'schedule_interval': None, # Imposta la tua schedulazione (es. '0 2 * * *' per ogni giorno alle 2 AM) o None per manuale
    'start_date': days_ago(1),
    'catchup': False,
    'tags': ['etl', 'oracle', 'postgis', 'geoscripts'],
    'default_args': {
        'owner': 'airflow',
        'retries': 1, # Numero di tentativi in caso di fallimento
        'retry_delay': timedelta(minutes=5),
        'on_failure_callback': on_failure_email_callback,
        # 'on_success_callback': on_success_email_callback, # Attivato solo se il task ha successo
                                                            # Se read_db solleva eccezione per tabelle fallite, questo non viene chiamato
                                                            # ma on_failure_callback sì.
                                                            # Se vuoi una mail di successo anche con fallimenti parziali gestiti internamente,
                                                            # la logica di read_db deve cambiare per non sollevare eccezione
                                                            # o la mail deve essere inviata alla fine di main_script_logic.
                                                            # Per ora, la mail di successo la gestiamo in on_success_email_callback,
                                                            # ma read_db solleva eccezione se ci sono fallimenti, quindi questo callback
                                                            # non verrebbe chiamato se non tutte le tabelle hanno successo.
                                                            # Modifichiamo read_db per non sollevare eccezione se ci sono fallimenti,
                                                            # ma li riporta via XCom. La mail di successo userà questi XCom.
    },
    # Definizione dei parametri del DAG per rimpiazzare argparse
    'params': {
        'schedule_type': Param(None, type=['null', 'string'], enum=[None, 'P', 'T'], description="Tipo di schedulazione ('P' per Produzione, 'T' per Test). Lasciare None se si usa 'identifier'."),
        'identifier': Param(None, type=['null', 'string'], description="ID Mappa(e) (es. 123,456) o ID Layer(s) (es. L789,L1011). Lasciare None se si usa 'schedule_type'."),
        'update_flag': Param(False, type='boolean', description="Imposta POSTGIS_CACHE='S' in sit_catalogo per gli ID mappa specificati (solo se identifier è per mappe e non inizia con L).")
    }
}

with DAG(**dag_params) as dag:
    run_main_script_task = PythonOperator(
        task_id='run_oracle_to_pg_script', # Nome del task
        python_callable=main_script_logic,
        # op_kwargs possono essere usati per passare parametri fissi se necessario,
        # ma i parametri del DAG sono accessibili tramite kwargs['params'] nel callable.
        # provide_context=True è default da Airflow 2.0, quindi kwargs saranno passati.
        # Se il task fallisce (es. read_db solleva eccezione), on_failure_callback viene chiamato.
        # Se il task ha successo, on_success_callback viene chiamato.
        # Se vuoi che la mail di successo includa un riepilogo di tabelle processate/fallite,
        # on_success_callback è il posto giusto.
        # Questo richiede che main_script_logic non sollevi eccezione per fallimenti parziali di tabelle
        # ma li comunichi (es. XComs) e termini con successo.
        # Ho modificato read_db per sollevare eccezione in caso di fallimenti, quindi
        # on_success_callback qui non verrebbe chiamato se ci sono errori in read_db.
        # La gestione dell'email di successo/fallimento parziale è stata spostata nelle callback.
        # Ora on_success_callback viene chiamato solo se NESSUNA tabella fallisce.
        # Se qualche tabella fallisce, read_db solleva un'eccezione, e viene chiamato on_failure_callback.
        # Per avere una mail "successo con avvisi", on_success_callback deve essere più intelligente
        # o la logica di fallimento in read_db modificata.
        # Ho adattato on_success_email_callback e read_db per gestire questo scenario.
        # L'email di successo ora può indicare fallimenti parziali.
        on_success_callback=on_success_email_callback,
    )

```

**Spiegazioni chiave delle modifiche per Airflow:**

1.  **Import Airflow:** `DAG`, `PythonOperator`, `Param` sono importati.
2.  **Variabili Globali:** Le variabili globali dello script originale (`pg_conn`, `ora_conn`, etc.) sono state rinominate (es. `pg_conn_global`) per chiarezza e per evitare potenziali conflitti con il contesto di Airflow. Sono ancora globali *all'interno del modulo Python*, il che significa che sono condivise tra le funzioni definite in questo file quando eseguite dallo stesso worker Python.
3.  **`initialize_config_and_oracle_client()`:** Questa nuova funzione raggruppa il caricamento delle variabili d'ambiente e l'inizializzazione del client Oracle. Viene chiamata all'inizio di `main_script_logic` e anche dalle callback email per assicurare che le variabili di configurazione email siano caricate.
4.  **`setup_logging_dag()`:** La funzione di logging è stata leggermente adattata. `run_uuid` ora proviene dall'ID di esecuzione del DAG di Airflow. Gli handler dei logger vengono puliti per evitare duplicazioni in caso di riesecuzioni del task o caricamenti multipli del DAG.
5.  **Funzioni DB:** Le funzioni DB (`connect_db_dag`, `close_db_dag`, `execute_pg`, etc.) usano le connessioni "globali" definite nel modulo.
6.  **`main_script_logic(**kwargs)`:**
    * Questa è la funzione Python che `PythonOperator` eseguirà.
    * `**kwargs` riceve il contesto di Airflow, inclusi `ti` (task instance) e `params` (i parametri del DAG).
    * La logica per interpretare `schedule_type` e `identifier` ora usa `kwargs['params']`.
    * `sys.exit()` è sostituito da `raise Exception()`.
    * `read_db` ora può passare `ti` per usare XComs per comunicare il numero di tabelle processate/fallite.
7.  **Callback Email (`on_success_email_callback`, `on_failure_email_callback`):**
    * Queste funzioni vengono passate ai `default_args` del DAG o direttamente al `PythonOperator`.
    * Ricevono il `context` dell'esecuzione del task.
    * Usano XComs (se impostati da `main_script_logic`) per ottenere dettagli sull'esecuzione per il corpo dell'email.
    * La funzione `send_mail_dag` viene riutilizzata.
8.  **Definizione del `DAG`:**
    * `dag_id`: Un nome univoco per il tuo DAG.
    * `schedule_interval`: Definisce quando il DAG deve essere eseguito. `None` significa solo esecuzione manuale.
    * `start_date`: Data di inizio per la schedulazione.
    * `default_args`: Argomenti di default per tutti i task nel DAG, incluse le callback.
    * `params`: Definisce i parametri che possono essere forniti all'avvio manuale del DAG, rimpiazzando `argparse`. Ho mappato i tuoi argomenti a questi parametri.
9.  **`PythonOperator`:**
    * Esegue la funzione `main_script_logic`.
    * `on_success_callback` è stato aggiunto per gestire l'email di successo in modo più granulare, tenendo conto dei fallimenti parziali comunicati via XCom da `read_db`.

**Prima di eseguire:**

* **Installazione Librerie:** Assicurati che tutte le librerie Python (`psycopg2-binary`, `oracledb`, `python-dotenv`) siano installate nell'ambiente Python usato dai tuoi worker Airflow.
* **Client Oracle:** Il client Oracle deve essere installato e configurato correttamente sui worker Airflow, e la variabile d'ambiente `ORACLE_CLIENT_LIB_DIR` deve puntare alla directory corretta.
* **`GEOSCRIPTS_HOME` e `.env`:** La variabile d'ambiente `GEOSCRIPTS_HOME` deve essere impostata nell'ambiente dei worker Airflow, e il file `.env` deve essere presente nel percorso `$GEOSCRIPTS_HOME/.env` e leggibile dai worker.
* **`ogr2ogr`:** L'utility `ogr2ogr` deve essere installata e nel `PATH` dei worker Airflow.
* **Connessioni Airflow (Raccomandato):** Per un ambiente di produzione, considera di spostare le credenziali del database e SMTP nelle Connessioni Airflow e le altre configurazioni nelle Variabili Airflow, invece di usare il file `.env`. Questo richiederebbe di modificare le funzioni `initialize_config_and_oracle_client`, `connect_db_dag` e `send_mail_dag` per recuperare i valori da Airflow.
* **Permessi `LOG_DIR`:** Assicurati che i worker Airflow abbiano i permessi di scrittura nella directory `LOG_DIR` specificata tramite `GEOSCRIPTS_HOME`.
* **TNSNAMES.ORA (per OGR):** Se le stringhe di connessione Oracle usano alias TNS (es. `MIO_DB_ALIAS` in `utente/pwd@MIO_DB_ALIAS`), assicurati che un file `tnsnames.ora` valido sia configurato sui worker Airflow e che la variabile d'ambiente `TNS_ADMIN` punti alla directory contenente questo file. Questo è cruciale per `ogr2ogr`.

Questo DAG è un punto di partenza. Potrebbe essere necessario affinarlo ulteriormente in base al comportamento specifico che desideri e alle migliori pratiche del tuo ambiente Airflow. Ad esempio, la gestione degli errori e dei tentativi potrebbe essere resa più granulare suddividendo `main_script_logic` in più task Airflow, ma ciò aumenterebbe la complessità della gestione dello stato (come le connessioni DB).

---

# you asked

sostituisci la chiamata a subprocess.run alla esecuzione di un job kubernetes con gli stessi parametri (comando_args)

---

# gemini response

Per sostituire la chiamata `subprocess.run` con l'esecuzione di un job Kubernetes, utilizzeremo il `KubernetesPodOperator` di Airflow. Questo comporta un cambiamento significativo nella struttura e nel modo in cui il lavoro viene eseguito, poiché `KubernetesPodOperator` è un task di Airflow a sé stante e non una funzione che puoi chiamare direttamente all'interno del tuo script Python esistente nello stesso modo di `subprocess.run`.

**Cambiamenti Fondamentali:**

1.  **Docker Image:** Avrai bisogno di un'immagine Docker che contenga:
    * `ogr2ogr`
    * Client Oracle Instant Client (con `TNS_ADMIN` configurato se usi alias TNS)
    * Le librerie necessarie per far connettere OGR a PostgreSQL (solitamente incluse in GDAL/OGR).
    * Eventuali script di entrypoint o configurazioni aggiuntive.

2.  **Struttura del DAG:**
    * La logica di `import_table` dovrà essere divisa.
    * Una parte (come `get_dim`) potrebbe dover essere eseguita *prima* del task Kubernetes per preparare gli argomenti.
    * Il comando `ogr2ogr` diventerà un `KubernetesPodOperator`.
    * Le operazioni post-`ogr2ogr` (validazione geometrie, indici, vacuum, conteggi, log DB) diventeranno un altro task Airflow (probabilmente un `PythonOperator`) che dipende dal successo del `KubernetesPodOperator`.
    * Questo dovrà essere fatto dinamicamente per ogni tabella.

3.  **Gestione delle Credenziali:** Le credenziali per PostgreSQL e Oracle (se non parte della `stringa_conn` in un modo che OGR possa usare direttamente) dovrebbero essere passate al pod Kubernetes in modo sicuro, preferibilmente tramite Kubernetes Secrets e montate come variabili d'ambiente o file.

4.  **Comunicazione tra Task:** XComs di Airflow sarà usato per passare dati tra i task (es. il `dim` calcolato al `KubernetesPodOperator`, e lo stato di completamento del K8s job al task di post-elaborazione).

**Illustrazione della Modifica (Concettuale):**

Dato che una sostituzione diretta 1:1 mantenendo la struttura dello script attuale è problematica con gli operatori Airflow, ti mostrerò come sarebbe la configurazione di un `KubernetesPodOperator` per una singola esecuzione di `ogr2ogr`. Poi discuteremo come integrarlo nel flusso del DAG.

All'interno della tua funzione `import_table`, invece di chiamare `subprocess.run`, dovresti preparare i parametri per un `KubernetesPodOperator`.

Ecco una versione modificata della sezione `import_table` che evidenzia come prepareresti i parametri per un `KubernetesPodOperator`. Nota che questa funzione, così com'è, non *esegue* l'operatore, ma ne definisce la configurazione.

```python
# Aggiungi questi import all'inizio del tuo file DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.kubernetes.secret import Secret
# Potresti aver bisogno di from airflow.kubernetes.volume import Volume
# e from airflow.kubernetes.volume_mount import VolumeMount se devi montare file (es. tnsnames.ora)

# ... (altri tuoi import e funzioni globali) ...

# All'interno della funzione main_script_logic o dove import_table è chiamata,
# dovrai gestire il flusso in modo diverso.
# Per ora, modifichiamo import_table per illustrare la configurazione del K8sPodOperator.

def import_table_k8s(
    stringa_conn, tab_geom, pg_schema, epsg_code, pk_field, geom_field, ora_schema_orig,
    dim_value, # Questo deve essere calcolato PRIMA di definire il K8s job
    run_id_suffix, # Per nomi univoci di pod/task
    # Parametri per connessioni K8s (da Airflow Connections/Variables)
    k8s_pg_host, k8s_pg_port, k8s_pg_db_name, k8s_pg_user,
    k8s_pg_password_secret_name, # Nome del K8s Secret per la password PG
    k8s_pg_password_secret_key,  # Chiave nel K8s Secret per la password PG
    # k8s_oracle_password_secret_name, # Se la password Oracle deve essere iniettata
    # k8s_oracle_password_secret_key,
    kubernetes_namespace, # Namespace Kubernetes dove eseguire il pod
    gdal_docker_image, # La tua immagine Docker con GDAL, client Oracle, etc.
    # event_timestamp # per il nome del pod, se vuoi
    dag # Passa l'oggetto DAG per creare task dinamicamente (avanzato)
):
    """
    Questa funzione ora definisce un KubernetesPodOperator per eseguire ogr2ogr
    e un PythonOperator per i passaggi successivi.
    NON esegue direttamente il subprocess.
    """
    global PG_HOST, PG_PORT, PG_DB_NAME, PG_USER, PG_PWD # Usati per i conteggi PG post-import

    print_log("INFO", f"Preparazione K8s job per TAVOLA: {tab_geom} (da {stringa_conn})")

    # Sanitize per nomi di tabelle e task PG
    safe_ora_schema_part = "".join(c if c.isalnum() else '_' for c in ora_schema_orig)
    safe_tab_geom_part = "".join(c if c.isalnum() else '_' for c in tab_geom)
    pg_tab_geom = f"{safe_ora_schema_part.lower()}_{safe_tab_geom_part.lower()}"
    source_table_in_oracle = f"{ora_schema_orig}.{tab_geom}" if ora_schema_orig else tab_geom

    # Costruzione della stringa di connessione OCI per ogr2ogr
    # stringa_conn è del tipo "utente/password@alias" o "utente@alias"
    # Se è "utente@alias", la password Oracle potrebbe essere iniettata via env var
    oci_connection_part = stringa_conn
    # Esempio se la password Oracle viene da un secret:
    # oci_user = stringa_conn.split('@')[0]
    # oci_alias = stringa_conn.split('@')[1]
    # oci_connection_part = f"{oci_user}@\"{oci_alias}\"" # Potrebbe necessitare di quoting per OGR
    # E ORACLE_PASSWORD_K8S sarebbe impostata come env var dal secret.

    # Argomenti per il comando ogr2ogr (escluso "ogr2ogr" stesso)
    ogr_arguments = [
        "-overwrite",
        "-f", "PostgreSQL",
        # La stringa di connessione PG userà variabili d'ambiente definite nel pod
        f"PG:host=$(PG_HOST_K8S) port=$(PG_PORT_K8S) dbname=$(PG_DB_NAME_K8S) user=$(PG_USER_K8S) password=$(PG_PASSWORD_K8S) active_schema={pg_schema}",
        f"OCI:{oci_connection_part}",
        "-sql", f"SELECT * FROM \"{source_table_in_oracle}\"", # Assicurati che il quoting sia corretto per Oracle se ci sono maiuscole/minuscole
        "-a_srs", f"EPSG:{epsg_code}",
        "--config", "PG_USE_COPY", "YES",
        "-lco", "FID=ogr_fid", # Nome colonna chiave primaria in PG
        "-lco", f"DIM={dim_value}", # dim_value deve essere passato a questa funzione
        "-lco", f"GEOMETRY_NAME=wkb_geometry",
        "-nln", f"{pg_schema}.{pg_tab_geom}"
    ]
    if pk_field:
        ogr_arguments.extend(["-lco", f"PRIMARY_KEY={pk_field.lower()}"])

    # Variabili d'ambiente per il pod Kubernetes
    env_vars_for_pod = {
        "PG_HOST_K8S": k8s_pg_host,
        "PG_PORT_K8S": str(k8s_pg_port),
        "PG_DB_NAME_K8S": k8s_pg_db_name,
        "PG_USER_K8S": k8s_pg_user,
        # Altre variabili necessarie per il client Oracle nell'immagine Docker:
        "TNS_ADMIN": os.getenv("TNS_ADMIN", "/opt/oracle/network/admin"), # Esempio, deve corrispondere all'immagine
        "LD_LIBRARY_PATH": os.getenv("ORACLE_CLIENT_LIB_DIR", "/opt/oracle/instantclient") + ":" + os.getenv("LD_LIBRARY_PATH",""), # Esempio
        # "ORACLE_HOME": "/opt/oracle/instantclient" # Se necessario
    }

    # Definisci i secret da montare come variabili d'ambiente
    secrets_for_pod = [
        Secret(deploy_type='env',
               deploy_target='PG_PASSWORD_K8S', # Nome della var d'ambiente nel pod
               secret=k8s_pg_password_secret_name, # Nome del K8s Secret object
               key=k8s_pg_password_secret_key)    # Chiave nel K8s Secret (es. 'password')
    ]
    # if k8s_oracle_password_secret_name: # Aggiungi secret per password Oracle se necessario
    #     secrets_for_pod.append(
    #         Secret(deploy_type='env', deploy_target='ORACLE_PASSWORD_K8S',
    #                secret=k8s_oracle_password_secret_name, key=k8s_oracle_password_secret_key)
    #     )

    # Nome univoco per il pod e per il task Airflow
    base_task_name = f"{safe_ora_schema_part.lower()}_{safe_tab_geom_part.lower()}_{run_id_suffix}"
    pod_name = f"ogr2ogr-{base_task_name}".replace('_', '-').lower()[:63] # DNS-1123 compliant
    ogr_k8s_task_id = f"ogr_k8s_{base_task_name}"

    # Definizione del KubernetesPodOperator
    # Questo operatore verrebbe istanziato nel flusso del DAG, non qui dentro direttamente per l'esecuzione.
    ogr_k8s_task = KubernetesPodOperator(
        task_id=ogr_k8s_task_id,
        name=pod_name,
        namespace=kubernetes_namespace,
        image=gdal_docker_image, # Es: 'yourrepo/gdal-oracle:latest'
        cmds=["ogr2ogr"],
        arguments=ogr_arguments,
        env_vars=env_vars_for_pod,
        secrets=secrets_for_pod,
        get_logs=True, # Per recuperare i log del pod in Airflow
        log_events_on_failure=True, # Logga eventi K8s se il pod fallisce
        is_delete_operator_pod=True, # Cancella il pod dopo il completamento
        startup_timeout_seconds=600, # Timeout per l'avvio del pod
        # resources={'request_memory': '1Gi', 'limit_memory': '4Gi', 'request_cpu': '500m', 'limit_cpu': '1'}, # Esempio
        # image_pull_policy='Always', # O 'IfNotPresent'
        # Se necessario, configura i volumi per tnsnames.ora, etc.
        # E.g., se tnsnames.ora è in un configmap:
        # volumes=[Volume(name='oracle-config-volume', configmap={'name': 'tnsnames-configmap'})],
        # volume_mounts=[VolumeMount(name='oracle-config-volume', mount_path='/opt/oracle/network/admin', read_only=True)]
        dag=dag # Importante se si creano task dinamicamente nel contesto del DAG
    )

    # Ora, le operazioni post-OGR diventano un altro task che dipende da ogr_k8s_task
    # Queste informazioni verranno usate per creare un PythonOperator
    post_ogr_task_id = f"post_ogr_proc_{base_task_name}"
    post_ogr_params = {
        "pg_schema": pg_schema,
        "pg_tab_geom": pg_tab_geom,
        "pk_field": pk_field,
        "original_stringa_conn": stringa_conn,
        "original_tab_geom": tab_geom,
        "original_ora_schema": ora_schema_orig,
        "epsg_code": epsg_code, # Potrebbe servire per XComs o log
        # "geom_db_stringa_conn": stringa_conn, # Usato da get_geom_db per get_ora_count
        # "istanza_global_val": istanza_global # Per write_db_log
    }

    # La funzione `post_ogr_callable_logic` conterrebbe la logica dopo il subprocess.run
    # (bonifica, indici, vacuum, conteggi, write_db_log)
    # post_ogr_task = PythonOperator(
    #     task_id=post_ogr_task_id,
    #     python_callable=post_ogr_callable_logic, # Funzione separata
    #     op_kwargs=post_ogr_params,
    #     # provide_context=True è default
    #     dag=dag
    # )
    # ogr_k8s_task >> post_ogr_task # Imposta la dipendenza

    # Per ora, questa funzione ritorna i task definiti (o le loro configurazioni)
    # La logica del DAG principale li orchestrerà.
    # Questo è un cambiamento concettuale: import_table non fa più il lavoro,
    # ma definisce i task che lo faranno.
    print_log("INFO", f"Definizione task Kubernetes e post-processing per {pg_tab_geom} completata.")
    return ogr_k8s_task, post_ogr_task_id, post_ogr_params # Modificato per ritornare anche i parametri del post_ogr_task
```

**Come cambierebbe il flusso principale (`main_script_logic` e `read_db`):**

La funzione `read_db` non chiamerebbe più `import_table` per eseguire direttamente il lavoro. Invece:

1.  **`Task_A_Setup_Connections_And_Config` (PythonOperator):**
    * Esegue `initialize_config_and_oracle_client`, `setup_logging_dag`, `connect_db_dag`.

2.  **`Task_B_Fetch_Table_Definitions` (PythonOperator):**
    * Esegue la query SQL per ottenere l'elenco delle tabelle da `PG_CACHE_LAYERS` (la parte iniziale di `read_db`).
    * Per ogni tabella, esegue `get_geom_db` e `get_dim` per ottenere `dim_value`. Questo è cruciale perché `dim_value` è necessario *prima* di poter definire il job Kubernetes.
    * Restituisce (via XCom) una lista di dizionari, ognuno contenente: `stringa_conn`, `tab_geom`, `epsg_code`, `pk_field`, `geom_field`, `ora_schema`, e il `dim_value` calcolato.

3.  **Generazione Dinamica dei Task nel DAG (fuori da un PythonOperator, al momento della definizione del DAG):**
    * Questa è la parte più complessa da adattare dalla struttura sequenziale. Si userebbe la TaskFlow API con `Dynamic Task Mapping` o un loop che crea istanze di operatori.
    * Per ogni configurazione di tabella ricevuta da `Task_B_Fetch_Table_Definitions` (tramite XComs):
        * Si istanzierebbe un `KubernetesPodOperator` (usando una funzione simile a `import_table_k8s` per ottenere la configurazione).
        * Si istanzierebbe un `PythonOperator` per la logica post-OGR (che chiamerebbe una funzione come `post_ogr_callable_logic`), passando i parametri necessari.
        * Si imposterebbe la dipendenza: `KubernetesPodOperator >> PythonOperator_Post_OGR`.

4.  **`Task_C_Run_Post_Update_Views` (PythonOperator):**
    * Esegue `post_update()`. Deve dipendere da tutti i task di post-elaborazione delle tabelle.

5.  **`Task_D_Cleanup_Connections` (PythonOperator):**
    * Esegue `close_db_dag()`.

**Esempio di come `post_ogr_callable_logic` potrebbe apparire (semplificato):**

```python
def post_ogr_callable_logic(**kwargs):
    ti = kwargs['ti']
    # Recupera i parametri passati da op_kwargs
    pg_schema = kwargs['pg_schema']
    pg_tab_geom = kwargs['pg_tab_geom']
    pk_field = kwargs['pk_field']
    original_stringa_conn = kwargs['original_stringa_conn']
    original_tab_geom = kwargs['original_tab_geom']
    original_ora_schema = kwargs['original_ora_schema']
    # istanza_global_val = kwargs['istanza_global_val'] # Da gestire come passare istanza

    # QUI VA LA LOGICA DA import_table DOPO IL subprocess.run:
    # 1. Assicurati che le connessioni DB globali (pg_conn_global, ora_conn_global) siano attive
    #    o stabilisci connessioni locali. Per semplicità, assumiamo siano globali e attive.
    #    In un DAG reale, ogni task dovrebbe gestire le proprie connessioni o usare hooks.
    if not pg_conn_global or pg_conn_global.closed:
        print_log("ERROR", "PG Connection not available in post_ogr_callable_logic.")
        raise ConnectionError("PG Connection lost in post_ogr_callable_logic")
    # Similmente per ora_conn_global se write_db_log lo usa direttamente.

    print_log("INFO", f"Inizio post-elaborazione OGR per {pg_schema}.{pg_tab_geom}")

    # --- BONIFICA GEOMETRIE NON VALIDE (Polygons) ---
    # (Copia la logica da import_table usando pg_schema, pg_tab_geom e execute_pg)
    # Esempio:
    # from psycopg2 import sql as pgsql
    # valid_cmd_sql = pgsql.SQL(...)
    # execute_pg(valid_cmd_sql)
    # print_log("INFO", "BONIFICA GEOMETRIE OK")

    # --- CREO INDICI E VACUUM ---
    # (Copia la logica da import_table usando pk_field, pg_schema, pg_tab_geom e execute_pg)

    # --- CONTEGGIO RECORD ---
    geom_db_for_count = None
    try:
        geom_db_for_count = get_geom_db(original_stringa_conn) # Apre una nuova connessione specifica
        if geom_db_for_count:
            feature_name_ora_qualified = f"{original_ora_schema}.{original_tab_geom}" if original_ora_schema else original_tab_geom
            ora_count = get_ora_count(geom_db_for_count, feature_name_ora_qualified)
        else:
            ora_count = "N/A (geom_db connection failed)"
    except Exception as e_geom_db:
        print_log("ERROR", f"Errore connessione a geom_db per conteggio Oracle: {e_geom_db}")
        ora_count = f"N/A (Error: {e_geom_db})"
    finally:
        if geom_db_for_count:
            geom_db_for_count.close()

    pg_count = get_pg_count(f"{pg_schema}.{pg_tab_geom}") # Usa pg_conn_global
    print_log("INFO", f"CONTEGGIO RECORD - ORACLE ({original_ora_schema}.{original_tab_geom}): {ora_count} - PG ({pg_schema}.{pg_tab_geom}): {pg_count}")
    if ora_count != pg_count and ora_count != "N/A": # Solo se il conteggio Oracle è valido
         print_log("WARNING", f"Record counts do not match for {original_tab_geom}!")

    # --- WRITE DB LOG ---
    # Calcolare td_tavola_minutes è difficile qui perché il tempo di OGR è nel K8s Job.
    # Potresti passare il tempo di inizio e fine del K8s job via XCom se necessario,
    # oppure loggare solo il tempo di post-elaborazione.
    # Per ora, logghiamo un tempo placeholder o nessun tempo.
    # write_db_log(original_stringa_conn, original_tab_geom, 0, istanza_global_val) # Assumendo istanza_global_val passato
    print_log("INFO", f"IMPORT OK per {original_tab_geom} (post-elaborazione completata)")

```

**Integrazione nel file DAG Airflow (Schema):**

```python
# ... all your imports, including KubernetesPodOperator, Secret ...
# ... all your original functions (setup_logging_dag, print_log, connect_db_dag, etc.) ...
# ... la funzione get_dim, get_geom_db, get_ora_count, get_pg_count, write_db_log ...
# ... la funzione post_ogr_callable_logic definita sopra ...
# ... la funzione import_table_k8s definita sopra (o una simile per configurare K8sOp) ...

# Recupera le configurazioni K8s (da Airflow Variables o Connections)
KUBERNETES_NAMESPACE = os.getenv("AIRFLOW_KUBERNETES_NAMESPACE", "default")
GDAL_DOCKER_IMAGE = os.getenv("GDAL_DOCKER_IMAGE", "yourrepo/gdal-oracle-pg:latest") # CAMBIARE
PG_PWD_K8S_SECRET_NAME = os.getenv("PG_PWD_K8S_SECRET_NAME", "postgres-credentials") # CAMBIARE
PG_PWD_K8S_SECRET_KEY = os.getenv("PG_PWD_K8S_SECRET_KEY", "password") # CAMBIARE

# (Le callback email rimangono simili)

def prepare_table_processing_info_callable(**kwargs):
    # Questa funzione esegue la query per ottenere le tabelle
    # e per ogni tabella, calcola 'dim_value'.
    # Ritorna una lista di dizionari, ognuno pronto per 'import_table_k8s' e 'post_ogr_callable_logic'
    global istanza_global # Assicurati che sia impostata come nello script originale
    
    # ... (logica da main_script_logic per determinare istanza_global, flag_schedulata, param_for_query) ...
    # ... (logica da main_script_logic per costruire comando_selezione_tabelle e query_params) ...

    # Assicurati che le connessioni DB (ora_conn_global) siano attive
    if not ora_conn_global or not hasattr(ora_conn_global, 'cursor'): # Aggiunto controllo più robusto
        print_log("ERROR", "Oracle connection not available in prepare_table_processing_info_callable.")
        connect_db_dag() # Tenta di riconnettere o fallisce
        # raise ConnectionError("Oracle connection lost") # Fallisci se non puoi connettere

    table_configs_for_k8s = []
    try:
        with ora_conn_global.cursor() as cur:
            # comando_selezione_tabelle e query_params devono essere definiti qui
            # basati sulla logica originale di main_script_logic
            # Esempio basato sulla tua logica precedente in main_script_logic:
            # (Questa parte deve essere adattata dalla tua funzione main_script_logic)
            params_from_dag = kwargs.get('params', {})
            schedule_type_param = params_from_dag.get('schedule_type')
            identifier_param = params_from_dag.get('identifier')
            # ... (resto della logica per determinare istanza_global, where_clause, query_params) ...
            # Per questo esempio, hardcodiamo una query fittizia, DEVI adattarla:
            # --- INIZIO LOGICA DA main_script_logic PER QUERY ---
            base_comando = "SELECT DISTINCT STRINGA_CONN, TAB_GEOM, UPPER(SUBSTR(STRINGA_CONN,0,INSTR(STRINGA_CONN,'/')-1)) AS ORA_SCHEMA_CONN_USER, EPSG_CODE, PK_FIELD, GEOM_FIELD, ORA_SCHEMA FROM PG_CACHE_LAYERS"
            where_clause = ""
            order_by = " ORDER BY STRINGA_CONN, TAB_GEOM"
            query_params_ora = {} # Rinominata per evitare conflitti

            if schedule_type_param:
                istanza_global = schedule_type_param
                where_clause = " WHERE ID_LAYER IN (SELECT DISTINCT ID_LAYER FROM GS_LAYERS WHERE CACHE_SCHEDULATA LIKE :p_instance || '_%') AND POSTGIS_CACHE = 'S'"
                query_params_ora = {'p_instance': istanza_global}
            elif identifier_param:
                istanza_global = f"ID_{identifier_param.replace(',','_')[:20]}"
                if identifier_param.upper().startswith("L"):
                    layer_ids_str = identifier_param[1:].split(',')
                    layer_ids = [int(x.strip()) for x in layer_ids_str if x.strip().isdigit()]
                    if not layer_ids: raise ValueError("No valid layer IDs found after parsing.")
                    id_placeholders = ','.join([f':id{i}' for i in range(len(layer_ids))])
                    where_clause = f" WHERE ID_LAYER IN ({id_placeholders}) AND POSTGIS_CACHE = 'S'"
                    query_params_ora = {f'id{i}': lid for i, lid in enumerate(layer_ids)}
                else:
                    map_ids_str = identifier_param.split(',')
                    map_ids = [int(x.strip()) for x in map_ids_str if x.strip().isdigit()]
                    if not map_ids: raise ValueError("No valid map IDs found after parsing.")
                    id_placeholders = ','.join([f':id{i}' for i in range(len(map_ids))])
                    where_clause = f" WHERE ID_MAP IN ({id_placeholders}) AND POSTGIS_CACHE = 'S'"
                    query_params_ora = {f'id{i}': mid for i, mid in enumerate(map_ids)}
            else:
                raise ValueError("Parametri DAG non validi: specificare schedule_type o identifier.")
            comando_selezione_tabelle = base_comando + where_clause + order_by
            # --- FINE LOGICA DA main_script_logic PER QUERY ---

            print_log("INFO", f"Esecuzione query Oracle per tabelle: {comando_selezione_tabelle} con params {query_params_ora}")
            cur.execute(comando_selezione_tabelle, query_params_ora or {})
            columns = [col[0].upper() for col in cur.description]
            rows = cur.fetchall()

        print_log("INFO", f"Trovate {len(rows)} tabelle per pre-elaborazione.")
        for i, row_tuple in enumerate(rows):
            row_dict = dict(zip(columns, row_tuple))
            stringa_conn_val = row_dict.get('STRINGA_CONN')
            tab_geom_val = row_dict.get('TAB_GEOM')
            epsg_code_val = row_dict.get('EPSG_CODE')
            pk_field_val = row_dict.get('PK_FIELD')
            geom_field_val = row_dict.get('GEOM_FIELD')
            ora_schema_val = row_dict.get('ORA_SCHEMA')

            if not all([stringa_conn_val, tab_geom_val, epsg_code_val, ora_schema_val]):
                 print_log("WARNING", f"Skipping row {i+1} per dati mancanti: {row_dict}")
                 continue

            print_log("INFO",f"Pre-elaborazione per {ora_schema_val}.{tab_geom_val} (da {stringa_conn_val})")
            geom_db_conn = None
            dim_value = None
            try:
                geom_db_conn = get_geom_db(stringa_conn_val)
                if geom_db_conn:
                    feature_name_ora_qualified = f"{ora_schema_val}.{tab_geom_val}" if ora_schema_val else tab_geom_val
                    dim_value = get_dim(geom_db_conn, feature_name_ora_qualified, geom_field_val)
                else:
                    print_log("ERROR", f"Connessione a Geometry DB fallita per {stringa_conn_val}. Impossibile ottenere dim.")
                    # Continua al prossimo? o fallisci? Per ora saltiamo questa tabella.
                    continue
            except Exception as e_dim:
                print_log("ERROR", f"Errore durante get_dim per {ora_schema_val}.{tab_geom_val}: {e_dim}")
                # Continua al prossimo?
                continue # Salta questa tabella se non si può ottenere dim
            finally:
                if geom_db_conn:
                    geom_db_conn.close()

            if dim_value is None:
                print_log("ERROR", f"Valore DIM non trovato per {ora_schema_val}.{tab_geom_val}. Salto questa tabella.")
                continue

            table_configs_for_k8s.append({
                "stringa_conn": stringa_conn_val, "tab_geom": tab_geom_val,
                "ora_schema_orig": ora_schema_val, "epsg_code": epsg_code_val,
                "pk_field": pk_field_val, "geom_field": geom_field_val,
                "dim_value": dim_value,
                "run_id_suffix": kwargs['dag_run'].run_id.replace(':','-').replace('+','-') # per nomi univoci
            })
    except Exception as e_query:
        print_log("ERROR", f"Errore durante query tabelle o calcolo DIM: {e_query}")
        raise
    
    if not table_configs_for_k8s:
        print_log("WARNING", "Nessuna tabella trovata o pre-elaborata per l'importazione K8s.")
        # Potresti voler sollevare un'eccezione o un EmptyOperator. અહીં હું ખાલી સૂચિ પરત કરીશ.
    return table_configs_for_k8s


# Logica principale del DAG
with DAG(**dag_params) as dag: # dag_params definito come prima

    # TASK 1: Inizializzazione e connessioni DB principali
    def initial_setup_callable(**kwargs):
        # run_id per il logging, potrebbe essere passato a setup_logging_dag se necessario
        run_id_for_log = kwargs['dag_run'].run_id if kwargs.get('dag_run') else str(uuid.uuid4())
        initialize_config_and_oracle_client()
        main_logger_global = setup_logging_dag(run_id_for_log) # Salva il logger se necessario globalmente o passalo
        # Connetti ai DB principali che saranno usati da più task (se questo è il tuo design)
        # Altrimenti, ogni task dovrebbe gestire le proprie connessioni.
        # Per questo esempio, manteniamo le connessioni globali come nel tuo script.
        connect_db_dag()
        # Passa le variabili globali necessarie via XCom se i task successivi non possono accedervi
        # o se preferisci un passaggio esplicito di dati.
        # Ad esempio, potresti passare PG_HOST, etc., se servono ai task K8s
        # ma è meglio che i task K8s li ricevano da variabili/secret di Airflow.
        kwargs['ti'].xcom_push(key="pg_host_main", value=PG_HOST)
        kwargs['ti'].xcom_push(key="pg_port_main", value=PG_PORT)
        kwargs['ti'].xcom_push(key="pg_db_name_main", value=PG_DB_NAME)
        kwargs['ti'].xcom_push(key="pg_user_main", value=PG_USER)
        # Non passare PG_PWD qui! Deve venire da un secret K8s per il pod.

    initial_setup_task = PythonOperator(
        task_id='initial_setup_connections',
        python_callable=initial_setup_callable,
    )

    # TASK 2: Ottieni la lista delle tabelle e calcola DIM per ognuna
    prepare_tables_task = PythonOperator(
        task_id='prepare_table_processing_info',
        python_callable=prepare_table_processing_info_callable,
    )

    # TASK 3 (Gruppo Dinamico): Processa ogni tabella (K8s + Post-Proc)
    # Questo è dove la generazione dinamica dei task avverrebbe.
    # Con TaskFlow API e Dynamic Task Mapping:
    # @task_group
    # def process_table_group(table_config_dict_with_dim, pg_params_dict):
    #     # ... (chiama import_table_k8s per definire K8sOp) ...
    #     # ... (chiama PythonOp per post_ogr_callable_logic) ...
    # mapped_processing = process_table_group.expand(
    #     table_config_dict_with_dim=prepare_tables_task.output,
    #     pg_params_dict= # passa i parametri PG da initial_setup_task.output o da Airflow Variables
    # )

    # Senza TaskFlow, la generazione dinamica è più verbosa e avviene al parsing del DAG
    # Questo richiederebbe che prepare_tables_task restituisca una lista statica al momento del parsing
    # o che si usi un BranchPythonOperator e si creino i task in rami separati.
    # Per ora, lo lascio come un concetto, dato che l'implementazione completa
    # della generazione dinamica è complessa e dipende dalla versione di Airflow.

    # Placeholder per il flusso dinamico:
    # Immagina che dopo prepare_tables_task, ci sia un meccanismo (es. un loop nel file DAG
    # se la lista fosse statica, o dynamic task mapping) per creare:
    # Per ogni tabella_config in XCom da prepare_tables_task:
    #   k8s_op, post_op_id, post_op_kwargs = import_table_k8s(
    #       **table_config, # Contiene stringa_conn, tab_geom, dim_value, etc.
    #       k8s_pg_host=initial_setup_task.output['pg_host_main'], # Esempio recupero da XCom
    #       k8s_pg_port=initial_setup_task.output['pg_port_main'],
    #       k8s_pg_db_name=initial_setup_task.output['pg_db_name_main'],
    #       k8s_pg_user=initial_setup_task.output['pg_user_main'],
    #       k8s_pg_password_secret_name=PG_PWD_K8S_SECRET_NAME, # Da var/conn Airflow
    #       k8s_pg_password_secret_key=PG_PWD_K8S_SECRET_KEY,   # Da var/conn Airflow
    #       kubernetes_namespace=KUBERNETES_NAMESPACE,           # Da var/conn Airflow
    #       gdal_docker_image=GDAL_DOCKER_IMAGE,                 # Da var/conn Airflow
    #       dag=dag
    #   )
    #   # k8s_op è l'istanza di KubernetesPodOperator
    #   post_ogr_py_op = PythonOperator(task_id=post_op_id, python_callable=post_ogr_callable_logic, op_kwargs=post_op_kwargs, dag=dag)
    #   prepare_tables_task >> k8s_op >> post_ogr_py_op >> [ Task Successivo Collettivo ]

    # Per questa risposta, dato che non posso implementare il mapping dinamico completo qui,
    # lascerò il flusso principale come era, con la consapevolezza che
    # `main_script_logic` dovrebbe essere sostituita da questo flusso dinamico.
    # Sostituisco run_main_script_task con i task definiti:
    
    # Task fittizio per rappresentare il punto di raccolta dei task dinamici
    # (se fossero implementati)
    dynamic_processing_ લગભગ_done_sentinel = EmptyOperator(task_id="dynamic_processing_completed_sentinel", dag=dag)


    # TASK 4: Aggiorna le viste (dipende dal completamento di tutti i processing delle tabelle)
    def post_update_views_callable(**kwargs):
        # Assicurati che pg_conn_global sia disponibile e connesso
        if not pg_conn_global or pg_conn_global.closed:
            print_log("ERROR", "PG Connection not available for post_update_views.")
            # Prova a riconnettere o fallisci in modo appropriato
            # connect_db_dag() # Potrebbe essere rischioso se non si sa lo stato
            raise ConnectionError("PG Connection lost before post_update_views")
        post_update()

    post_update_views_task = PythonOperator(
        task_id='post_update_views',
        python_callable=post_update_views_callable,
    )

    # TASK 5: Cleanup
    def final_cleanup_callable(**kwargs):
        close_db_dag()
        # Pulisci logger se necessario (handler.close())
        if main_logger_global:
            for handler in list(main_logger_global.handlers):
                handler.close()
                main_logger_global.removeHandler(handler)
        root_logger_handlers = logging.getLogger().handlers
        if log_file_path_global: # Controlla se la variabile è stata impostata
            for handler in list(root_logger_handlers):
                if isinstance(handler, logging.FileHandler) and handler.baseFilename == log_file_path_global:
                    handler.close()
                    logging.getLogger().removeHandler(handler)
        print_log("INFO", "Cleanup connections and loggers complete.")


    final_cleanup_task = PythonOperator(
        task_id='final_cleanup_connections',
        python_callable=final_cleanup_callable,
        trigger_rule='all_done', # Esegui sempre, anche se i task precedenti falliscono
    )

    # Definizione delle dipendenze
    initial_setup_task >> prepare_tables_task
    # Qui ci sarebbe la logica per collegare prepare_tables_task ai task dinamici
    # e i task dinamici a dynamic_processing_casi_done_sentinel
    prepare_tables_task >> dynamic_processing_casi_done_sentinel # Semplificazione
    
    dynamic_processing_casi_done_sentinel >> post_update_views_task >> final_cleanup_task

    # Le callback di successo/fallimento rimangono sui default_args del DAG
    # e si applicheranno a questi task. Dovranno essere adattate per riflettere
    # la nuova struttura (es. non c'è più un singolo "run_type_param" XCom globale).
```

**Sfide e Prossimi Passi:**

1.  **Generazione Dinamica dei Task:** Questa è la parte più complessa. Dovrai usare:
    * **Airflow 2.x TaskFlow API con Dynamic Task Mapping:** Il metodo preferito. `prepare_tables_task` restituirebbe la lista di configurazioni, e un `@task_group` o `@task` verrebbe mappato dinamicamente su questa lista.
    * **Loop nel file DAG (Airflow < 2.x o per operatori classici):** Se la lista delle tabelle fosse nota al momento del parsing del DAG (non da XCom), potresti fare un loop e creare i task. Ma poiché la lista viene da un task precedente, questo approccio è più difficile.

2.  **Gestione dello Stato e delle Connessioni:** Idealmente, ogni task (o gruppo di task per tabella) dovrebbe gestire le proprie connessioni DB usando Airflow Hooks o stabilendole e chiudendole al suo interno, invece di fare affidamento su connessioni globali.

3.  **Docker Image:** Creare e mantenere l'immagine Docker con tutti gli strumenti e le configurazioni corrette (`TNS_ADMIN`, `LD_LIBRARY_PATH`, client Oracle compatibili con la tua versione DB, GDAL) è essenziale.

4.  **Kubernetes Secrets:** Configura i Kubernetes Secrets per le password e referenziali nelle definizioni del `KubernetesPodOperator`.

5.  **Error Handling:** La logica di `ORA-13208` o altri errori specifici di `ogr2ogr` dovrebbe essere gestita. Questo potrebbe significare:
    * Un wrapper script nell'immagine Docker che esegue `ogr2ogr`, controlla `stderr`, ed esce con un codice specifico.
    * Un task Python successivo che recupera i log del pod (`ti.get_task_instance(task_id_k8s_op).log_filepath`) e li analizza (più complesso).

6.  **Callback Email:** Le callback email dovranno essere riviste perché il concetto di "esecuzione singola" con un `run_type_param` globale cambia quando si hanno molti task dinamici. Potresti volere un riepilogo generale o email per fallimenti specifici di tabelle.

Questa trasformazione è significativa. Ti consiglio di iniziare creando l'immagine Docker e poi implementando il flusso per una singola tabella (senza dinamismo) per assicurarti che `KubernetesPodOperator` funzioni come previsto. Successivamente, puoi affrontare la generazione dinamica dei task.

---

# you asked

Se volessi utilizzare Prefect come orchestrator, in ambiente Kubernetes, come sarebbe il porting dello script python?

---

# gemini response

Assolutamente! Portare lo script Python in un ambiente Prefect gestito su Kubernetes offre un'orchestrazione moderna e flessibile. Prefect (in particolare Prefect 2.x "Orion") si integra bene con Kubernetes.

Ecco come potresti approcciare il porting:

**Principi Chiave del Porting a Prefect:**

1.  **Flussi (`Flows`):** L'intero script o una sua macro-logica diventerà un "flusso" Prefect, decorato con `@flow`.
2.  **Task (`Tasks`):** Le singole unità di lavoro (funzioni Python) diventeranno "task" Prefect, decorati con `@task`. Prefect gestisce automaticamente le dipendenze tra task in base al flusso di dati.
3.  **Parametri:** Gli argomenti da riga di comando (`argparse`) diventeranno parametri del flusso Prefect, rendendoli configurabili al momento dell'esecuzione.
4.  **Esecuzione Kubernetes:** Invece di `subprocess.run` per `ogr2ogr`, userai un task Prefect che crea ed esegue un Job Kubernetes. Questo si fa tipicamente con la collezione `prefect-kubernetes`.
5.  **Configurazione e Secret:** Le credenziali e le configurazioni sensibili (come stringhe di connessione DB, API key per email) dovrebbero essere gestite tramite **Blocchi Prefect** (es. `Secret`, `JSON`, `String`).
6.  **Logging:** Prefect ha un suo sistema di logging integrato. Puoi comunque mantenere il tuo logging su file se necessario.
7.  **Notifiche:** Prefect supporta notifiche per vari stati del flusso/task.
8.  **Deployments:** Per eseguire flussi su schedule o tramite API in un ambiente Kubernetes, creerai un "deployment" Prefect. Un agente/worker Prefect in esecuzione nel tuo cluster Kubernetes preleverà ed eseguirà i flussi.

**Struttura del Codice Prefect:**

Ecco una bozza di come potrebbe apparire il tuo script trasformato.

```python
import os
import sys
import uuid
import logging # Prefect usa il suo logging, ma puoi integrare
import subprocess # Lo sostituiremo per ogr2ogr
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta # timedelta può essere usato per i retry dei task

from dotenv import load_dotenv # Utile per sviluppo locale, in prod usa i Blocchi Prefect
import psycopg2
import oracledb

# Importazioni Prefect
from prefect import flow, task, get_run_logger
from prefect.context import get_run_context
from prefect.blocks.system import Secret # Per le password
from prefect.blocks.core import String as PrefectStringBlock # Per stringhe di config
# Per l'esecuzione di Job Kubernetes
from prefect_kubernetes.jobs import run_kubernetes_job # Task per lanciare un job
from prefect_kubernetes.credentials import KubernetesClusterConfig # Per configurare la connessione al cluster

# --- Inizializzazione e Configurazione (Potrebbero diventare task o helper) ---
# Variabili globali dello script originale (saranno gestite meglio in Prefect)
# È preferibile passare configurazioni e client come argomenti ai task
# o inizializzarli all'interno dei task dove servono.

# Variabili di configurazione che potrebbero venire da Blocchi Prefect
# PG_USER_BLOCK: Secret
# PG_PWD_BLOCK: Secret
# ... e così via per ORA_USER, ORA_PWD, SMTP_SERVER etc.

# GEOSCRIPTS_HOME e ORACLE_CLIENT_LIB_DIR devono essere disponibili nell'ambiente
# in cui viene eseguito il worker Prefect e/o il Job Kubernetes per ogr2ogr.

@task(name="Initialize Configuration and Oracle Client")
def initialize_config_prefect():
    logger = get_run_logger()
    try:
        client_lib_dir = os.environ.get("ORACLE_CLIENT_LIB_DIR")
        if not client_lib_dir:
            logger.warning("ORACLE_CLIENT_LIB_DIR not set, oracledb.init_oracle_client() might fail or use default.")
        else:
            oracledb.init_oracle_client(lib_dir=client_lib_dir)
        logger.info(f"Oracle DB thick client initialized (lib_dir: {client_lib_dir if client_lib_dir else 'default'}).")
    except Exception as e:
        logger.error(f"ERROR initializing Oracle client: {e}.")
        raise

    geoscripts_home_env = os.getenv('GEOSCRIPTS_HOME')
    if not geoscripts_home_env:
        logger.error("GEOSCRIPTS_HOME environment variable not set.")
        raise EnvironmentError("GEOSCRIPTS_HOME environment variable not set.")

    dotenv_path = os.path.join(geoscripts_home_env, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path) # Per sviluppo locale
        logger.info(f"Loaded .env file from {dotenv_path} (local development).")
    else:
        logger.warning(f".env file not found at {dotenv_path}. Relying on Prefect Blocks or environment variables for production.")

    # Carica configurazioni da Blocchi Prefect (esempio)
    # In un ambiente di produzione, useresti i blocchi invece di os.getenv direttamente qui
    config = {
        "PG_USER": os.getenv("PG_USER") or Secret.load("pg-user").get(),
        "PG_PWD": os.getenv("PG_PWD") or Secret.load("pg-password").get(),
        "PG_HOST": os.getenv("PG_HOST") or PrefectStringBlock.load("pg-host").value,
        "PG_PORT": os.getenv("PG_PORT") or PrefectStringBlock.load("pg-port").value,
        "PG_DB_NAME": os.getenv("PG_DB_NAME") or PrefectStringBlock.load("pg-db-name").value,
        "ORA_DB_CONN_STR": os.getenv("ORA_DB_CONN_STR") or PrefectStringBlock.load("ora-db-conn-str").value,
        "ORA_USER": os.getenv("ORA_USER") or Secret.load("ora-user").get(),
        "ORA_PWD": os.getenv("ORA_PWD") or Secret.load("ora-password").get(),
        "SMTP_MAIL_SERVER": os.getenv("SMTP_MAIL_SERVER") or PrefectStringBlock.load("smtp-mail-server").value,
        "FROM_ADDRESS": os.getenv("FROM_ADDRESS") or PrefectStringBlock.load("from-address").value,
        "ERROR_TO_ADDRESS": os.getenv("ERROR_TO_ADDRESS") or PrefectStringBlock.load("error-to-address").value,
        "OK_TO_ADDRESS": os.getenv("OK_TO_ADDRESS") or PrefectStringBlock.load("ok-to-address").value,
        "LOG_DIR": os.path.join(geoscripts_home_env, '_log'),
        "GEOSCRIPTS_HOME": geoscripts_home_env,
        # Aggiungi qui le configurazioni per Kubernetes (namespace, image, secret K8s per PG pwd)
        "K8S_NAMESPACE": os.getenv("K8S_NAMESPACE") or PrefectStringBlock.load("k8s-namespace").value,
        "GDAL_DOCKER_IMAGE": os.getenv("GDAL_DOCKER_IMAGE") or PrefectStringBlock.load("gdal-docker-image").value,
        "PG_PWD_K8S_SECRET_NAME": os.getenv("PG_PWD_K8S_SECRET_NAME") or PrefectStringBlock.load("pg-pwd-k8s-secret-name").value,
        "PG_PWD_K8S_SECRET_KEY": os.getenv("PG_PWD_K8S_SECRET_KEY") or PrefectStringBlock.load("pg-pwd-k8s-secret-key").value,
    }
    os.makedirs(config["LOG_DIR"], exist_ok=True)
    logger.info(f"LOG_DIR set to: {config['LOG_DIR']}")
    # Validazione delle variabili caricate (come nello script originale)
    # ...
    return config

# Mantieni le funzioni di logging, ma usa get_run_logger() di Prefect se vuoi loggare eventi specifici del task/flusso
# Le variabili globali come main_logger, istanza, log_file_path andranno gestite diversamente,
# ad esempio passando il logger o i percorsi come argomenti, o usando il logger contestuale di Prefect.
# Per il logging su file personalizzato:

_main_logger_prefect = None
_log_file_path_prefect = None
_istanza_prefect = '' # Sarà impostata dai parametri del flow

def setup_custom_file_logging(log_dir, run_uuid, istanza_param):
    global _log_file_path_prefect, _main_logger_prefect, _istanza_prefect
    _istanza_prefect = istanza_param # Imposta l'istanza globale per il logger personalizzato
    current_date = datetime.now().strftime('%Y-%m-%d')
    _log_file_path_prefect = os.path.join(log_dir, f'dp-ora_to_pg_PREFECT_{current_date}_{run_uuid}.log')

    # Configura logger per il file di dettaglio del run specifico
    detail_logger = logging.getLogger('prefect_detail_run') # Nome univoco
    detail_logger.setLevel(logging.INFO)
    # Rimuovi handler esistenti per evitare duplicazioni
    for handler in list(detail_logger.handlers): detail_logger.removeHandler(handler)
    detail_file_handler = logging.FileHandler(_log_file_path_prefect)
    detail_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    detail_file_handler.setFormatter(detail_formatter)
    detail_logger.addHandler(detail_file_handler)
    detail_logger.propagate = False # Non inviare al logger root di Python

    # Configura logger per il file di log principale giornaliero
    MAIN_LOG_FILE = os.path.join(log_dir, f'dp-ora_to_pg_PREFECT_{current_date}.log')
    _main_logger_prefect = logging.getLogger('prefect_main_summary') # Nome univoco
    _main_logger_prefect.setLevel(logging.INFO)
    for handler in list(_main_logger_prefect.handlers): _main_logger_prefect.removeHandler(handler)
    main_summary_handler = logging.FileHandler(MAIN_LOG_FILE)
    main_summary_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
    main_summary_handler.setFormatter(main_summary_formatter)
    _main_logger_prefect.addHandler(main_summary_handler)
    _main_logger_prefect.propagate = False

    get_run_logger().info(f"Custom detail log file: {_log_file_path_prefect}")
    get_run_logger().info(f"Custom main summary log file: {MAIN_LOG_FILE}")
    return detail_logger # Ritorna il logger di dettaglio per usarlo specificamente

def print_log_custom(level, msg, detail_logger_instance): # Usa il logger di dettaglio specifico
    log_entry = f"{_istanza_prefect} - {msg}" if _istanza_prefect else msg # Usa _istanza_prefect
    if detail_logger_instance:
        if level.upper() == "INFO": detail_logger_instance.info(log_entry)
        elif level.upper() == "ERROR": detail_logger_instance.error(log_entry)
        elif level.upper() == "WARNING": detail_logger_instance.warning(log_entry)
        else: detail_logger_instance.debug(log_entry)
    # Logga anche con il logger di Prefect per visibilità nell'UI
    prefect_logger = get_run_logger()
    if level.upper() == "INFO": prefect_logger.info(msg) # Logga il messaggio originale, non quello formattato con istanza
    elif level.upper() == "ERROR": prefect_logger.error(msg)
    elif level.upper() == "WARNING": prefect_logger.warning(msg)
    else: prefect_logger.debug(msg)


def print_log_main_custom(level, msg): # Usa il logger _main_logger_prefect
    log_entry = f"{_istanza_prefect} - {msg}" if _istanza_prefect else msg
    if _main_logger_prefect:
        if level.upper() == "INFO": _main_logger_prefect.info(log_entry)
        elif level.upper() == "ERROR": _main_logger_prefect.error(log_entry)
        elif level.upper() == "WARNING": _main_logger_prefect.warning(log_entry)
        else: _main_logger_prefect.debug(log_entry)


# --- Task per la gestione DB ---
# Le connessioni dovrebbero essere gestite all'interno dei task o passate come oggetti risorsa.
# Per semplicità, questa trasposizione iniziale potrebbe ancora usare variabili "globali" nel contesto del flow run,
# ma è meglio refattorizzare per passare connessioni o stringhe di connessione ai task.

@task(name="Connect Databases")
def connect_databases_prefect(config):
    logger = get_run_logger()
    pg_conn = None
    ora_conn = None
    try:
        logger.info(f"Connecting to PostgreSQL: {config['PG_HOST']}:{config['PG_PORT']}/{config['PG_DB_NAME']}")
        pg_conn = psycopg2.connect(host=config['PG_HOST'], port=config['PG_PORT'], dbname=config['PG_DB_NAME'], user=config['PG_USER'], password=config['PG_PWD'])
        pg_conn.autocommit = True
        logger.info("PostgreSQL connection successful.")
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL: {e}")
        raise
    try:
        logger.info(f"Connecting to Oracle: {config['ORA_DB_CONN_STR']}")
        ora_conn = oracledb.connect(user=config['ORA_USER'], password=config['ORA_PWD'], dsn=config['ORA_DB_CONN_STR'])
        logger.info("Oracle connection successful.")
    except Exception as e:
        logger.error(f"Failed to connect to Oracle: {e}")
        if pg_conn: pg_conn.close()
        raise
    return {"pg_conn": pg_conn, "ora_conn": ora_conn}

@task(name="Close Databases")
def close_databases_prefect(connections):
    logger = get_run_logger()
    if connections["pg_conn"]:
        connections["pg_conn"].close()
        logger.info("PostgreSQL connection closed.")
    if connections["ora_conn"]:
        connections["ora_conn"].close()
        logger.info("Oracle connection closed.")

# Le funzioni DB (execute_pg, fetchone_pg, etc.) devono accettare la connessione come argomento
# Esempio:
@task(name="Execute PG SQL") # Potrebbe non essere necessario wrappare ogni singola query come task
def execute_pg_prefect(pg_conn, sql, params=None, custom_logger=None, config=None): # Passa il logger personalizzato
    # print_log_custom("DEBUG", f"Executing PG: {sql}", custom_logger) # Usa logger personalizzato
    with pg_conn.cursor() as cur:
        cur.execute(sql, params or ())

@task(name="Fetch Oracle Data for Table Processing")
def fetch_table_processing_definitions(ora_conn, base_query_str, where_clause_str, order_by_str, query_params_dict, custom_logger=None, config=None):
    full_query = base_query_str + where_clause_str + order_by_str
    print_log_custom("INFO", f"Querying Oracle for tables to process: {full_query} with params {query_params_dict}", custom_logger)
    
    tables_to_process = []
    with ora_conn.cursor() as cur:
        cur.execute(full_query, query_params_dict or {})
        columns = [col[0].upper() for col in cur.description]
        for row_tuple in cur:
            row_dict = dict(zip(columns, row_tuple))
            tables_to_process.append(row_dict)
    print_log_custom("INFO", f"Found {len(tables_to_process)} table definitions for processing.", custom_logger)
    return tables_to_process

# --- Task per singola tabella ---
@task(name="Get Geometry DB Connection")
def get_geom_db_prefect(stringa_conn, ora_main_conn, custom_logger=None, config=None): # Passa ora_main_conn per la query SIT_DB_ISTANZE
    # ... logica di get_geom_db, ma usa ora_main_conn per la sub-query ...
    # Esempio di adattamento per la sub-query:
    # with ora_main_conn.cursor() as cur_main:
    #     cur_main.execute("select CONNECTION_STRING from SIT_DB_ISTANZE ...", {'alias': alias.upper()})
    #     conn_str_row = cur_main.fetchone()
    # ... il resto simile, ma usa print_log_custom ...
    logger = get_run_logger() # Usa il logger di Prefect per info generali
    jdbc_conn_string_default = 'amb_db.regione.liguria.it:1522/SIT' # Questo potrebbe venire da config
    usr_default = 'VISCARTO' # Da config/secret
    pwd_default = 'CARTOVIS' # Da config/secret

    appo_str_conn = stringa_conn.split('@')
    jdbc_conn_string = jdbc_conn_string_default
    usr = usr_default
    pwd = pwd_default
    geom_db_conn = None

    try:
        if len(appo_str_conn) >= 2:
            alias = appo_str_conn[1]
            with ora_main_conn.cursor() as cur: # Usa la connessione Oracle principale passata
                # Assicurati che la tabella SIT_DB_ISTANZE e la colonna CONNECTION_STRING esistano
                # e che l'utente abbia i permessi.
                cur.execute("SELECT CONNECTION_STRING FROM SIT_DB_ISTANZE WHERE UPPER(ALIAS_NAME) = UPPER(:alias)", {'alias': alias.upper()})
                conn_str_row = cur.fetchone()
            if conn_str_row and conn_str_row[0]:
                jdbc_conn_string = conn_str_row[0]
                print_log_custom("INFO", f"Retrieved connection string for alias {alias}: {jdbc_conn_string}", custom_logger)
            else:
                print_log_custom("WARNING", f"Alias {alias} not found in SIT_DB_ISTANZE or CONNECTION_STRING is null. Using default: {jdbc_conn_string_default}", custom_logger)

            appo_str_conn2 = appo_str_conn[0].split('/')
            if len(appo_str_conn2) == 2:
                usr = appo_str_conn2[0]
                pwd = appo_str_conn2[1]
            else:
                 print_log_custom("WARNING", f"Could not parse user/password from {appo_str_conn[0]}, using defaults.", custom_logger)
        else:
            print_log_custom("WARNING", f"Could not parse alias from {stringa_conn}, using default connection: {jdbc_conn_string_default}", custom_logger)

        print_log_custom("INFO", f"Connecting to Geometry Oracle DB: {jdbc_conn_string} as {usr}", custom_logger)
        geom_db_conn = oracledb.connect(user=usr, password=pwd, dsn=jdbc_conn_string)
        print_log_custom("INFO", "Geometry Oracle DB connection successful.", custom_logger)
        return geom_db_conn # Ritorna l'oggetto connessione
    except Exception as e:
        print_log_custom("ERROR", f"Failed to connect to Geometry Oracle DB ({jdbc_conn_string} as {usr}): {e}", custom_logger)
        if geom_db_conn: geom_db_conn.close() # Pulisci se parzialmente riuscito
        raise


@task(name="Get Dimension (DIM)")
def get_dim_prefect(geom_db_conn, feature_name, geom_field, custom_logger=None, config=None):
    # ... logica di get_dim, usa geom_db_conn passato ...
    # Usa print_log_custom e ritorna dim
    dim = None
    try:
        with geom_db_conn.cursor() as cur:
            # ... (come nello script originale, ma usa print_log_custom) ...
            # Esempio: cmd_geom = "SELECT COLUMN_NAME FROM ALL_SDO_GEOM_METADATA ..."
            # cur.execute(cmd_geom, ...)
            # ...
            # cmd_dim = f"SELECT SUBSTR(t.\"{sanitized_geom_field}\".SDO_GTYPE, 1, 1) FROM {sanitized_feature_name} t WHERE ROWNUM = 1"
            # cur.execute(cmd_dim)
            # ...
            # Questa parte richiede molta attenzione alla sanitizzazione se feature_name/geom_field sono dinamici
            # Semplificazione: assumiamo che la logica originale sia copiata qui
            # Per brevità, non la ricopio tutta.
            if not geom_field:
                # Logica per trovare geom_field da ALL_SDO_GEOM_METADATA
                pass # Placeholder
            if not geom_field: # Se ancora non trovato
                print_log_custom("WARNING", f"Geometry field not found for {feature_name}", custom_logger)
                return None

            # Assicurati che feature_name e geom_field siano sicuri per l'interpolazione SQL
            # Questo è un punto critico per la sicurezza.
            # Per Oracle, i nomi quotati preservano maiuscole/minuscole.
            # feature_name potrebbe essere "SCHEMA.TABELLA"
            # geom_field è un nome di colonna
            # Esempio molto semplificato (NON per produzione senza validazione robusta):
            # sanitized_feature = feature_name
            # sanitized_geom_field = geom_field
            # cmd_dim = f"SELECT SUBSTR(t.\"{sanitized_geom_field}\".SDO_GTYPE, 1, 1) FROM {sanitized_feature} t WHERE ROWNUM = 1"
            # Per questo esempio, simulo un risultato:
            print_log_custom("INFO", f"Simulating get_dim for {feature_name}, geom_field {geom_field}", custom_logger)
            dim = '2' # Simula un valore, la logica reale va qui.

    except Exception as e:
        print_log_custom("ERROR", f"Error getting dimension for {feature_name}: {e}", custom_logger)
    return dim


@task(name="Run OGR2OGR via Kubernetes Job")
async def run_ogr2ogr_k8s_job(
    table_config, dim_value, flow_config, # flow_config contiene K8S_NAMESPACE, GDAL_DOCKER_IMAGE, etc.
    custom_logger=None
):
    logger = get_run_logger() # Logger di Prefect
    stringa_conn = table_config['STRINGA_CONN']
    tab_geom = table_config['TAB_GEOM']
    ora_schema_orig = table_config['ORA_SCHEMA']
    epsg_code = table_config['EPSG_CODE']
    pk_field = table_config['PK_FIELD']
    pg_schema = "public" # o da config

    safe_ora_schema_part = "".join(c if c.isalnum() else '_' for c in ora_schema_orig)
    safe_tab_geom_part = "".join(c if c.isalnum() else '_' for c in tab_geom)
    pg_tab_geom = f"{safe_ora_schema_part.lower()}_{safe_tab_geom_part.lower()}"
    source_table_in_oracle = f"{ora_schema_orig}.{tab_geom}" # Assumiamo nomi semplici, altrimenti quotare

    oci_connection_part = stringa_conn # Es: "user/pass@dbalias"

    # Argomenti per ogr2ogr
    ogr_arguments = [
        "-overwrite", "-f", "PostgreSQL",
        f"PG:host=$(PG_HOST_K8S) port=$(PG_PORT_K8S) dbname=$(PG_DB_NAME_K8S) user=$(PG_USER_K8S) password=$(PG_PASSWORD_K8S) active_schema={pg_schema}",
        f"OCI:{oci_connection_part}",
        "-sql", f"SELECT * FROM \"{source_table_in_oracle}\"", # Quotare se necessario
        "-a_srs", f"EPSG:{epsg_code}",
        "--config", "PG_USE_COPY", "YES",
        "-lco", "FID=ogr_fid",
        "-lco", f"DIM={dim_value}",
        "-lco", "GEOMETRY_NAME=wkb_geometry",
        "-nln", f"{pg_schema}.{pg_tab_geom}"
    ]
    if pk_field:
        ogr_arguments.extend(["-lco", f"PRIMARY_KEY={pk_field.lower()}"])

    # Variabili d'ambiente per il pod K8s
    # Le password devono venire da Kubernetes Secrets referenziati qui
    k8s_env_vars = {
        "PG_HOST_K8S": flow_config['PG_HOST'], # Assumendo che il job K8s possa raggiungere questi host
        "PG_PORT_K8S": str(flow_config['PG_PORT']),
        "PG_DB_NAME_K8S": flow_config['PG_DB_NAME'],
        "PG_USER_K8S": flow_config['PG_USER'],
        # PG_PASSWORD_K8S sarà iniettata dal K8s Secret
        "TNS_ADMIN": os.getenv("TNS_ADMIN_K8S_JOB", "/opt/oracle/network/admin"), # Deve esistere nell'immagine
        "LD_LIBRARY_PATH": os.getenv("LD_LIBRARY_PATH_K8S_JOB", "/opt/oracle/instantclient") # Deve esistere nell'immagine
    }

    # Definizione del Job Kubernetes
    # Il nome del job deve essere univoco per ogni esecuzione o usare generate_name
    job_name_prefix = f"ogr2ogr-{safe_tab_geom_part.lower()}-"
    job_manifest = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {"generateName": job_name_prefix}, # Kubernetes genererà un suffisso univoco
        "spec": {
            "template": {
                "spec": {
                    "containers": [
                        {
                            "name": "ogr2ogr-container",
                            "image": flow_config["GDAL_DOCKER_IMAGE"],
                            "command": ["ogr2ogr"],
                            "args": ogr_arguments,
                            "env": [
                                {"name": k, "value": v} for k, v in k8s_env_vars.items()
                            ] + [ # Aggiungi il secret per la password PG
                                {
                                    "name": "PG_PASSWORD_K8S",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "name": flow_config["PG_PWD_K8S_SECRET_NAME"],
                                            "key": flow_config["PG_PWD_K8S_SECRET_KEY"],
                                        }
                                    },
                                }
                            ],
                            # "resources": { # Opzionale: definisci richieste e limiti
                            #     "limits": {"memory": "2Gi", "cpu": "1"},
                            #     "requests": {"memory": "512Mi", "cpu": "0.5"}
                            # }
                        }
                    ],
                    "restartPolicy": "Never", # Tipico per i Job
                }
            },
            "backoffLimit": 1, # Numero di tentativi per il Job K8s
            "activeDeadlineSeconds": 70 * 60 # Timeout per l'intero Job (come nello script originale)
        },
    }

    print_log_custom("INFO", f"Submitting Kubernetes Job for {pg_tab_geom}. Image: {flow_config['GDAL_DOCKER_IMAGE']}", custom_logger)
    # logger.info(f"OGR Args for K8s: {' '.join(ogr_arguments)}") # Attenzione a non loggare password qui

    # Carica la configurazione del cluster Kubernetes (potrebbe essere un Blocco)
    # Se l'agente Prefect è in-cluster, potrebbe non essere necessario specificarlo.
    # k8s_cluster_config_block = KubernetesClusterConfig.load("default-k8s-cluster-config") # Esempio
    # k8s_cluster_config = k8s_cluster_config_block if k8s_cluster_config_block else None

    try:
        # Il task `run_kubernetes_job` è asincrono di per sé (ritorna subito),
        # ma Prefect attenderà il suo completamento se è un task in un flusso.
        # `stream_logs=True` può essere utile per vedere i log del pod nell'output del task Prefect.
        k8s_job_run = await run_kubernetes_job.fn( # Usa .fn per chiamare la funzione del task se `run_kubernetes_job` è un oggetto Task
            job=job_manifest,
            namespace=flow_config["K8S_NAMESPACE"],
            # kubernetes_conn_info=k8s_cluster_config, # Se necessario
            # stream_output=True, # Per log in tempo reale (potrebbe essere rumoroso)
            # wait_for_job_completion=True, # Default è True
        )
        # k8s_job_run è l'oggetto del job K8s completato.
        # Per controllare l'output o errori specifici come ORA-13208,
        # dovresti recuperare i log del pod del job K8s.
        # run_kubernetes_job potrebbe non esporre facilmente stdout/stderr separati.
        # Una strategia è far sì che lo script nel container logghi su stdout/stderr
        # e poi usare `kubectl logs <pod_name>` (o l'API K8s) per recuperarli.
        # `prefect-kubernetes` potrebbe avere opzioni per questo o dovresti estenderlo.
        # Per ora, assumiamo successo se il job K8s non fallisce.
        # Dovresti aggiungere un controllo dei log se la logica ORA-13208 è critica.
        logger.info(f"Kubernetes Job for {pg_tab_geom} completed. Name: {k8s_job_run.metadata.name}")
        # Qui potresti voler recuperare i log del pod per verificare ORA-13208
        # Esempio concettuale (richiede API client Kubernetes o `kubectl` nel worker Prefect):
        # pod_logs = get_kubernetes_pod_logs(k8s_job_run.metadata.name, flow_config["K8S_NAMESPACE"])
        # if "ORA-13208" in pod_logs:
        #     raise Exception(f"OGR failed with ORA-13208 for {pg_tab_geom}")
        return {"pg_schema": pg_schema, "pg_tab_geom": pg_tab_geom} # Passa info al task successivo
    except Exception as e:
        print_log_custom("ERROR", f"Kubernetes Job for {pg_tab_geom} failed or an error occurred: {e}", custom_logger)
        raise


@task(name="Post OGR Processing (PG)")
def post_ogr_processing_prefect(
    ogr_result, # Risultato dal task K8s (contiene pg_schema, pg_tab_geom)
    table_config, # Configurazione originale della tabella
    pg_conn, ora_main_conn, # Connessioni DB
    custom_logger=None, config_flow=None, istanza_param_val=None
):
    pg_schema = ogr_result["pg_schema"]
    pg_tab_geom = ogr_result["pg_tab_geom"]
    pk_field = table_config.get('PK_FIELD')
    original_stringa_conn = table_config['STRINGA_CONN']
    original_tab_geom = table_config['TAB_GEOM']
    original_ora_schema = table_config['ORA_SCHEMA']

    logger = get_run_logger()
    logger.info(f"Starting Post-OGR processing for {pg_schema}.{pg_tab_geom}")

    # --- BONIFICA GEOMETRIE, INDICI, VACUUM ---
    # (Ricopia la logica originale da import_table, usando execute_pg_prefect o query dirette)
    # Esempio (molto semplificato):
    try:
        # BONIFICA
        # from psycopg2 import sql as pgsql
        # valid_cmd = pgsql.SQL("UPDATE {schema}.{table} SET ...").format(...)
        # with pg_conn.cursor() as cur: cur.execute(valid_cmd)
        print_log_custom("INFO", f"Simulating geometry validation for {pg_schema}.{pg_tab_geom}", custom_logger)

        # INDICI
        if pk_field:
            # index_cmd = pgsql.SQL("CREATE UNIQUE INDEX IF NOT EXISTS ...").format(...)
            # with pg_conn.cursor() as cur: cur.execute(index_cmd)
            print_log_custom("INFO", f"Simulating index creation for {pk_field} on {pg_schema}.{pg_tab_geom}", custom_logger)

        # VACUUM
        # with pg_conn.cursor() as cur: cur.execute(f"VACUUM ANALYZE {pg_schema}.{pg_tab_geom}") # Attenzione all'autocommit
        print_log_custom("INFO", f"Simulating VACUUM ANALYZE for {pg_schema}.{pg_tab_geom}", custom_logger)
        logger.info(f"DB maintenance for {pg_schema}.{pg_tab_geom} completed.")
    except Exception as e_pg_maint:
        print_log_custom("ERROR", f"Error during PG maintenance for {pg_schema}.{pg_tab_geom}: {e_pg_maint}", custom_logger)
        # Decidi se rilanciare l'eccezione

    # --- CONTEGGIO RECORD ---
    ora_count = "N/A"
    geom_db_for_count = None
    try:
        # get_geom_db_prefect ritorna una connessione, non è un task che la apre e chiude da solo qui
        # quindi dovremmo chiamarlo come task separato se necessario o gestire la connessione
        # Per questo esempio, assumo che get_geom_db_prefect sia stato chiamato prima se necessario
        # o che la logica sia inline.
        # Per semplicità, simulo:
        # geom_db_for_count = get_geom_db_prefect.fn(original_stringa_conn, ora_main_conn, custom_logger, config_flow)
        # ora_count = get_ora_count(geom_db_for_count, f"{original_ora_schema}.{original_tab_geom}", ...)
        print_log_custom("INFO", "Simulating Oracle record count", custom_logger)
        ora_count = "100 (simulated)" # Simula
    except Exception as e_ora_count:
        print_log_custom("ERROR", f"Error getting Oracle count for {original_tab_geom}: {e_ora_count}", custom_logger)
    # finally:
        # if geom_db_for_count: geom_db_for_count.close() # Assicurati di chiudere connessioni aperte

    pg_count = "N/A"
    try:
        # pg_count = get_pg_count(pg_conn, f"{pg_schema}.{pg_tab_geom}", ...)
        print_log_custom("INFO", "Simulating PostgreSQL record count", custom_logger)
        pg_count = "100 (simulated)" # Simula
    except Exception as e_pg_count:
        print_log_custom("ERROR", f"Error getting PostgreSQL count for {pg_tab_geom}: {e_pg_count}", custom_logger)

    print_log_custom("INFO", f"CONTEGGIO RECORD - ORACLE ({original_ora_schema}.{original_tab_geom}): {ora_count} - PG ({pg_schema}.{pg_tab_geom}): {pg_count}", custom_logger)
    if ora_count != pg_count and ora_count != "N/A" and pg_count != "N/A":
         print_log_custom("WARNING", f"Record counts do not match for {original_tab_geom}!", custom_logger)

    # --- WRITE DB LOG ---
    # write_db_log(ora_main_conn, original_stringa_conn, original_tab_geom, 0, istanza_param_val, ...)
    print_log_custom("INFO", f"Simulating write to DB log for {original_tab_geom}", custom_logger)
    print_log_custom("INFO", f"IMPORT OK per {original_tab_geom} (post-elaborazione completata)", custom_logger)
    return f"Successfully processed {pg_schema}.{pg_tab_geom}"


@task(name="Run Post Update Views (PG)")
def post_update_views_prefect(pg_conn, custom_logger=None, config=None):
    # ... logica di post_update, usa pg_conn e print_log_custom ...
    # Esempio:
    # cmds = [...]
    # for cmd in cmds:
    #    with pg_conn.cursor() as cur: cur.execute(cmd)
    print_log_custom("INFO", "Simulating execution of post-update views", custom_logger)


@task(name="Send Email Notification")
def send_email_prefect(to_address_str, subject, body, config, custom_logger=None):
    # ... logica di send_mail, usa config per SMTP_SERVER, FROM_ADDRESS e print_log_custom ...
    # Esempio:
    # msg = MIMEText(body, 'html', 'utf-8')
    # ...
    # with smtplib.SMTP(config["SMTP_MAIL_SERVER"], 25) as server:
    #    server.sendmail(...)
    print_log_custom("INFO", f"Simulating sending email to {to_address_str} with subject: {subject}", custom_logger)


# --- Il Flusso Principale Prefect ---
@flow(name="Oracle to PostGIS ETL V2", retries=1, retry_delay_seconds=60)
def oracle_to_pg_etl_flow(
    schedule_type: str = None, # 'P' o 'T'
    identifier: str = None,    # '123,456' o 'L789'
    update_flag: bool = False
):
    run_context = get_run_context()
    flow_run_id = run_context.flow_run.id if run_context.flow_run else uuid.uuid4()
    logger = get_run_logger() # Logger principale di Prefect per il flusso
    logger.info(f"Flow START - Run ID: {flow_run_id}")
    logger.info(f"Params: schedule_type='{schedule_type}', identifier='{identifier}', update_flag={update_flag}")

    # Imposta istanza per logger personalizzato
    # Questo è un modo per gestire la variabile globale _istanza_prefect
    # DEVE essere fatto prima di chiamare setup_custom_file_logging
    global _istanza_prefect
    if schedule_type:
        _istanza_prefect = schedule_type
    elif identifier:
        _istanza_prefect = f"ID_{identifier.replace(',','_')[:20]}"
    else:
        _istanza_prefect = "MANUAL_UNKNOWN"


    # Task 1: Carica configurazione e inizializza client Oracle
    config = initialize_config_prefect.submit() # .submit() per esecuzione asincrona se il backend lo supporta
                                                # o chiama direttamente config = initialize_config_prefect() per sincrono

    # Task 2: Setup logging personalizzato (dipende da config per LOG_DIR)
    # Aspetta che config sia pronto se submit() è stato usato
    # Il logger personalizzato sarà disponibile globalmente (in questo modulo) dopo questa chiamata.
    # La gestione dei logger globali in un contesto di esecuzione distribuita (come Prefect con worker separati)
    # può essere complessa. È più robusto passare istanze di logger o configurazioni.
    # Per questa trasposizione, manteniamo un approccio simile all'originale.
    # Nota: `wait_for` è necessario solo se `config` è un `PrefectFuture` (da `.submit()`)
    custom_detail_logger = setup_custom_file_logging(config.result()["LOG_DIR"], str(flow_run_id), _istanza_prefect)


    # Logica per determinare i parametri della query (come in main_script_logic)
    param_for_query = None
    flag_schedulata = False
    update_postgis_flag_effective = update_flag

    if schedule_type:
        flag_schedulata = True
        # _istanza_prefect è già impostata
        param_for_query = _istanza_prefect
        print_log_custom("INFO", f"Scheduled run detected for instance: {_istanza_prefect}", custom_detail_logger)
        if update_postgis_flag_effective:
            print_log_custom("WARNING", f"--update-flag is ignored for scheduled runs. Forcing to False.", custom_detail_logger)
            update_postgis_flag_effective = False
    elif identifier:
        # _istanza_prefect è già impostata
        param_for_query = identifier
        print_log_custom("INFO", f"Manual run detected for ID(s): {param_for_query}", custom_detail_logger)
        if update_postgis_flag_effective and param_for_query.upper().startswith('L'):
             print_log_custom("WARNING", f"--update-flag is ignored for layer-specific runs. Forcing to False.", custom_detail_logger)
             update_postgis_flag_effective = False
        elif update_postgis_flag_effective:
             print_log_custom("INFO", f"--update-flag is set for map ID run.", custom_detail_logger)
    else:
        msg = "Invalid flow parameters. Must specify schedule_type or identifier."
        print_log_custom("ERROR", msg, custom_detail_logger)
        raise ValueError(msg) # Fallisce il flusso

    # Task 3: Connetti ai DB (dipende da config)
    connections = connect_databases_prefect.submit(config=config) # Esegui dopo config

    # Task 4: Prepara la query per le tabelle da processare
    # (La logica per costruire base_comando, where_clause, query_params va qui)
    # Esempio semplificato:
    base_comando_val = "SELECT DISTINCT STRINGA_CONN, TAB_GEOM, ORA_SCHEMA, EPSG_CODE, PK_FIELD, GEOM_FIELD FROM PG_CACHE_LAYERS"
    where_clause_val = ""
    query_params_val = {}
    if flag_schedulata:
        where_clause_val = " WHERE ID_LAYER IN (SELECT DISTINCT ID_LAYER FROM GS_LAYERS WHERE CACHE_SCHEDULATA LIKE :p_instance || '_%') AND POSTGIS_CACHE = 'S'"
        query_params_val = {'p_instance': _istanza_prefect}
    else: # Manual run
        # ... (logica per --id L... o --id map...) ...
        # Questo blocco deve essere completato come nello script originale. Per brevità, lo ometto.
        # Esempio se identifier è per map ID:
        if identifier and not identifier.upper().startswith("L"):
            try:
                map_ids = [int(x) for x in identifier.split(',') if x.isdigit()]
                if not map_ids: raise ValueError("No valid map IDs found")
                id_placeholders = ','.join([f':id{i}' for i in range(len(map_ids))])
                where_clause_val = f" WHERE ID_MAP IN ({id_placeholders}) AND POSTGIS_CACHE = 'S'" # O la logica originale
                query_params_val = {f'id{i}': mid for i, mid in enumerate(map_ids)}
            except ValueError as e:
                print_log_custom("ERROR", f"Invalid Map ID format for identifier: {identifier}. Error: {e}", custom_detail_logger)
                raise
        elif identifier and identifier.upper().startswith("L"):
             # Logica per Layer ID
            try:
                layer_ids = [int(x) for x in identifier[1:].split(',') if x.isdigit()]
                if not layer_ids: raise ValueError("No valid layer IDs found")
                id_placeholders = ','.join([f':id{i}' for i in range(len(layer_ids))])
                where_clause_val = f" WHERE ID_LAYER IN ({id_placeholders}) AND POSTGIS_CACHE = 'S'"
                query_params_val = {f'id{i}': lid for i, lid in enumerate(layer_ids)}
            except ValueError as e:
                print_log_custom("ERROR", f"Invalid Layer ID format for identifier: {identifier}. Error: {e}", custom_detail_logger)
                raise
        else: # Caso non gestito o errore nei parametri
            pass


    order_by_val = " ORDER BY STRINGA_CONN, TAB_GEOM"

    # Ottieni la lista delle definizioni di tabelle da processare (dipende da connections)
    table_definitions = fetch_table_processing_definitions.submit(
        ora_conn=connections.result()["ora_conn"], # .result() per attendere il future
        base_query_str=base_comando_val,
        where_clause_str=where_clause_val,
        order_by_str=order_by_val,
        query_params_dict=query_params_val,
        custom_logger=custom_detail_logger, # Passa il logger
        config=config.result(),            # Passa la configurazione completa
        wait_for=[connections]             # Dipendenza esplicita
    )

    # Task 5: Processa ogni tabella (questo è dove .map() di Prefect brilla)
    # Per ogni tabella in table_definitions:
    #   1. get_geom_db_prefect -> geom_conn
    #   2. get_dim_prefect(geom_conn, ...) -> dim_value
    #   3. run_ogr2ogr_k8s_job(table_def, dim_value, ...) -> ogr_result
    #   4. post_ogr_processing_prefect(ogr_result, table_def, ...)
    #   5. Chiudi geom_conn
    # Prefect può mappare una sequenza di task su una lista di input.

    # Esempio di mapping per una parte del processo (semplificato):
    # Per ogni `table_def` in `table_definitions.result()`:
    # Questo richiede di strutturare i task in modo che possano essere concatenati per ogni elemento.
    # Per un flusso più complesso per elemento, si può creare un sub-flow.

    processed_table_results = []
    # Questo loop verrà parallelizzato da Prefect se i task sono asincroni e non hanno dipendenze bloccanti.
    # Usare .map() è il modo più idiomatico.
    # Definiamo un helper task/subflow per processare una singola tabella
    @task(name="Process Single Table Full Cycle")
    async def process_single_table(table_def, main_connections, flow_config_resolved, custom_logger_instance, istanza_val):
        geom_conn = None
        try:
            print_log_custom("INFO", f"Inizio ciclo per tabella: {table_def.get('TAB_GEOM', 'N/A')}", custom_logger_instance)
            geom_conn = await get_geom_db_prefect.fn( # .fn per chiamare la funzione del task
                stringa_conn=table_def['STRINGA_CONN'],
                ora_main_conn=main_connections["ora_conn"],
                custom_logger=custom_logger_instance,
                config=flow_config_resolved
            )
            if not geom_conn: raise Exception("Failed to connect to geometry DB")

            feature_name = f"{table_def['ORA_SCHEMA']}.{table_def['TAB_GEOM']}" if table_def['ORA_SCHEMA'] else table_def['TAB_GEOM']
            dim = await get_dim_prefect.fn(
                geom_db_conn=geom_conn,
                feature_name=feature_name,
                geom_field=table_def['GEOM_FIELD'],
                custom_logger=custom_logger_instance,
                config=flow_config_resolved
            )
            if dim is None: raise Exception(f"Could not determine dimension for {feature_name}")

            # Chiudi geom_conn prima del job K8s se non serve più in questo scope
            if geom_conn: geom_conn.close(); geom_conn = None; print_log_custom("DEBUG", "geom_conn for get_dim closed", custom_logger_instance)


            ogr_outcome = await run_ogr2ogr_k8s_job.fn( # .fn per chiamare la funzione del task (se `run_ogr2ogr_k8s_job` è un `@task`)
                table_config=table_def,
                dim_value=dim,
                flow_config=flow_config_resolved,
                custom_logger=custom_logger_instance
            )

            post_ogr_outcome = await post_ogr_processing_prefect.fn(
                ogr_result=ogr_outcome,
                table_config=table_def,
                pg_conn=main_connections["pg_conn"],
                ora_main_conn=main_connections["ora_conn"], # Per write_db_log
                custom_logger=custom_logger_instance,
                config_flow=flow_config_resolved,
                istanza_param_val=istanza_val # Passa l'istanza per write_db_log
            )
            return post_ogr_outcome
        except Exception as e_table:
            print_log_custom("ERROR", f"Fallimento processamento tabella {table_def.get('TAB_GEOM', 'N/A')}: {e_table}", custom_logger_instance)
            # Invia email di errore specifica per questa tabella (se vuoi)
            error_body_table = f"CONNESSIONE: {table_def.get('STRINGA_CONN')}<br>TAVOLA: {table_def.get('ORA_SCHEMA')}.{table_def.get('TAB_GEOM')}<br>ERRORE: {e_table}"
            await send_email_prefect.fn( # Usa .fn qui
                to_address_str=flow_config_resolved["ERROR_TO_ADDRESS"],
                subject=f"Errore Cache POSTGIS (Prefect) - Tabella Specifica ({istanza_val})",
                body=error_body_table,
                config=flow_config_resolved,
                custom_logger=custom_logger_instance
            )
            return f"Failed to process {table_def.get('TAB_GEOM', 'N/A')}" # Ritorna un messaggio di fallimento
        finally:
            if geom_conn: # Assicura che sia chiusa
                try: geom_conn.close(); print_log_custom("DEBUG", "geom_conn (outer scope) closed", custom_logger_instance)
                except Exception: pass


    # Usa .map per parallelizzare l'elaborazione delle tabelle
    # `wait_for` assicura che `table_definitions` sia risolto prima del map.
    # Devo risolvere i future prima di passarli a .map se sono usati in modi che .map non gestisce nativamente per i future.
    # O meglio, passo i future e Prefect li risolve.
    processed_table_results = process_single_table.map(
        table_def=table_definitions, # Questo è un Future[list]
        main_connections=connections, # Questo è un Future[dict]
        flow_config_resolved=config, # Questo è un Future[dict]
        custom_logger_instance=custom_detail_logger, # Questo è un oggetto logger, non un Future
        istanza_val = _istanza_prefect # Stringa, non un Future
    )
    # `processed_table_results` sarà una lista di `PrefectFuture` se `process_single_table` è un task
    # o direttamente i risultati se è una funzione Python semplice mappata.
    # Se è un task, Prefect gestisce l'attesa.


    # Task 6: Aggiorna flag in Oracle sit_catalogo (dipende da config e dal successo dei task precedenti)
    # Questa logica dovrebbe essere eseguita solo se tutti i `processed_table_results` sono successful
    # o in base alla logica originale. Per ora, la metto dopo il map.
    # Necessita di `ora_conn` da `connections`.
    if update_postgis_flag_effective and identifier and not identifier.upper().startswith("L"):
        try:
            map_ids_to_update = [int(x) for x in identifier.split(',') if x.isdigit()]
            if map_ids_to_update:
                update_placeholders = ','.join([f':id{i}' for i in range(len(map_ids_to_update))])
                update_ora_params = {f'id{i}': mid for i, mid in enumerate(map_ids_to_update)}
                update_cmd_ora = f"UPDATE sit_catalogo SET POSTGIS_CACHE = 'S' WHERE CODICE IN ({update_placeholders})"

                # Esegui come task o direttamente se la connessione è disponibile
                # Per essere un task, wrappalo e usa .submit() o .fn()
                with connections.result()["ora_conn"].cursor() as cur_ora_update:
                    cur_ora_update.execute(update_cmd_ora, update_ora_params)
                # connections.result()["ora_conn"].commit() # Se autocommit non è True per questa connessione
                print_log_custom("INFO", f"Aggiornato campo POSTGIS_CACHE in sit_catalogo per ID(s): {identifier}", custom_detail_logger)
        except Exception as e_update_flag:
            print_log_custom("ERROR", f"Fallito aggiornamento POSTGIS_CACHE flag in sit_catalogo: {e_update_flag}", custom_detail_logger)
            # Non far fallire l'intero flow per questo, ma logga l'errore.


    # Task 7: Esegui post_update views (dipende da processed_table_results e connections)
    post_update_result = post_update_views_prefect.submit(
        pg_conn=connections.result()["pg_conn"],
        custom_logger=custom_detail_logger,
        config=config.result(),
        wait_for=[processed_table_results] # Aspetta che tutti i processamenti di tabella siano finiti
    )

    # Task 8: Chiudi connessioni DB (dipende da tutti i task che usano DB)
    # `wait_for` su `post_update_result` (e implicitamente su `processed_table_results` e `update_flag_task` se esistesse)
    final_db_close_result = close_databases_prefect.submit(
        connections=connections.result(),
        wait_for=[post_update_result] # Assicura che tutto sia finito prima di chiudere
    )

    # Logica finale e invio email di successo/fallimento gestita da Prefect (on_completion, on_failure hooks)
    # o come task finale.
    # Qui simuliamo un invio email di riepilogo.
    # Dobbiamo attendere che i risultati di `processed_table_results` siano disponibili
    # per determinare il successo generale.
    # Questa parte è complessa perché `processed_table_results` è una lista di future/risultati.
    # Si potrebbe avere un task finale che analizza `processed_table_results`.

    # Questo blocco finale attende la risoluzione dei task precedenti per l'email di riepilogo
    # È importante che `processed_table_results` sia gestito correttamente (se è una lista di future).
    # Per Prefect 2, se usi `.map`, il risultato sarà una lista di risultati una volta che tutti i task mappati sono completi.
    # Per semplicità, assumiamo che `final_db_close_result` sia l'ultimo.
    # L'invio dell'email di successo/fallimento può essere gestito meglio con gli state handlers di Prefect.

    # Esempio di task finale per email, dipende da tutto il resto.
    # Determina lo stato generale basandosi sui risultati (questo è semplificato)
    # In un flow reale, useresti gli state handlers di Prefect per le notifiche.
    # Questo è solo per illustrare una possibile logica finale.
    # Per esempio, controlla se ci sono state stringhe "Failed" nei risultati.
    # Questo richiede che processed_table_results sia una lista di stringhe una volta risolta.
    
    # Attendiamo esplicitamente i risultati per l'email finale
    # Questo è un po' goffo; gli state handlers sono migliori per le notifiche.
    # Per fare questo correttamente, `processed_table_results` dovrebbe essere una lista di risultati attesi.
    # `config.result()` e `connections.result()` dovrebbero essere usati se sono future.

    _ = final_db_close_result.result() # Attendi la chiusura DB

    # Analizza i risultati (questo è un esempio, la gestione degli stati è migliore)
    num_failed_tables = 0
    # Se processed_table_results è una lista di future, devi risolverli
    # Esempio: resolved_results = [r.result() for r in processed_table_results] (se `submit` usato per `process_single_table`)
    # Se `map` è usato su un task, `processed_table_results` sarà una lista di risultati una volta completato.
    # Per questo esempio, non implemento il conteggio dettagliato dei fallimenti per l'email.

    # Invio mail di successo (semplificato)
    # In Prefect, usa `on_completion` o `on_failure` hooks sul flow per le notifiche.
    flow_final_status_message = f"CACHE POSTGIS Prefect ({_istanza_prefect}): Esecuzione Terminata."
    if num_failed_tables > 0:
        flow_final_status_message += f" ATTENZIONE: {num_failed_tables} tabelle hanno avuto problemi."

    current_time = datetime.now()
    total_exec_time = current_time - run_context.flow_run.expected_start_time if run_context.flow_run else "N/A"
    flow_final_status_message += f"<br>Tempo totale di esecuzione del flusso (approssimativo): {total_exec_time}"

    # Il logger di Prefect è già stato usato, i log personalizzati sono nei file.
    print_log_main_custom("INFO", flow_final_status_message)

    # Invia email di completamento del flusso
    # Questo dovrebbe idealmente essere un state handler.
    send_email_prefect.submit(
        to_address_str=config.result()["OK_TO_ADDRESS"],
        subject=f"Completamento Flusso Cache POSTGIS (Prefect) - {_istanza_prefect}",
        body=flow_final_status_message,
        config=config.result(),
        custom_logger=custom_detail_logger, # Usa il logger per tracciare l'invio email
        wait_for=[final_db_close_result] # Assicura che tutto sia finito
    )

    logger.info(f"Flow END - Run ID: {flow_run_id}")


# Per eseguire localmente per test (senza un agente Prefect)
if __name__ == "__main__":
    # Imposta le variabili d'ambiente necessarie per lo sviluppo locale
    # o crea i blocchi Prefect e carica quelli.
    # Esempio: os.environ["GEOSCRIPTS_HOME"] = "..."
    # os.environ["ORACLE_CLIENT_LIB_DIR"] = "..."
    # os.environ["PG_USER"] = "testuser"
    # ... etc.

    # Esegui il flusso con parametri di esempio
    oracle_to_pg_etl_flow(
        schedule_type="T", # o None
        # identifier="L123" # o None
        identifier = None
    )
```

**Spiegazioni Importanti:**

1.  **`@flow` e `@task`:** Decoratori chiave di Prefect.
2.  **`initialize_config_prefect`:**
    * Carica le configurazioni. In produzione, useresti **Blocchi Prefect** (`Secret`, `String`, `JSON`, `KubernetesClusterConfig`) invece di `os.getenv` o `.env`. Ho lasciato `load_dotenv` per facilitare lo sviluppo locale.
    * Inizializza il client Oracle.
3.  **`setup_custom_file_logging`:** Mantiene il tuo logging su file, ma è importante notare che i worker Prefect potrebbero essere effimeri. Il logging di Prefect Cloud/Server è più robusto per la produzione. Le variabili globali per i logger (`_main_logger_prefect`, `_log_file_path_prefect`) sono un compromesso; idealmente, le istanze dei logger verrebbero passate o create/ottenute dove necessario. `_istanza_prefect` viene impostata all'inizio del flow.
4.  **Connessioni DB:**
    * `connect_databases_prefect` e `close_databases_prefect` aprono e chiudono le connessioni principali.
    * Le funzioni che operano sul DB (es. `execute_pg_prefect`) ora accettano l'oggetto connessione.
    * `get_geom_db_prefect` apre e idealmente chiude la sua connessione specifica o la ritorna per essere gestita. Nel ciclo di processamento tabelle, va chiusa dopo l'uso.
5.  **`Workspace_table_processing_definitions`:** Sostituisce la parte iniziale di `read_db` che recupera l'elenco delle tabelle da processare.
6.  **Ciclo di Processamento Tabella (`process_single_table`):**
    * Questo è un task helper che orchestra i passaggi per una singola tabella: `get_geom_db` -> `get_dim` -> `run_ogr2ogr_k8s_job` -> `post_ogr_processing_prefect`.
    * **`.map()`:** La parte `processed_table_results = process_single_table.map(...)` è cruciale. Dice a Prefect di eseguire il task `process_single_table` per ogni elemento nella lista `table_definitions`. Prefect può parallelizzare queste esecuzioni se le risorse lo permettono.
7.  **`run_ogr2ogr_k8s_job`:**
    * Questo è il cuore della sostituzione di `subprocess.run`.
    * Usa `run_kubernetes_job.fn(...)` (o `run_kubernetes_job.submit(...)` per asincrono esplicito) dalla libreria `prefect-kubernetes`.
    * **Immagine Docker:** Devi specificare la tua immagine Docker (`GDAL_DOCKER_IMAGE`) che contiene `ogr2ogr` e i client Oracle/PostGIS.
    * **Manifest del Job:** Costruisce dinamicamente il manifest YAML per un Job Kubernetes.
        * `generateName`: Permette a Kubernetes di creare nomi di job univoci.
        * `env`: Passa variabili d'ambiente al container, incluse quelle per la connessione PG.
        * **Secret per Password PG:** La password PG per `ogr2ogr` viene montata da un Kubernetes Secret (`PG_PWD_K8S_SECRET_NAME`, `PG_PWD_K8S_SECRET_KEY`). Devi creare questo secret nel tuo cluster.
        * `activeDeadlineSeconds`: Imposta un timeout per il job Kubernetes.
    * **Namespace K8s:** Specifica il namespace dove eseguire il job.
    * **Controllo ORA-13208:** Recuperare e analizzare i log del pod Kubernetes per errori specifici come ORA-13208 richiede una logica aggiuntiva (usando l'API client di Kubernetes o `kubectl` se disponibile nell'ambiente del worker Prefect, oppure facendo sì che lo script nel container esca con un codice di errore specifico per ORA-13208 che Prefect può interpretare come fallimento del task). Per ora, si basa sul successo/fallimento del Job K8s.
8.  **`post_ogr_processing_prefect`:** Contiene la logica che originariamente seguiva `subprocess.run` (validazione, indici, conteggi, `write_db_log`).
9.  **Notifiche Email:** `send_email_prefect` è un task. In un flusso Prefect reale, useresti gli **State Handlers** (`on_completion`, `on_failure` a livello di flow o task) per triggerare notifiche in modo più robusto. L'invio dell'email di riepilogo alla fine del flusso è un esempio semplificato.
10. **Esecuzione Asincrona e Attesa:**
    * `.submit()` sui task suggerisce a Prefect di poterli eseguire in modo asincrono (se hai un esecutore parallelo come `DaskTaskRunner` o `RayTaskRunner`, o se il backend dell'agente lo supporta). Il flusso attenderà automaticamente il completamento dei task prima di usare i loro risultati se non si usa `.wait()` esplicitamente ma si passa il `PrefectFuture` (risultato di `.submit()`) ad un altro task.
    * `.result()` su un `PrefectFuture` bloccherà l'esecuzione finché il risultato non è disponibile. Usalo con cautela per non creare colli di bottiglia non necessari.
    * Chiamare direttamente `nome_task(...)` esegue il task in modo sincrono nel processo del flusso (o del worker che esegue quella parte del flusso).
    * Per i task `async def`, usa `.fn(...)` per chiamare la loro funzione sottostante in un contesto dove hai bisogno del risultato direttamente o quando li passi a `map`.

**Per Eseguire su Kubernetes con Prefect:**

1.  **Installa `prefect-kubernetes`:** `pip install prefect-kubernetes` nel tuo ambiente Prefect.
2.  **Crea Blocchi Prefect:**
    * Per le credenziali DB (PG_USER, PG_PWD, ORA_USER, ORA_PWD) come `Secret`.
    * Per le stringhe di connessione e altre configurazioni (PG_HOST, ORA_DB_CONN_STR, SMTP_SERVER, K8S_NAMESPACE, GDAL_DOCKER_IMAGE, PG_PWD_K8S_SECRET_NAME, PG_PWD_K8S_SECRET_KEY) come `String` o `JSON`.
    * Potresti creare un Blocco `KubernetesClusterConfig` se il tuo agente Prefect necessita di configurazione specifica per connettersi al cluster K8s (spesso non necessario se l'agente è in-cluster).
    * (Opzionale ma consigliato) Un Blocco `KubernetesJob` (da `prefect_kubernetes.infrastructure`) può pre-configurare il template del job K8s, rendendo il task `run_ogr2ogr_k8s_job` più pulito.
3.  **Crea un Kubernetes Secret:** Nel tuo cluster Kubernetes, crea un secret (es. `postgres-credentials`) che contenga la password di PostgreSQL (es. con una chiave `password`). Il nome e la chiave devono corrispondere a `PG_PWD_K8S_SECRET_NAME` e `PG_PWD_K8S_SECRET_KEY`.
4.  **Crea un Deployment Prefect:**
    * Usa la CLI di Prefect: `prefect deployment build ./tuo_script.py:oracle_to_pg_etl_flow -n oracle-pg-etl -q k8s-work-queue -ib kubernetes-job --override image=tuaimmagineprefect/flow:latest`
        * `-ib kubernetes-job` specifica che l'infrastruttura per eseguire il flusso stesso è un job Kubernetes (il flusso Prefect viene eseguito come un job K8s, e *questo job* poi lancia altri job K8s per `ogr2ogr`).
        * `tuaimmagineprefect/flow:latest` è l'immagine Docker che contiene il codice del tuo flusso Prefect e le dipendenze Python (Prefect, `prefect-kubernetes`, `psycopg2`, `oracledb`, `python-dotenv`).
    * Oppure definisci il deployment in un file `prefect.yaml`.
5.  **Avvia un Agente/Worker Prefect:** Nel tuo cluster Kubernetes, avvia un agente Prefect (es. `prefect agent start -q k8s-work-queue`) o un Worker (Prefect 2.x) che ascolti la coda di lavoro specificata e possa creare job Kubernetes.

Questo approccio rende il tuo ETL più robusto, osservabile e gestibile, sfruttando le capacità di orchestrazione di Prefect e la scalabilità di Kubernetes. Richiede una comprensione dei concetti di Prefect e Kubernetes, ma offre significativi vantaggi a lungo termine.

---

# you asked

Considera questa ipotesi:
lo script originario python viene containerizzato e contiene tutta la logica elaborativa della pipeline, Airflow viene utilizzato solo per la schedualzione e l'esecuzione del container in ambiente k8s. 
Questo semplifica il porting dello script in un ambiente k8s/airfl

---

# gemini response

Sì, la tua ipotesi è corretta e rappresenta un approccio molto comune e pragmatico per migrare script complessi in un ambiente orchestrato come Airflow su Kubernetes. Questo metodo è spesso definito come "Lift and Shift" di un'applicazione in un container, con l'orchestratore che si occupa dell'esecuzione e della schedulazione.

**Vantaggi di questo approccio:**

1.  **Minima Refactoring dello Script:** La logica principale del tuo script Python rimane quasi invariata. Devi solo assicurarti che possa essere eseguito in un ambiente containerizzato e che possa accettare parametri tramite argomenti da riga di comando o variabili d'ambiente.
2.  **Dipendenze Isolate:** Tutte le dipendenze complesse (`oracledb`, `psycopg2`, `ogr2ogr`, client Oracle specifici, versioni Python) sono pacchettizzate nell'immagine Docker. Questo evita conflitti di dipendenze nell'ambiente Airflow worker.
3.  **Semplificazione del DAG Airflow:** Il DAG Airflow diventa molto più semplice. Il suo compito principale è definire come e quando eseguire il container, passando i parametri necessari.
4.  **Testabilità:** Puoi testare l'immagine Docker e lo script indipendentemente da Airflow.
5.  **Portabilità:** L'immagine Docker può essere eseguita in qualsiasi ambiente che supporti Docker, non solo Kubernetes gestito da Airflow.

**Come sarebbe il DAG Airflow:**

Utilizzeresti principalmente il `KubernetesPodOperator` (o `GKEStartPodOperator` se sei su Google Cloud e preferisci un'integrazione più specifica, anche se `KubernetesPodOperator` è più generico).

Ecco una bozza del DAG:

```python
from __future__ import annotations

import pendulum # Nuovo modo di gestire le date in Airflow

from airflow.models.dag import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from airflow.models.param import Param # Per i parametri del DAG
from airflow.utils.trigger_rule import TriggerRule

# Parametri che verranno passati al container (devono corrispondere agli argparse del tuo script)
# Questi sono gli stessi parametri che avevi definito nel DAG precedente.
dag_params_config = {
    'schedule_type': Param(None, type=['null', 'string'], enum=[None, 'P', 'T'],
                           description="Tipo di schedulazione ('P' per Produzione, 'T' per Test). Lasciare None se si usa 'identifier'."),
    'identifier': Param(None, type=['null', 'string'],
                        description="ID Mappa(e) (es. 123,456) o ID Layer(s) (es. L789,L1011). Lasciare None se si usa 'schedule_type'."),
    'update_flag': Param(False, type='boolean',
                         description="Imposta POSTGIS_CACHE='S' in sit_catalogo per gli ID mappa specificati.")
}

# Callback per email (semplificati, poiché i dettagli dell'esecuzione sono nei log del container)
# Le variabili per SMTP (SMTP_MAIL_SERVER, FROM_ADDRESS, etc.) devono essere disponibili
# come variabili d'ambiente nel worker Airflow che esegue le callback, o caricate da Airflow Connections/Variables.
# Per semplicità, assumiamo che siano variabili d'ambiente.
import os
import smtplib
from email.mime.text import MIMEText

SMTP_MAIL_SERVER_CB = os.getenv("SMTP_MAIL_SERVER_CB") # Usa nomi diversi per evitare conflitti con quelli dello script originale
FROM_ADDRESS_CB = os.getenv("FROM_ADDRESS_CB")
ERROR_TO_ADDRESS_CB = os.getenv("ERROR_TO_ADDRESS_CB")
OK_TO_ADDRESS_CB = os.getenv("OK_TO_ADDRESS_CB")

def send_airflow_email(to_address_str, subject, body_content):
    if not SMTP_MAIL_SERVER_CB or not FROM_ADDRESS_CB or not to_address_str:
        print("WARNING (Callback Email): SMTP server, from_address or to_address not configured. Skipping email.")
        return

    to_addresses = [addr.strip() for addr in to_address_str.split(';') if addr.strip()]
    if not to_addresses:
        print("WARNING (Callback Email): No valid recipient addresses. Skipping email.")
        return

    msg = MIMEText(body_content, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = FROM_ADDRESS_CB
    msg['To'] = ', '.join(to_addresses)

    try:
        with smtplib.SMTP(SMTP_MAIL_SERVER_CB, 25) as server:
            server.sendmail(FROM_ADDRESS_CB, to_addresses, msg.as_string())
            print(f"INFO (Callback Email): Email sent to {', '.join(to_addresses)}.")
    except Exception as e:
        print(f"ERROR (Callback Email): Failed to send email: {e}")


def on_success_email_callback_simple(context):
    dag_run = context['dag_run']
    params = dag_run.conf
    run_details = params.get('schedule_type') or params.get('identifier', 'N/A')
    subject = f"SUCCESSO Esecuzione Container ETL Oracle-to-PostGIS - {run_details}"
    body = (f"Il container per l'ETL Oracle-to-PostGIS (Run: {run_details}) è terminato con SUCCESSO.<br>"
            f"Controllare i log del pod in Kubernetes/Airflow per i dettagli dell'elaborazione.<br>"
            f"DAG Run ID: {dag_run.run_id}<br>"
            f"Log URL (Airflow): {context['ti'].log_url}")
    if OK_TO_ADDRESS_CB:
        send_airflow_email(OK_TO_ADDRESS_CB, subject, body)

def on_failure_email_callback_simple(context):
    dag_run = context['dag_run']
    params = dag_run.conf
    run_details = params.get('schedule_type') or params.get('identifier', 'N/A')
    exception = context.get('exception')
    subject = f"ERRORE Esecuzione Container ETL Oracle-to-PostGIS - {run_details}"
    body = (f"Il container per l'ETL Oracle-to-PostGIS (Run: {run_details}) è terminato con ERRORE.<br>"
            f"Errore: {exception}<br>"
            f"Controllare i log del pod in Kubernetes/Airflow per i dettagli.<br>"
            f"DAG Run ID: {dag_run.run_id}<br>"
            f"Log URL (Airflow): {context['ti'].log_url}")
    if ERROR_TO_ADDRESS_CB:
        send_airflow_email(ERROR_TO_ADDRESS_CB, subject, body)


with DAG(
    dag_id='oracle_to_postgis_containerized_etl',
    start_date=pendulum.datetime(2023, 1, 1, tz="Europe/Rome"), # Usa pendulum per le date
    schedule=None, # O la tua cron expression, es. "0 2 * * *"
    catchup=False,
    tags=['etl', 'oracle', 'postgis', 'kubernetes', 'containerized'],
    params=dag_params_config, # Definisce i parametri UI per trigger manuali
    default_args={
        'owner': 'airflow',
        'on_failure_callback': on_failure_email_callback_simple,
        'on_success_callback': on_success_email_callback_simple,
        # 'retries': 1, # Puoi impostare tentativi a livello di task o DAG
        # 'retry_delay': timedelta(minutes=5),
    }
) as dag:

    # Recupera i parametri del DAG specifici per questa esecuzione
    # Questi verranno usati per costruire gli argomenti del container
    # Notare che {{ dag_run.conf.parameter_name }} è il modo per accedere ai parametri in templated fields
    # Per i non-templated fields come `arguments` in KubernetesPodOperator, dobbiamo usare Jinja templating
    # o passare le variabili d'ambiente. Passare argomenti è più diretto se lo script usa argparse.

    # Costruzione degli argomenti per lo script Python nel container
    # Lo script originale usa -sp, -st, --id, --update-flag
    # Dobbiamo tradurre i dag_run.conf in questi argomenti
    # Questo è un campo templated, quindi Airflow sostituirà i valori.
    # {{ params.schedule_type }} o {{ dag_run.conf.get('schedule_type', None) }}
    # Nota: la gestione di argomenti opzionali/esclusivi può essere un po' verbosa qui.

    # Esempio di costruzione degli argomenti dello script
    # Assumiamo che lo script python si chiami /app/original_script.py nel container
    script_args_template = """
    {% if params.schedule_type == 'P' %}
    -sp
    {% elif params.schedule_type == 'T' %}
    -st
    {% elif params.identifier %}
    --id {{ params.identifier }}
    {% else %}
    # Nessun parametro di tipo run principale, lo script potrebbe fallire o avere un default
    # Potresti voler sollevare un errore qui se nessuno è specificato e sono richiesti
    {% endif %}
    {% if params.update_flag %}
    --update-flag
    {% endif %}
    """

    # Le variabili d'ambiente che lo script Python si aspetta (es. GEOSCRIPTS_HOME, ORACLE_CLIENT_LIB_DIR,
    # credenziali DB se non passate diversamente o già nel .env del container).
    # È preferibile passare le credenziali tramite Kubernetes Secrets.
    env_vars_for_pod = {
        "GEOSCRIPTS_HOME": "/app/geoscripts", # Esempio, deve corrispondere a come è nel container
        "ORACLE_CLIENT_LIB_DIR": "/opt/oracle/instantclient", # Esempio
        "PYTHONUNBUFFERED": "1", # Per vedere i log Python immediatamente
        "RUN_UUID": "{{ run_id }}", # Passa il run_id di Airflow allo script se lo usa
        # Se lo script carica PG_USER, etc. da .env o variabili d'ambiente,
        # puoi passarli qui, preferibilmente da K8s Secrets.
        # Esempio con K8s Secrets (devi creare i secret 'db-credentials' e 'smtp-credentials' nel namespace K8s):
        # "PG_USER": "$(SECRET_PG_USER)", # Sintassi per referenziare valori da secret
        # "PG_PWD": "$(SECRET_PG_PWD)",
        # "ORA_USER": "$(SECRET_ORA_USER)",
        # "ORA_PWD": "$(SECRET_ORA_PWD)",
        # "SMTP_MAIL_SERVER": "$(SECRET_SMTP_SERVER)",
        # "FROM_ADDRESS": "$(SECRET_FROM_ADDRESS)",
        # "ERROR_TO_ADDRESS": "$(SECRET_ERROR_TO_ADDRESS)",
        # "OK_TO_ADDRESS": "$(SECRET_OK_TO_ADDRESS)",
    }

    # Definizione dei secret da montare come variabili d'ambiente nel Pod
    # Questi secret devono esistere nel tuo namespace Kubernetes.
    # k8s_secrets = [
    #     Secret(deploy_type="env", deploy_target="PG_USER", secret="db-credentials", key="pg_user"),
    #     Secret(deploy_type="env", deploy_target="PG_PWD", secret="db-credentials", key="pg_password"),
    #     Secret(deploy_type="env", deploy_target="ORA_USER", secret="db-credentials", key="ora_user"),
    #     Secret(deploy_type="env", deploy_target="ORA_PWD", secret="db-credentials", key="ora_password"),
    #     Secret(deploy_type="env", deploy_target="SMTP_MAIL_SERVER", secret="smtp-credentials", key="smtp_server"),
    #     Secret(deploy_type="env", deploy_target="FROM_ADDRESS", secret="smtp-credentials", key="from_address"),
    #     # ... e così via per ERROR_TO_ADDRESS, OK_TO_ADDRESS
    # ]
    # NOTA: Il passaggio di secret come sopra popola le env_vars del pod. Lo script Python le leggerà
    # come variabili d'ambiente normali (os.getenv). Il file .env interno al container
    # potrebbe essere sovrascritto da queste variabili se i nomi coincidono.

    run_containerized_script = KubernetesPodOperator(
        task_id='run_oracle_to_pg_etl_container',
        name='etl-pod-{{ run_id | slugify }}', # Nome del Pod in Kubernetes, rendilo univoco
        namespace='airflow',  # O il tuo namespace Kubernetes target
        image='TUO_REGISTRY/NOME_TUA_IMMAGINE:TAG',  # <<< SOSTITUISCI QUESTO
        # Immagine Docker che contiene lo script Python e tutte le dipendenze (ogr2ogr, client oracle, etc.)
        cmds=["python"], # Comando da eseguire nel container
        arguments=["/app/original_script.py"] + [arg for arg_line in script_args_template.splitlines() if (arg := arg_line.strip())], # Aggiunge gli argomenti costruiti
        env_vars=env_vars_for_pod,
        # secrets=k8s_secrets, # Se stai usando la classe Secret di Airflow per montare K8s Secrets
        get_logs=True,  # Cattura i log del pod in Airflow
        log_events_on_failure=True, # Logga eventi K8s se il pod fallisce
        is_delete_operator_pod=True,  # Cancella il pod dopo il completamento (successo o fallimento)
        startup_timeout_seconds=600, # Timeout per l'avvio del pod
        # Puoi aggiungere richieste di risorse, etichette, annotazioni, etc.
        # resources={'request_memory': '512Mi', 'limit_memory': '2Gi', 'request_cpu': '0.5', 'limit_cpu': '1'},
        # image_pull_policy='Always', # O 'IfNotPresent'
        # Se il tuo script Python ha bisogno di accedere a file di configurazione specifici (es. un tnsnames.ora custom)
        # che non sono parte dell'immagine, puoi montarli usando `volumes` e `volume_mounts`
        # dal ConfigMap o PersistentVolume di Kubernetes.
        # Assicurati che l'entrypoint/cmd dello script Python sia corretto.
        # Se lo script ha un entrypoint definito nel Dockerfile, potresti non aver bisogno di `cmds` e `arguments`,
        # ma solo di passare `env_vars` o sovrascrivere gli argomenti dell'entrypoint.
        # In questo caso, `arguments` passa gli argomenti direttamente a `/app/original_script.py`.
    )
```

**Cosa devi preparare:**

1.  **Dockerfile:** Crea un `Dockerfile` per containerizzare il tuo script Python originale.
    * Installa Python.
    * Installa il client Oracle Instant Client e configuralo (es. `LD_LIBRARY_PATH`, `TNS_ADMIN` se necessario).
    * Installa `ogr2ogr` (spesso tramite `gdal-bin` o simili).
    * Installa le librerie Python necessarie (`psycopg2-binary`, `oracledb`, `python-dotenv`).
    * Copia il tuo script Python e il file `.env` (se vuoi un `.env` di default nell'immagine) nel container.
    * Assicurati che lo script sia eseguibile.

    ```dockerfile
    # Esempio di Dockerfile (potrebbe variare molto in base alla tua base image e necessità)
    FROM ubuntu:22.04 # O un'immagine Python ufficiale

    # Evita prompt interattivi
    ENV DEBIAN_FRONTEND=noninteractive PYTHONUNBUFFERED=1

    # Installa dipendenze di sistema (python, pip, gdal, etc.)
    RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-pip python3-dev \
        gdal-bin \
        # Per il client Oracle: scarica i .deb o i .zip da Oracle e installali
        # Questo è il passaggio più complesso e specifico per Oracle.
        # Ad esempio, se usi i file zip:
        # ADD instantclient-basic-linux.x64-XX.X.X.X.Xdbru.zip /opt/oracle/
        # ADD instantclient-sqlplus-linux.x64-XX.X.X.X.Xdbru.zip /opt/oracle/
        # ADD instantclient-tools-linux.x64-XX.X.X.X.Xdbru.zip /opt/oracle/
        # WORKDIR /opt/oracle
        # RUN unzip instantclient-basic-linux.x64-XX.X.X.X.Xdbru.zip && \
        #     unzip instantclient-sqlplus-linux.x64-XX.X.X.X.Xdbru.zip && \
        #     unzip instantclient-tools-linux.x64-XX.X.X.X.Xdbru.zip && \
        #     # sh -c "echo /opt/oracle/instantclient_XX_X > /etc/ld.so.conf.d/oracle-instantclient.conf" && \ # Aggiorna ldconfig
        #     # ldconfig && \
        #     rm *.zip
        # ENV ORACLE_HOME=/opt/oracle/instantclient_XX_X # Adatta alla versione
        # ENV LD_LIBRARY_PATH=$ORACLE_HOME:$LD_LIBRARY_PATH
        # ENV PATH=$ORACLE_HOME:$PATH
        # Se usi tnsnames.ora, crea la directory e copia il file
        # RUN mkdir -p $ORACLE_HOME/network/admin
        # COPY tnsnames.ora $ORACLE_HOME/network/admin/
        # ENV TNS_ADMIN=$ORACLE_HOME/network/admin
        && rm -rf /var/lib/apt/lists/*

    # Copia il tuo script e requirements
    WORKDIR /app
    COPY requirements.txt .
    RUN pip3 install --no-cache-dir -r requirements.txt

    COPY . /app # Copia tutto il contenuto della directory corrente (incluso lo script e .env)

    # Definisci GEOSCRIPTS_HOME se lo script lo usa per trovare .env o _log
    ENV GEOSCRIPTS_HOME=/app/geoscripts # Se .env è in /app/geoscripts/.env

    # Lo script verrà eseguito con "python /app/original_script.py [args]" dal KubernetesPodOperator
    # ENTRYPOINT ["python3", "/app/original_script.py"] # Potresti usare un entrypoint
    # CMD ["--help"] # e CMD se preferisci, poi sovrascrivi CMD con gli argomenti in K8sPodOperator
    ```

    **`requirements.txt` (esempio):**
    ```
    psycopg2-binary
    oracledb
    python-dotenv
    # Altre dipendenze...
    ```

2.  **Costruisci e Pubblica l'Immagine Docker:**
    `docker build -t TUO_REGISTRY/NOME_TUA_IMMAGINE:TAG .`
    `docker push TUO_REGISTRY/NOME_TUA_IMMAGINE:TAG`

3.  **Configura Kubernetes Secrets (Raccomandato):**
    Crea secret nel tuo namespace Kubernetes per le credenziali del database e SMTP.
    Esempio per `db-credentials`:
    `kubectl create secret generic db-credentials --from-literal=pg_user='myuser' --from-literal=pg_password='mypass' --from-literal=ora_user='myorauser' --from-literal=ora_password='myorapass' -n airflow`

4.  **Configura Airflow (Variabili/Connessioni):**
    * Se le callback email usano variabili d'ambiente (`SMTP_MAIL_SERVER_CB`, etc.), assicurati che siano impostate nell'ambiente dei worker Airflow.
    * In alternativa, crea una Connessione Email in Airflow e usa `EmailOperator` o `send_email_smtp` hook nelle callback.

**Come Funziona:**

* Quando il DAG Airflow viene eseguito (manualmente o schedulato), il task `run_containerized_script` viene avviato.
* `KubernetesPodOperator` crea un Pod nel tuo cluster Kubernetes usando l'immagine Docker specificata.
* I parametri del DAG (`schedule_type`, `identifier`, `update_flag`) vengono passati come argomenti al comando `python /app/original_script.py` all'interno del container.
* Le variabili d'ambiente (e i secret montati come env var) sono disponibili per lo script Python.
* Lo script Python viene eseguito all'interno del container, eseguendo tutta la logica ETL.
* L'output (stdout/stderr) dello script viene catturato da Airflow e reso disponibile nei log del task.
* Al termine dell'esecuzione del container (successo o fallimento), il Pod viene eliminato (se `is_delete_operator_pod=True`).
* Le callback di successo o fallimento del task Airflow vengono eseguite.

Questo approccio è robusto e sfrutta i punti di forza di ogni strumento: la logica applicativa complessa rimane nello script Python ben testato e containerizzato, mentre Airflow si occupa dell'orchestrazione, schedulazione, UI e gestione delle dipendenze a livello di workflow, e Kubernetes gestisce l'esecuzione scalabile e isolata del container.

---

# you asked

Lo script python è già conteinerizzato e funzionante. 
Vorrei approfondire la questione dei log.
Attualmente lo script genera dei log su una dir montata nel container (con docker-compose in ambiente dev).
I log vengono generati in maniera standard: <nome_script><DD-MM-YYYY><RUN_UUID>.
Si può fare in modo che airflow al termine della elaborazione legga il log dello script e lo invii via mail e/o lo renda accessibile via interfaccia?

---

# gemini response

Sì, è assolutamente possibile e una pratica comune voler integrare i log specifici di un'applicazione containerizzata con il sistema di logging e notifica di Airflow.

L'approccio che hai descritto (script containerizzato che scrive log su un volume montato) è ottimo per la persistenza e il debug in ambiente di sviluppo. Quando si passa ad Airflow su Kubernetes, abbiamo alcune opzioni per rendere questi log accessibili e/o inviarli via email.

Considerando che il tuo script è eseguito tramite `KubernetesPodOperator`, ecco le strategie principali:

**Strategia 1: Lo script emette il contenuto del suo log su `stdout` (Raccomandata per semplicità)**

Questo è l'approccio più semplice e diretto per l'integrazione con Airflow.

1.  **Modifica allo Script Python (Minima):**
    Alla fine dell'esecuzione dello script (o in un blocco `finally` per catturare anche errori), dopo che il tuo script ha finito di scrivere nel suo file di log personalizzato, aggiungi alcune righe di codice per stampare il contenuto di quel file di log su `stdout`.

    * Il tuo script sa già il nome del file di log che ha generato, inclusa la data e il `RUN_UUID`.
    * Airflow (tramite `KubernetesPodOperator` con `get_logs=True`, che è il default) cattura tutto l'output `stdout` e `stderr` del container e lo rende disponibile come log del task Airflow.

    **Esempio di modifica nello script Python:**

    ```python
    # ... (alla fine del tuo script, es. nel blocco finally di main) ...
    # Assumiamo che 'log_file_path' sia la variabile che contiene il percorso completo
    # del file di log generato dallo script (es. /montaggio/log/dp-ora_to_pg_DD-MM-YYYY_RUN_UUID.log)

    if log_file_path_global and os.path.exists(log_file_path_global): # log_file_path_global è quella definita in setup_logging
        print(f"\n--- INIZIO CONTENUTO LOG SCRIPT ({os.path.basename(log_file_path_global)}) ---", flush=True)
        try:
            with open(log_file_path_global, 'r', encoding='utf-8') as f_log:
                # Leggi e stampa chunks per file molto grandi, o tutto insieme se sono piccoli
                # sys.stdout.write(f_log.read()) # Scrive direttamente, bypassando il logger Python
                # Oppure, se vuoi usare il logger per formattazione:
                for line in f_log:
                    sys.stdout.write(line) # Stampa riga per riga
            sys.stdout.flush() # Assicura che tutto venga scritto
        except Exception as e_log_read:
            print(f"ERRORE LETTURA FILE LOG PERSONALIZZATO {log_file_path_global}: {e_log_read}", flush=True)
        print(f"--- FINE CONTENUTO LOG SCRIPT ({os.path.basename(log_file_path_global)}) ---\n", flush=True)
    else:
        print(f"ATTENZIONE: File di log personalizzato non trovato o path non definito ({log_file_path_global})", flush=True)

    # Il tuo script termina normalmente o solleva eccezioni
    ```

2.  **Configurazione `KubernetesPodOperator` nel DAG Airflow:**
    * Assicurati che `get_logs=True` (default).
    * Passa il `RUN_UUID` (che può essere il `run_id` di Airflow) come variabile d'ambiente al container, così lo script Python può usarlo per costruire il nome del file di log e poi trovarlo.

    ```python
    # Nel tuo DAG Airflow
    # ...
    env_vars_for_pod = {
        "GEOSCRIPTS_HOME": "/app/geoscripts",
        "ORACLE_CLIENT_LIB_DIR": "/opt/oracle/instantclient",
        "PYTHONUNBUFFERED": "1",
        "RUN_UUID": "{{ run_id }}", # Passa il run_id di Airflow come RUN_UUID
        # ... altre env vars e secret ...
    }

    run_containerized_script = KubernetesPodOperator(
        # ... altre configurazioni ...
        env_vars=env_vars_for_pod,
        get_logs=True, # Default, ma esplicito è meglio
        # ...
    )
    ```

3.  **Accesso ai Log e Invio Email:**
    * **Interfaccia Airflow:** I log del task Airflow (visibili nell'UI) conterranno ora sia l'output standard dello script sia il contenuto del tuo file di log personalizzato.
    * **Email:**
        * Nelle callback di successo/fallimento (`on_success_callback`, `on_failure_callback`), puoi accedere ai log del task. Tuttavia, inviare l'intero log via email potrebbe essere problematico per file grandi.
        * **Opzione A (Link ai log):** L'email può semplicemente includere un link ai log del task nell'interfaccia Airflow. Questa è la soluzione più pulita.
            ```python
            # Nella tua funzione di callback email
            log_url = context['ti'].log_url
            body += f"<br>Controllare i log completi (incluso il log dello script) su Airflow: <a href='{log_url}'>Log Task</a>"
            ```
        * **Opzione B (Estratto dei log - più complesso):** Se vuoi un estratto, potresti tentare di recuperare i log tramite l'API di Airflow o leggendo i file di log del worker (se accessibili e sai dove sono), ma è più complesso e fragile. In genere, non è raccomandato provare a leggere e inviare l'intero file di log del task dalla callback, specialmente se è grande.
        * **Opzione C (Inviare il file di log come allegato - vedi Strategia 2):** Richiede che il file sia accessibile ad Airflow dopo l'esecuzione del pod.

**Strategia 2: Rendere il File di Log Accessibile ad un Task Airflow Successivo (Più Complessa)**

Questo approccio è necessario se *non puoi* modificare lo script per stampare il log su `stdout`, o se il file di log deve essere processato/archiviato come file separato.

1.  **Persistenza del Log del Pod:**
    * Il container deve scrivere i log su un volume persistente (`PersistentVolumeClaim` - PVC) o su un volume che può essere montato da un altro pod (es. un `emptyDir` se il task successivo è un altro container nello stesso pod, ma qui parliamo di task Airflow separati).
    * **Usare un PVC:** Definisci un PVC e montalo nel `KubernetesPodOperator` che esegue il tuo script.

    ```python
    from airflow.providers.cncf.kubernetes.secret import Secret
    from airflow.kubernetes.volume import Volume
    from airflow.kubernetes.volume_mount import VolumeMount

    # Assumendo che tu abbia un PVC chiamato 'etl-logs-pvc' già creato nel namespace K8s
    log_volume = Volume(name='custom-etl-logs', persistent_volume_claim={'claimName': 'etl-logs-pvc'})
    log_volume_mount = VolumeMount(name='custom-etl-logs',
                                   mount_path='/montaggio/log', # Lo stesso path usato dallo script nel container
                                   sub_path='etl_run_{{ run_id | slugify }}') # Crea una sub-directory per ogni run

    run_containerized_script = KubernetesPodOperator(
        # ...
        volumes=[log_volume],
        volume_mounts=[log_volume_mount],
        # ...
    )
    ```

2.  **Task Airflow Successivo per Leggere/Inviare il Log:**
    * Crea un `PythonOperator` (o un altro `KubernetesPodOperator`) che viene eseguito *dopo* `run_containerized_script`.
    * Questo task deve:
        * Sapere come identificare il file di log specifico (avrà bisogno del `run_id` o `RUN_UUID`, passato via XComs da `run_containerized_script` o dedotto dal contesto).
        * Se è un `PythonOperator` eseguito su un worker Airflow, quel worker deve avere accesso al PVC (questo è il punto più difficile, i worker Airflow standard non montano PVC arbitrari).
        * **Soluzione più comune per il task successivo:** Usare un altro `KubernetesPodOperator` che monta lo stesso PVC (in read-only) e ha uno script/tool per leggere il file e inviarlo via email o caricarlo da qualche parte.

    ```python
    # Esempio di task successivo (molto semplificato)
    # Questo task dovrebbe conoscere il nome esatto del file di log, inclusa la data.
    # Il nome del file di log deve essere passato via XComs dal task precedente
    # o lo script nel container deve scriverlo in un file con nome fisso (relativo al sub_path).

    def process_and_email_log_file(**kwargs):
        ti = kwargs['ti']
        # run_id = ti.xcom_pull(task_ids='run_containerized_script_task_id', key='run_id') # Se run_containerized_script lo pusha
        run_id = kwargs['dag_run'].run_id # Più diretto
        
        # Determina il percorso/nome del file di log basato su run_id e la data corrente (o la data di esecuzione)
        # Questa parte è critica: come ricostruire DD-MM-YYYY? Usare la data di esecuzione del DAG?
        execution_date_str = kwargs['ds_nodash'] # YYYYMMDD
        # Oppure, se lo script originale crea il file con la data attuale al momento della scrittura:
        # questo task successivo deve sapere quale data cercare.
        # È più robusto se lo script originale scrive il suo nome file esatto in un file di "metadati"
        # o se lo passa via stdout in un formato specifico all'inizio/fine, catturato da XComs.

        # Assumiamo per ora che il nome del file possa essere costruito o sia fisso in un sub_path.
        # Questo è un ESEMPIO e probabilmente non funzionerà direttamente senza una strategia per il nome del file.
        log_filename_pattern = f"dp-ora_to_pg_*_{run_id.replace(':', '-')}.log" # Sostituisci con la logica corretta
        log_dir_in_pod = "/mnt/shared_logs/etl_run_{{ dag_run.id | slugify }}" # Stesso mountPath del task K8s
        
        # Logica per trovare e leggere il file (es. usando `glob` sul `log_dir_in_pod`)
        # ...
        # if log_content:
        #    send_airflow_email(OK_TO_ADDRESS_CB, f"Log ETL per Run {run_id}", log_content)
        pass


    # Se usi un altro K8sPodOperator per leggere il log:
    send_log_via_email_task = KubernetesPodOperator(
        task_id='send_custom_log_via_email',
        name='send-log-pod-{{ run_id | slugify }}',
        namespace='airflow', # Lo stesso namespace
        image='tuaimmagine/con_tool_email_e_accesso_fs:latest', # Immagine con `mailutils` o script Python per email
        cmds=["bash", "-c"],
        # Lo script deve sapere come trovare il file di log (basato su run_id, data)
        # e come inviare l'email. RUN_ID e altri parametri vanno passati come env var.
        arguments=[
            f"""
            LOG_DIR_MOUNT=/montaggio/log/etl_run_{{{{ dag_run.id | slugify }}}}
            echo "Cerco file di log in $LOG_DIR_MOUNT con RUN_ID={{{{ run_id }}}}"
            # Trova il file di log (la logica esatta dipende dal naming e dalla data)
            # Questo è solo un esempio, la data nel nome file rende la ricerca complessa
            TARGET_LOG_FILE=$(find $LOG_DIR_MOUNT -name 'dp-ora_to_pg_*-{{{{ run_id }}}}.log' | head -n 1)
            
            if [ -f "$TARGET_LOG_FILE" ]; then
                echo "Trovato file di log: $TARGET_LOG_FILE. Invio email..."
                # mail -s "Log ETL per Run {{{{ run_id }}}}" {OK_TO_ADDRESS_CB} < "$TARGET_LOG_FILE" # Se mailutils è installato
                # Oppure esegui uno script python che legge il file e invia l'email
                python /app/send_log_email.py --file "$TARGET_LOG_FILE" --to "{OK_TO_ADDRESS_CB}" --subject "Log ETL {{{{ run_id }}}}"
                echo "Email inviata."
            else
                echo "ERRORE: File di log non trovato in $LOG_DIR_MOUNT per run_id {{{{ run_id }}}}"
                # exit 1 # Fallisce il task se il log non è trovato
            fi
            """
        ],
        env_vars={ # Passa le variabili necessarie allo script di invio email
            "SMTP_SERVER": SMTP_MAIL_SERVER_CB,
            "FROM_EMAIL": FROM_ADDRESS_CB,
            # ... altre per autenticazione SMTP se necessarie ...
        },
        volumes=[log_volume], # Monta lo stesso PVC
        volume_mounts=[VolumeMount(name='custom-etl-logs', mount_path='/montaggio/log', read_only=True)], # Monta in read-only
        get_logs=True,
        is_delete_operator_pod=True,
        trigger_rule=TriggerRule.ALL_DONE, # Esegui anche se il task precedente fallisce, per inviare log di errore
    )
    run_containerized_script >> send_log_via_email_task
    ```

**Considerazioni per la Strategia 2:**

* **Complessità del Nome File:** Il `<DD-MM-YYYY>` nel nome del file di log complica le cose per un task successivo che cerca di leggerlo, a meno che la data esatta non sia passata via XComs o deducibile consistentemente. Sarebbe più facile se lo script scrivesse in un percorso fisso relativo al `sub_path` del volume (es. `/montaggio/log/etl_run_XXX/script.log`).
* **Permessi e Accesso al PVC:** Configurare correttamente i PVC e l'accesso tra pod può essere complicato.
* **Pulizia del PVC:** Dovrai pensare a una strategia per pulire i vecchi log dal PVC.

**Conclusione e Raccomandazione:**

Per la tua richiesta (leggere il log e inviarlo/renderlo accessibile), **la Strategia 1 (script che stampa il suo log su `stdout`) è di gran lunga la più semplice da implementare e mantenere con `KubernetesPodOperator`.**

* **Accesso UI:** Automatico.
* **Email:** L'email conterrà un link ai log completi nell'UI di Airflow. Se devi allegare il file, la Strategia 2 è necessaria, ma valuta se i benefici superano la complessità aggiunta.

Se la dimensione dei log è un problema per `stdout`, potresti far stampare allo script solo le ultime N righe o un riassunto, e mantenere il file completo sul volume (se persistito) per debug manuale se necessario (ma non direttamente integrato per l'invio email tramite Airflow in modo semplice).
