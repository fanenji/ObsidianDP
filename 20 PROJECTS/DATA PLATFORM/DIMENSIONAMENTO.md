---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - minio
  - dimensionamento
---

### MinIO

| **Componente** | **Numero di nodi** | **CPU** | **RAM** | **Storage	Network**              |
| -------------- | ------------------ | ------- | ------- | -------------------------------- |
| MinIO          | 4                  | 16 vCPU | 32 GB   | 4 X 4 TB (preferibili NVMe SSDs) |

Con questa configurazione, utilizzando un Erasure Code Stripe Size di 16 ed un Erasure Code Parity di 8, avremmo:

- Capacità usabile: 32 TiB
- Capacità totale: 64 TiB
- Efficienza dello storage: 50%
- Drive Failure Tolerance: possiamo perdere 8 drive su 16
- Server Failure Tolerance: possiamo perdere 2 server su 4

### Project Nessie

Si può installare la linea di comando e il servizio (che può essere sia containerizzato o sia lanciato come `.jar`) in una macchina con i seguenti requisiti:

| **Componente** | **Numero di nodi** | **CPU** | **RAM** | **Storage** |
| -------------- | ------------------ | ------- | ------- | ----------- |
| Project Nessie | 1                  | 2 vCPU  | 8 GB    | 50 GB       |

Si può pensare di accorparlo con altri servizi che richiedono dimensionamenti basici.

### Dremio

| **Componente** | **Numero di nodi** | **CPU** | **RAM** | **Storage** |
| -------------- | ------------------ | ------- | ------- | ----------- |
| Coordinator    | 1                  | 16 vCPU | 32 GB   | 200 GB      |
| Executor       | 3                  | 16 vCPU | 128 GB  | 300 GB      |

Serviranno anche 300-500 GB di distributed storage che possiamo prendere da quelli disponibili su MinIO.

### Kafka

| **Componente**                                           | **Numero di nodi** | **CPU** | **RAM** | **Storage** |
| -------------------------------------------------------- | ------------------ | ------- | ------- | ----------- |
| Broker + Zookeeper                                       | 3                  | 12 vCPU | 64 GB   | 1 TB        |
| Worker Node (Connect, Schema Registry, Kafka REST Proxy) | 2                  | 12vCPU  | 8 GB    | 50 GB       |

### Pipeline orchestrator

| **Componente**        | **Numero di nodi** | **CPU** | **RAM** | **Storage** |
| --------------------- | ------------------ | ------- | ------- | ----------- |
| Pipeline orchestrator | 1                  | 2 vCPU  | 8 GB    | 100 GB      |

### Data Catalog

Di seguito illustreremo il sizing necessario per il deployment di uno dei due Data Catalog scelti. In particolare, questo sizing è da tenere in considerazione se dovessimo utilizzare la versione containerizzata in Docker:

| **Componente** | **Numero di nodi** | **CPU** | **RAM** | **Storage** |
| -------------- | ------------------ | ------- | ------- | ----------- |
| DataHub        | 1                  | 6 vCPU  | 8 GB    | 50 GB       |
| Open Metadata  | 1                  | 6 vCPU  | 8 GB    | 50 GB       |

Open Metadata offre la possibilità di essere installato anche in modalità bare metal. Per cui, su uno stesso nodo con le medesime dimensioni individuate per l'ambiente containerizzato, posso essere installate le seguenti componenti:

- Open Metadata server;
- Elasticsearch/Opensearch;
- Database (MySQL o Postgres).

### Opensearch

| **Componente**       | **Numero di nodi** | **CPU** | **RAM** | **Storage** |
| -------------------- | ------------------ | ------- | ------- | ----------- |
| Coordinating node    | 1                  | 12 vCPU | 8 GB    | 50 GB       |
| Cluster Manager node | 1                  | 2 vCPU  | 8 GB    | 50 GB       |
| Data node            | 2                  | 4 vCPU  | 64 GB   | 500 GB      |

### Superset

| **Componente** | **Numero di nodi** | **CPU** | **RAM** | **Storage** |
| -------------- | ------------------ | ------- | ------- | ----------- |
| Superset       | 1                  | 2 vCPU  | 8 GB    | 50 GB       |

### Spark

| **Componente** | **Numero di nodi** | **CPU** | **RAM** | **Storage** |
| -------------- | ------------------ | ------- | ------- | ----------- |
| Spark          | 4                  | 4 vCPU  | 16 GB   | 100 GB      |

### Apache Zeppelin

| **Componente**  | **Numero di nodi** | **CPU** | **RAM** | **Storage** |
| --------------- | ------------------ | ------- | ------- | ----------- |
| Apache Zeppelin | 1                  | 2 vCPU  | 8 GB    | 50 GB       |

### Jupyter Notebook

| **Componente**   | **Numero di nodi** | **CPU** | **RAM** | **Storage** |
| ---------------- | ------------------ | ------- | ------- | ----------- |
| Jupyter Notebook | 1                  | 2 vCPU  | 8 GB    | 50 GB       |
