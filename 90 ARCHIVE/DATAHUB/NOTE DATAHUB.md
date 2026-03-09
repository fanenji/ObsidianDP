---
tags: ["integrating-with-dbt-test"]
---

# CONCEPTS

## **Assertions** (DATA QUALITY)

An assertion is **a data quality test that finds data that violates a specified rule.** Assertions serve as the building blocks of [Data Contracts](https://docs-website-t9sv4w3gr-acryldata.vercel.app/docs/managed-datahub/observe/data-contract) – this is how we verify the contract is met.

**3rd Party Runners**

You can integrate 3rd party tools as follows:

- [DBT Test](https://docs.datahub.com/docs/1.3.0/generated/ingestion/sources/dbtintegrating-with-dbt-test)
- [Great Expectations](https://docs.datahub.com/docs/1.3.0/metadata-ingestion/integration_docs/great-expectations)

If you opt for a 3rd party tool, it will be your responsibility to ensure the assertions are run based on the Data Contract spec stored in DataHub. With 3rd party runners, you can get the Assertion Change events by subscribing to our Kafka topic using the [DataHub Actions Framework](https://docs.datahub.com/docs/1.3.0/actions).

**Alerts**

Beyond the ability to see the results of the assertion checks (and history of the results) both on the physical asset’s page in the DataHub UI and as the result of DataHub API calls, you can also get notified via [Slack messages](https://docs.datahub.com/docs/1.3.0/managed-datahub/slack/saas-slack-setup) (DMs or to a team channel) based on your [subscription](https://youtu.be/VNNZpkjHG_I?t=79) to an assertion run event, or when an [incident](https://docs.datahub.com/docs/1.3.0/incidents/incidents)is raised or resolved.

## **Business Glossary**

When working in complex data ecosystems, it is very useful to organize data assets using a shared vocabulary. The Business Glossary feature in DataHub helps you do this, by providing a framework for defining a standardized set of data concepts and then associating them with the physical assets that exist within your data ecosystem.

A Business Glossary is comprised of two important primitives: Terms and Term Groups.

- **Terms**: words or phrases with a specific business definition assigned to them.
- **Term Groups**: act like folders, containing Terms and even other Term Groups to allow for a nested structure.

For Glossary Terms, you are also able to establish relationships between different Terms in the **Related Terms**tab. Here you can create Contains and Inherits relationships. Finally, you can view all of the entities that have been tagged with a Term in the **Related Entities** tab.

## **Data Contracts**

A Data Contract is **an agreement between a data asset's producer and consumer**, serving as a promise about the quality of the data. It often includes [assertions](https://docs-website-t9sv4w3gr-acryldata.vercel.app/docs/managed-datahub/observe/assertions) about the data’s schema, freshness, and data quality.

Some of the key characteristics of a Data Contract are:

- **Verifiable** : based on the actual physical data asset, not its metadata (e.g., schema checks, column-level data checks, and operational SLA-s but not documentation, ownership, and tags).
- **A set of assertions** : The actual checks against the physical asset to determine a contract’s status (schema, freshness, volume, custom, and column)
- **Producer oriented** : One contract per physical data asset, owned by the producer.

## Data Products

Data Products are an innovative way to organize and manage your Data Assets, such as Tables, Topics, Views, Pipelines, Charts, Dashboards, etc., within DataHub. These Data Products belong to a specific Domain and can be easily accessed by various teams or stakeholders within your organization.

Data Products are independent units of data managed by a specific domain team. They are responsible for defining, publishing, and maintaining their data assets while ensuring high-quality data that meets the needs of its consumers.

Data Products help in curating a coherent set of logical entities, simplifying data discovery and governance. By grouping related Data Assets into a Data Product, it allows stakeholders to discover and understand available data easily, supporting data governance efforts by managing and controlling access to Data Products

Data Products can be created using the UI or via a YAML file that is managed using software engineering (GitOps) practices

## **Domains**

DataHub supports grouping data assets into logical collections called **Domains**. Domains are curated, top-level folders or categories where related assets can be explicitly grouped. Management of Domains can be centralized, or distributed out to Domain owners Currently, an asset can belong to only one Domain at a time.

**All SQL-based ingestion sources support assigning domains during ingestion using the `domain` configuration.**

## Incidents

**Incidents** are a concept used to flag particular Data Assets as being in an unhealthy state. Each incident has an independent lifecycle and details including a state (active, resolved), a title, a description, & more.

A couple scenarios in which incidents can be useful are

1. **Communicating Assets with Ongoing Issues**: You can mark a known-bad data asset as under an ongoing incident so consumers and stakeholders can be informed about the health status of a data asset via the DataHub UI. Moreover, they can follow the incident as it progresses toward resolution.
2. **Pipeline Circuit Breaking (advanced):** You can use Incidents as a basis for orchestrating and blocking data pipelines that have inputs with active issues to avoid propagating bad data downstream.

## Lineage

Data lineage is a **map that shows how data flows through your organization.** It details where your data originates, how it travels, and where it ultimately ends up. This can happen within a single system (like data moving between Snowflake tables) or across various platforms.

With data lineage, you can

- Maintaining Data Integrity
- Simplify and Refine Complex Relationships
- Perform [Lineage Impact Analysis](https://docs-website-t9sv4w3gr-acryldata.vercel.app/docs/act-on-metadata/impact-analysis)
- [Propagate Metadata](https://blog.datahubproject.io/acryl-data-introduces-lineage-support-and-automated-propagation-of-governance-information-for-339c99536561) Across Lineage

## **Ownership**

Custom Ownership Types are an improvement on the way to establish ownership relationships between users and the data assets they manage within DataHub.

## **Tags**

Tags are informal, loosely controlled labels that help in search & discovery. They can be added to datasets, dataset schemas, or containers, for an easy way to label or categorize entities – without having to associate them to a broader business glossary or vocabulary.

Tags can help help you in:

- Querying: Tagging a dataset with a phrase that a co-worker can use to query the same dataset
- Mapping assets to a category or group of your choice

# INTEGRATIONS

[DATAHUB / DREMIO](./DATAHUB DREMIO.md)

[DATAHUB / DBT](./DATAHUB DBT.md)
