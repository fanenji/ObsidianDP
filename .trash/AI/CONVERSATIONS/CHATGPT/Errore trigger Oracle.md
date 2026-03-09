---
type: conversation
topic: data-platform
created: 2026-02-13
tags:
  - oracle
  - trigger
---
> From: https://chatgpt.com/c/67c86104-eaf8-8008-b954-3c4ba4c50c46

# you asked

Please help me solve a problem with an Oracle trigger
---
This is the trigger:
CREATE OR REPLACE TRIGGER POSTINS_LOB_STAZ_GRID AFTER INSERT ON LOBG05_SPECIE_P FOR EACH ROW
DECLARE
  v_job_name VARCHAR2(50);
BEGIN
	v_job_name := 'JOB_GRID_INSERT_' || TO_CHAR(SYSTIMESTAMP, 'YYYYMMDDHH24MISS');
	DBMS_SCHEDULER.CREATE_JOB (
     job_name        => v_job_name,
     job_type        => 'PLSQL_BLOCK',
     job_action      => 'BEGIN LIBIOSS_OSS_GRID_INSERT(' || :NEW.ID_STAZ || '); END;',
     start_date      => SYSTIMESTAMP + INTERVAL '10' SECOND,
     enabled         => TRUE,
     auto_drop       => TRUE,
     comments        => 'Job scheduled to execute LIBIOSS_OSS_GRID_INSERT 30 seconds after insert'
  );
END;
---
This is the procedure:
CREATE OR REPLACE PROCEDURE LIBIOSS_ETRF89.LIBIOSS_OSS_GRID_INSERT (p_id_staz number) AS
BEGIN
	INSERT INTO LOBG05_SPECIE_P_GR_10KM
	SELECT l.CELLCODE, p.ID_STAZ FROM CTEMI_ETRF89.LIGURIA_1KM_6707 l
	JOIN LOBG05_SPECIE_P p ON SDO_RELATE(p.ORA_GEOMETRY, l.GEOMETRY, 'mask=ANYINTERACT') = 'TRUE'
	WHERE p.ID_STAZ = p_id_staz;
	INSERT INTO LOBG05_SPECIE_P_GR_1KM
	SELECT l.CELLCODE, p.ID_STAZ FROM CTEMI_ETRF89.LIGURIA_1KM_6707 l
	JOIN LOBG05_SPECIE_P p ON SDO_RELATE(p.ORA_GEOMETRY, l.GEOMETRY, 'mask=ANYINTERACT') = 'TRUE'
	WHERE p.ID_STAZ = p_id_staz;
END LIBIOSS_OSS_GRID_INSERT;
---
This is the error:
Errore SQL [4092] [42000]: ORA-04092: impossibile  in un trigger
ORA-06512: a "SYS.DBMS_ISCHED", line 135
ORA-06512: a "SYS.DBMS_SCHEDULER", line 271
ORA-06512: a "LIBIOSS_ETRF89.POSTINS_LOB_STAZ_GRID", line 7
ORA-04088: errore durante esecuzione del trigger 'LIBIOSS_ETRF89.POSTINS_LOB_STAZ_GRID'

---

# chatgpt response

The error **ORA-04092** occurs because **you cannot commit or perform transactional control operations inside a trigger**, and `DBMS_SCHEDULER.CREATE_JOB` implicitly commits changes.  

### Solution:
Instead of calling `DBMS_SCHEDULER.CREATE_JOB` directly inside the trigger, move the job creation logic into a separate **autonomous transaction procedure**, and call that procedure from the trigger.

---

### Fix:
1. **Create a new autonomous transaction procedure** for job scheduling:
   ```sql
   CREATE OR REPLACE PROCEDURE LIBIOSS_ETRF89.SCHEDULE_GRID_INSERT (p_id_staz NUMBER) AS
   PRAGMA AUTONOMOUS_TRANSACTION;
   v_job_name VARCHAR2(50);
   BEGIN
       v_job_name := 'JOB_GRID_INSERT_' || TO_CHAR(SYSTIMESTAMP, 'YYYYMMDDHH24MISS');
       
       DBMS_SCHEDULER.CREATE_JOB (
           job_name        => v_job_name,
           job_type        => 'PLSQL_BLOCK',
           job_action      => 'BEGIN LIBIOSS_ETRF89.LIBIOSS_OSS_GRID_INSERT(' || p_id_staz || '); END;',
           start_date      => SYSTIMESTAMP + INTERVAL '10' SECOND,
           enabled         => TRUE,
           auto_drop       => TRUE,
           comments        => 'Job scheduled to execute LIBIOSS_OSS_GRID_INSERT 10 seconds after insert'
       );
       
       COMMIT; -- Required for autonomous transactions
   END SCHEDULE_GRID_INSERT;
   ```

2. **Modify the trigger to call the new procedure**:
   ```sql
   CREATE OR REPLACE TRIGGER POSTINS_LOB_STAZ_GRID 
   AFTER INSERT ON LOBG05_SPECIE_P 
   FOR EACH ROW
   BEGIN
       LIBIOSS_ETRF89.SCHEDULE_GRID_INSERT(:NEW.ID_STAZ);
   END;
   ```

---

### Why This Works:
- **PRAGMA AUTONOMOUS_TRANSACTION** ensures that `DBMS_SCHEDULER.CREATE_JOB` executes in a separate transaction, avoiding trigger restrictions.
- The trigger now only calls a procedure, which is allowed.
- `COMMIT` in the procedure ensures that the job is scheduled successfully.

This should resolve the `ORA-04092` error and allow your job to be scheduled properly. 🚀
