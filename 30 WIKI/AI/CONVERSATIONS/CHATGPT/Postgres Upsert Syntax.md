---
type: conversation
topic: data-platform
created: 2026-02-13
tags:
  - postgresql
  - upsert
---
> From: https://chatgpt.com/c/68012d88-096c-8008-a6dc-be316ba32f94

# you asked

how can i execute an upsert in postgres?

---

# chatgpt response

In PostgreSQL, you can perform an **upsert** (update or insert) using the `INSERT ... ON CONFLICT` syntax. Here's the general form:

```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...)
ON CONFLICT (conflict_target)
DO UPDATE SET column1 = EXCLUDED.column1,
              column2 = EXCLUDED.column2,
              ...;
```

### Example

Suppose you have a table:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    name TEXT
);
```

To upsert based on the `email` column:

```sql
INSERT INTO users (email, name)
VALUES ('user@example.com', 'Alice')
ON CONFLICT (email)
DO UPDATE SET name = EXCLUDED.name;
```

- `conflict_target` refers to the column(s) with a `UNIQUE` or `PRIMARY KEY` constraint.
- `EXCLUDED` refers to the row that would have been inserted.

If you want to do nothing on conflict:

```sql
INSERT INTO users (email, name)
VALUES ('user@example.com', 'Alice')
ON CONFLICT (email) DO NOTHING;
```

Let me know if you need to upsert with composite keys or additional conditions.

---

# you asked

transform this groovy code in a upsert:
                def cmd_ins = """
                    insert into varie.sit_catalogo_mappe 
                    (ID_MAP,DESCRIZIONE,NOTE,ORIGINE,MACROCATEGORIA,CATEGORIA,TEMA_INSPIRE,
                    FLAG_ACQUISTA,FLAG_ACQUISTA_SPORTELLO,FLAG_DOWNLOAD,FLAG_DOWNLOAD_EXTRANET,
                    FLAG_VISUALIZZATORE,REPCARTO_PUB,REPCARTO_INT, NOME_ENTE, LIVELLI)
                    values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """
                pg_db.executeInsert(cmd_ins, [it.ID_MAP,it.DESCRIZIONE,it.NOTE,it.ORIGINE,it.MACROCATEGORIA,it.CATEGORIA,
                    it.INSPIRE_TEMA,it.FLAG_ACQUISTA,it.FLAG_ACQUISTA_SPORTELLO,it.FLAG_DOWNLOAD,it.FLAG_DOWNLOAD_EXTRANET,
                    it.FLAG_VISUALIZZATORE,it.REPCARTO_PUB,it.REPCARTO_INT, it.NOME_ENTE, it.LIVELLI])

---

# chatgpt response

To transform your Groovy code into an **upsert** using PostgreSQL's `ON CONFLICT`, you must identify the conflict target — usually a `PRIMARY KEY` or `UNIQUE` constraint (assume `ID_MAP` is unique or primary key).

Here's the **upsert** version of your Groovy code:

```groovy
def cmd_upsert = """
    INSERT INTO varie.sit_catalogo_mappe 
    (ID_MAP, DESCRIZIONE, NOTE, ORIGINE, MACROCATEGORIA, CATEGORIA, TEMA_INSPIRE,
     FLAG_ACQUISTA, FLAG_ACQUISTA_SPORTELLO, FLAG_DOWNLOAD, FLAG_DOWNLOAD_EXTRANET,
     FLAG_VISUALIZZATORE, REPCARTO_PUB, REPCARTO_INT, NOME_ENTE, LIVELLI)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ON CONFLICT (ID_MAP) DO UPDATE SET
        DESCRIZIONE = EXCLUDED.DESCRIZIONE,
        NOTE = EXCLUDED.NOTE,
        ORIGINE = EXCLUDED.ORIGINE,
        MACROCATEGORIA = EXCLUDED.MACROCATEGORIA,
        CATEGORIA = EXCLUDED.CATEGORIA,
        TEMA_INSPIRE = EXCLUDED.TEMA_INSPIRE,
        FLAG_ACQUISTA = EXCLUDED.FLAG_ACQUISTA,
        FLAG_ACQUISTA_SPORTELLO = EXCLUDED.FLAG_ACQUISTA_SPORTELLO,
        FLAG_DOWNLOAD = EXCLUDED.FLAG_DOWNLOAD,
        FLAG_DOWNLOAD_EXTRANET = EXCLUDED.FLAG_DOWNLOAD_EXTRANET,
        FLAG_VISUALIZZATORE = EXCLUDED.FLAG_VISUALIZZATORE,
        REPCARTO_PUB = EXCLUDED.REPCARTO_PUB,
        REPCARTO_INT = EXCLUDED.REPCARTO_INT,
        NOME_ENTE = EXCLUDED.NOME_ENTE,
        LIVELLI = EXCLUDED.LIVELLI
"""

