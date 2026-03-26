---
title: "Nessie vs LakeKeeper"
type: conversation
topic: data-platform
created: 2026-02-13
tags:
  - nessie
  - iceberg
---
**Source:** https://aistudio.google.com/u/1/prompts/1byABnNb2e-UlgAoHW9tjnzwjrQCDm9ow

## System Instructions

Optional tone and style instructions for the model

---

### User

Can you give me a comparison between nessie and lakekeeper as iceberg catalog?
I plan to use them with dremio and a minio s3 object store.
Give me comparison table of the functionalities  of both and the pros and cons of each.
I'm interested in particular to the travel functionalities and to the git-like versioning and branching features.
Eventually compare both with a solution like lakefs.

---

### Model

Nessie vs. LakeKeeper: A Comparative Guide for Your Dremio and MinIO Lakehouse

Choosing the right Iceberg catalog is a critical decision for building a modern data lakehouse. For users of Dremio and MinIO S3 object storage, both Project Nessie and LakeKeeper emerge as powerful contenders, each with distinct strengths. While Nessie offers a Git-like experience for the entire catalog, enabling cross-table versioning and branching, LakeKeeper provides a high-performance, secure, and easy-to-use Iceberg REST catalog with a focus on robust governance.

This in-depth comparison will explore the functionalities, pros, and cons of both Nessie and LakeKeeper, with a special focus on their time travel and versioning capabilities. We will also draw a parallel to a solution like LakeFS to provide a broader context.

Functionality Showdown: Nessie vs. LakeKeeper
Feature	Project Nessie	LakeKeeper
Core Concept	A transactional catalog for data lakes that provides a Git-like experience for data.[1] It versions the entire catalog, not just individual tables.	A secure, fast, and user-friendly Apache Iceberg REST Catalog built with Rust.[2][3]
Versioning	Catalog-level versioning: Commits, branches, and tags apply to the entire catalog, enabling multi-table transactions and consistent point-in-time views across tables.[4][5]	Table-level versioning (via Iceberg REST API): Supports standard Iceberg time travel and snapshot management for individual tables.[3][6] Multi-table transactions are enabled through its relational database backend.[7]
Branching & Merging	Full Git-like semantics: Create branches to isolate development or data ingestion, experiment with changes, and merge them back into the main branch atomically across multiple tables.[5][7]	Implements the Iceberg REST API, which supports table-level branching and tagging.[8] This allows for isolated changes on a per-table basis.
Time Travel	Catalog-level time travel: Query the state of the entire catalog at a specific commit hash or timestamp, ensuring a consistent historical view across all tables.[5][7]	Table-level time travel: Query historical data of a specific table using a snapshot ID or a timestamp, as per the Iceberg specification.[9][10][11]
Architecture	Java-based service that manages metadata pointers to Iceberg table metadata files.[12]	A single binary executable written in Rust, with no JVM dependency. It uses a normalized relational database (like PostgreSQL) to store metadata.[2][6][7]
Integration	Seamlessly integrates with Dremio, Spark, Flink, Trino, and Hive.[12][13][14] There are established patterns for using Nessie with Dremio and MinIO.[13][14]	As a standard Iceberg REST Catalog, it is compatible with any engine that supports the REST API, including Dremio, Spark, Flink, and Trino.[6] It has documented support for S3-compatible storage like MinIO.[15]
Security & Governance	Provides its own access control features and allows for managing permissions on branches.[16]	Strong focus on security with integrations for OpenFGA and Open Policy Agent (OPA) for fine-grained access control.[17][18] It also supports vended credentials for secure access to storage.[6]
The Git-Like Experience: A Closer Look at Travel and Versioning

Your interest in time travel and Git-like versioning is where the philosophical differences between Nessie and LakeKeeper become most apparent.

Nessie's "Git for Data" Approach: Nessie extends the versioning concepts of Git to the entire data catalog. This means you can:

Create a branch of your entire data lakehouse with a single command. This is a metadata operation and does not duplicate the data, making it instantaneous and cost-effective.

