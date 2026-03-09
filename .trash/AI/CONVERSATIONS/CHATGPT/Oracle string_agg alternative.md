---
type: conversation
topic: data-platform
created: 2026-02-13
tags:
  - oracle
  - sql
---
> From: https://chatgpt.com/c/67ffc1b3-16c8-8008-80d1-fb9f1960bb2f

# you asked

is there in oracle 11 a function similar to the postgres function string_agg()?

---

# chatgpt response

Oracle 11g does not have a direct equivalent of PostgreSQL’s `string_agg()` function. However, you can achieve similar functionality using the `LISTAGG()` function, which was introduced in Oracle 11g Release 2 (11.2).

### Syntax:
```sql
LISTAGG(column_name, 'delimiter') WITHIN GROUP (ORDER BY column_name)
```

### Example:
```sql
SELECT department_id,
       LISTAGG(employee_name, ', ') WITHIN GROUP (ORDER BY employee_name) AS employees
FROM employees
GROUP BY department_id;
```

This will concatenate employee names within each department, separated by commas.

### Notes:
- `LISTAGG` will throw an error if the result exceeds 4000 characters in Oracle 11g.
- If you're on Oracle 11g **Release 1 (11.1)**, `LISTAGG` is not available, and you would need to use `WM_CONCAT` (undocumented) or a custom aggregation function using `XMLAGG`.

Let me know if you're on 11.1 and need the XMLAGG workaround.

---

# you asked

what if the select returns this error
ORA-01489 : Il risultato della concatenazione della stringa è troppo lungo

---

# chatgpt response

The error `ORA-01489: result of string concatenation is too long` occurs with `LISTAGG` in Oracle 11g when the resulting concatenated string exceeds **4000 bytes**, which is the limit for a `VARCHAR2` in SQL context (not PL/SQL).

### Solutions:

#### 1. **Use `XMLAGG` as a workaround**  
Unlike `LISTAGG`, `XMLAGG` returns a `CLOB`, allowing results larger than 4000 characters.

##### Example:
```sql
SELECT department_id,
       RTRIM(XMLAGG(XMLELEMENT(e, employee_name || ', ').EXTRACT('//text()') ORDER BY employee_name).GetClobVal(), ', ') AS employees
FROM employees
GROUP BY department_id;
```

- `XMLELEMENT` builds an XML fragment for each value.
- `XMLAGG` concatenates them.
- `GetClobVal()` returns the result as a CLOB.
- `RTRIM(..., ', ')` removes the trailing delimiter.

#### 2. **PL/SQL Function with CLOB Output**  
You can write a custom aggregation function using PL/SQL if you need more control or need to reuse it.

Let me know if you'd like the code for such a user-defined aggregate function.

---

# you asked

i prefer a varchar2 type give me a select that truncate the string

---

# chatgpt response

To avoid `ORA-01489` while keeping the result as `VARCHAR2`, you can **truncate the output manually** by wrapping `LISTAGG` with `SUBSTR`.

Here’s a safe version of the query:

```sql
SELECT department_id,
       SUBSTR(
           LISTAGG(employee_name, ', ') WITHIN GROUP (ORDER BY employee_name),
           1, 4000
       ) AS employees
FROM employees
GROUP BY department_id;
```

This ensures the result never exceeds the 4000-byte limit of `VARCHAR2`. The truncation happens after the aggregation, so the string may be cut mid-value or mid-delimiter — but it will not throw an error.

If you need truncation on clean delimiter boundaries, a more complex solution is required. Let me know if that's needed.
