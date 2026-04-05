---
title: Handling Sensitive Data in Your Data Platform
source: https://medium.com/@mariusz_kujawski/handling-sensitive-data-in-your-data-platform-ec3b1ccb45ca
author:
  - "[[Mariusz Kujawski]]"
published: 2025-11-25
created: 2026-04-04
description: Handling Sensitive Data in Your Data Platform In this post, I’ll walk through several techniques for handling sensitive data in a modern data platform. Working with sensitive information isn’t …
tags:
  - clippings
  - data-governance
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)

In this post, I’ll walk through several techniques for handling sensitive data in a modern data platform. Working with sensitive information isn’t just about anonymising or securing access from unauthorised users, it’s also about identification, governance, and ensuring full GDPR compliance.

When a data team starts to work on new ingestion processes and plans to onboard data sources containing PII, the first question should always be: **Do we actually need this sensitive information in the platform?**  
If the answer is *no*, don’t ingest it. It’s far easier to avoid collecting sensitive data than to manage protection and deletion later.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*cMygoDPPVZ0FLMpNx5dOiQ.png)

If you *do* need sensitive data in your data lake, warehouse, or lakehouse, ensure your technology stack supports GDPR-compliant data handling, particularly the ability to delete or modify PII when requested. Data formats and storage architecture matter here.

You may need to protect several categories of sensitive data, including:

- **Personally identifiable information (PII):** Social security numbers, driver’s licence numbers, passport numbers
- **Protected health information (PHI):** Medical records, patient histories, insurance details
- **Financial data:** Credit card numbers, bank accounts, transaction details
- **Intellectual property:** Trade secrets, patents, copyrighted materials
- **Confidential business information:** Strategic plans, customer lists, pricing information

A common best practice is **sensitive data isolation**, storing sensitive attributes in a separate layer within your data lake or even in a physically separated cloud storage account. This reduces the risk of accidental access.

## Data Identification

Data classification shouldn’t rest solely on the data engineering team. It requires joint processes and policies involving data owners and governance teams.

Many modern data governance tools support automated profiling to detect sensitive data and store the classification in a data catalogue. The drawback, of course, is licensing cost.

If you’re using Databricks, you can enable **Data Classification** on Unity Catalog to automatically detect sensitive fields.

Other detection options include:

- **Open-source frameworks**, such as Microsoft Presidio
- **Custom tools built using Generative AI**

## Data Processing Techniques

Once you’ve identified sensitive data, you can apply one or more of these techniques depending on downstream requirements:

**1\. Removal**

If there is no justifiable use case for a sensitive field, remove it.

**2\. Anonymisation**

Mask parts of a value or replace it entirely.  
Example: replacing characters with “\*” or “x”.

**3\. Pseudonymisation**

Replacing personal identifiers with artificial identifiers or pseudonyms.

**4\. Generalisation**

Reducing detail.  
Example: converting exact ages into age groups (e.g., 20–29).

**5\. Clear text storage**

Sometimes sensitive information must remain in clear text for analytics (e.g., employee salaries). In those cases, apply strict access controls.

## Masking

Masking is the simplest anonymisation technique. Databricks provides built-in functions to mask values during ingestion and ETL. Masking can be partial or full, depending on reporting needs.

```c
SELECT
  email,
  regexp_replace(email, '^[^@]+', '***') AS email_redacted,
  phone,
  regexp_replace(phone, '[0-9]', 'X') AS phone_redacted
FROM user

SELECT
  text,
  replace(text, 'Paris', 'CITY') AS text_anonymised
FROM sentences;

SELECT
  ssn,
  mask(ssn, 'X', '#', '*') AS ssn_mask_custom
FROM ids
```

## Tokenization

Tokenization is useful when you must store sensitive information but want to limit where it appears. The original value and token are stored in a secure, isolated layer. Other layers store only the token, not the sensitive value.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*0iDDmWQhu1N1LQy3eqotjw.png)

## Encryption

Encryption allows you to store data securely and decrypt it only when necessary. In Databricks, you can use `aes_encrypt` and store the encryption key in a Key Vault.

This is especially useful for fields like salaries, ensuring that even if someone gains physical access to files, they cannot read the values.

```c
> SELECT base64(aes_encrypt('Spark', 'abcdefghijklmnop'));
  4A5jOAh9FNGwoMeuJukfllrLdHEZxA2DyuSQAWz77dfn

> SELECT cast(aes_decrypt(unbase64('4A5jOAh9FNGwoMeuJukfllrLdHEZxA2DyuSQAWz77dfn'),
                          'abcdefghijklmnop') AS STRING);
  Spark
```

## Hashing

Hashing generates an irreversible hash value. It’s useful when you need consistency (the same input always produces the same hash) but don’t need to restore the original value.  
However, hashing carries the risk of re-identification through cross-reference with known hashed datasets.

```c
SELECT sha2('Spark', 256);
  529bc3b07127ecb7e53a4dcf1991d9152c24537d919178022b2c42657f79a26b

SELECT md5('Spark');
 8cde774d6f7333752ed72cacddb05126

SELECT hash('Spark', array(123), 2);
 -1321691492
```

## Sensitive Data Detection in Databricks

Databricks’ **Data Classification** can automatically scan your Unity Catalog to detect columns containing sensitive categories like names, emails, and credit card numbers.

Unity Catalog also supports **attribute-based access control (ABAC)**. You can tag sensitive columns and then create policies that apply masking or restrict access for specific groups.

![](https://miro.medium.com/v2/resize:fit:2000/format:webp/0*OLmDiZDPMNheyhI9)

## Final Thoughts

Dealing with sensitive data it’s not only a matter of technical implementation, but also procedures, architecture decisions, and the right approach to sensitive data. The goal is to build a platform where:  
\- Sensitive data is ingested only when justified  
\- Sensitive data are isolated  
\- Log access to data and changes in permissions to them  
\- Remember about flexibility in the case of new regulations