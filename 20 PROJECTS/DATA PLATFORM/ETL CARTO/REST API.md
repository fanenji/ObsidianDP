
Esposizione script python tramite servizio REST FastApi

Sì, è possibile lanciare script Python come ora_to_pg.py o load_postgis.py da un servizio REST implementato con FastAPI.

Un approccio comune è utilizzare il modulo subprocess di Python all'interno dell'applicazione FastAPI per eseguire lo script desiderato.

Ad esempio, un endpoint FastAPI potrebbe:

1. Ricevere una richiesta HTTP (es. con i parametri necessari per lo script).
2. Costruire il comando per eseguire lo script, potenzialmente utilizzando lo script run_script per assicurarsi che venga eseguito all'interno dell'ambiente Docker corretto con le dipendenze necessarie.
3. Avviare il processo dello script usando subprocess.Popen o subprocess.run.

Per script di lunga durata, è consigliabile eseguire il processo in background (ad esempio, usando le Background Tasks di FastAPI o una coda di task come Celery) per non bloccare la risposta HTTP.

# PROCESSI ASYNCH

## Background Tasks

Le `BackgroundTasks` di FastAPI consentono di eseguire operazioni dopo aver restituito una risposta HTTP. Questo è utile per attività che richiedono tempo, come l'esecuzione di uno script, senza far attendere il client.

Ecco un esempio di come potresti usare `BackgroundTasks` per lanciare uno script Python tramite `subprocess`:

```python
from fastapi import FastAPI, BackgroundTasks
import subprocess
import shlex

app = FastAPI()

def run_script_in_background(script_path: str, *args):
    """
    Funzione eseguita in background per lanciare uno script.
    """
    try:
        # Costruisce il comando, potenzialmente usando lo script 'run'
        # command = f"/srv/geoscript/run {script_path}" # Esempio con lo script 'run'
        command = f"python {script_path}" # Esempio diretto
        if args:
            # Aggiunge argomenti allo script, facendo attenzione al quoting
            command += " " + " ".join(shlex.quote(str(arg)) for arg in args)

        print(f"Esecuzione comando in background: {command}")
        # Usa Popen per non bloccare, anche se la Background Task gestisce già l'asincronicità
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate() # Aspetta la fine del processo (nella background task)

        if process.returncode == 0:
            print(f"Script {script_path} completato con successo.")
            print(f"Output:\n{stdout.decode()}")
        else:
            print(f"Errore durante l'esecuzione di {script_path}.")
            print(f"Errore:\n{stderr.decode()}")
    except Exception as e:
        print(f"Errore nell'esecuzione della background task per {script_path}: {e}")

@app.post("/run-script/{script_name}")
async def trigger_script(script_name: str, background_tasks: BackgroundTasks):
    """
    Endpoint per avviare l'esecuzione di uno script in background.
    """
    # Mappa il nome ricevuto a un percorso di script valido
    # ATTENZIONE: Assicurati che 'script_name' non permetta path traversal!
    # Dovresti avere una mappatura sicura o validare l'input.
    scripts_available = {
        "ora_to_pg": "/srv/geoscript/dp/ora_to_pg.py",
        "load_postgis": "/srv/geoscript/rqa/load_postgis.py"
        # Aggiungi altri script qui
    }

    script_path = scripts_available.get(script_name)

    if not script_path:
        return {"message": "Script non valido"}

    # Aggiunge l'esecuzione dello script alle background tasks
    # Puoi passare argomenti aggiuntivi dopo script_path
    background_tasks.add_task(run_script_in_background, script_path) # , arg1, arg2...)

    return {"message": f"Esecuzione dello script '{script_name}' avviata in background."}

# Per eseguire questa app: uvicorn your_fastapi_app:app --reload
```

**Spiegazione:**

1. **`BackgroundTasks`:** Viene iniettato come dipendenza nell'endpoint (`trigger_script`).
2. **`add_task`:** Si usa `background_tasks.add_task(nome_funzione, arg1, arg2, ...)` per registrare una funzione da eseguire in background dopo l'invio della risposta.
3. **`run_script_in_background`:** Questa è la funzione che viene eseguita in background. Al suo interno:
    - Si costruisce il comando per lanciare lo script Python desiderato. Potresti voler usare il percorso assoluto allo script run fornito (run) seguito dal percorso dello script Python specifico (`dp/ora_to_pg.py` o `rqa/load_postgis.py`) per assicurarti che l'ambiente virtuale e le dipendenze siano gestite correttamente, specialmente se FastAPI gira in un container diverso o senza l'ambiente attivato.
    - Si usa `subprocess.Popen` per avviare lo script come processo separato.
    - `process.communicate()` attende la fine del processo (ma questo accade nel thread/task in background, quindi non blocca FastAPI).
    - Viene gestito l'output e gli eventuali errori. L'output viene stampato nei log del server FastAPI.

