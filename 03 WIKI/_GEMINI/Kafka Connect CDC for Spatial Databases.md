---
title: "Kafka Connect CDC for Spatial Databases"
type: conversation
topic: gis
created: 2026-02-13
tags:
  - kafka
  - cdc
  - spatial
---
**Source:** https://aistudio.google.com/u/1/prompts/1IF7q90fjRcHnxyKnibrIZOpdaWPpQYe8

## System Instructions

Optional tone and style instructions for the model

---

### User

how to setup a cdc with kafka connect from a oracle 11g spatial database and a postgres/postgis database

---

### Model

Setting Up Real-Time Geospatial Data Pipelines: A Guide to CDC with Kafka Connect for Oracle 11g Spatial and PostgreSQL/PostGIS

This guide provides a comprehensive approach to establishing a Change Data Capture (CDC) pipeline using Kafka Connect, capturing real-time data modifications from an Oracle 11g Spatial database and a PostgreSQL/PostGIS database. This allows for the creation of powerful, event-driven architectures fueled by geospatial data.

Key Considerations and Technologies

At the core of this setup is Apache Kafka Connect, a framework for reliably streaming data between Apache Kafka and other systems. For our specific databases, we will leverage two primary connectors:

Confluent Oracle CDC Source Connector: This connector is designed to capture changes from Oracle databases by reading the database's redo logs through Oracle LogMiner. It's important to note that Confluent has announced that support for Oracle Database 11g will reach its end-of-life on June 30, 2025.[1][2]

Debezium PostgreSQL Connector: A popular open-source connector, Debezium is well-suited for capturing row-level changes from PostgreSQL. It utilizes PostgreSQL's logical decoding feature, making it highly efficient.

A crucial aspect of this pipeline is the handling of spatial data types: SDO_GEOMETRY in Oracle and geometry in PostGIS. While the Debezium connector for PostgreSQL has explicit support for PostGIS data types, the handling of Oracle's SDO_GEOMETRY by the Confluent CDC connector requires more attention.

Setting up CDC from PostgreSQL/PostGIS with Debezium

The Debezium PostgreSQL connector offers robust support for PostGIS, making the setup relatively straightforward.

1. PostgreSQL Database Configuration:

Your PostgreSQL database must be configured to allow logical replication. This involves modifying the postgresql.conf file:

code
Ini
download
content_copy
expand_less
wal_level = logical

A server restart is required for this change to take effect. You will also need to create a dedicated user with replication privileges for the Debezium connector.

2. Debezium Connector for PostgreSQL Installation:

You will need to add the Debezium PostgreSQL connector to your Kafka Connect environment. This can be done by downloading the connector archive and placing it in the plugin.path of your Kafka Connect workers.

3. Connector Configuration:

When configuring the Debezium PostgreSQL connector, you will need to provide details about your database connection and specify the tables to be captured. A key aspect is the handling of PostGIS data.

PostGIS Data Handling: The Debezium connector for PostgreSQL automatically handles PostGIS data types.[3][4] It represents PostGIS geometry and geography types as a STRUCT in the Kafka message. This STRUCT contains two fields:

srid (INT32): The Spatial Reference System Identifier.

wkb (BYTES): The Well-Known Binary representation of the geometry.[3][4]

Here is a sample configuration snippet for the Debezium PostgreSQL connector:

code
JSON
download
content_copy
expand_less
{
  "name": "postgis-cdc-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "your-postgres-host",
    "database.port": "5432",
    "database.user": "your-replication-user",
    "database.password": "your-password",
    "database.dbname": "your-database",
    "database.server.name": "your-logical-server-name",
    "table.include.list": "public.your_spatial_table",
    "plugin.name": "pgoutput"
  }
}
Setting up CDC from Oracle 11g Spatial with Confluent Oracle CDC Connector

Capturing changes from Oracle 11g Spatial presents a few more challenges, primarily due to the lack of explicit documentation on SDO_GEOMETRY handling by the Confluent Oracle CDC connector.

1. Oracle Database 11g Configuration:

The Confluent Oracle CDC connector uses Oracle LogMiner to read the redo logs. Therefore, the database must be in ARCHIVELOG mode, and supplemental logging must be enabled. You will also need to create a database user with the necessary privileges for LogMiner and access to the tables being captured.[1]

2. Confluent Oracle CDC Source Connector Installation:

This is a premium connector and requires a Confluent subscription.[4] Once you have the connector, you'll install it in your Kafka Connect environment.

3. Connector Configuration and SDO_GEOMETRY Handling:

The configuration for the Oracle CDC connector will include connection details, the tables to monitor, and settings related to LogMiner.

The official documentation for the Confluent Oracle CDC connector mentions support for Large Object Types (LOBs).[2] SDO_GEOMETRY objects are often stored internally as a user-defined type that can contain LOBs. However, there is no explicit confirmation of how SDO_GEOMETRY is serialized into Kafka messages.

Possible Scenarios for SDO_GEOMETRY Representation:

Well-Known Text (WKT) or Well-Known Binary (WKB): Ideally, the connector would convert the SDO_GEOMETRY object to a standard format like WKT (a string) or WKB (a byte array).

Internal Oracle Format: The connector might serialize the raw internal representation of the SDO_GEOMETRY object, which would require custom deserialization logic in the consumer.

Unsupported: In the worst-case scenario, the SDO_GEOMETRY column might be ignored or cause errors during the CDC process.

A Practical Approach to Determine SDO_GEOMETRY Handling:

Given the lack of explicit documentation, a practical test is the best way to determine the behavior:

Set up a test environment: Create a simple table with an SDO_GEOMETRY column and insert some sample data.

Configure and run the Oracle CDC connector: Point the connector to your test table.

Inspect the Kafka topic: Use a Kafka consumer tool (like kafka-console-consumer) to inspect the raw messages produced in the topic for your test table. Analyze the format of the field corresponding to the SDO_GEOMETRY column.

Here is a sample configuration snippet for the Confluent Oracle CDC Source Connector:

code
JSON
download
content_copy
expand_less
{
  "name": "oracle-spatial-cdc-connector",
  "config": {
    "connector.class": "io.confluent.connect.oracle.cdc.OracleCdcSourceConnector",
    "tasks.max": "1",
    "oracle.server": "your-oracle-host",
    "oracle.port": "1521",
    "oracle.sid": "your-sid",
    "oracle.username": "your-cdc-user",
    "oracle.password": "your-password",
    "table.include.list": "YOUR_SCHEMA.YOUR_SPATIAL_TABLE",
    "start.from": "snapshot",
    "confluent.topic.bootstrap.servers": "your-kafka-brokers",
    "confluent.topic.replication.factor": "1"
  }
}
Building a Downstream Consumer

Once the data is flowing into Kafka, you'll need a consumer application to process the geospatial events. The implementation of the consumer will depend on how the spatial data is represented in the Kafka topics.

For PostGIS data: Your consumer will need to be able to deserialize the STRUCT containing the SRID and the WKB byte array. Libraries like JTS (Java Topology Suite) or its ports in other languages can be used to parse the WKB and work with the geometry.

For Oracle Spatial data:

If the data is in WKB or WKT format, you can use standard geospatial libraries for processing.

If the data is in a proprietary Oracle format, you may need to use Oracle's own client libraries or develop custom parsing logic to interpret the data.

Conclusion and Recommendations

Setting up a CDC pipeline with Kafka Connect for both Oracle 11g Spatial and PostgreSQL/PostGIS is a feasible but nuanced task.

For PostgreSQL/PostGIS, the path is clear and well-supported by the Debezium connector, which provides a standard representation for spatial data.

For Oracle 11g Spatial, the approach is more speculative due to the lack of explicit documentation on SDO_GEOMETRY handling. It is crucial to perform tests to understand the data format before building a production consumer.

Crucially, the impending end-of-life for Confluent's support for Oracle 11g is a major consideration. Any new development using this setup should be done with a clear migration plan to a newer version of Oracle or an alternative database.

By carefully configuring the connectors and implementing a robust consumer, you can successfully build a real-time data pipeline that unlocks the value of your changing geospatial data.

---