pg_db.executeInsert(cmd_upsert, [
    it.ID_MAP, it.DESCRIZIONE, it.NOTE, it.ORIGINE, it.MACROCATEGORIA, it.CATEGORIA,
    it.INSPIRE_TEMA, it.FLAG_ACQUISTA, it.FLAG_ACQUISTA_SPORTELLO, it.FLAG_DOWNLOAD,
    it.FLAG_DOWNLOAD_EXTRANET, it.FLAG_VISUALIZZATORE, it.REPCARTO_PUB, it.REPCARTO_INT,
    it.NOME_ENTE, it.LIVELLI
])
```

### Notes:
- Replace `ID_MAP` in `ON CONFLICT (ID_MAP)` with the appropriate unique constraint if different.
- `EXCLUDED.column_name` refers to the incoming value that caused the conflict.

Let me know if multiple columns form the conflict target.

---

# you asked

it gives this error 
ERROR: there is no unique or exclusion constraint matching the ON CONFLICT specification
apr 17, 2025 7:10:33 PM groovy.sql.Sql eachRow
but there is a constrain
CREATE TABLE varie.sit_catalogo_mappe (
	id_map numeric(10) NULL,
	descrizione varchar(150) NULL,
	note varchar(1000) NULL,
	origine varchar(500) NULL,
	macrocategoria varchar(200) NULL,
	categoria varchar(200) NULL,
	tema_inspire varchar(200) NULL,
	flag_acquista varchar(1) NULL,
	flag_acquista_sportello varchar(1) NULL,
	flag_download varchar(1) NULL,
	flag_download_extranet varchar(1) NULL,
	flag_visualizzatore varchar(1) NULL,
	repcarto_pub varchar(1) NULL,
	repcarto_int varchar(1) NULL,
	nome_ente varchar(100) NULL,
	livelli varchar(4000) NULL,
	"document" tsvector GENERATED ALWAYS AS (to_tsvector('italian'::regconfig, (((((((((COALESCE(descrizione, ''::character varying)::text || ' '::text) || COALESCE(note, ''::character varying)::text) || ' '::text) || COALESCE(categoria, ''::character varying)::text) || ' '::text) || COALESCE(tema_inspire, ''::character varying)::text) || ' '::text) || COALESCE(origine, ''::character varying)::text) || ' '::text) || COALESCE(livelli, ''::character varying)::text)) STORED NULL,
	CONSTRAINT sit_catalogo_mappe_unique UNIQUE (id_map, repcarto_pub, repcarto_int)
);

---

# chatgpt response

The error occurs because your `ON CONFLICT` clause refers only to `id_map`, but the table constraint is a **composite unique constraint**:

```sql
CONSTRAINT sit_catalogo_mappe_unique UNIQUE (id_map, repcarto_pub, repcarto_int)
```

To fix this, modify your `ON CONFLICT` clause to use the **full composite key**:

### ✅ Corrected Groovy Upsert Code:

```groovy
def cmd_upsert = """
    INSERT INTO varie.sit_catalogo_mappe 
    (ID_MAP, DESCRIZIONE, NOTE, ORIGINE, MACROCATEGORIA, CATEGORIA, TEMA_INSPIRE,
     FLAG_ACQUISTA, FLAG_ACQUISTA_SPORTELLO, FLAG_DOWNLOAD, FLAG_DOWNLOAD_EXTRANET,
     FLAG_VISUALIZZATORE, REPCARTO_PUB, REPCARTO_INT, NOME_ENTE, LIVELLI)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ON CONFLICT (ID_MAP, REPCARTO_PUB, REPCARTO_INT) DO UPDATE SET
        DESCRIZIONE = EXCLUDED.DESCRIZIONE,
        NOTE = EXCLUDED.NOTE,
        ORIGINE = EXCLUDED.ORIGINE,
        MACROCATEGORIA = EXCLUDED.MACROCATEGORIA,
        CATEGORIA = EXCLUDED.CATEGORIA,
        TEMA_INSPIRE = EXCLUDED.TEMA_INSPIRE,
        FLAG_ACQUISTA = EXCLUDED.FLAG_ACQUISTA,
        FLAG_ACQUISTA_SPORTELLO = EXCLUDED.FLAG_ACQUISTA_SPORTELLO,
        FLAG_DOWNLOAD = EXCLUDED.FLAG_DOWNLOAD,
        FLAG_DOWNLOAD_EXTRANET = EXCLUDED.FLAG_DOWNLOAD_EXTRANET,
        FLAG_VISUALIZZATORE = EXCLUDED.FLAG_VISUALIZZATORE,
        NOME_ENTE = EXCLUDED.NOME_ENTE,
        LIVELLI = EXCLUDED.LIVELLI
"""

pg_db.executeInsert(cmd_upsert, [
    it.ID_MAP, it.DESCRIZIONE, it.NOTE, it.ORIGINE, it.MACROCATEGORIA, it.CATEGORIA,
    it.INSPIRE_TEMA, it.FLAG_ACQUISTA, it.FLAG_ACQUISTA_SPORTELLO, it.FLAG_DOWNLOAD,
    it.FLAG_DOWNLOAD_EXTRANET, it.FLAG_VISUALIZZATORE, it.REPCARTO_PUB, it.REPCARTO_INT,
    it.NOME_ENTE, it.LIVELLI
])
```

### Summary:
Use `ON CONFLICT (id_map, repcarto_pub, repcarto_int)` to match the unique constraint. This resolves the error.