Questo approccio permette all'endpoint `/run-script/{script_name}` di rispondere immediatamente al client, mentre lo script Python viene eseguito in background.

## CELERY

Celery è un sistema di code di task distribuite, più robusto e scalabile rispetto alle `BackgroundTasks` integrate di FastAPI. È ideale per:

- Task molto lunghe.
- Task che devono essere eseguite su worker separati (potenzialmente su macchine diverse).
- Necessità di meccanismi avanzati come tentativi automatici (retries), scheduling, rate limiting.
- Monitoraggio dello stato delle task.

**Componenti principali:**

1. **Broker:** Un message broker (come Redis o RabbitMQ) che riceve le richieste di task da FastAPI e le mette in coda.
2. **Worker:** Processi separati che prelevano le task dalla coda (tramite il broker) e le eseguono.
3. **Backend (Opzionale):** Un database o un altro storage (come Redis o un database relazionale) per memorizzare i risultati delle task.

**Integrazione con FastAPI:**

1. **Installazione:**

```python
pip install celery redis
```

1. (Userai Redis come broker/backend in questo esempio).
2. **Configurazione Celery:** Crea un file per la configurazione di Celery, ad esempio `celery_worker.py`.

```python
# filepath: /path/to/your/celery_worker.py
from celery import Celery
import subprocess
import shlex
import os

# Assicurati che il broker (Redis) sia in esecuzione
# Esempio: redis://localhost:6379/0
# Potresti usare variabili d'ambiente per la configurazione
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

# Configurazione opzionale
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Rome',
    enable_utc=True,
)

@celery_app.task(name="run_script_task")
def run_script_task(script_path: str, *args):
    """
    Task Celery per eseguire uno script Python usando lo script 'run'.
    """
    # Usa lo script 'run' per garantire l'ambiente corretto
    run_script_path = "/srv/geoscript/run" # Percorso dello script 'run'
    target_script_relative_path = script_path # Es: 'dp/ora_to_pg.py'

    # Verifica che lo script target esista (opzionale ma consigliato)
    full_target_path = os.path.join("/srv/geoscript", target_script_relative_path)
    if not os.path.exists(full_target_path):
         print(f"Errore: Script target non trovato: {full_target_path}")
         # Potresti voler sollevare un'eccezione o restituire uno stato di errore
         return {"status": "error", "message": "Script target non trovato"}

    try:
        # Costruisce il comando usando lo script 'run'
        command = f"{run_script_path} {target_script_relative_path}"
        if args:
            command += " " + " ".join(shlex.quote(str(arg)) for arg in args)

        print(f"Esecuzione comando Celery: {command}")
        # Esegue il comando
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd="/srv/geoscript")
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print(f"Script {target_script_relative_path} completato con successo.")
            print(f"Output:\n{stdout.decode()}")
            return {"status": "success", "output": stdout.decode()}
        else:
            print(f"Errore durante l'esecuzione di {target_script_relative_path}.")
            print(f"Errore:\n{stderr.decode()}")
            return {"status": "error", "error": stderr.decode()}
    except Exception as e:
        print(f"Errore nella task Celery per {target_script_relative_path}: {e}")
        # Rilancia l'eccezione per farla gestire da Celery (es. retry)
        raise e # O return {"status": "error", "message": str(e)}
```

1. **Endpoint FastAPI:** Modifica l'endpoint per inviare la task a Celery.

```python
# filepath: /path/to/your/fastapi_app.py
from fastapi import FastAPI # , BackgroundTasks # Rimuovi BackgroundTasks se non più usato altrove
# Importa l'istanza di Celery e la task
from .celery_worker import celery_app, run_script_task
from celery.result import AsyncResult

app = FastAPI()

# ... (altri endpoint)

@app.post("/run-script-celery/{script_name}", status_code=202)
async def trigger_script_celery(script_name: str):
    """
    Endpoint per avviare l'esecuzione di uno script tramite Celery.
    """
    # Mappa il nome ricevuto a un percorso di script relativo alla root del progetto
    # ATTENZIONE: Validazione input è cruciale!
    scripts_available = {
        "ora_to_pg": "dp/ora_to_pg.py",
        "load_postgis": "rqa/load_postgis.py"
        # Aggiungi altri script qui
    }

    script_relative_path = scripts_available.get(script_name)

    if not script_relative_path:
        return {"message": "Script non valido"}

    # Invia la task alla coda di Celery
    # .delay() è una scorciatoia per .apply_async()
    task = run_script_task.delay(script_relative_path) # Passa argomenti aggiuntivi qui se necessario

    return {"message": f"Task per '{script_name}' inviata.", "task_id": task.id}

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """
    Endpoint (opzionale) per controllare lo stato di una task Celery.
    """
    task_result = AsyncResult(task_id, app=celery_app)
    result = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result # Contiene il return della task o l'errore
    }
    return result

# Per eseguire questa app: uvicorn your_fastapi_app:app --reload
```