Work in isolation on this branch, for example, to ingest and validate new data or run complex transformations across multiple tables without affecting the production environment.[5]

Perform atomic merges of your changes back to the main branch. This ensures that a set of changes across several tables either all succeed or all fail, maintaining data consistency.

Time travel the entire catalog to a previous state, which is invaluable for reproducibility of experiments, auditing, and recovering from errors that affect multiple tables.[5]

LakeKeeper's Iceberg-Native Approach: LakeKeeper, by implementing the Iceberg REST API, provides the powerful versioning features inherent to Apache Iceberg itself. This includes:

Snapshots: Every change to an Iceberg table creates a new snapshot, which is an immutable version of the table's metadata.[12]

Time Travel: You can query any historical snapshot of a table, allowing you to see the state of that specific table at any point in time.[9][10][11]

Branching and Tagging at the Table Level: Iceberg supports creating branches and tags on individual tables. This allows for isolated development and marking specific versions of a single table for releases or rollbacks.[8]

While LakeKeeper enables multi-table transactions through its database backend, the Git-like branching and merging workflow for the entire catalog is a hallmark feature of Nessie.

Pros and Cons for Your Dremio and MinIO Stack
Project Nessie

Pros:

Multi-table transactional consistency: The ability to branch and merge across the entire catalog is a significant advantage for complex data engineering workflows.[5]

Data-as-Code workflows: Enables Git-like development practices for data, improving collaboration, and allowing for CI/CD pipelines for data.

Zero-copy branching: Quickly create development and testing environments without duplicating large datasets on MinIO.[5]

Strong Dremio Integration: Nessie is well-integrated with Dremio, with native support in the Dremio UI for switching between branches.[13][14] Dremio's commercial offering, Dremio Arctic, is based on Nessie.[16]

Cons:

Learning Curve: Teams unfamiliar with Git concepts might face an initial learning curve.

Additional Service to Manage: Nessie runs as a separate service that needs to be deployed and maintained.

LakeKeeper

Pros:

High Performance and Efficiency: Being written in Rust, LakeKeeper offers a lightweight and fast alternative to JVM-based catalogs.[2][6]

Focus on Security and Governance: Advanced security features and integrations with modern authorization systems like OpenFGA provide robust data governance.[17][18]

Ease of Use: Distributed as a single binary, it is simple to deploy and manage.[6]

Standard Compliance: Adherence to the Iceberg REST API ensures broad compatibility with the Iceberg ecosystem.[3][6]

Cons:

Catalog-level versioning is not the primary focus: While supporting Iceberg's native versioning, it doesn't offer the same built-in, cross-catalog branching and merging experience as Nessie.

Newer Project: As a more recent project compared to Nessie, the community and ecosystem around it are still growing.

Comparison with LakeFS

LakeFS offers another powerful approach to data versioning, but it operates at a different layer of the data stack.

Aspect	Nessie & LakeKeeper	LakeFS
Versioning Layer	Metadata Layer: They version the pointers to the data files (the Iceberg metadata).	Storage Layer: It creates a Git-like repository on top of your S3-compatible object store (like MinIO) and versions the actual data files.[12]
Data Format Agnostic	Primarily focused on Apache Iceberg tables.[4]	Can version any type of data stored in your object storage, including Iceberg tables, Delta Lake tables, Parquet files, CSVs, images, etc.
Integration	Integrates with query engines as an Iceberg catalog.	Exposes an S3-compatible endpoint, so tools interact with it as if it were an S3 bucket.
Granularity	Versioning is tied to table or catalog commits.	Versioning is at the file level, tracking individual file additions, deletions, and modifications.[12]

In essence:

Choose Nessie if your primary goal is to bring Git-like workflows to your Iceberg tables at a catalog level, enabling multi-table transactions and seamless integration with Dremio's branching features.

Choose LakeKeeper if your priorities are a lightweight, high-performance, and highly secure Iceberg catalog with strong governance capabilities, and table-level versioning is sufficient for your needs.

