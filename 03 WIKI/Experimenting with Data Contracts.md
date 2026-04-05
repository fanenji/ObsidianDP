---
title: Experimenting with Data Contracts
source: https://medium.com/data-mesh-learning/experimenting-with-data-contracts-9d36219e139e
author:
  - "[[Jean-Georges Perrin]]"
published: 2025-07-31
created: 2026-04-04
description: Experimenting with Data Contracts Are you among the curious who understand a data contract but fail to apprehend its power? Are you writing data contracts by hand, and would you like to proofread …
tags:
  - clippings
  - data-governance
  - data-contracts
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)## [Data Mesh Learning](https://medium.com/data-mesh-learning?source=post_page---publication_nav-47bae5dde70c-9d36219e139e---------------------------------------)

[![Data Mesh Learning](https://miro.medium.com/v2/resize:fill:76:76/1*xmJgQUIT7PkSqmmtodLylg.png)](https://medium.com/data-mesh-learning?source=post_page---post_publication_sidebar-47bae5dde70c-9d36219e139e---------------------------------------)

Your home for data mesh. Sharing best practices, concepts, and practical advice. Curated by the Data Mesh Learning community.

Are you among the curious who understand a data contract but fail to apprehend its power? Are you writing data contracts by hand, and would you like to proofread them easily? Search no more! Today, I am offering a free service to build, validate, and store your data contracts.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*bPxe9SRYKjf_ebtVueuk5w.png)

Let's experiment and learn with fun tools and services!

This tutorial is the first of a series of four, explaining how you can use and get value from Data Contracts & Data Products in a very hands-on way. Over ninety people participated in the early alpha and beta in May and June 2025, with testimonies such as the one from Muhammed Inzamam: *This tutorial masterfully demystifies data contracts, turning a complex concept into a few simple and practical \`curl\` commands. A fantastic, hands-on introduction!*

Check out [my list of data contracts & data products tutorials](https://medium.com/data-mesh-learning/so-you-want-to-work-with-data-contracts-and-data-products-03e86f099710) on Medium; you'll find the link to the other three tutorials and the surveys. The [associated GitHub repo](https://github.com/jgpai/cloud-services) contains extra information. When you finish the four tutorials and four surveys, you will receive a digital badge to show your recently acquired knowledge.

This tutorial does not explain what a data contract or product is, but focuses on experimenting with them. If you need to know more about data contracts, check:

- [Data Contract 101](https://medium.com/profitoptics/data-contract-101-568a9adbf9a9).
- [What Exactly is a Data Product?](https://medium.com/data-mesh-learning/what-exactly-is-a-data-product-7f6935a17912)
- [Defining Data Products: A Community Effort](https://medium.com/data-mesh-learning/defining-data-products-a-community-effort-77363611e5c5).

Today, I am introducing **several REST-based services to ease the management of data contracts and products.** All are free on the JGP.ai cloud (the free part might not last forever).

To perform those experiments, you will need *curl*, a text editor (*vi* is excellent), and, optionally, *jq*. The examples here use zsh on macOS, but they are basic enough to be easily transposed to any shell and command line. If you are using Windows, the command-line examples for this tutorial are [available in the repository](https://github.com/jgpai/cloud-services/blob/main/resources/tutorial1-process-cmd.md) (thanks to

[Alisdair Smyth](https://medium.com/u/4080c804bdb0?source=post_page---user_mention--9d36219e139e---------------------------------------)

).

## Contextualize first

Let's imagine you have a (very basic) customer table, which we can represent as:

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*Ah4xySWDcMRf7347ITGdOw.png)

Figure 1 — A very basic Customer entity relationship diagram (ERD).

If you don't like ERDs, here is some real code.

```rb
-- Table: Customer
CREATE TABLE Customer (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20)
);

-- Table: AddressType
CREATE TABLE AddressType (
    address_type_id SERIAL PRIMARY KEY,
    address_type VARCHAR(20) NOT NULL
);