1. **Esecuzione:**
- **Avvia il Broker:** Assicurati che Redis (o il broker scelto) sia in esecuzione. Se usi Docker, puoi avviare un container Redis.
- **Avvia FastAPI:** `uvicorn your_fastapi_app:app --reload`
- **Avvia il Worker Celery:** Apri un altro terminale, vai nella directory del tuo progetto e avvia il worker:

```python
celery -A your_module.celery_worker worker --loglevel=info
```

(Sostituisci `your_module.celery_worker` con il percorso Python corretto al file `celery_worker.py`, ad esempio `src.celery_worker` se il file è in `src/`). Il worker si connetterà al broker e inizierà a processare le task.

**Vantaggi rispetto a `BackgroundTasks`:**

- **Scalabilità:** Puoi avviare più worker, anche su macchine diverse, per processare più task in parallelo.
- **Affidabilità:** Celery offre meccanismi di retry automatico in caso di fallimenti temporanei.
- **Separazione:** I worker sono processi distinti, quindi un crash in una task non impatta l'applicazione FastAPI principale.
- **Monitoraggio:** Strumenti come Flower permettono di monitorare lo stato delle code e dei worker.
- **Scheduling:** Celery Beat permette di pianificare l'esecuzione periodica delle task.

Celery introduce maggiore complessità (necessità di un broker e di processi worker separati), ma offre molta più potenza e flessibilità per la gestione di task in background.

# IMPLEMENTAZIONE

Ho aggiornato i file requirements.txt e Dockerfile come richiesto.

Ricorda di sostituire `"main:app"` nel `CMD` del Dockerfile con il percorso corretto del tuo modulo FastAPI e dell'istanza dell'applicazione (ad esempio, se il file è `api/server.py` e l'istanza è `my_app = FastAPI()`, dovresti usare `"api.server:my_app"`).

Creo un nuovo file `main.py` nella directory geoscript e inserisco il codice FastAPI con l'esempio di `BackgroundTasks`.

Questo codice presuppone che gli script da eseguire (`ora_to_pg.py`, `load_postgis.py`) si trovino nei percorsi `/srv/geoscript/dp/` e `/srv/geoscript/rqa/` *all'interno del container Docker*, come definito nel Dockerfile. Utilizzerà lo script `/srv/geoscript/run` per eseguire gli script Python nell'ambiente virtuale corretto.

Ho creato il file main.py con l'applicazione FastAPI e l'endpoint `/run-script/{script_name}` che utilizza `BackgroundTasks` per eseguire gli script specificati (`dp/ora_to_pg.py` o `rqa/load_postgis.py`) in background.

Il codice utilizza lo script `/srv/geoscript/run` per assicurarsi che gli script Python vengano eseguiti all'interno dell'ambiente virtuale corretto definito nel container Docker.

Ora puoi costruire l'immagine Docker e avviare il container. Una volta avviato, potrai inviare richieste POST all'endpoint, ad esempio:

`curl -X POST http://localhost:8000/run-script/ora_to_pg`

(Assumendo che tu abbia mappato la porta 8000 del container alla porta 8000 del tuo host con `docker run -p 8000:8000 ...`).

ESEMPIO DI CHIAMATA

```other
curl -X POST http://localhost:8000/run-script-async/ora_to_pg \
  -H "Content-Type: application/json" \
  -d '{"args": ["--id", "56"], "email": "destinatario@esempio.com"}'

http://localhost:8000/run-script-async/ora_to_pg?args=--id&args=56&email=fanenji@gmail.com

curl "http://localhost:8000/run-script-sync/ora_to_pg?args=--id&args=56"
```

# EMAIL MSG

In the background execution implement after completion or error the sending of a email message.

the email address shoud be in a input parameter "email" and the configuration (SMTP_MAIL_SERVER and FROM_ADDRESS) are in the geoscript/.env file

If no email address in the parameters use the ERROR_TO_ADDRESS and OK_TO_ADDRESS in the env file