Consider LakeFS if you need to version a broader range of data formats beyond Iceberg or if you prefer a versioning system that operates directly on the storage layer, independent of the table format's catalog.

For your specific use case with Dremio and MinIO, both Nessie and LakeKeeper are excellent choices. The decision will ultimately depend on whether the "Git for the entire catalog" paradigm of Nessie is a critical requirement for your data engineering and governance workflows, or if the performance, security, and simplicity of LakeKeeper with its robust Iceberg-native versioning capabilities better align with your operational priorities.

---

### User

Please expand the comparison with apache polaris

---

### Model

Excellent question. Adding Apache Polaris to the comparison provides a more complete picture of the modern Iceberg catalog landscape. Polaris, an open-source project initiated by Snowflake with contributions from the Dremio team, is designed to be a centralized, secure, and engine-agnostic catalog for Iceberg, making it a very relevant option for your Dremio and MinIO setup.

Here is an expanded comparison between Nessie, LakeKeeper, and the newly included Apache Polaris.

The Rise of the Open Lakehouse Catalog

For users of Dremio and MinIO, the choice of an Iceberg catalog is pivotal. It dictates not only how you manage metadata but also how you implement data governance and versioning. While Nessie offers a unique "Git-for-Data" experience across your entire lakehouse and LakeKeeper provides a high-performance, security-focused Rust-based alternative, Apache Polaris enters the scene with a strong emphasis on centralized governance and interoperability through the standard Iceberg REST API.

Functionality Showdown: Nessie vs. LakeKeeper vs. Apache Polaris
Feature	Project Nessie	LakeKeeper	Apache Polaris
Core Concept	A transactional catalog providing a Git-like experience. It versions the entire catalog, enabling cross-table consistency.	A secure, fast, and user-friendly Apache Iceberg REST Catalog built in Rust with a focus on strong governance.	An open-source, engine-agnostic metadata catalog purpose-built for Iceberg to centralize metadata management and governance.[1][2]
Versioning	Catalog-level: Commits, branches, and tags apply to the entire catalog, enabling multi-table transactions.	Table-level: Supports standard Iceberg time travel and snapshot management for individual tables via the REST API.	Table-level: Natively supports all of Iceberg's versioning capabilities, including snapshots and time travel for individual tables.[1][3] Catalog-level versioning is a planned future feature.[4]
Branching & Merging	Full Git-like semantics: Create, merge, and manage branches for the entire catalog, allowing for isolated development and atomic multi-table updates.	Implements table-level branching and tagging as supported by the Iceberg REST API for isolated changes on a per-table basis.	Supports standard table-level operations via the Iceberg REST API. Does not currently have multi-table, Git-like branching and merging, but it is on the project's roadmap.[4]
Time Travel	Catalog-level: Query the consistent state of the entire catalog at a specific commit or timestamp.	Table-level: Query historical data of a specific table using a snapshot ID or timestamp, as per the Iceberg specification.	Table-level: Enables querying historical versions of any single table, leveraging Iceberg's snapshot history.[1][5]
Architecture	Java-based service managing pointers to Iceberg metadata files.	A single binary executable written in Rust, with no JVM dependency. Uses a relational database for its own metadata.	A service that implements the Iceberg REST API and uses a database for its own metadata storage.[6] It is designed to be a centralized control plane.[7]
Integration	Seamless integration with Dremio, Spark, Flink, and others.[8][9] Dremio's commercial offering, Dremio Arctic, was originally based on Nessie.[10]	Standard Iceberg REST Catalog, compatible with any engine that supports the API, including Dremio. Works with S3-compatible storage like MinIO.	Built on the Iceberg REST API for broad interoperability with engines like Dremio, Spark, and Flink.[2][11][12] Can be used with MinIO.[13] Dremio's current enterprise catalog is being built on Polaris.[10][13]
Security & Governance	Provides its own access control features for managing permissions on branches.	Strong focus on security with integrations for OpenFGA and Open Policy Agent (OPA) for fine-grained access control.	A primary focus area. Implements a built-in Role-Based Access Control (RBAC) model to centrally manage access for principals (users, services) to catalogs, namespaces, and tables.[14][15][16]
The Git-Like Experience: A Deeper Dive