-- Table: Address
CREATE TABLE Address (
    address_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    street1 VARCHAR(255) NOT NULL,
    street2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country_cd CHAR(2) NOT NULL,
    address_type_id INT,

    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
    CONSTRAINT fk_address_type FOREIGN KEY (address_type_id) REFERENCES AddressType(address_type_id)
);
```

Together, we will turn this into a data contract.

> To simplify, you can find the files I use in the associated repository on GitHub at [https://github.com/jgpdotai/cloud-services](https://github.com/jgpdotai/cloud-services).

## Setting up the playground

For simplicity, I will export all key values as environment variables, so it will be easier to copy/paste the curl calls (which can be tedious).

```rb
export BITOL_URL=https://cloud.jgp.ai/api
export BITOL_USER_PW=BitolRu7ez!
export BITOL_USER_EMAIL=jgp@jgp.net
```

Ok, you can use the same password if you want, but **do not use the same** **email**. A real email is needed. And there it goes, create your account.

```rb
curl -X POST "$BITOL_URL/v1/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'"$BITOL_USER_EMAIL"'",
    "password": "'"$BITOL_USER_PW"'",
    "firstName": "<<Your first name>>",
    "lastName": "<<Your last name>>",
    "company": "<<Your company>>",
    "dob": "<<your date of birth>>",
    "code": "Playground",
    "comment": "<<Something nice is always appreciated.>>"
}'
```

If you don't feel chatty, only the email & password are required. The service should reply something like:

```rb
{"email":"jgp@jgp.net",
"firstName":"Jean-Georges",
"lastName":"Perrin",
"company":"Bitol",
"dob":null,
"comment":"I love Building Data Products.",
"createdAt":"2025-04-25T15:50:29.650725", 
"updatedAt":"2025-04-25T15:50:29.650736",
"apiKey":"97d09209-9021-4b24-89a9-620aae063d40"}
```

The important part is the API key: *97d09209–9021–4b24–89a9–620aae063d40*, which I recommend exporting as well.

```rb
export BITOL_API_KEY=97d09209-9021-4b24-89a9-620aae063d40
```

At this stage, you should have received an email with instructions on how to validate your account. Do not forget to do it!

## Let's create our first contract!

If we want to build a data product, let’s start with our promise, or the data contract. I will use the basic example of a client and their addresses.

I will simply send the DDL of my database to the service, and it will create the embryo of the data contract for me.

```rb
cat resources/customer.sql | \
curl -X POST "$BITOL_URL/v1/contracts?sourceFormat=DDL&version=0.1.0&\
name=CustomerContract&domain=Customer&tenant=QuantumClimate" \
     -H "X-API-KEY: $BITOL_API_KEY" \
     -H "X-USER-PASSWORD: $BITOL_USER_PW" \
     -F "file=@-"
```

Let’s analyze the call:

- sourceFormat=DDL specifies that the format of the source the service is getting is the DDL.
- version=0.1.0 specifies a semantic version ([semver](https://semver.org/)) number. Non-semantic versioning is not supported.
- name=CustomerContract is the name of the contract.
- domain=Customer is the business domain associated with this contract.
- tenant= [QuantumClimate](https://learning.oreilly.com/library/view/implementing-data-mesh/9781098156213/ch03.html) a specific tenant (or brand, or business unit, or department… ).

The result should look like:

```rb
{
  "domain":"Customer",
  "name":"CustomerContract",
  "id":"34cae6d7-7648-38b2-8f66-8db79e1e2ce4",
  "version":"0.1.0",
  "tenant":"QuantumClimate",
  "status":"draft"
}
```

The contract's identifier is *34cae6d7–7648–38b2–8f66–8db79e1e2ce4,* and you should have the same one as the service is designed to be idempotent. Like the other elements, let’s export it to the environment:

```rb
export BITOL_CONTRACT_ID=34cae6d7-7648-38b2-8f66-8db79e1e2ce4
```

Now I can retrieve the contract:

```rb
curl -X GET "$BITOL_URL/v1/contracts/$BITOL_CONTRACT_ID" \
  -H "X-API-KEY: $BITOL_API_KEY" \
  -H "X-USER-PASSWORD: $BITOL_USER_PW"
```

Or, if I want it in a file:

```rb
curl -X GET "$BITOL_URL/v1/contracts/$BITOL_CONTRACT_ID" \
  -H "X-API-KEY: $BITOL_API_KEY" \
  -H "X-USER-PASSWORD: $BITOL_USER_PW" \
  --output $BITOL_CONTRACT_ID-0.1.0.odcs.yaml
```

If you look at the file, you should get something like:

```rb
apiVersion: "v3.0.2"
contractCreatedTs: "2025-05-09T21:34:58.759+00:00"
dataProduct: ""
description:
  usage: "DDL upload for contract generation"
  purpose: "Defines schema based on uploaded DDL"
  limitations: "None"
domain: "Customer"
id: "34cae6d7-7648-38b2-8f66-8db79e1e2ce4"
kind: "DataContract"
name: "CustomerContract"
schema:
- logicalType: "object"
  name: "Customer"
  physicalName: "Customer"
  physicalType: "table"
  properties:
  - logicalType: "number"
    name: "customer_id"
    physicalName: "customer_id"
    physicalType: "SERIAL"
    primaryKey: true
    required: true
...
status: "draft"
team:
- description: "Automatically generated"
  dateIn: "2025-05-09T21:34:58.760Z"
  email: "jgp@jgp.net"
  name: "Jean-Georges Perrin"
  role: "DPO"
  username: "jgp@jgp.net"
tenant: "QuantumClimate"
version: "v0.1.0"
```

You can now edit, enrich, and more, following the [Bitol ODCS specs](https://github.com/bitol-io/open-data-contract-standard). Once you're done, upload it to the service:

```rb
curl -X POST "$BITOL_URL/v1/contracts?version=0.1.1" \
  -H "X-API-KEY: $BITOL_API_KEY" \
  -H "X-USER-PASSWORD: $BITOL_USER_PW" \
  -F "file=@./$BITOL_CONTRACT_ID-0.1.0.odcs.yaml"
