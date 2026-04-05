---
created: 2026-03-27
tags:
  - note
  - journal
type: note
topic:
---

# PROGETTO

/Users/S.Parodi/Development/DP/docker-project



# Installazione ambiente sviluppo

- Container Locale
- Ambiente Jupyter (Lorenzo)
- ICE4AI

## Container Locale

Container con jupyter + vscode + progetto dbt


### BUILD IMMAGINE
```
export GITLAB_TOKEN="glpat-zMAxJLSkqdmnurZTRhrB" && docker compose build
```

### RUN

```bash
docker run -d --name dbt-dev \
    -p 8888:8888 \
    -v /Users/S.Parodi/Development/DP/dbt-dev-environment:/home/developer \
    dbt-dev-environment:latest
```


### REGISTRY


DEPLOY IMMAGINE SU REGISTRY
- Creato gruppo pubblico ["Risorse Pubbliche"](https://gitlab-test.dataliguria.it/risorse-pubbliche) per immagini pubbliche
- REGISTRY: https://gitlab-test.dataliguria.it/risorse-pubbliche/dbt-dev-environment/container_registry


### USER WORKFLOW

[README](https://gitlab-test.dataliguria.it/risorse-pubbliche/dbt-dev-environment/-/blob/main/README.md?ref_type=heads) 

- Creazione cartella locale per sviluppo progetti dbt (es: /Users/S.Parodi/Development/DP/dbt-dev-env)
- Configurazione git (user.name / user.email)
	- lancio ```git config --global``` nel container
	- creazione .gitconfig su cartella locale
	- env var a runtime -e GIT_USER_NAME="fanenji" -e GIT_USER_EMAIL="s.parodi@liguriadigitale.it"
- Docker login registry 
- Lancio del container 


Docker Login
```
docker login gitlab-test.dataliguria.it:5050
```

Lancio del container
```
docker run -it --rm -p 8888:8888 -v /Users/S.Parodi/Development/DP/dbt-dev-environment:/home/developer gitlab-test.dataliguria.it:5050/risorse-pubbliche/dbt-dev-environment:latest
```

Configurazione git
```
git config --global user.name "fanenji" && git config --global user.email "s.parodi@liguriadigitale.it"
```

esempio .gitconfig
```
[user]
	name = fanenji
	email = s.parodi@liguriadigitale.it
```

### CONTAINER WORKFLOW

- cd progetto creato 
- creare .venv
- installare requirements `pip install -r requirements.txt`
- aprire vscode (code server)
- configurare .env.local (Dremio pwd & OpenMetadata JWT Token)
- dbt-workflow run

```bash
DREMIO_PASSWORD=yLNuGBP8UtUDAYaZyfmE
OPENMETADATA_JWT_TOKEN=eyJraWQiOiJHYjM4OWEtOWY3Ni1nZGpzLWE5MmotMDI0MmJrOTQzNTYiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuLW1ldGFkYXRhLm9yZyIsInN1YiI6ImxkYWRtaW4iLCJyb2xlcyI6WyJBZG1pbiJdLCJlbWFpbCI6ImxkYWRtaW5AbGQub3JnIiwiaXNCb3QiOmZhbHNlLCJ0b2tlblR5cGUiOiJQRVJTT05BTF9BQ0NFU1MiLCJpYXQiOjE3NjU4MTg0OTYsImV4cCI6MTc3MzU5NDQ5Nn0.ZN2SxVCtgLYFnWDalhulWw7n_PpGZd2HLOuUNvi6RVlcD_0YGwl3GeltwesKA7NwP2UXvtrdsmWTV13DlVfwT2FqvflvvfWpdGiBplroogzyp2EPa_OnEKH7L75GvdbUsIPT8cifAQ9pRWfkDtbHv32tEHeYkeC8QYnxa_0MxJZalGF7Xody6gRIGBTp_TGUpDRtJWa8XXzERW0jh0k6RHH9hXqKRqM5CAXDE3dcWgffLuXPQaH6Lx1xbE81lPeIMj7ZmBQEtffHHAYWpnbKC-QTLiZe7wl6esHvySpGpZHbIvioymhsn7ss7ZW80xSBqx1mcLZQVbLUqrI8l0MyRg
```


### TODO


- test dbt-workflow: network timeout - configurare timeout Dremio
- dbt-osmosis richiede conferma 'y' ma non compare messaggio





## Prompt


**PROMPT 1**

Help me with this: creating a container for a consistent python developement environment.

The environment must support the development of dbt projects for a data platform. 
These are the major on-prem components that are involved in the current stages of development:
- gitlab (to get packages and to use as version control)
- dbt (a package in the container as a framework)
- dremio (as data source and sink)
- openmetadata (to push and pull metadata)
- kestra (to push and pull yaml files)
- an ollama server (exposes different models through api)
- possibly more to come (for context, no action required)

There are two phases we have identified: a build scenario and a development/runtime scenario.

Information for the build scenario:
- install dbt-creator package
    -git+https://company-url//data-platform/dbt/models/dbt-project-creator.git
- install custom packages from gitlab (as git repos with pip git+https)
    -git+https://company-url/data-platform/dbt/models/dbt-osmosis-1.2.2.git
    -git+https://company-url//data-platform/dbt/models/dbt-workflow.git
    -git+https://company-url/data-platform/custom-images/openmetadata-dremio-connect.git#subdirectory=connector
- gitlab must be authenticated with access token and HTTPS
- install packages from public repos through pip (no auth)
   -pre-commit>=4.5.0
   -dbt-dremio==1.9.0
   -openai~=1.58.1
   -cachetools==7.0.5
- all current and future dependencies are in requierements.txt
- must contain jupyter and code-server (https://github.com/coder/code-server)
Please ask more questions if we missed something

Information about the development/runtime scenario:
- the developer opens his browser to reach a localhost version of jupyter
- the developer has access to a code-server button in the jupyter interface and open it
- the developer has a code server interface where they code and have access to their /home/
    -in the /home/ folder they store all their projects
- the environment needs to persist data on the running machine disk
- the development has these phases:
    -dbt-creator: interactive wizard that boostraps a new complaint dbt project
        -gathers the information needed:
            -name of project, gitlab group, gitlab token...
        -creates a project from a git template both remote and local
        
    -the developer develops the dbt models
    
    -dbt-workflow: pipeline of stages that ensure the correct process:
        -load env variables
        -pull the git repository
        -dbt deps 
        -dbt build
        -dbt-osmosis yaml refactor --syntesize
        -dbt docs generate
        -pre-commit (dbt-checkpoint sanity checks)
        -metadata injections to openmetadata
        -git commit and push


First inspect the relevant information and brainstorm.
Then make a detail plan, with a short summary. 
Then implement the smallest correct change that satisfies the request.

Constraints:
- do not make changes without asking first
- python version must be 3.12.xx
- stay consistent with existing patterns
- avoid unrelated refactors
- avoid new dependencies unless necessary
- keep the diff minimal

Validation:
- run the most relevant checks available
- if full validation is too heavy, run the smallest meaningful subset and say what you verified
- check and present to us any conflicting information we might have provided (requirements/constraints/context)

Response structure:
- what you changed
- why
- files touched
- checks run
- any remaining caveats

Final output (releases):
- a document with every choice and why they were made
- a dockerfile
- synthetic readme presenting structure and how to use
- diagrams embedded in md
- final user guideline 

```
Before I proceed, I need your input on:
1. The double-slash URLs — are those typos or intentional? 
2. Are you OK with jupyter-server-proxy + jupyter-codeserver-proxy as new dependencies for the code-server-in-Jupyter integration? 
3. Non-root user developer — good name, or do you prefer something else? 
4. BuildKit secrets for Gitlab token — this means building with DOCKER_BUILDKIT=1 and passing --secret id=gitlab_token,env=GITLAB_TOKEN. OK with that approach? 
5. Split requirements (public vs private) — or do you prefer a single requirements.txt with everything? 
6. Any specific versions for Jupyter or code-server you want pinned? 
7. The bind mount path — ./workspace:/home/developer or different mapping?
```

**PROMPT 2**

- IMPORTANT NOTE: the real final output is actually the archifact of the dockerfile: a vm-like environment in a seamless fashion
- for further information this image will run on local developers machines, but we plan in the future to migrate the environment to a jupyter proxy env that will instantiate on demand new environments for deployment in a private k8s (rke2) cloud infrastructure 
- in docker-compose there should be no env vars for Dremio/OpenMetadata/Kestra/Ollama endpoints and will be statically provided 
Reguarding your questions?
1) double-slash urls are a typo  
2) ok
3) ok
4) ok
5) split
6) no 
7) the bind mount path should be expressed at run time (in the container run command)