Your interest in time travel and Git-like versioning highlights the key philosophical differences between these catalogs.

Nessie's "Git for Data": This remains Nessie's standout feature. The ability to branch the entire catalog, work in isolation across dozens of tables, and then atomically merge the changes back is a powerful paradigm for complex data engineering, CI/CD for data, and guaranteed reproducibility.

LakeKeeper and Polaris's Iceberg-Native Approach: Both LakeKeeper and Polaris fully embrace the versioning capabilities built into Apache Iceberg. This includes powerful features like time travel, snapshot management, and schema evolution on a per-table basis. They provide the tools to manage the history of each table effectively.

The crucial distinction is that Nessie extends this versioning concept to the catalog level, while Polaris and LakeKeeper currently focus on providing a robust and governable implementation of Iceberg's table-level versioning. It's noteworthy that the Polaris roadmap includes adding catalog-level versioning, indicating a convergence of ideas in the community.[4]

Pros and Cons for Your Dremio and MinIO Stack
Project Nessie

Pros: Unmatched multi-table transactional consistency, enables "Data-as-Code" workflows, zero-copy branching is highly efficient.

Cons: The Git paradigm can have a learning curve; requires managing an additional service.

LakeKeeper

Pros: High performance and low overhead (written in Rust), strong focus on modern security integrations (OPA, OpenFGA), simple to deploy.

Cons: Lacks catalog-level branching and merging, newer project with a smaller but growing community.

Apache Polaris

Pros:

Centralized Governance: Its built-in RBAC model is a significant advantage for enterprises needing to enforce consistent security policies across multiple query engines.[14][15]

Strong Ecosystem Momentum: Backed by companies like Snowflake and Dremio, it has significant industry support and a clear development roadmap.[5][17]

Interoperability: As a compliant Iceberg REST API implementation, it's designed from the ground up to work with a wide array of tools.[11][12][16]

Future-Proof: Dremio is building its next-generation managed catalog on Polaris, ensuring deep and long-term integration.[10][13]

Cons:

No Catalog-Level Versioning (Yet): If you need true Git-like branching across your entire data lake today, Nessie is the only option among the three.

Still Maturing: While it has strong backing and recently reached a 1.0 release, it is still a relatively new project in the open-source world.[18]

Comparison with LakeFS

The comparison with LakeFS remains the same and provides important context. LakeFS operates at the storage layer, creating a Git-like repository over your MinIO buckets. This makes it format-agnostic (it can version Iceberg, Delta Lake, Parquet, CSVs, images, etc.) but means it is not an Iceberg catalog itself. Nessie, LakeKeeper, and Polaris are all metadata catalogs that are specifically designed for Apache Iceberg.

Conclusion: Which Catalog is Right for You?

The addition of Apache Polaris makes the decision more nuanced and dependent on your primary strategic goals.

Choose Project Nessie if... your most critical requirement is implementing Git-like workflows (branching, merging, commits) across your entire data lakehouse for multi-table transactions and data CI/CD pipelines.

Choose LakeKeeper if... your top priorities are deployment simplicity, a lightweight and high-performance architecture (non-JVM), and a need for cutting-edge, pluggable security frameworks like OPA.

Choose Apache Polaris if... your main objective is to establish a robust, centralized governance and security model for your Iceberg tables that is consistent across all your data tools. Its strong industry backing and deep integration with the future of Dremio's platform make it a compelling and forward-looking choice.

For your specific stack of Dremio and MinIO, Polaris emerges as a very strong contender. Its focus on centralized RBAC aligns perfectly with enterprise needs, and its adoption by Dremio as the foundation for their own catalog ensures first-class support and a seamless integration experience moving forward. While it doesn't offer Nessie's cross-table branching today, its roadmap suggests it may in the future, making it a safe and strategic bet for building a governed and interoperable data lakehouse.

---
