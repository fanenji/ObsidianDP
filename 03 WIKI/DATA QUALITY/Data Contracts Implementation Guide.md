---
title: "Data Contracts: Implementation Guide"
source: https://aicontext.substack.com/p/data-contracts-implementation-guide?utm_campaign=post&utm_medium=web
author:
  - "[[Jatin Solanki]]"
published: 2024-02-08
created: 2026-04-04
description: In this article, I will be talking about the concept of data contracts, their criticality and how it drives collaboration.
tags:
  - clippings
  - data-quality
  - data-contracts
topic:
type: note
---
### In this article, I will be talking about the concept of data contracts, their criticality and how it drives collaboration.

![man writing on paper](https://images.unsplash.com/photo-1450101499163-c8848c66ca85?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wzMDAzMzh8MHwxfHNlYXJjaHwxfHxhZ3JlZW1lbnR8ZW58MHx8fHwxNzA3Mzk2MDg2fDA&ixlib=rb-4.0.3&q=80&w=1080)

Photo by Scott Graham on Unsplash

> *I would like to thank [Andrew Jones](https://www.linkedin.com/in/andrewrhysjones/), creator of Data contracts concept and [how he has implemented at GoCardless](https://medium.com/gocardless-tech/data-contracts-at-gocardless-6-months-on-bbf24a37206e).*

A lot has been talked about data contracts since 2022, however the challenge is technical platform or capability but more around culture and how to drive the adoption.

Software Engineers or tech team have been practicing standardization CI/CD across many years; however, we have not seen that getting implemented within data teams at scale.

## What is Data Contract?

In simple terms, it is an agreement between Data producers and consumers on expected data values. If any event violates the contract the flow should break and raise notification to relevant stakeholders.

Data contracts define the structure, semantic layer, data quality checks along with metadata level restrictions if any.

**Here is sample YAML of Data contract:**

```markup
table_name: customer_bookings
version: 1.1
owner: jack_dawson
schema:
  - column_name: tx_date
    type: timestamp
    constraints:
      not_null: true
      no_future_dates: true
  - column_name: customer_email
    type: string
    constraints:
      not_null: true
      check_pii: true
  - column_name: sales_amt
    type: decimal
    constraints:
      not_negative: true
  - column_name: revenue_amt
    type: decimal
    constraints:
      not_negative: true
  - column_name: booking_type
    type: string
    constraints:
      enum: [air, hotel, train]
```

**Who owns the data contract?**

It’s usually owned by data engineers since they also are owner of data pipeline and quality of the information flowing to raw-layer.

The biggest question is how did we arrive at the stage of creating YAML on whose instruction data engineers are building this YAML or contracts.

This is where things get little tricky.

## Real-life scenario:

Ryan, a marketing analytics manager, was tasked with aiding his team in utilizing insights for business decision-making. As the company ventured into online business, new data sources like Google Analytics and Facebook Ads were integrated, requiring the creation of new data tables and a performance dashboard for strategy development.

Initially, Ryan coordinated with the data engineering team to incorporate these new sources into the company’s data warehouse. He detailed the required columns and business logic for custom fields, guiding the data engineering team in developing the necessary integration layer and custom logic.

Within a week, Ryan prepared scripts to aggregate data and set up SQL jobs for PowerBI publishing. However, on the tenth day, the marketing team, influenced by a perceived doubling in performance shown on the dashboard, altered their strategy. Four days later, discrepancies were noticed between Google Ads clicks and the dashboard figures, leading to the discovery of a pipeline script bug causing data duplication.

This incident highlighted the importance of data quality for Ryan. He quickly addressed the issue, ensuring that robust data quality measures were implemented across the product to prevent future errors.

## Setting the expectation:

Ryan will have detailed discussion with the Data team in laying down the data product expectation.

Some of the pointers he will ensure:

- **Schema checks**: All data types should be followed.
- **Data quality checks:** Duplicate checks, non-negative values for metrics like clicks, CTR, impression etc.
- **Freshness:** Table to be updated every 30 mins.
- **Masking critical data** — customer address and email should be masked. Check on email format being captured correctly.

Ryan wants to know about any changes in the data-assets which power the Online performance dashboard product.

Using the above information DE will write the YAML file and enforce it in CI/CD pipeline.

> *Data Contracts reduces the proximity between business and data teams.*

## How can we implement data contracts at scale?

It’s an uphill task and more dependent on cultural and process shift before going and achieving at scale.

For smaller teams, it is relatively easy to deploy changes and enforce critical processes. As a company grows, things get messier.

What we are about to discuss may not appeal to everyone, but we believe it’ is the most effective method to drive adoption and attain scale.

![](https://substackcdn.com/image/fetch/$s_!wlKJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa578af73-cc05-48cd-9264-24a9c082f719_1521x839.png)

1. **Deploy Data Discovery:** The initial step involves deploying data discovery tools to identify and catalog our data assets. This will enable us to understand our existing data landscape and prepare for structure governance.
2. **Create Domains & Assign Ownership:** Following the discovery phase, we will create specific data domains and assign ownership. This ensures accountability and clear stewardship for different data segments, which is crucial for maintaining data integrity.
3. **Adding Assets within Domains:** Once domains are established, we will proceed with adding assets to each domain. This process includes cataloging datasets and systems under their respective domain owners.
4. **Create Data Products**: With the assets in place, we will then create data products. These are curated datasets or analytical models designed to meet specific business requirements.
5. **Filter Assets to Meet Data Products Requirements**: It is essential to filter and select the appropriate assets that align with the requirements of our data products. This selection is guided by the relevance and quality of the data.
6. **Apply Validation, Schema, and Metadata Rules**: Our next move is to apply validation rules, define schema, and set metadata rules. This step is pivotal in ensuring the data meets our standards and is fit for purpose.
7. **Generate YAML File or Create One**: For each data product, we will generate a YAML file that encapsulates the data contract, which includes the schema, metadata, and validation rules.
8. **Enforce via GitHub**: Finally, the YAML files will be enforced through GitHub, allowing us to integrate data contract enforcement into our CI/CD pipeline. This ensures that any changes in data are automatically validated against the data contracts, maintaining the integrity and reliability of our data products.
	![](https://substackcdn.com/image/fetch/$s_!8Ilw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e0049b8-4e59-4393-8cb2-486093b6e6c4_700x431.png)

One of the most significant and vital responsibilities is to create a data domain and include appropriate data assets in it. People may get lethargic to link assets in a specific domain, which might slow down the complete process. There is not a straightforward or automated method for bringing all the relevant assets into a given domain.

## How do I enforce a Data Contract?

Well, it all depends upon CI/CD practices within an organization and how the data team leverages the Git-like platform.

Suppose you have a YAML file defining the schema of a user database in your project. This data contract specifies fields like `userID`, `name`, `email`, `creationDate`, and `isActive`, along with their data types and constraints.

**1\. Git Branching and Version Control**

- You have a `main` branch that represents the stable version of your data contract.
- Developers create feature branches (e.g., `feature/update-user-schema`) for any proposed changes to the data contract.

**2\. Code Reviews and Merge Requests**

- Developers submit a pull request (PR) or merge request (MR) to merge their changes into `main`.
- Team members review the changes in the PR to ensure they adhere to data standards and meet the project’s needs.

**3\. Continuous Integration (CI) Pipeline**

- When a PR is created, a CI pipeline is triggered.
- The CI pipeline performs several checks:
- YAML Linting: To ensure the file is syntactically correct and adheres to defined styling standards.
- Schema Validation: Using a tool like `yamale` or `jsonschema`, the pipeline validates the YAML file against the defined schema. This ensures the changes meet the structural and data type requirements.
- Unit Tests: Run any unit tests that verify the logic that depends on this data contract, ensuring the changes do not break existing functionalities.
- If any of these checks fail, the CI pipeline flags the PR as failing, and the developer is notified to make corrections.

**4\. Documentation and Change Log**

- The PR description should document what changes were made and why. This serves as a record for future reference.
- A change log is updated with details about the changes once the PR is merged.

**5\. Merging and Deployment**

- Once all CI checks pass and the PR is approved, it is merged into the `main` branch.
- The updated data contract in the `main` branch can then be deployed to your data systems or data catalog as needed.

**6\. Access Control and Security**

- Access to merge into the `main` branch is restricted to authorized personnel, such as lead data engineers or project maintainers.
- Sensitive data within the YAML file, if any, is handled according to security best practices.

## Things to consider:

1. Defining clear data producers, data consumers are super critical.
2. Platform or tech is just a channel to drive the process and the shift.
3. Processes need to be laid down on driving changes and even proposing new assets for a given data product.
4. Processes should be built to ensure maximum collaboration before rolling out new data product.
5. Data Product usually include detailed documentation which explains the process, sometimes glossary etc.
6. There is a possibility of including transformation code within the data product too.

## FAQ’s

1. **Can data consumers write data validation if the platform supports no-low code?** Data Consumers can propose validation rules, but data producers must agree and update the YAML.
2. **What is the difference between data contracts and data catalog (Discovery)?** Data Contracts is more about preventive measures and lets the users know during the code push about the impact on downstream assets.
3. **Who owns the data contract?** Ownership remains with data engineers.
4. **Can we buy data a contract platform?** [decube](http://decube.io/), [datakitchen](https://datakitchen.io/solutions/dataops-software-for-data-contracts/), [dremio](https://www.dremio.com/wiki/data-contract/), and open source [datacontract](http://datacontract.com/)
5. **Share some examples of data products?** Here is the list which can give you some flavor:
- Recommender systems.
- Profit and Loss Dashboard.
- Marketing Campaign Performance Dashboard.

Hope you liked the article, feel free to comment.

Article written by [Jatin Solanki](https://linkedin.com/in/jatinsolanki) | founder of [decube](https://www.decube.io/) (Data trust platform for GenAI era). We will soon be launching our data contracts module — stay tuned and expect our next updates in March this year.