```

The data contract will be validated as you submit it. The semantic version you pass via the URL will be stored, regardless of the version in the YAML file.

If you have an issue, please submit it via [GitHub](https://github.com/jgpdotai/cloud-services/issues). Once you've completed this tutorial, go to the [main service page on GitHub](https://github.com/jgpdotai/cloud-services) to access the other tutorials, surveys, and reference material.

## More experimentations

Here are some ideas for more fun & experimentation.

### Extract real schemas

Turn this PostgreSQL database of yours into a data contract using the *pg\_dump* command, as in:

```rb
pg_dump --schema-only <database-name>
```

Pipe it to the *curl* command as we did just before with *cat*. And you can use similar commands with other databases like *dbschema* for Informix, *mysqldump -d* for MySQL, and many more.

Check the mapping between the implementation type (physicalType) and business type (logicalType)!

### Add documentation at the fields

The data contract is your source of truth for your meta data, so it should be very rich in term of description, business name, and more. Refer to the [Bitol ODCS specifications](https://github.com/bitol-io/open-data-contract-standard) for more details.

```rb
...
  - logicalType: "string"
    name: "phone"
    physicalName: "phone"
    physicalType: "VARCHAR (20)"
    description: "The phone number of the customer with the international prefix"
    businessName: "Customer phone number"
...
```

### Add SLAs and data quality rules

Follow the [Bitol ODCS specifications](https://github.com/bitol-io/open-data-contract-standard) to add service-level agreements.

Here is the retention period:

```rb
slaProperties:
  - property: retention
    value: 3
    unit: y
```

And here is a data quality rule on the *customer\_id* field:

```rb
...
  properties:
  - logicalType: "number"
    name: "customer_id"
    physicalName: "customer_id"
    physicalType: "SERIAL"
    primaryKey: true
    required: true
    quality:
    - type: sql 
      query: |
        SELECT COUNT(*) FROM ${object} WHERE ${property} IS NOT NULL
      mustBeLessThan: 100    
...
```

## Congratulations!

> 🎉 **And there you have it — your first taste of building real, open-standard Data Contracts!** 🎉

You’ve gone from a humble CREATE TABLE to a fully validated ODCS-aligned contract, hosted, versioned, and ready to serve your Data Product dreams: all in just a few curl calls. Not bad for a day’s play, right?

Whether you’re a seasoned architect or a data rebel searching for clarity, this playground is for *you*. So go ahead: tweak it, break it (gently), improve it, and share your experience. And who knows? You might unlock one of those mysterious *rewards of unestimated value*.

Jump in. Experiment. Learn. Have fun.

Updates:

- 2025–07–31 Published.

[![Data Mesh Learning](https://miro.medium.com/v2/resize:fill:96:96/1*xmJgQUIT7PkSqmmtodLylg.png)](https://medium.com/data-mesh-learning?source=post_page---post_publication_info--9d36219e139e---------------------------------------)

[![Data Mesh Learning](https://miro.medium.com/v2/resize:fill:128:128/1*xmJgQUIT7PkSqmmtodLylg.png)](https://medium.com/data-mesh-learning?source=post_page---post_publication_info--9d36219e139e---------------------------------------)

[Last published Aug 8, 2025](https://medium.com/data-mesh-learning/ddl-is-not-a-data-contract-1465e325821f?source=post_page---post_publication_info--9d36219e139e---------------------------------------)

Your home for data mesh. Sharing best practices, concepts, and practical advice. Curated by the Data Mesh Learning community.

[![Jean-Georges Perrin](https://miro.medium.com/v2/resize:fill:96:96/1*WVLhe7gm534XyyvS7ar6TA.jpeg)](https://medium.com/@jgperrin?source=post_page---post_author_info--9d36219e139e---------------------------------------)

[![Jean-Georges Perrin](https://miro.medium.com/v2/resize:fill:128:128/1*WVLhe7gm534XyyvS7ar6TA.jpeg)](https://medium.com/@jgperrin?source=post_page---post_author_info--9d36219e139e---------------------------------------)

[100 following](https://medium.com/@jgperrin/following?source=post_page---post_author_info--9d36219e139e---------------------------------------)

#Knowledge = 𝑓 ( ∑(#SmallData, #BigData), #DataScience U #AI, #Software ). Lifetime #IBMChampion. #KeepLearning. @ [http://jgp.ai](http://jgp.ai/)

## Responses (2)

S Parodi

What are your thoughts?  

```rb
It bothers me that this is basically a physical data model (DDL) with some extra tags. Most of the work is already done in the physical model and you could simply add tags to the DDL to add this extra info
```

1

```rb
This is easy to do in Collate. https://youtu.be/xtQ_7IOpW7c
```