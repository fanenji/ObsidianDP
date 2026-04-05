---
title: "Data Engineering Cookbook"
type: note
topic: data-platform
created: 2026-04-04
tags:
  - data-engineering
  - cookbook
  - reference
source: https://github.com/andkret/Cookbook
---

## Table of Contents

- Introduction
- Basic Computer Science Skills
- Data Scientists and Machine Learning
- Advanced Data Engineering Skills
- Data Engineering Course: Building A Data Platform
- Case Studies
- Best Practices Cloud Platforms
- AWS
- Azure
- GCP
- 100 Plus Data Sources Data Science
- 1001 Data Engineering Interview Questions
- Recommended Books, Courses, and Podcasts
- Updates

---

Introduction
============

## Contents

- What is this Cookbook
- Data Engineers
- My Data Science Platform Blueprint
  - Connect
  - Buffer
  - Processing Framework
  - Store
  - Visualize
- Who Companies Need
- How to Learn Data Engineering
  - Andreas interview on the Super Data Science Podcast
  - Building Blocks to Learn Data Engineering
  - Roadmap for Beginners
  - Roadmap for Data Analysts
  - Roadmap for Data Scientists
  - Roadmap for Software Engineers
- Data Engineers Skills Matrix
- How to Become a Senior Data Engineer



## What is this Cookbook

I get asked a lot:
"What do you actually need to learn to become an awesome data engineer?"

Well, look no further. You'll find it here!

If you are looking for AI algorithms and such data scientist things,
this book is not for you.

**How to use this Cookbook:**
This book is intended to be a starting point for you. It is not a training! I want to help you to identify the topics to look into to become an awesome data engineer in the process.

It hinges on my Data Science Platform Blueprint. Check it out below. Once you understand it, you can find in the book tools that fit into each key area of a Data Science platform (Connect, Buffer, Processing Framework, Store, Visualize).

Select a few tools you are interested in, then research and work with them.

Don't learn everything in this book! Focus.

**What types of content are in this book?**
You are going to find five types of content in this book: Articles
I wrote, links to my podcast episodes (video & audio), more than 200
links to helpful websites I like, data engineering interview questions
and case studies.

**This book is a work in progress!**
As you can see, this book is not finished. I'm constantly adding new
stuff and doing videos for the topics. But, obviously, because I do this
as a hobby, my time is limited. You can help make this book even
better.

**Help make this book awesome!**
If you have some cool links or topics for the cookbook, please become a
contributor on GitHub: <https://github.com/andkret/Cookbook>. Fork the
repo, add them, and create a pull request. Or join the discussion by
opening Issues. Tell me your thoughts, what you value,
what you think should be included, or correct me where I am wrong.
You can also write me an email any time to
plumbersofdatascience\@gmail.com anytime.

**This Cookbook is and will always be free!**


## If You Like This Book & Need More Help:
Check out my Data Engineering Academy at LearnDataEngineering.com

**Visit learndataengineering.com:** [Click Here](https://learndataengineering.com)

- Huge Step by step Data Engineering Academy with over 30 courses
- Unlimited access incl. future courses during subsciption
- Access to all courses and example projects in the Academy
- Associate Data Engineer Certification
- Data Engineering on AWS E-Commerce example project
- Microsoft Azure example project
- Document Streaming example project with Docker, FastAPI, Apache Kafka, Apache Spark,
- MongoDB and Streamlit
- Time Series example project with InfluxDB and Grafana
- Lifetime access to the private Discord Workspace
- Course certificates
- Currently over 54 hours of videos


## Support This Book For Free!
- **Amazon:** [Click Here](https://www.amazon.com/shop/plumbersofdatascience) buy whatever you like from Amazon using this link* (Also check out my complete podcast gear and books)


## How To Contribute
If you have some cool links or topics for the cookbook, please become a contributor.

Simply pull the repo, add your ideas and create a pull request.
You can also open an issue and put your thoughts there.

Please use the "Issues" function for comments.



Data Engineers
-------------------------------


Data Engineers are the link between the management's data strategy
and the data scientists or analysts that need to work with data.

What they do is build the platforms that enable data scientists to do
their magic.

These platforms are usually used in five different ways:

-   Data ingestion and storage of large amounts of data.

-   Algorithm creation by data scientists.

-   Automation of the data scientist's machine learning models and
    algorithms for production use.

-   Data visualization for employees and customers.

-   Most of the time these guys start as traditional solution architects
    for systems that involve SQL databases, web servers, SAP
    installations and other "standard" systems.

But, to create big data platforms, the engineer needs to be an expert in
specifying, setting up, and maintaining big data technologies like:
Hadoop, Spark, HBase, Cassandra, MongoDB, Kafka, Redis, and more.

What they also need is experience on how to deploy systems on cloud
infrastructure like at Amazon or Google, or on-premise hardware.


| Podcast Episode: #048 From Wannabe Data Scientist To Engineer My Journey
|------------------|
|In this episode Kate Strachnyi interviews me for her humans of data science podcast. We talk about how I found out that I am more into the engineering part of data science.  
| [Watch on YouTube](https://youtu.be/pIZkTuN5AMM) \ [Listen on Anchor](https://anchor.fm/andreaskayy/episodes/048-From-Wannabe-Data-Scientist-To-Engineer-My-Journey-e45i2o)|


## My Data Science Platform Blueprint

I have created a simple and modular big data platform
blueprint. It is based on what I have seen in the field and
read in tech blogs all over the internet.

Why do I believe it will be super useful to you? Because, unlike other blueprints, it is not focused on technology.

Following my blueprint will allow you to create the big data platform
that fits exactly your needs. Building the perfect platform will allow
data scientists to discover new insights. It will enable you to perfectly handle big data and allow you to make
data-driven decisions.

The blueprint is focused on the five key areas: Connect, Buffer, Processing Frameworks, Store, and Visualize.

![Data Science Platform Blueprint](/images/Data-Science-Blueprint-New.jpg)

Having the platform split like this turns it into a modular platform with
loosely coupled interfaces.

Why is it so important to have a modular platform?

If you have a platform that is not modular, you end up with something
that is fixed or hard to modify. This means you can not adjust the
platform to changing requirements of the company.

Because of modularity, it is possible to specifically select tools for your use case. It also allows you to replace every component, if you need it.

Now, lets talk more about each key area.

### Connect

Ingestion is all about getting the data in from the source and making it
available to later stages. Sources can be everything from tweets to server
logs, to IoT sensor data (e.g. from cars).

Sources send data to your API Services. The API is going to push the
data into temporary storage.

The temporary storage allows other stages simple and fast access to
incoming data.

A great solution is to use messaging queue systems like Apache Kafka,
RabbitMQ or AWS Kinesis. Sometimes people also use caches for
specialised applications like Redis.

A good practice is that the temporary storage follows the
publish-subscribe pattern. This way APIs can publish messages and
Analytics can quickly consume them.

### Buffer

In the buffer phase you have pub/sub systems like Apache Kafka, Redis, or other Cloud tools like Google pub/sub or AWS Kinesis.

These systems are more or less message Queues.
You put something in on one side and take it out on the other.

The idea behind buffers is to have an intermediate system for the incoming data.

How this works is, for instance, you're getting data in from from an API.
The API is publishing into the message queue. Data is buffered there until it is picked up by the processing.

If you don't have a buffer, you can run into problems when writing directly into a store or you're processing the data directly. You can always have peaks of incoming data that stall the systems.

Like, it's lunch break and people are working with your app way more than usual.
There's more data coming in very very fast, faster than the analytics of the storage can handle.

In this case, you would run into problems, because the whole system would stall. It would therefore take long to process the data, and your customers would be annoyed.

With a buffer, you buffer the incoming data. Processes for storage and analytics can take out only as much data as they can process. You are no longer in danger of overpowering systems.

Buffers are also really good for building pipelines.

You take data out of Kafka, pre-process it, and put it back into Kafka.
Then, with another analytics process, you take the processed data back out and put it into a store.

Ta-da! A pipeline.

### Processing Framework

The analyse stage is where the actual analytics is done in
the form of stream and batch processing.

Streaming data is taken from ingest and fed into analytics. Streaming
analyses the "live" data, thus generating fast results.

As the central and most important stage, analytics also has access to
the big data storage. Because of that connection, analytics can take a
big chunk of data and analyse it.

This type of analysis is called batch processing. It will deliver you
answers for the big questions.

For a short video about batch and stream processing and their use cases, click on the link below:

[Adding Batch to a Streaming Pipeline](https://www.youtube.com/watch?v=o-aGi3FmdfU)

The analytics process, batch or streaming, is not a one-way process.
Analytics can also write data back to the big data storage.

Oftentimes, writing data back to the storage makes sense. It allows you
to combine previous analytics outputs with the raw data.

Analytics give insights when you combine
raw data. This combination will often allow you to create even more
useful insights.

A wide variety of analytics tools are available. Ranging from MapReduce
or AWS Elastic MapReduce to Apache Spark and AWS lambda.

### Store

This is the typical big-data storage where you just store everything. It
enables you to analyse the big picture.

Most of the data might seem useless for now, but it is of utmost
importance to keep it. Throwing data away is a big no-no.

Why not throw something away when it is useless?

Although it seems useless for now, data scientists can work with the
data. They might find new ways to analyse the data and generate valuable
insights from it.

What kind of systems can be used to store big data?

Systems like Hadoop HDFS, Hbase, Amazon S3 or DynamoDB are a perfect fit
to store big data.

Check out my podcast how to decide between SQL and NoSQL:
<https://anchor.fm/andreaskayy/embed/episodes/NoSQL-Vs-SQL-How-To-Choose-e12f1o>

### Visualize

Displaying data is as important as ingesting, storing, and analysing it.
Visualizations enable business users to make data-driven decisions.

This is why it is important to have a good visual presentation of the
data. Sometimes you have a lot of different use cases or projects using
the platform.

It might not be possible to build the perfect UI that fits
everyone's needs. What you should do in this case is enable others to build the
perfect UI themselves.

How to do that? By creating APIs to access the data and making them
available to developers.

Either way, UI or API, the trick is to give the display stage direct
access to the data in the big-data cluster. This kind of access will
allow the developers to use analytics results as well as raw data to
build the perfect application.


## Who Companies Need

For a company, it is important to have well-trained data engineers.

That's why companies are looking for people with experience of tools in every part of the above platform blueprint. One common theme I see is cloud platform experience on AWS, Azure or GCP.

## How to Learn Data Engineering

### Interview with Andreas on the Super Data Science Podcast

#### Summary

This interview with Andreas  on Jon Krohn's Super Data Science podcast delves into the intricacies of data engineering, highlighting its critical role in the broader data science ecosystem. Andreas, calling from Northern Bavaria, Germany, shares his journey from a data analyst to becoming a renowned data engineering educator through his Learn Data Engineering Academy. The conversation touches upon the foundational importance of data engineering in ensuring data quality, scalability, and accessibility for data scientists and analysts.

Andreas emphasizes that the best data engineers often have a background in the companies domain/niche, which equips them with a deep understanding of the end user's needs. The discussion also explores the essential tools and skills required in the field, such as relational databases, APIs, ETL tools, data streaming with Kafka, and the significance of learning platforms like AWS, Azure, and GCP. Andreas highlights the evolving landscape of data engineering, with a nod towards the emergence of roles like analytics engineers and the increasing importance of automation and advanced data processing tools like Snowflake, Databricks, and DBT.

The interview is not just a technical deep dive but also a personal journey of discovery and passion for data engineering, underscoring the perpetual learning and adaptation required in the fast-evolving field of data science.

| Watch or listen to this interview -> 657: How to Learn Data Engineering — with Andreas Kretz
|------------------|
| Was super fun talking with Jon about Data Engineering on the podcast. Think this will be very helpful for you :)
| [Watch on YouTube](https://youtu.be/sbDFADS-zo8) / [Listen to the Podcast](https://www.superdatascience.com/podcast/how-to-learn-data-engineering)|

#### Q&A Highlights

**Q: What is data engineering, and why is it important?** A: Data engineering is the foundation of the data science process, focusing on collecting, cleaning, and managing data to make it accessible and usable for data scientists and analysts. It's crucial for automating data processes, ensuring data quality, and enabling scalable data analysis and machine learning models.

**Q: How does one transition from data analysis to data engineering?**
A: The transition involves gaining a deep understanding of data pipelines, learning to work with various data processing and management tools, and developing skills in programming languages and technologies relevant to data engineering, such as SQL, Python, and cloud platforms like AWS or Azure.

**Q: What are the key skills and tools for a data engineer?**
A: Essential skills include proficiency in SQL, experience with ETL tools, knowledge of programming languages like Python, and familiarity with cloud services and data processing frameworks like Apache Spark. Tools like Kafka for data streaming and platforms like Snowflake and Databricks are also becoming increasingly important.

**Q: Can you elaborate on the emerging role of analytics engineers?**
A: Analytics engineers focus on bridging the gap between raw data management and data analysis, working closely with data warehouses and using tools like dbt to prepare and model data for easy analysis. This role is pivotal in making data more accessible and actionable for decision-making processes.

**Q: What advice would you give to someone aspiring to become a data engineer?**
A: Start by mastering the basics of SQL and Python, then explore and gain experience with various data engineering tools and technologies. It's also important to understand the data science lifecycle and how data engineering fits within it. Continuous learning and staying updated with industry trends are key to success in this field.

**Q: How does a data engineer's role evolve with experience?**
A: A data engineer's journey typically starts with focusing on specific tasks or segments of data pipelines, using a limited set of tools. As they gain experience, they broaden their skill set, manage entire data pipelines, and take on more complex projects. Senior data engineers often lead teams, design data architectures, and collaborate closely with data scientists and business stakeholders to drive data-driven decisions.

**Q: What distinguishes data engineering from machine learning engineering?**
A: While both fields overlap, especially in the use of data, data engineering focuses on the infrastructure and processes for handling data, ensuring its quality and accessibility. Machine learning engineering, on the other hand, centers on deploying and maintaining machine learning models in production environments. A strong data engineering foundation is essential for effective machine learning engineering.

**Q: Why might a data analyst transition to data engineering?**
A: Data analysts may transition to data engineering to work on more technical aspects of data handling, such as building and maintaining data pipelines, automating data processes, and ensuring data scalability. This transition allows them to have a more significant impact on the data lifecycle and contribute to more strategic data initiatives within an organization.

**Q: Can you share a challenging project you worked on as a data engineer?**
A: One challenging project involved creating a scalable data pipeline for real-time processing of machine-generated data. The complexity lay in handling vast volumes of data, ensuring its quality, and integrating various data sources while maintaining high performance. This project highlighted the importance of selecting the right tools and technologies, such as Kafka for data streaming and Apache Spark for data processing, to meet the project's demands.

**Q: How does the cloud influence data engineering?**
A: Cloud platforms like AWS, Azure, and GCP have transformed data engineering by providing scalable, flexible, and cost-effective solutions for data storage, processing, and analysis. They offer a wide range of services and tools that data engineers can leverage to build robust data pipelines and infrastructure, facilitating easier access to advanced data processing capabilities and enabling more innovative data solutions.

**Q: What future trends do you see in data engineering?**
A: Future trends in data engineering include the increasing adoption of cloud-native services, the rise of real-time data processing and analytics, greater emphasis on data governance and security, and the continued growth of machine learning and AI-driven data processes. Additionally, tools and platforms that simplify data engineering tasks and enable more accessible data integration and analysis will become more prevalent, democratizing data across organizations.

**Q: How does the background of a data analyst contribute to their success as a data engineer?**
A: Data analysts have a unique advantage when transitioning to data engineering due to their understanding of data's end-use. Their experience in analyzing data gives them insights into what makes data valuable and usable, enabling them to design more effective and user-centric data pipelines and storage solutions.

**Q: What role does automation play in data engineering?**
A: Automation is crucial in data engineering for scaling data processes, reducing manual errors, and ensuring consistency in data handling. Automated data pipelines allow for real-time data processing and integration, making data more readily available for analysis and decision-making.

**Q: Can you discuss the significance of cloud platforms in data engineering?**
A: Cloud platforms like AWS, Azure, and GCP offer scalable, flexible, and cost-effective solutions for data storage, processing, and analysis. They provide data engineers with a suite of tools and services to build robust data pipelines, implement machine learning models, and manage large volumes of data efficiently.

**Q: How does data engineering support data science and machine learning projects?**
A: Data engineering lays the groundwork for data science and machine learning by preparing and managing the data infrastructure. It ensures that high-quality, relevant data is available for model training and analysis, thereby enabling more accurate predictions and insights.

**Q: What emerging technologies or trends should data engineers be aware of?**
A: Data engineers should keep an eye on the rise of machine learning operations (MLOps) for integrating machine learning models into production, the growing importance of real-time data processing and analytics, and the adoption of serverless computing for more efficient resource management. Additionally, technologies like containerization (e.g., Docker) and orchestration (e.g., Kubernetes) are becoming critical for deploying and managing scalable data applications.

**Q: What challenges do data engineers face, and how can they be addressed?**
A: Data engineers often grapple with data quality issues, integrating disparate data sources, and scaling data infrastructure to meet growing data volumes. Addressing these challenges requires a solid understanding of data architecture principles, continuous monitoring and testing of data pipelines, and adopting best practices for data governance and management.

**Q: How important is collaboration between data engineers and other data professionals?**
A: Collaboration is key in the data ecosystem. Data engineers need to work closely with data scientists, analysts, and business stakeholders to ensure that data pipelines are aligned with business needs and analytical goals. Effective communication and a shared understanding of data objectives are vital for the success of data-driven projects.


### Building Blocks to Learn Data Engineering

The following Roadmaps all hinge on the courses in my Data Engineering Academy. They are designed to help students who come from many different professions and enable to build a customized curriculum.

Here are all the courses currently available February 2024:

**Colors:** Blue (The Basics), Green (Platform & Pipeline Fundamentals), Orange (Fundamental Tools), Red (Example Projects)

![Building blocks of your curriculum](/images/All-Courses-at-Learn-Data-Engineering.jpg)


### Roadmap for Beginners

Start this roadmap at my Academy: [Start Today](https://learndataengineering.com/p/data-engineering-for-beginners)

#### 11-Week Data Engineering Roadmap for Beginners & Graduates

#### Master the Fundamentals and Build Your First Data Pipelines

#### Starting in Data Engineering

Starting in data engineering can feel overwhelming, especially if you’re coming from a non-technical background or have only limited experience with coding and databases.

This 11-week roadmap, with a time commitment of 5–10 hours per week, is designed to help you build strong foundations in data engineering, step by step, before moving into cloud platforms and more advanced pipelines. You’ll learn essential concepts, hands-on coding, data modeling, and cloud ETL development—everything you need to kickstart your career as a data engineer.

---

#### Why This Roadmap is for You

- You’re just starting in data engineering and need a clear learning path
- You want to build a strong foundation in data platforms, SQL, and Python
- You need hands-on experience with data modeling, cloud ETL, and automation
- You want to work on real-world projects that prepare you for a data engineering job

By the end of this roadmap, you’ll have the skills, tools, and project experience to confidently apply for entry-level data engineering roles and start your career in the field.

![Building blocks of your curriculum](/images/Roadmap-For-Beginners.jpg)

---

#### What You’ll Achieve in This Roadmap

This roadmap is structured to help you understand the full data engineering workflow: from learning the fundamentals of data platforms and modeling to working with Python, SQL, and cloud-based ETL pipelines.

#### Learning Goals

| Goal        | Description                                         |
| ----------- | --------------------------------------------------- |
| **Goal #1** | Gain Experience in Data Platforms & Pipeline Design |
| **Goal #2** | Work with Data Like a Data Engineer Using Python & SQL |
| **Goal #3** | Learn Dimensional Data Modeling & Data Warehousing with Snowflake |
| **Goal #4** | Gain Experience with ELT Using dbt & Orchestration with Airflow |
| **Goal #5** | Build Your First ETL Pipeline on a Cloud Platform |

---

#### 11-Week Learning Roadmap

| Week            | Topic                                     | Key Learning Outcomes                                                           |
| --------------- | ----------------------------------------- | ------------------------------------------------------------------------------- |
| **Week 1**      | Introduction & Platform & Pipeline Design | Understand data platforms, data pipelines, and the tools used in data engineering  |
| **Week 2**      | Relational Data Modeling                  | Develop skills in creating relational data models for structured data           |
| **Week 3 & 4**  | Python for Data Engineers                 | Learn Python for data processing, data manipulation, and pipeline development    |
| **Week 5**      | Advanced SQL                              | Gain expertise in querying, storing, and manipulating data in relational databases |
| **Week 6**      | Dimensional Data Modeling                 | Master the techniques of dimensional modeling for analytics and reporting       |
| **Week 7**      | Snowflake Data Warehousing                | Learn how to use Snowflake as a cloud data warehouse                           |
| **Week 8**      | Data Transformation with dbt              | Transform and model data efficiently using dbt                                 |
| **Week 9**      | Data Pipeline Orchestration with Airflow  | Automate and manage data workflows using Apache Airflow                        |
| **Week 10 & 11**| End-to-End Project on AWS, Azure, or GCP  | Complete an end-to-end project on a cloud platform of your choice              |

---


#### Week 1: Introduction & Platform & Pipeline Design

##### 1. Learn the Basics of Platform & Pipeline Design

##### Data Platform and Pipeline Design

**Learn how to build data pipelines with templates and examples for Azure, GCP, and Hadoop**

##### Description

Data pipelines are the backbone of any Data Science platform. They are essential for data ingestion, processing, and machine learning workflows. This training will help you understand how to create stream and batch processing pipelines as well as machine learning pipelines by going through the most essential basics—complemented by templates and examples for useful cloud computing platforms.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/data-pipeline-design)

##### Detailed Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **Platform & Pipeline Basics**  | The Platform Blueprint | 10:11 |
| | Data Engineering Tools Guide | 2:44 |
| | End-to-End Pipeline Example | 6:18 |
| **Ingestion Pipelines** | Push Ingestion Pipelines | 3:42 |
| | Pull Ingestion Pipelines | 3:34 |
| **Pipeline Types** | Batch Pipelines | 3:07 |
| | Streaming Pipelines | 3:34 |
| **Visualization** | Stream Analytics | 2:26 |
| | Visualization Pipelines | 3:47 |
| | Visualization with Hive & Spark on Hadoop | 6:21 |
| | Visualization Data via Spark Thrift Server | 3:27 |
| **Platform Examples** | AWS, Azure, GCP (Currently Slides Only) | START |

---

##### 2. Get to Know the Different Data Stores

##### Choosing Data Stores

**Learn the different types of data storages and when to use which**

##### Description

One part of creating a data platform and pipelines is to choose data stores, which is the focus of this training. You will learn about relational databases, NoSQL databases, data warehouses, and data lakes. The goal is to help you understand when to use each type of data storage and how to incorporate them into your pipeline.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/choosing-data-stores)


##### Detailed Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| | What are Data Stores? | 2:09 |
| **Data Stores Basics** | OLTP vs OLAP | 7:34 |
| | ETL vs ELT | 5:45 |
| | Data Stores Ranking | 4:05 |
| **Relational Databases** | How to Choose Data Stores | 8:11 |
| | Relational Databases Concepts | 6:34 |
| **NoSQL Databases** | NoSQL Basics | 10:39 |
| | Document Stores | 5:56 |
| | Time Series Databases | 5:00 |
| | Search Engines | 4:18 |
| | Wide Column Stores | 4:22 |
| | Key Value Stores | 4:59 |
| | Graph Databases | 1:05 |
| **Data Warehouses & Data Lakes** | Data Warehouses | 5:32 |
| | Data Lakes | 7:10 |

---

#### 3. See Data Modeling Examples for the Learned Data Stores

##### Data Modeling 1

**Learn how to design schemas for SQL, NoSQL, and Data Warehouses**

##### Description

Schema design is a critical skill for data engineers. This training covers schema design for different data stores using an e-commerce dataset. You will see examples of how the same dataset is modeled for relational databases, NoSQL stores, wide column stores, document stores, key-value stores, and data warehouses. This will help you understand how to create maintainable models and avoid data swamps.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/data-modeling)

##### Detailed Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| | Why Data Modeling Is Important | 5:44 |
| | A Good Dataset | 1:28 |
| **Relational Databases** | Schema Design | 9:27 |
| **Wide Column Stores** | Schema Design | 7:35 |
| **Document Stores** | Schema Design | 7:28 |
| **Key Value Stores** | Schema Design | 4:49 |
| **Data Warehouses** | Schema Design | 4:44 |
| **Data Modeling Workshop** | November 2024 | 101:49 |

---


#### Week 2: Relational Data Modeling

##### Start with Relational Data Modeling

**Relational Data modeling** is an essential skill, as even in modern "big data" environments, relational databases are often used for managing and serving metadata. This week focuses on building a strong foundation in relational data modeling, which is crucial for structuring data effectively and optimizing query performance.

##### Relational Data Modeling

**Learn the most important basics to create a data model for OLTP data stores**

###### Description

This course covers everything you need to know about relational data modeling—from understanding entities, attributes, and relationships to normalizing data models up to the third normal form (3NF). You will learn how to design conceptual, logical, and physical data models, implement primary and foreign keys, and ensure data quality through constraints and validations. Practical exercises include setting up a MySQL server with Docker and creating ER diagrams using MySQL Workbench.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/relational-data-modeling)

##### Detailed Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **Basics and Prepare the Environment** | Relational Data Models History | 3:16 |
| | Installing MySQL Server and MySQL Workbench | 8:04 |
| | MySQL Workbench Introduction | 4:36 |
| **Create the Conceptual Data Model** | The Design Process Explained | 4:14 |
| | Discover the Entities | 10:24 |
| | Discover the Attributes | 13:09 |
| | Define Entity Relationships and Normalize the Data | 11:19 |
| **Defining and Resolving Relationships** | Identifying vs Non-Identifying Relationships | 2:01 |
| | How to Resolve Many-to-Many Relationships | 4:00 |
| | How to Resolve One-to-Many Relationships | 2:34 |
| | How to Resolve One-to-One Relationships | 1:45 |
| **Hands-On Workbench - Creating the Database** | Create Your ER Diagram Using Workbench | 19:46 |
| | Create a Physical Data Model | 4:13 |
| | Populate the MySQL DB with Data from .xls File | 15:13 |

---


#### Week 3 & 4: Python for Data Engineers

##### Description

This course offers a comprehensive guide to using Python for data engineering tasks. You’ll learn advanced Python features, including data processing with Pandas, working with APIs, interacting with PostgreSQL databases, and handling data types like JSON. The course also covers important programming concepts like exception handling, modules, unit testing, and object-oriented programming—all within the context of data engineering.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/python-for-data-engineers)

##### Detailed Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **Advanced Python** | Classes | 4:37 |
| | Modules | 3:06 |
| | Exception Handling | 8:55 |
| | Logging | 5:12 |
| **Data Engineering** | Datetime | 8:04 |
| | JSON | 9:54 |
| | JSON Validation | 15:10 |
| | UnitTesting | 16:44 |
| | Pandas: Intro & Data Types | 8:43 |
| | Pandas: Appending & Merging DataFrames | 7:49 |
| | Pandas: Normalizing & Lambdas | 4:12 |
| | Pandas: Pivot & Parquet Write, Read | 6:17 |
| | Pandas: Melting & JSON Normalization | 8:15 |
| | Numpy | 4:47 |
| **Working with Data Sources/Sinks** | Requests (Working with APIs) | 11:15 |
| | Working with Databases: Setup | 4:06 |
| | Working with Databases: Tables, Bulk Load, Queries | 8:12 |

---

#### Week 5: SQL for Data Engineers

##### Description

SQL is the backbone of working with relational databases, and if you’re getting into Data Engineering, mastering SQL is a must. This course provides the essential SQL skills needed to work with databases effectively. You'll learn how to manage data, build efficient queries, and perform advanced operations to handle real-world data challenges.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/sql-for-data-engineers)

##### Detailed Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **Basics** | Database Management Systems & SQL | 3:49 |
| | The Chinook Database | 3:03 |
| | SQLite Installation | 7:02 |
| | DBeaver Installation | 4:08 |
| | Data Types in SQLite | 6:15 |
| **Basic SQL** | DML & DDL | 15:06 |
| | Select Statements | 6:03 |
| | Grouping & Aggregation | 10:12 |
| | Joins | 10:05 |
| **Advanced SQL** | TCP Transaction Control Language | 6:42 |
| | Common Table Expressions & Subqueries | 10:26 |
| | Window Functions 1: Concept & Syntax | 5:00 |
| | Window Functions 2: Aggregate Functions | 7:24 |
| | Window Functions 3: Ranking Functions | 6:05 |
| | Window Functions 4: Analytical Functions | 7:20 |
| **Optimization** | Query Optimization | START |
| | Indexing Best Practices | START |


---

#### Week 6: Dimensional Data Modeling

##### Description

Dimensional data modeling is a crucial skill for data engineers working with analytics use-cases where data needs to be structured efficiently for reporting and business insights. This course covers the basics of dimensional modeling, the medallion architecture, and how to create data models for OLAP data stores.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/data-modeling-3-dimensional-data-modeling)

##### Detailed Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| | Data Warehousing Basics | 6:42 |
| **Dimensional Modeling Basics** | Approaches to building a data warehouse | 5:20 |
| | Dimension tables explained | 5:34 |
| | Fact tables explained | 6:34 |
| | Identifying dimensions | 3:16 |
| **Data Warehouse Setup** | What is DuckDB | 5:58 |
| | First DuckDB hands-on | 2:20 |
| | Creating tables in DuckDB | 2:40 |
| | Installing DBeaver | 6:49 |
| **Working With The Data Warehouse** | Exploring SCD0 and SCD1 | 19:57 |
| | Exploring SCD2 | 13:52 |
| | Exploring transaction fact table | 6:28 |
| | Exploring accumulating fact table | 7:17 |

---

#### Week 7: Snowflake for Data Engineers

##### Description

Snowflake is a highly popular cloud-based data warehouse that is ideal for beginners due to its simplicity and powerful features. In this course, you will learn how to set up Snowflake, load and process data, and create visualizations. The course covers both SQL and Python methods for managing data within Snowflake, and provides hands-on experience with connecting Snowflake to other tools such as PowerBI.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/snowflake-for-data-engineers)

##### Detailed Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **Introduction** | Snowflake basics | 4:16 |
| | Data Warehousing basics | 4:13 |
| | How Snowflake fits into data platforms | 3:14 |
| **Setup** | Snowflake Account setup | 4:24 |
| | Creating your warehouse & UI overview | 4:15 |
| **Loading CSVs from your PC** | Our dataset & goals | 3:01 |
| | Setup Snowflake database | 10:29 |
| | Preparing the upload file | 8:31 |
| | Using internal stages with SnowSQL | 12:37 |
| | Splitting a data table into two tables | 6:38 |
| **Visualizing Data** | Creating a visualization worksheet | 7:08 |
| | Creating a dashboard | 5:23 |
| | Connect PowerBI to Snowflake | 6:03 |
| | Query data with Python | 7:35 |
| **Automation** | Create import task | 9:18 |
| | Create table refresh task | 3:40 |
| | Test our pipeline | 3:14 |
| **AWS S3 Integration** | Working with external stages for AWS S3 | 10:20 |
| | Implementing snowpipe with S3 | 6:19 |

---

#### Week 8: dbt for Data Engineers

##### Description

This course introduces dbt (Data Build Tool), a SQL-first transformation workflow that allows you to transform, test, and document data directly within your data warehouse. You will learn how to set up dbt, connect it with Snowflake, create data pipelines, and implement advanced features like CI/CD and documentation generation. This training is ideal for data engineers looking to build trusted datasets for reporting, machine learning, and operational workflows.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/dbt-for-data-engineers)

##### Detailed Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **dbt Introduction & Setup** | Modern data experience | 5:42 |
| | Introduction to dbt | 4:38 |
| | Goals of this course | 4:50 |
| | Snowflake preparation | 7:29 |
| | Loading data into Snowflake | 4:48 |
| | Setup dbt Core | 9:35 |
| | Preparing the GitHub repository | 3:32 |
| **Working with dbt-Core** | dbt models & materialization explained | 6:16 |
| | Creating your first SQL model | 5:48 |
| | Working with custom schemas | 5:28 |
| | Creating your first Python model | 4:35 |
| | dbt sources | 1:55 |
| | Configuring sources | 4:03 |
| | Working with seed files | 4:20 |
| **Tests in dbt** | Generic tests | 3:19 |
| | Tests with Great Expectations | 3:25 |
| | Writing custom generic tests | 2:49 |
| **Working with dbt-Cloud** | dbt cloud setup | 7:25 |
| | Creating dbt jobs | 5:14 |
| | CI/CD automation with dbt cloud and GitHub | 10:52 |
| | Documentation in dbt | 7:38 |

---

#### Week 9: Apache Airflow Workflow Orchestration

##### Description

Airflow is a platform-independent workflow orchestration tool that offers many possibilities to create and monitor stream and batch pipeline processes. It supports complex, multi-stage processes across major platforms and tools in the data engineering world, such as AWS or Google Cloud. Airflow is not only great for planning and organizing your processes but also provides robust monitoring capabilities, allowing you to keep track of data workflows and troubleshoot effectively.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/learn-apache-airflow)

##### Detailed Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **Airflow Workflow Orchestration** | Airflow Usage | 3:19 |
| **Airflow Fundamental Concepts** | Fundamental Concepts | 2:47 |
| | Airflow Architecture | 3:09 |
| | Example Pipelines | 4:49 |
| | Spotlight 3rd Party Operators | 2:17 |
| | Airflow XComs | 4:32 |
| **Hands-On Setup** | Project Setup | 1:43 |
| | Docker Setup Explained | 2:06 |
| | Docker Compose & Starting Containers | 4:23 |
| | Checking Services | 1:48 |
| | Setup WeatherAPI | 1:33 |
| | Setup Postgres DB | 1:58 |
| **Learn Creating DAGs** | Airflow Webinterface | 4:37 |
| | Creating DAG With Airflow 2.0 | 9:46 |
| | Running our DAG | 4:15 |
| | Creating DAG With TaskflowAPI | 6:59 |
| | Getting Data From the API With SimpleHTTPOperator | 3:38 |
| | Writing into Postgres | 4:12 |
| | Parallel Processing | 4:15 |

---


#### Week 10 & 11: End-to-End Project on AWS, Azure, or GCP

##### Important: Choose One Project
Participants need to select **one** of the following cloud platforms to complete their end-to-end data engineering project. It is not necessary to complete all three projects.

##### AWS Project Introduction

The AWS project is designed for those who want to get started with cloud platforms, particularly with Amazon Web Services, the leading platform in data processing. This project will guide you through setting up an end-to-end data engineering pipeline using AWS tools like Lambda, API Gateway, Glue, Redshift, Kinesis, and DynamoDB. You will work with an e-commerce dataset, learn data modeling, and implement both stream and batch processing pipelines.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/data-engineering-on-aws)

##### Detailed AWS Project Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| | Data Engineering | 4:15 |
| | Data Science Platform | 5:20 |
| **The Dataset** | Data Types You Encounter | 3:03 |
| | What Is A Good Dataset | 2:54 |
| | The Dataset We Use | 3:16 |
| | Defining The Purpose | 6:27 |
| | Relational Storage Possibilities | 3:46 |
| | NoSQL Storage Possibilities | 6:28 |
| **Platform Design** | Selecting The Tools | 3:49 |
| | Client | 3:05 |
| | Connect | 1:18 |
| | Buffer | 1:28 |
| | Process | 2:42 |
| | Store | 3:41 |
| | Visualize | 3:00 |
| **Data Pipelines** | Data Ingestion Pipeline | 3:00 |
| | Stream To Raw Storage Pipeline | 2:19 |
| | Stream To DynamoDB Pipeline | 3:09 |
| | Visualization API Pipeline | 2:56 |
| | Visualization Redshift Data Warehouse Pipeline | 5:29 |
| | Batch Processing Pipeline | 3:19 |
| **AWS Basics** | Create An AWS Account | 1:58 |
| | Things To Keep In Mind | 2:45 |
| | IAM Identity & Access Management | 4:06 |
| | Logging | 2:22 |
| | AWS Python API Boto3 | 2:57 |
| **Data Ingestion Pipeline** | Development Environment | 4:02 |
| | Create Lambda for API | 2:33 |
| | Create API Gateway | 8:30 |
| | Setup Kinesis | 1:38 |
| | Setup IAM for API | 5:00 |
| | Create Ingestion Pipeline (Code) | 6:09 |
| | Create Script to Send Data | 5:46 |
| | Test The Pipeline | 4:53 |
| **Stream To Raw S3 Storage Pipeline** | Setup S3 Bucket | 3:42 |
| | Configure IAM For S3 | 3:21 |
| | Create Lambda For S3 Insert | 7:16 |
| | Test The Pipeline | 4:01 |
| **Stream To DynamoDB Pipeline** | Setup DynamoDB | 9:00 |
| | Setup IAM For DynamoDB Stream | 3:36 |
| | Create DynamoDB Lambda | 9:20 |
| **Visualization API** | Create API & Lambda For Access | 6:10 |
| | Test The API | 4:47 |
| **Visualization Pipeline Redshift Data Warehouse** | Setup Redshift Data Warehouse | 8:08 |
| | Security Group For Firehose | 3:12 |
| | Create Redshift Tables | 5:51 |
| | S3 Bucket & jsonpaths.json | 3:02 |
| | Configure Firehose | 7:58 |
| | Debug Redshift Streaming | 7:43 |
| | Bug-fixing | 5:58 |
| | Power BI | 12:16 |
| **Batch Processing Pipeline** | AWS Glue Basics | 5:14 |
| | Glue Crawlers | 13:09 |
| | Glue Jobs | 13:43 |
| | Redshift Insert & Debugging | 7:16 |

---


##### Azure Project Introduction

The Azure project is designed for those who want to build a streaming data pipeline using Microsoft Azure's robust cloud platform. This project introduces you to Azure services such as APIM, Blob Storage, Azure Functions, Cosmos DB, and Power BI. You will gain practical experience by building a pipeline that ingests, processes, stores, and visualizes data, using Python and Visual Studio Code.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/build-streaming-data-pipelines-in-azure)

##### Detailed Azure Project Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **Project Introduction** | Data Engineering in Azure - Streaming Data Pipelines | 2:43 |
| **Datasets and Local Preprocessing** | Introduction to Datasets and Local Preprocessing | 7:06 |
| | Deploying Code on Visual Studio to Docker Containers | 5:27 |
| **Azure Functions and Blob Storage** | Develop Azure Functions via Python and VS Code | 5:52 |
| | Deploy Azure Function to Azure Function App and Test It | 6:26 |
| | Integrate Azure Function with Blob Storage via Bindings | 4:58 |
| **Add Azure Function to Azure API Management (APIM)** | Expose Azure Function as a Backend | 7:05 |
| | Securely Store Secrets in Azure Key Vault | 4:41 |
| | Add Basic Authentication in API Management | 4:35 |
| | Test APIM and Imported Azure Function via Local Python Program | 2:34 |
| **Create and Combine Event Hubs, Azure Function, and Cosmos DB** | Create Event Hubs and Test Capture Events Feature | 6:59 |
| | Modify Existing Azure Function to Include Event Hubs Binding | 6:42 |
| **Write Tweets to Cosmos DB (Core SQL) from Event Hub** | Create a Cosmos DB (Core SQL) | 9:03 |
| | Create a New Azure Function that Writes Messages to Cosmos DB | 9:03 |
| **Connect Power BI Desktop to Your Cosmos DB** | Connect Power BI Desktop via Connector and Create a Dashboard | 6:32 |

---

##### GCP Project Introduction

The GCP project is designed for those who want to learn how to build, manage, and optimize data pipelines on Google Cloud Platform. This project focuses on building an end-to-end pipeline that extracts data from an external weather API, processes it through GCP's data tools, and visualizes the results using Looker Studio. This project offers practical, hands-on experience with tools like Cloud SQL, Compute Engine, Cloud Functions, Pub/Sub, and Looker Studio.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/data-engineering-on-gcp)

##### Detailed GCP Project Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **Introduction** | Introduction | 1:13 |
| | GitHub & the Team | 1:30 |
| **Data & Goals** | Architecture of the Project | 3:19 |
| | Introduction to Weather API | 2:18 |
| | Setup Google Cloud Account | 2:12 |
| **Project Setup** | Creating the Project | 2:35 |
| | Enabling the Required APIs | 1:34 |
| | Configure Scheduling | 2:20 |
| **Pipeline Creation - Extract from API** | Setup VM for Database Interaction | 2:53 |
| | Setup MySQL Database | 2:16 |
| | Setup VM Client and Create Database | 2:46 |
| | Creating Pub/Sub Message Queue | 1:41 |
| | Create Cloud Function to Pull Data from API | 4:17 |
| | Explanation of Code to Pull from API | 4:20 |
| **Pipeline Creation - Write to Database** | Create Function to Write to Database | 7:47 |
| | Explanation of Code to Write Data to Database | 5:56 |
| | Testing the Function | 5:51 |
| | Create Function Write Data to DB - Pull | 3:53 |
| | Explanation Code Write Data to DB - Pull | 4:33 |
| **Visualization** | Setup Looker Studio and Create Bubble Chart | 2:20 |
| | Setup Looker Studio and Create Time Series Chart | 1:57 |
| | Pipeline Monitoring | 6:20 |

---


##### What’s Next?

After completing this roadmap, you’ll have the confidence and skills to not just analyze data but to engineer and optimize it like a pro! Explore advanced topics, start contributing to projects, and showcase your new skills to potential employers.



### Roadmap for Data Analysts

Start this roadmap at my Academy: [Start Today](https://learndataengineering.com/p/data-engineering-for-data-analysts)

#### Go Beyond SQL and Learn How to Build, Automate, and Optimize Data Pipelines Like an Engineer

#### Who Is This 10 Week Roadmap For?

- Data Analysts who want to understand the full data lifecycle
- Those looking to move beyond SQL and build real data pipelines
- Professionals seeking hands-on, practical experience to boost their resumes
- Anyone wanting to stay competitive in the job market

#### What You’ll Achieve

This roadmap provides a step-by-step approach to mastering data engineering skills. You'll start with Python and data modeling, move on to building pipelines, work with cloud platforms, and finally automate workflows using industry-standard tools.


![Building blocks of your curriculum](/images/Roadmap-From-Data-Analyst-to-Engineer.jpg)

---

#### Learning Goals

| Goal        | Description                                         |
| ----------- | --------------------------------------------------- |
| **Goal #1** | Master Python & Relational Data Modeling            |
| **Goal #2** | Build Your First ETL Pipeline on AWS (or Azure/GCP) |
| **Goal #3** | Gain Hands-On Experience with Snowflake & dbt       |
| **Goal #4** | Connect AWS and Snowflake                           |
| **Goal #5** | Automate Your Data Pipeline with Airflow            |

---

#### 10-Week Learning Roadmap

| Week            | Topic                                     | Key Learning Outcomes                                                           |
| --------------- | ----------------------------------------- | ------------------------------------------------------------------------------- |
| **Week 1**      | Introduction to Data Engineering & Python | Understand core concepts of data engineering and Python programming basics      |
| **Week 2**      | Platform & Pipeline Design                | Learn how to design effective data platforms and pipelines                      |
| **Week 3**      | Relational Data Modeling                  | Develop skills in creating relational data models for structured data           |
| **Week 4**      | Dimensional Data Modeling                 | Master the techniques of dimensional modeling for analytics and reporting       |
| **Week 5**      | Docker Fundamentals & APIs                | Get hands-on with containerization using Docker and working with APIs           |
| **Week 8**      | Working with Snowflake                    | Gain practical experience using Snowflake as a data warehouse                   |
| **Week 9**      | Transforming Data With dbt                | Learn to transform and model data efficiently using dbt                         |
| **Week 10**     | Pipeline Orchestration with Airflow       | Automate and manage data workflows using Apache Airflow                         |

---

#### Detailed Weekly Content

#### Week 1: Introduction to Data Engineering & Python

If you want to take your data engineering skills to the next level, you are in the right place. Python has become the go-to language for data analysis and machine learning, and with our training, you will learn how to successfully use Python to build robust data pipelines and manipulate data efficiently.

This comprehensive training program is designed for data engineers of all levels. Whether you are just starting out in data engineering or you are an experienced engineer looking to expand your skill set, our Python for Data Engineers training will give you the tools you need to excel in your field.

At the end of the training, you will have a strong foundation in Python and data engineering and be ready to tackle complex data engineering projects with ease.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/python-for-data-engineers)

##### Course Curriculum

| Lesson | Duration |
|--------|----------|
| Classes | 4:37 |
| Modules | 3:06 |
| Exception Handling | 8:55 |
| Logging | 5:12 |
| Datetime | 8:04 |
| JSON | 9:54 |
| JSON Validation | 15:10 |
| UnitTesting | 16:44 |
| Pandas: Intro & data types | 8:43 |
| Pandas: Appending & Merging DataFrames | 7:49 |
| Pandas: Normalizing & Lambdas | 4:12 |
| Pandas: Pivot & Parquet write, read | 6:17 |
| Pandas: Melting & JSON normalization | 8:15 |
| Numpy | 4:47 |
| Requests (Working with APIs) | 11:15 |
| Working with Databases: Setup | 4:06 |
| Working with Databases: Tables, bulk load, queries | 8:12 |

---

#### Week 2: Platform & Pipeline Design

##### Description
Data pipelines are the number one thing within the Data Science platform. Without them, data ingestion or machine learning processing, for example, would not be possible.

This 110-minute long training will help you understand how to create stream and batch processing pipelines as well as machine learning pipelines by going through some of the most essential basics - complemented by templates and examples for useful cloud computing platforms.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/data-pipeline-design)

##### Course Curriculum

| Lesson | Duration |
|--------|----------|
| Platform Blueprint & End to End Pipeline Example | 10:11 |
| Data Engineering Tools Guide | 2:44 |
| End to End Pipeline Example | 6:18 |
| Push Ingestion Pipelines | 3:42 |
| Pull Ingestion Pipelines | 3:34 |
| Batch Pipelines | 3:07 |
| Streaming Pipelines | 3:34 |
| Stream Analytics | 2:26 |
| Lambda Architecture | 4:02 |
| Visualization Pipelines | 3:47 |
| Visualization with Hive & Spark on Hadoop | 6:21 |
| Visualization Data via Spark Thrift Server | 3:27 |

---


#### Week 3: Relational Data Modeling

##### Description
Relational modeling is often used for building transactional databases. You might say, 'But I'm not planning to become a back-end engineer'. Apart from knowing how to move data, you should also know how to store it effectively which involves designing a scalable data model optimized to drive faster query response time and efficiently retrieve data.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/relational-data-modeling)

##### Course Curriculum

| Lesson | Duration |
|--------|----------|
| Relational Data Models History | 3:16 |
| Installing MySQL Server and MySQL Workbench | 8:04 |
| MySQL Workbench Introduction | 4:36 |
| The Design Process Explained | 4:14 |
| Discover the Entities | 10:24 |
| Discover the Attributes | 13:09 |
| Define Entity Relationships and Normalize the Data | 11:19 |
| Identifying vs Non-identifying Relationships | 2:01 |
| Resolve Many-to-Many Relationships | 4:00 |
| Resolve One-to-Many Relationships | 2:34 |
| Resolve One-to-One Relationships | 1:45 |
| Create ER Diagram Using Workbench | 19:46 |
| Create a Physical Data Model | 4:13 |
| Populate MySQL DB with Data from .xls File | 15:13 |
| Course Conclusion | 1:28 |

---

#### Week 4: Dimensional Data Modeling

##### Description
In today’s data-driven world, efficient data organization is key to enabling insightful analysis and reporting. Dimensional data modeling is a crucial technique that helps structure your data for faster querying and better decision-making.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/data-modeling-3-dimensional-data-modeling)

##### Course Curriculum

| Lesson | Duration |
|--------|----------|
| Intro to Data Warehousing | 6:42 |
| Approaches to Building a Data Warehouse | 5:20 |
| Dimension Tables Explained | 5:34 |
| Fact Tables Explained | 6:34 |
| Identifying Dimensions | 3:16 |
| What is DuckDB | 5:58 |
| First DuckDB Hands-on | 2:20 |
| Creating Tables in DuckDB | 2:40 |
| Installing DBeaver | 6:49 |
| Exploring SCD0 and SCD1 | 19:57 |
| Exploring SCD2 | 13:52 |
| Exploring Transaction Fact Table | 6:28 |
| Exploring Accumulating Fact Table | 7:17 |
| Course Conclusion | 0:52 |

---

#### Week 5: Docker Fundamentals & APIs

##### Description
Week 5 covers two crucial topics: containerization using Docker and building APIs with FastAPI. Docker is essential for creating lightweight, self-sustained containers, while APIs are the backbone of data platforms.

Check out Docker Fundamentals in my Academy: [Learn More](https://learndataengineering.com/p/docker-fundamentals)

Check out Building APIs with FastAPI in my Academy: [Learn More](https://learndataengineering.com/p/apis-with-fastapi-course)

##### Course Curriculum

##### Docker Fundamentals

| Lesson | Duration |
|--------|----------|
| Docker vs Virtual Machines | 6:23 |
| Docker Terminology | 5:56 |
| Installing Docker Desktop | 4:09 |
| Pulling Images & Running Containers | 6:34 |
| Docker Compose | 6:34 |
| Build & Run Simple Image | 6:28 |
| Build Image with Dependencies | 5:05 |
| Using DockerHub Image Registry | 4:24 |
| Image Layers & Security Best Practices | 7:55 |
| Managing Docker with Portainer | 4:04 |

##### Building APIs with FastAPI

| Lesson | Duration |
|--------|----------|
| What are APIs? | 8:29 |
| Hosting vs Using APIs | 4:08 |
| HTTP Methods & Media Types | 6:56 |
| API Parameters & Response Codes | 9:40 |
| Setting up FastAPI | 4:55 |
| Creating APIs: POST, GET, PUT | 16:18 |
| Testing APIs with Postman | 4:22 |
| Deploying FastAPI with Docker | 6:01 |
| API Security Best Practices | 3:48 |

---


#### Week 6 & 7: End-to-End Project on AWS, Azure, or GCP

##### Important: Choose One Project
Participants need to select **one** of the following cloud platforms to complete their end-to-end data engineering project. It is not necessary to complete all three projects.

##### AWS Project Introduction

The AWS project is designed for those who want to get started with cloud platforms, particularly with Amazon Web Services, the leading platform in data processing. This project will guide you through setting up an end-to-end data engineering pipeline using AWS tools like Lambda, API Gateway, Glue, Redshift, Kinesis, and DynamoDB. You will work with an e-commerce dataset, learn data modeling, and implement both stream and batch processing pipelines.

Check out this project in my Academy: [Learn More](https://learndataengineering.com/p/data-engineering-on-aws)

##### Detailed AWS Project Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| | Data Engineering | 4:15 |
| | Data Science Platform | 5:20 |
| **The Dataset** | Data Types You Encounter | 3:03 |
| | What Is A Good Dataset | 2:54 |
| | The Dataset We Use | 3:16 |
| | Defining The Purpose | 6:27 |
| | Relational Storage Possibilities | 3:46 |
| | NoSQL Storage Possibilities | 6:28 |
| **Platform Design** | Selecting The Tools | 3:49 |
| | Client | 3:05 |
| | Connect | 1:18 |
| | Buffer | 1:28 |
| | Process | 2:42 |
| | Store | 3:41 |
| | Visualize | 3:00 |
| **Data Pipelines** | Data Ingestion Pipeline | 3:00 |
| | Stream To Raw Storage Pipeline | 2:19 |
| | Stream To DynamoDB Pipeline | 3:09 |
| | Visualization API Pipeline | 2:56 |
| | Visualization Redshift Data Warehouse Pipeline | 5:29 |
| | Batch Processing Pipeline | 3:19 |
| **AWS Basics** | Create An AWS Account | 1:58 |
| | Things To Keep In Mind | 2:45 |
| | IAM Identity & Access Management | 4:06 |
| | Logging | 2:22 |
| | AWS Python API Boto3 | 2:57 |
| **Data Ingestion Pipeline** | Development Environment | 4:02 |
| | Create Lambda for API | 2:33 |
| | Create API Gateway | 8:30 |
| | Setup Kinesis | 1:38 |
| | Setup IAM for API | 5:00 |
| | Create Ingestion Pipeline (Code) | 6:09 |
| | Create Script to Send Data | 5:46 |
| | Test The Pipeline | 4:53 |
| **Stream To Raw S3 Storage Pipeline** | Setup S3 Bucket | 3:42 |
| | Configure IAM For S3 | 3:21 |
| | Create Lambda For S3 Insert | 7:16 |
| | Test The Pipeline | 4:01 |
| **Stream To DynamoDB Pipeline** | Setup DynamoDB | 9:00 |
| | Setup IAM For DynamoDB Stream | 3:36 |
| | Create DynamoDB Lambda | 9:20 |
| **Visualization API** | Create API & Lambda For Access | 6:10 |
| | Test The API | 4:47 |
| **Visualization Pipeline Redshift Data Warehouse** | Setup Redshift Data Warehouse | 8:08 |
| | Security Group For Firehose | 3:12 |
| | Create Redshift Tables | 5:51 |
| | S3 Bucket & jsonpaths.json | 3:02 |
| | Configure Firehose | 7:58 |
| | Debug Redshift Streaming | 7:43 |
| | Bug-fixing | 5:58 |
| | Power BI | 12:16 |
| **Batch Processing Pipeline** | AWS Glue Basics | 5:14 |
| | Glue Crawlers | 13:09 |
| | Glue Jobs | 13:43 |
| | Redshift Insert & Debugging | 7:16 |

---


##### Azure Project Introduction

The Azure project is designed for those who want to build a streaming data pipeline using Microsoft Azure's robust cloud platform. This project introduces you to Azure services such as APIM, Blob Storage, Azure Functions, Cosmos DB, and Power BI. You will gain practical experience by building a pipeline that ingests, processes, stores, and visualizes data, using Python and Visual Studio Code.

Check out this project in my Academy: [Learn More](https://learndataengineering.com/p/build-streaming-data-pipelines-in-azure)

##### Detailed Azure Project Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **Project Introduction** | Data Engineering in Azure - Streaming Data Pipelines | 2:43 |
| **Datasets and Local Preprocessing** | Introduction to Datasets and Local Preprocessing | 7:06 |
| | Deploying Code on Visual Studio to Docker Containers | 5:27 |
| **Azure Functions and Blob Storage** | Develop Azure Functions via Python and VS Code | 5:52 |
| | Deploy Azure Function to Azure Function App and Test It | 6:26 |
| | Integrate Azure Function with Blob Storage via Bindings | 4:58 |
| **Add Azure Function to Azure API Management (APIM)** | Expose Azure Function as a Backend | 7:05 |
| | Securely Store Secrets in Azure Key Vault | 4:41 |
| | Add Basic Authentication in API Management | 4:35 |
| | Test APIM and Imported Azure Function via Local Python Program | 2:34 |
| **Create and Combine Event Hubs, Azure Function, and Cosmos DB** | Create Event Hubs and Test Capture Events Feature | 6:59 |
| | Modify Existing Azure Function to Include Event Hubs Binding | 6:42 |
| **Write Tweets to Cosmos DB (Core SQL) from Event Hub** | Create a Cosmos DB (Core SQL) | 9:03 |
| | Create a New Azure Function that Writes Messages to Cosmos DB | 9:03 |
| **Connect Power BI Desktop to Your Cosmos DB** | Connect Power BI Desktop via Connector and Create a Dashboard | 6:32 |

---

##### GCP Project Introduction

The GCP project is designed for those who want to learn how to build, manage, and optimize data pipelines on Google Cloud Platform. This project focuses on building an end-to-end pipeline that extracts data from an external weather API, processes it through GCP's data tools, and visualizes the results using Looker Studio. This project offers practical, hands-on experience with tools like Cloud SQL, Compute Engine, Cloud Functions, Pub/Sub, and Looker Studio.

Check out this project in my Academy: [Learn More](https://learndataengineering.com/p/data-engineering-on-gcp)

##### Detailed GCP Project Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **Introduction** | Introduction | 1:13 |
| | GitHub & the Team | 1:30 |
| **Data & Goals** | Architecture of the Project | 3:19 |
| | Introduction to Weather API | 2:18 |
| | Setup Google Cloud Account | 2:12 |
| **Project Setup** | Creating the Project | 2:35 |
| | Enabling the Required APIs | 1:34 |
| | Configure Scheduling | 2:20 |
| **Pipeline Creation - Extract from API** | Setup VM for Database Interaction | 2:53 |
| | Setup MySQL Database | 2:16 |
| | Setup VM Client and Create Database | 2:46 |
| | Creating Pub/Sub Message Queue | 1:41 |
| | Create Cloud Function to Pull Data from API | 4:17 |
| | Explanation of Code to Pull from API | 4:20 |
| **Pipeline Creation - Write to Database** | Create Function to Write to Database | 7:47 |
| | Explanation of Code to Write Data to Database | 5:56 |
| | Testing the Function | 5:51 |
| | Create Function Write Data to DB - Pull | 3:53 |
| | Explanation Code Write Data to DB - Pull | 4:33 |
| **Visualization** | Setup Looker Studio and Create Bubble Chart | 2:20 |
| | Setup Looker Studio and Create Time Series Chart | 1:57 |
| | Pipeline Monitoring | 6:20 |

---


#### Week 8: Working with Snowflake

##### Description

Currently, Snowflake is the analytics store/data warehouse everybody is talking about. It is a 100% cloud-based platform that offers many advantages, including flexible data access and the ability to scale services as needed. Snowflake is widely used in the industry, and learning it will enhance your data engineering skill set.

This training covers everything from the basics of Snowflake and data warehousing to advanced integration and automation techniques. By the end, you will have the knowledge to prepare, integrate, manage data on Snowflake, and connect other systems to the platform.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/snowflake-for-data-engineers)

##### Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| | Snowflake Basics | 4:16 |
| | Data Warehousing Basics | 4:13 |
| | How Snowflake Fits into Data Platforms | 3:14 |
| **Setup** | Snowflake Account Setup | 4:24 |
| | Creating Your Warehouse & UI Overview | 4:15 |
| **Loading CSVs from Your PC** | Our Dataset & Goals | 3:01 |
| | Setup Snowflake Database | 10:29 |
| | Preparing the Upload File | 8:31 |
| | Using Internal Stages with SnowSQL | 12:37 |
| | Splitting a Data Table into Two Tables | 6:38 |
| **Visualizing Data** | Creating a Visualization Worksheet | 7:08 |
| | Creating a Dashboard | 5:23 |
| | Connect PowerBI to Snowflake | 6:03 |
| | Query Data with Python | 7:35 |
| **Automation** | Create Import Task | 9:18 |
| | Create Table Refresh Task | 3:40 |
| | Test Our Pipeline | 3:14 |
| **AWS S3 Integration** | Working with External Stages for AWS S3 | 10:20 |
| | Implementing Snowpipe with S3 | 6:19 |

---

#### Week 9: Transforming Data With dbt

##### Description

dbt is a SQL-first transformation workflow that simplifies the process of transforming, testing, and documenting data. It allows teams to work directly within the data warehouse, creating trusted datasets for reporting, machine learning, and operational workflows. This training is the perfect starting point to get hands-on experience with dbt Core, dbt Cloud, and Snowflake.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/dbt-for-data-engineers)

##### Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **dbt Introduction & Setup** | Modern Data Experience | 5:42 |
| | Introduction to dbt | 4:38 |
| | Goals of this Course | 4:50 |
| | Snowflake Preparation | 7:29 |
| | Loading Data into Snowflake | 4:48 |
| | Setup dbt Core | 9:35 |
| | Preparing the GitHub Repository | 3:32 |
| **Working with dbt-Core** | dbt Models & Materialization Explained | 6:16 |
| | Creating Your First SQL Model | 5:48 |
| | Working with Custom Schemas | 5:28 |
| | Creating Your First Python Model | 4:35 |
| | dbt Sources | 1:55 |
| | Configuring Sources | 4:03 |
| | Working with Seed Files | 4:20 |
| **Tests in dbt** | Generic Tests | 3:19 |
| | Tests with Great Expectations | 3:25 |
| | Writing Custom Generic Tests | 2:49 |
| **Working with dbt-Cloud** | dbt Cloud Setup | 7:25 |
| | Creating dbt Jobs | 5:14 |
| | CI/CD Automation with dbt Cloud and GitHub | 10:52 |
| | Documentation in dbt | 7:38 |

---

#### Week 10: Pipeline Orchestration with Airflow

##### Description

Apache Airflow is a powerful, platform-independent workflow orchestration tool widely used in the data engineering world. It allows you to create and monitor both stream and batch pipeline processes with ease. Airflow supports integration with major platforms and tools such as AWS, Google Cloud, and many more.

Airflow not only helps in planning and organizing workflows but also offers robust monitoring features, allowing you to troubleshoot and maintain complex ETL pipelines effectively. As one of the most popular tools for workflow orchestration, mastering Airflow is highly valuable for data engineers.

Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/learn-apache-airflow)

##### Course Curriculum

| Module | Lesson | Duration |
|--------|--------|----------|
| **Airflow Workflow Orchestration** | Airflow Usage | 3:19 |
| **Airflow Fundamental Concepts** | Fundamental Concepts | 2:47 |
| | Airflow Architecture | 3:09 |
| | Example Pipelines | 4:49 |
| | Spotlight 3rd Party Operators | 2:17 |
| | Airflow XComs | 4:32 |
| **Hands-On Setup** | Project Setup | 1:43 |
| | Docker Setup Explained | 2:06 |
| | Docker Compose & Starting Containers | 4:23 |
| | Checking Services | 1:48 |
| | Setup WeatherAPI | 1:33 |
| | Setup Postgres DB | 1:58 |
| **Learn Creating DAGs** | Airflow Webinterface | 4:37 |
| | Creating DAG With Airflow 2.0 | 9:46 |
| | Running our DAG | 4:15 |
| | Creating DAG With TaskflowAPI | 6:59 |
| | Getting Data From the API With SimpleHTTPOperator | 3:38 |
| | Writing into Postgres | 4:12 |
| | Parallel Processing | 4:15 |
| **Recap** | Recap & Outlook | 4:38 |

---

#### What’s Next?

After completing this roadmap, you’ll have the confidence and skills to not just analyze data but to engineer and optimize it like a pro! Explore advanced topics, start contributing to projects, and showcase your new skills to potential employers.



### Roadmap for Data Scientists

#### 14-Week Data Engineering Roadmap for Data Scientists

#### From Notebooks to Production: Build, Deploy, and Scale Your ML Workflows

#### Start this roadmap at my Academy: [Start Today](https://learndataengineering.com/p/data-engineering-for-data-scientists)

---

#### Who Is This Roadmap For?

- Data Scientists who want to deploy and maintain ML models in production
- ML practitioners struggling with real-time data, CI/CD, and orchestration
- Data professionals looking to expand their engineering toolkit
- Anyone ready to go beyond notebooks and automate their ML workflows

---

#### What You’ll Achieve

This roadmap provides a step-by-step approach to gaining production-grade data engineering skills. You'll start with pipelines and containerization, move on to deployment and orchestration, and finish with big data and monitoring.

![Building blocks of your curriculum](/images/Roadmap-Data-Engineering-For-Data-Scientists.jpg)

#### Learning Goals

| Goal #  | Description                                        |
| ------- | -------------------------------------------------- |
| Goal #1 | Build an End-to-End ML Pipeline on AWS             |
| Goal #2 | Add CI/CD & Containerization to Your Platform      |
| Goal #3 | Implement the Lakehouse Architecture in AWS or GCP |
| Goal #4 | Orchestrate Your Pipelines with Airflow            |
| Goal #5 | Process Big Data with Apache Spark & Streaming     |
| Goal #6 | Analyze Your ML Training Logs with Elasticsearch   |

---

#### 14-Week Learning Roadmap

| Week       | Topic                                        |
| ---------- | -------------------------------------------- |
| Week 1     | Platform & Pipeline Design                   |
| Week 2     | Docker Fundamentals                          |
| Week 3     | Relational Data Modeling                     |
| Week 4     | Working & Designing APIs                     |
| Week 5 & 6 | ML & Containerization on AWS                 |
| Week 7     | ETL & CI/CD on AWS                           |
| Week 8     | Building a Lakehouse on AWS or GCP           |
| Week 9     | Orchestrate with Airflow                     |
| Week 10    | Pre-Process Data with Apache Spark           |
| Week 11-13 | Build a Streaming Pipeline (AWS, Azure, GCP) |
| Week 14    | Analyze Training Logs with Elasticsearch     |

---

#### Week 1: Platform & Pipeline Design

##### Description
Data pipelines are the foundation of any data platform. In this 110-minute training, you'll learn about stream, batch, and ML pipelines. You'll also explore platform blueprints, architecture components, and Lambda architecture.

**Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/data-pipeline-design)**

##### Course Curriculum

| Lesson                                           | Duration    |
| ------------------------------------------------ | ----------- |
| Platform Blueprint & End to End Pipeline Example | 10:11       |
| Data Engineering Tools Guide                     | 2:44        |
| End to End Pipeline Example                      | 6:18        |
| Push Ingestion Pipelines                         | 3:42        |
| Pull Ingestion Pipelines                         | 3:34        |
| Batch Pipelines                                  | 3:07        |
| Streaming Pipelines                              | 3:34        |
| Stream Analytics                                 | 2:26        |
| Lambda Architecture                              | 4:02        |
| Visualization Pipelines                          | 3:47        |
| Visualization with Hive & Spark on Hadoop        | 6:21        |
| Visualization Data via Spark Thrift Server       | 3:27        |
| Platform Examples (AWS, Azure, GCP, Hadoop)      | Slides Only |

---

#### Week 2: Docker Fundamentals

##### Description
Docker is the go-to container platform for engineers. This training covers key concepts, hands-on Docker usage, building and running containers, and how Docker fits into production workflows.

**Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/docker-fundamentals)**

##### Course Curriculum

| Lesson                              | Duration |
| ----------------------------------- | -------- |
| Docker vs Virtual Machines          | 6:23     |
| Docker Terminology                  | 5:56     |
| Installing Docker Desktop           | 4:09     |
| Pulling Images & Running Containers | 6:34     |
| CLI Cheat Sheet                     | 3:38     |
| Docker Compose Explained            | 6:34     |
| Build & Run Hello World Image       | 6:28     |
| Build Image with Dependencies       | 5:05     |
| Using DockerHub                     | 4:24     |
| Image Layers                        | 7:55     |
| Deployment in Production            | 5:47     |
| Security Best Practices             | 4:09     |
| Managing Docker with Portainer      | 4:04     |

---

#### Week 3: Relational Data Modeling

##### Description
Learn how to design efficient and scalable relational models. You'll go through conceptual to physical modeling and normalize your schema. You'll use MySQL and MySQL Workbench for hands-on practice.

**Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/relational-data-modeling)**

##### Course Curriculum

| Lesson                           | Duration |
| -------------------------------- | -------- |
| History of Relational Models     | 3:16     |
| Installing MySQL & Workbench     | 8:04     |
| Workbench Introduction           | 4:36     |
| The Design Process Explained     | 4:14     |
| Discover Entities                | 10:24    |
| Discover Attributes              | 13:09    |
| Normalize & Define Relationships | 11:19    |
| Identifying vs Non-identifying   | 2:01     |
| Resolve Many-to-Many             | 4:00     |
| Resolve One-to-Many              | 2:34     |
| Resolve One-to-One               | 1:45     |
| Create ER Diagram                | 19:46    |
| Create Physical Data Model       | 4:13     |
| Populate from XLS                | 15:13    |
| Course Conclusion                | 1:28     |

---

#### Week 4: Working & Designing APIs

##### Description
APIs are the backbone of modern data platforms. You'll learn how to build and test APIs using FastAPI, design schemas, and deploy them in Docker. Postman and Docker are used for testing and deployment.

**Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/apis-with-fastapi-course)**

##### Course Curriculum

| Lesson                        | Duration |
| ----------------------------- | -------- |
| What are APIs?                | 8:29     |
| Hosting vs Using APIs         | 4:08     |
| HTTP Methods & Media Types    | 6:56     |
| Response Codes & Parameters   | 9:40     |
| FastAPI Setup                 | 4:55     |
| POST, GET, PUT API Methods    | 16:18    |
| Testing with Postman          | 4:22     |
| Deploying FastAPI with Docker | 6:01     |
| API Security Best Practices   | 3:48     |

---

#### Week 5 & 6: ML & Containerization on AWS

##### Description
This hands-on project teaches you how to build a real-time ML pipeline on AWS. You'll pull data from the Twitter API (or The Guardian API), apply sentiment analysis with NLTK in a Lambda function, store results in a Postgres database via RDS, and build a Streamlit dashboard. Finally, you’ll containerize and deploy the dashboard using AWS ECS and ECR.

**Check out this project in my Academy: [Learn More](https://learndataengineering.com/p/ml-on-aws)**

##### Course Curriculum

| Lesson                                             | Duration |
| -------------------------------------------------- | -------- |
| Introduction                                       | 2:38     |
| Project Architecture Explained                     | 2:06     |
| RDS Setup                                          | 2:37     |
| VPC Inbound Rules                                  | 2:12     |
| PG Admin Installation & S3 Config                  | 4:05     |
| Lambda Intro & IAM Setup                           | 3:11     |
| Create Lambda Function                             | 1:24     |
| Lambda Code Explained                              | 8:22     |
| Insert Code Into Lambda                            | 0:56     |
| Add Layers from Klayers                            | 5:32     |
| Create Custom Layers                               | 4:40     |
| Test Lambda & Set Env Variables                    | 4:53     |
| Schedule Lambda with EventBridge                   | 3:15     |
| Setup Virtual Conda Environment                    | 4:07     |
| Install Dependencies with Poetry                   | 5:57     |
| Streamlit App Code Walkthrough                     | 7:52     |
| Setup ECR Container Registry                       | 1:52     |
| AWS CLI Install & Login                            | 5:19     |
| Dockerfile Build & Push                            | 2:52     |
| Create ECS Fargate Cluster                         | 1:34     |
| ECS Task Configuration & Deployment                | 4:59     |
| Fixing ECS Task                                    | 5:14     |
| Stop ECS Task                                      | 0:59     |
| Project Conclusion                                 | 5:06     |

---

#### Week 7: ETL & CI/CD on AWS

##### Description
In this project, you'll build a lightweight ETL job that pulls data from a public weather API and writes it into a time series database. You’ll dockerize the job, schedule it using AWS Lambda and EventBridge, and visualize the data using Grafana.

**Check out this project in my Academy: [Learn More](https://learndataengineering.com/p/timeseries-etl-with-aws-tdengine-grafana)**

### Course Curriculum

| Lesson                                       | Duration |
| -------------------------------------------- | -------- |
| Quick Note from Andreas                      | 0:43     |
| Project Introduction                         | 1:26     |
| Setup of the Project                         | 2:52     |
| Time Series Data Basics                      | 2:20     |
| Big Pros of Time Series Databases            | 2:06     |
| About TDengine                               | 1:22     |
| Setup Weather API                            | 1:04     |
| Code Query API                               | 2:41     |
| TDengine Setup                               | 3:04     |
| Connect Python to TDengine                   | 1:50     |
| Lambda Docker Container & Push to ECR        | 1:55     |
| AWS Setup                                    | 1:36     |
| Create Lambda Function Using Docker Image    | 1:04     |
| Schedule Function with EventBridge           | 1:25     |
| CloudWatch Lambda Events                     | 0:27     |
| Grafana Setup                                | 3:01     |

---

#### Week 8: Building a Lakehouse on AWS or GCP

##### Description
This week, you’ll learn how to combine data lakes and warehouses into a Lakehouse architecture. You’ll implement a full data analytics stack using tools like S3, Athena, BigQuery, Glue, Quicksight, and Data Studio.

**Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/modern-data-warehouses)**

##### Course Curriculum

| Lesson                                                  | Duration |
| -------------------------------------------------------- | -------- |
| Introduction                                             | 2:13     |
| Data Science Platform Overview                           | 4:10     |
| ETL & ELT in Warehouses                                  | 6:22     |
| Data Lake & Warehouse Integration                        | 3:29     |
| GCP Pipelines Overview                                   | 3:13     |
| Cloud Storage & BigQuery Hands-on                       | 8:35     |
| Create Dashboard in Data Studio                          | 7:33     |
| GCP Recap & AWS Goals                                    | 2:12     |
| Upload Data to S3                                        | 2:12     |
| Athena Manual Table Configuration                        | 3:48     |
| Create Dashboard in Quicksight                           | 5:05     |
| Athena via Glue Catalog                                  | 3:29     |
| Course Recap                                             | 2:36     |
| BONUS: Redshift Spectrum with S3                         | 2:57     |

---

#### Week 9: Orchestrate with Airflow

##### Description
This training will guide you through installing and running Apache Airflow in Docker, creating DAGs, using the Taskflow API, and monitoring workflow execution.

**Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/learn-apache-airflow)**

##### Course Curriculum

| Lesson                                        | Duration |
| --------------------------------------------- | -------- |
| Introduction                                  | 1:36     |
| Airflow Usage                                 | 3:19     |
| Fundamental Concepts                          | 2:47     |
| Airflow Architecture                          | 3:09     |
| Example Pipelines                             | 4:49     |
| Spotlight on 3rd Party Operators              | 2:17     |
| Airflow XComs                                 | 4:32     |
| Project Setup                                 | 1:43     |
| Docker Setup Explained                        | 2:06     |
| Docker Compose & Starting Containers          | 4:23     |
| Checking Services                             | 1:48     |
| Weather API Setup                             | 1:33     |
| Postgres DB Setup                             | 1:58     |
| Airflow Web Interface                         | 4:37     |
| Create DAG with Airflow 2.0                   | 9:46     |
| Run Your DAG                                  | 4:15     |
| Create DAG with Taskflow API                  | 6:59     |
| Get Data via SimpleHTTP Operator              | 3:38     |
| Write to Postgres                             | 4:12     |
| Parallel Processing                           | 4:15     |
| Recap & Outlook                               | 4:38     |

---

#### Week 10: Pre-Process Data with Apache Spark

##### Description
This training introduces Apache Spark fundamentals, showing you how to process large datasets using Spark DataFrames, RDDs, and SparkSQL inside Docker and Jupyter Notebooks.

**Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/learning-apache-spark-fundamentals)**

##### Course Curriculum

| Lesson                                | Duration |
| ------------------------------------- | -------- |
| Introduction & Contents               | 3:30     |
| Vertical vs Horizontal Scaling        | 3:55     |
| What Spark Is Good For                | 4:45     |
| Driver, Context & Executors           | 4:11     |
| Cluster Types                         | 1:59     |
| Client vs Cluster Deployment          | 6:11     |
| Where to Run Spark                    | 3:38     |
| Tools in Spark Course                 | 2:35     |
| Dataset Overview                      | 4:11     |
| Docker Setup                          | 2:52     |
| Jupyter Notebook Setup & Run         | 5:31     |
| RDDs                                  | 3:57     |
| DataFrames                            | 1:40     |
| Transformations & Actions Overview   | 2:59     |
| Transformations                       | 2:22     |
| Actions                               | 3:06     |
| JSON Transformations                  | 9:52     |
| Working with Schemas                  | 8:23     |
| Working with DataFrames               | 10:09    |
| SparkSQL                              | 5:04     |
| Working with RDDs                     | 12:52    |

---

#### Week 11–13: Build a Streaming Pipeline on AWS, Azure, or GCP

##### Description
In this 3-week section, you'll complete an end-to-end streaming data project on the cloud platform of your choice: AWS, Azure, or GCP. Each project teaches you how to ingest real-time data, process it, store it, and create visualizations.

You only need to complete one of the following three options:

---

##### Option 1: Streaming Pipeline on AWS

##### Description
You'll use AWS services like API Gateway, Kinesis, DynamoDB, Redshift, Lambda, Glue, and Power BI to create a complete streaming solution. You'll work with e-commerce data and build multiple ingestion and batch pipelines.

**Check out this project in my Academy: [Learn More](https://learndataengineering.com/p/data-engineering-on-aws)**

##### Course Curriculum

| Lesson                                       | Duration |
| -------------------------------------------- | -------- |
| Data Engineering                             | 4:15     |
| Data Science Platform                        | 5:20     |
| Dataset Introduction                         | 3:16     |
| Relational Storage Possibilities             | 3:46     |
| NoSQL Storage Possibilities                  | 6:28     |
| Platform Design & Pipeline Planning          | 3:49     |
| Client to Visualization Design               | 3:00     |
| Data Ingestion to Kinesis                    | 3:00     |
| Stream to S3 and DynamoDB                    | 5:28     |
| Visualization API & Redshift                 | 5:29     |
| AWS Setup & IAM                              | 4:06     |
| Create Lambda Functions                      | 2:33     |
| Configure Firehose & Debugging               | 7:43     |
| Power BI Setup                               | 12:16    |
| Glue Crawlers and Jobs                       | 26:52    |

---

##### Option 2: Streaming Pipeline on Azure

##### Description
You’ll build a Twitter-like JSON stream pipeline using Azure Functions, Event Hub, Cosmos DB, and Power BI. You’ll learn how to set up API management, key vaults, and authentication.

**Check out this project in my Academy: [Learn More](https://learndataengineering.com/p/build-streaming-data-pipelines-in-azure)**

#### Course Curriculum

| Lesson                                               | Duration |
| ---------------------------------------------------- | -------- |
| Project Introduction                                 | 2:43     |
| Local Preprocessing & Docker Setup                   | 7:06     |
| Develop & Deploy Azure Functions                     | 5:52     |
| Test Functions & Integrate with Blob Storage         | 6:26     |
| Add Functions to Azure API Management (APIM)         | 7:05     |
| Key Vault & Authentication                           | 4:41     |
| Create Event Hubs and Bindings                       | 6:59     |
| Write to Cosmos DB                                   | 9:03     |
| Power BI Connection and Dashboard Creation           | 6:32     |

---

##### Option 3: Streaming Pipeline on GCP

##### Description
This project shows how to extract weather data via API, stream it with Pub/Sub, write it into Cloud SQL, and visualize it with Looker Studio. You'll also learn function deployment and VM/database setup.

**Check out this project in my Academy: [Learn More](https://learndataengineering.com/p/data-engineering-on-gcp)**

##### Course Curriculum

| Lesson                                              | Duration |
| --------------------------------------------------- | -------- |
| Introduction & Setup                               | 2:43     |
| Architecture & Weather API                          | 5:31     |
| Enable APIs & Configure Scheduling                  | 4:00     |
| Setup MySQL Database & Compute Engine               | 4:40     |
| Create Cloud Functions for Data Ingestion           | 8:37     |
| Use Pub/Sub for Messaging                           | 1:41     |
| Write Data to Cloud SQL                             | 13:43    |
| Test and Monitor Data Flow                          | 5:51     |
| Setup Looker Studio & Build Dashboards              | 4:17     |
| Monitor Pipelines                                   | 6:20     |

---

##### Week 14: Analyze Training Logs with Elasticsearch

##### Description
Wrap up your roadmap by learning how to monitor pipelines using Elasticsearch. You’ll deploy Elasticsearch with Docker, send logs from your training pipelines, and visualize them in Kibana dashboards.

**Check out this course in my Academy: [Learn More](https://learndataengineering.com/p/log-analysis-with-elasticsearch)**

##### Course Curriculum

| Lesson                                           | Duration |
| ------------------------------------------------ | -------- |
| Course Introduction                              | 2:07     |
| Elasticsearch vs Relational Databases            | 5:43     |
| ETL Log Analysis & Debugging                     | 3:54     |
| Streaming Log Analysis & Debugging               | 2:48     |
| Solving Problems with Elasticsearch              | 4:37     |
| ELK Stack Overview                               | 2:03     |
| Setup Limiting RAM & Environment Config          | 4:26     |
| Running Elasticsearch                            | 4:07     |
| Elasticsearch APIs & Python Index Creation       | 7:31     |
| Write Logs (JSON) to Elasticsearch               | 4:46     |
| Create Kibana Visualizations & Dashboards        | 9:27     |
| Search Logs in Elasticsearch                     | 4:57     |
| Course Recap                                     | —        |

---

#### What’s Next?

After 14 weeks, you’ll have built scalable, production-ready data pipelines and ML workflows. You can now explore more advanced projects, optimize performance, and contribute to production systems with confidence. Need help showcasing your skills or getting hired? Reach out to my coaching program!


### Roadmap for Software Engineers

![Building blocks of your curriculum](/images/Data-Engineering-Roadmap-for-Software-Engineers.jpg)

if you're transitioning from a background in computer science or software engineering into data engineering, you're already equipped with a solid foundation. Your existing knowledge in coding, familiarity with SQL databases, understanding of computer networking, and experience with operating systems like Linux, provide you with a considerable advantage. These skills form the cornerstone of data engineering and can significantly streamline your learning curve as you embark on this new journey.

Here's a refined roadmap, incorporating your prior expertise, to help you excel in data engineering:

- **Deepen Your Python Skills:** Python is crucial in data engineering for processing and handling various data formats, such as APIs, CSV, and JSON. Given your coding background, focusing on Python for data engineering will enhance your ability to manipulate and process data effectively.
- **Master Docker:** Docker is essential for deploying code and managing containers, streamlining the software distribution process. Your understanding of operating systems and networking will make mastering Docker more intuitive, as you'll appreciate the importance of containerization in today's development and deployment workflows.
- **Platform and Pipeline Design:** Leverage your knowledge of computer networking and operating systems to grasp the architecture of data platforms. Understanding how to design data pipelines, including considerations for stream and batch processing, and emphasizing security, will be key. Your background will provide a solid foundation for understanding how different components integrate within a data platform.
- **Choosing the Right Data Stores:** Dive into the specifics of data stores, understanding the nuances between transactional and analytical databases, and when to use relational vs. NoSQL vs. document stores vs. time-series databases. Your experience with SQL databases will serve as a valuable baseline for exploring these various data storage options.
- **Explore Cloud Platforms:** Get hands-on with cloud services such as AWS, GCP, and Azure. Projects or courses that offer practical experience with these platforms will be invaluable. Your tasks might include building pipelines to process data from APIs, using message queues, or delving into data warehousing and lakes, capitalizing on your foundational skills.
- **Optional Deep Dives:** For those interested in advanced data processing, exploring technologies like Spark or Kafka for stream processing can be enriching. Additionally, learning how to build APIs and work with MongoDB for document storage can open new avenues, especially through practical projects.
- **Log Analysis and Data Observability:** Familiarize yourself with tools like Elasticsearch, Grafana, and InfluxDB to monitor and analyze your data pipelines effectively. This area leverages your comprehensive understanding of how systems communicate and operate, enhancing your ability to maintain and optimize data flows.

As you embark on this path, remember that your journey is unique. Your existing knowledge not only serves as a strong foundation but also as a catalyst for accelerating your growth in the realm of data engineering. Keep leveraging your strengths, explore areas of interest deeply, and continually adapt to the evolving landscape of data technology.

| Live Stream -> Data Engineering Roadmap for Computer Scientists / Developers
|------------------|
|In this live stream you'll find even more details how to read this roadmap for Data Scientists, why I chose these tools and why I think this is the right way to do it.
| [Watch on YouTube](https://youtube.com/live/0e4WfIUixRw)|


## Data Engineers Skills Matrix

![Data Engineer Skills Matrix](/images/Data-Engineer-Skills-Matrix.jpg)

If you're diving into the world of data engineering or looking to climb the ladder within this field, you're in for a treat with this enlightening YouTube video. Andreas kicks things off by introducing us to a very handy tool they've developed: the Data Engineering Skills Matrix. This isn't just any chart; it's a roadmap designed to navigate the complex landscape of data engineering roles, ranging from a Junior Data Engineer to the lofty heights of a Data Architect and Machine Learning Engineer.

| Live Stream -> Data Engineering Skills Matrix
|------------------|
|In this live stream you'll find even more details how to read this skills matrix for Data Engineers.  
| [Watch on YouTube](https://youtube.com/live/5E0UiBy0Kwo)|

Andreas takes us through the intricacies of this matrix, layer by layer. Starting with the basics, they discuss the minimum experience needed for each role. It's an eye-opener, especially when you see how experience requirements evolve from a beginner to senior levels. But it's not just about how many years you've spent in the field; it's about the skills you've honed during that time.

### Challenges & Responsibilities

As the conversation progresses, Andreas delves into the core responsibilities and main tasks associated with each role. You'll learn what sets a Junior Data Engineer apart from a Senior Data Engineer, the unique challenges a Data Architect faces, and the critical skills a Machine Learning Engineer must possess. This part of the video is golden for anyone trying to understand where they fit in the data engineering ecosystem or plotting their next career move.

### SQL & Soft Skills

Then there's the talk on SQL knowledge and its relevance across different roles. This segment sheds light on how foundational SQL is, irrespective of your position. But it's not just about technical skills; the video also emphasizes soft skills, like leadership and collaboration, painting a holistic picture of what it takes to succeed in data engineering.

For those who love getting into the weeds, Andreas doesn't disappoint. They discuss software development skills, debugging, and even dive into how data engineers work with SQL and databases. This part is particularly insightful for understanding the technical depth required at various stages of your career.

### Q&A

And here's the cherry on top: Andreas encourages interaction, inviting viewers to share their experiences and questions. This makes the video not just a one-way learning experience but a dynamic conversation that enriches everyone involved.

### Summary

By the end of this video, you'll walk away with a clear understanding of the data engineering field's diverse roles. You'll know the skills needed to excel in each role and have a roadmap for your career progression. Whether you're a recent graduate looking to break into data engineering or a seasoned professional aiming for a senior position, Andreas's video is a must-watch. It's not just a lecture; it's a guide to navigating the exciting world of data engineering, tailored by someone who's taken the time to lay out the journey for you.



## How to Become a Senior Data Engineer

Becoming a senior data engineer is a goal many in the tech industry aspire to. It's a role that demands a deep understanding of data architecture, advanced programming skills, and the ability to lead and communicate effectively within an organization. In this live stream series, I dove into what it takes to climb the ladder to a senior data engineering position. Here are the key takeaways. You can find the links to the videos and the shown images below.

### Understanding the Role
The journey to becoming a senior data engineer starts with a clear understanding of what the role entails. Senior data engineers are responsible for designing, implementing, and maintaining an organization's data architecture. They ensure data accuracy, accessibility, and security, often taking the lead on complex projects that require advanced technical skills and strategic thinking.

### Key Skills and Knowledge Areas
Based on insights from the live stream and consultations with industry experts, including GPT-3, here are the critical areas where aspiring senior data engineers should focus their development:

- **Advanced Data Modeling and Architecture:** Mastery of data modeling techniques and architecture best practices is crucial. This includes understanding of dimensional and Data Vault modeling, as well as expertise in SQL and NoSQL databases.
- **Big Data Technologies:** Familiarity with distributed computing frameworks (like Apache Spark), streaming technologies (such as Apache Kafka), and cloud-based big data technologies is essential.
Advanced ETL Techniques: Skills in incremental loading, data merging, and transformation are vital for efficiently processing large datasets.
- **Data Warehousing and Data Lake Implementation:** Building and maintaining scalable and performant data warehouses and lakes are fundamental responsibilities.
- **Cloud Computing:** Proficiency in cloud services from AWS, Azure, or GCP, along with platforms like Snowflake and Databricks, is increasingly important.
- **Programming and Scripting:** Advanced coding skills in languages relevant to data engineering, such as Python, Scala, or Java, are non-negotiable.
- **Data Governance and Compliance:** Understanding data governance frameworks and compliance requirements is critical, especially in highly regulated industries.
- **Leadership and Communication:** Beyond technical skills, the ability to lead projects, communicate effectively with both technical and non-technical team members, and mentor junior engineers is what differentiates a senior engineer.

### Learning Pathways
Becoming a senior data engineer requires continuous learning and real-world experience. Here are a few steps to guide your journey:

- **Educational Foundation:** Start with a strong foundation in computer science or a related field. This can be through formal education or self-study courses.
- **Gain Practical Experience:** Apply your skills in real-world projects. This could be in a professional setting, contributions to open-source projects, or personal projects.
- **Specialize and Certify:** Consider specializing in areas particularly relevant to your interests or industry needs. Obtaining certifications in specific technologies or platforms can also bolster your credentials.
- **Develop Soft Skills:** Work on your communication, project management, and leadership skills. These are as critical as your technical abilities.
- **Seek Feedback and Mentorship:** Learn from the experiences of others. Seek out mentors who can provide guidance and feedback on your progress.

### Video 1

| Live Stream -> How to become a Senior Data Engineer - Part 1
|------------------|
| In this part one I talked about Data Modeling, Big Data, ETL, Data Warehousing & Data Lakes as well as Cloud computing
| [Watch on YouTube](https://youtube.com/live/M-6xkTCKQQc)|

![Watch on YouTube](/images/Becoming-a-Senior-Data-Engineer-Video-1.jpg)

### Video 2

| Live Stream -> How to become a Senior Data Engineer - Part 2
|------------------|
| In part two I talked about real time data processing, programming & scripting, data governance, compliance and data security
| [Watch on YouTube](https://youtube.com/live/po96pzpjxvA)|

![Watch on YouTube](/images/Becoming-a-Senior-Data-Engineer-Video-2.jpg)

### Video 3

| Live Stream -> How to become a Senior Data Engineer - Part 3
|------------------|
| In part 3 I focused on everything regarding Leadership and Communication: team management, project management, collaboration, problem solving, strategic thinking, communication and leadership
| [Watch on YouTube](https://youtube.com/live/DMumpzSyRjI)|

![Watch on YouTube](/images/Becoming-a-Senior-Data-Engineer-Video-3.jpg)

### Final Thoughts
The path to becoming a senior data engineer is both challenging and rewarding. It requires a blend of technical prowess, continuous learning, and the development of soft skills that enable you to lead and innovate. Whether you're just starting out or looking to advance your career, focusing on the key areas outlined above will set you on the right path.


---


Basic Computer Science Skills
=============================

## Contents

- Learn to Code
- Get Familiar with Git
- Agile Development
  - Why Is Agile So Important?
  - Agile Rules I Learned Over the Years
  - Agile Frameworks
    - Scrum
    - OKR
- Software Engineering Culture
- Learn How a Computer Works
- Data Network Transmission
- Security and Privacy
  - SSL Public and Private Key Certificates
  - JSON Web Tokens
  - GDPR Regulations
- Linux
  - OS Basics
  - Shell Scripting
  - Cron Jobs
  - Packet Management
- Docker
  - What is Docker and How it Works
  - Kubernetes Container Deployment
  - Why and How To Do Docker Container Orchestration
  - Useful Docker Commands
- The Cloud
  - IaaS vs. PaaS vs. SaaS
  - AWS Azure IBM Google
  - Cloud vs. On-Premises
  - Security
  - Hybrid Clouds
- Data Scientists and Machine Learning
  - Machine Learning Workflow
  - Machine Learning Model and Data



Learn to Code
-------------

Why this is important: Without coding you cannot do much in data
engineering. I cannot count the number of times I needed a quick hack to solve a problem.

The possibilities are endless:

-   Writing or quickly getting some data out of a SQL DB.

-   Testing to produce messages to a Kafka topic.

-   Understanding the source code of a Webservice

-   Reading counter statistics out of a HBase key-value store.

So, which language do I recommend then?


If you would asked me a few years ago I would have said Java, 100%. Nowadays though the community moved heavily to Python. I highly recommend starting with it.

When you are getting into data processing with Spark you can use
Scala which is a JVM language, but Python is also very good here.

Python is a great choice. It is super versatile.


Where to Learn Python? There are free Python courses all over the internet.
- I have a beginner one in my Data Engineering academy: Introduction to Python course
- I also have a Python for Data Engineers one one in my Data Engineering academy: Python for Data Engineers course

Keep in mind to always keep it practical: Learning by doing!

I talked about the importance of learning by doing in this podcast:
<https://anchor.fm/andreaskayy/episodes/Learning-By-Doing-Is-The-Best-Thing-Ever---PoDS-035-e25g44>

Get Familiar with Git
---------------------

Why this is important: One of the major problems with coding is to keep
track of changes. It is also almost impossible to maintain a program you
have multiple versions of.

Another problem is the topic of collaboration and documentation, which
is super important.

Let's say you work on a Spark application and your colleagues need to
make changes while you are on holiday. Without some code management, they
are in huge trouble:

Where is the code? What have you changed last? Where is the
documentation? How do we mark what we have changed?

But, if you put your code on GitHub, your colleagues can find your code.
They can understand it through your documentation (please also have
in-line comments).

Developers can pull your code, make a new branch, and do the changes.
After your holiday, you can inspect what they have done and merge it with
your original code, and you end up having only one application.

Where to learn: Check out the GitHub Guides page where you can learn all
the basics: <https://guides.github.com/introduction/flow/>

This great GitHub commands cheat sheet saved my butt multiple times:
<https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet>

Also look into:

-   Pull

-   Push

-   Branching

-   Forking

GitHub uses markdown to write pages, a super simple language that is actually a lot of fun to write. Here's a markdown cheat cheatsheet:
<https://www.markdownguide.org/cheat-sheet/>

Pandoc is a great tool to convert any text file to and from markdown:
<https://pandoc.org>


Agile Development
-----------------

Agility is the ability to adapt quickly to changing circumstances.

These days, everyone wants to be agile. Big and small companies are
looking for the "startup mentality."

Many think it's the corporate culture. Others think it's the process of how
we create things that matters.

In this article, I am going to talk about agility and self-reliance,
about how you can incorporate agility in your professional career.

### Why Is Agile So Important?

Historically, development has been practiced as an explicitly defined process. You
think of something, specify it, have it developed, and then build in mass
production.

It's a bit of an arrogant process. You assume that you already know
exactly what a customer wants, or how a product has to look and how
everything works out.

The problem is that the world does not work this way!

Oftentimes the circumstances change because of internal factors.

Sometimes things just do not work out as planned or stuff is harder than
you think.

You need to adapt.

Other times you find out that you built something customers do not like
and needs to be changed.

You need to adapt.

That's why people jump on the Scrum train -- because Scrum is the
definition of agile development, right?

### Agile Rules I Learned Over the Years

#### Is the Method Making a Difference?

Yes, Scrum or Google's OKR can help to be more agile. The secret to
being agile, however, is not only how you create.

What makes me cringe is people trying to tell you that being agile
starts in your head. So, the problem is you?

No!

The biggest lesson I have learned over the past years is this: Agility
goes down the drain when you outsource work.

#### The Problem with Outsourcing

I know on paper outsourcing seems like a no-brainer: development costs
against the fixed costs.

It is expensive to bind existing resources on a task. It is even more
expensive if you need to hire new employees.

The problem with outsourcing is that you pay someone to build stuff for
you.

It does not matter who you pay to do something for you. He needs to make
money.

His agenda will be to spend as little time as possible on your work. That
is why outsourcing requires contracts, detailed specifications,
timetables, and delivery dates.

He doesn't want to spend additional time on a project, only because you
want changes in the middle. Every unplanned change costs him time and
therefore money.

If so, you need to make another detailed specification and a contract
change.

He is not going to put his mind into improving the product while
developing. Firstly, because he does not have the big picture. Secondly,
because he does not want to.

He is doing as he is told.

Who can blame him? If I were the subcontractor, I would do exactly the
same!

Does this sound agile to you?

#### Knowledge Is King: A lesson from Elon Musk

Doing everything in house -- that's why startups are so productive. No
time is wasted on waiting for someone else.

If something does not work or needs to be changed, there is someone on
the team who can do it right away.

One very prominent example who follows this strategy is Elon Musk.

Tesla's Gigafactories are designed to get raw materials in on one side
and spit out cars on the other. Why do you think Tesla is building
Gigafactories that cost a lot of money?

Why is SpaceX building its own space engines? Clearly, there are other,
older companies who could do that for them.

Why is Elon building tunnel boring machines at his new boring company?

At first glance, this makes no sense!

#### How You Really Can Be Agile

If you look closer, it all comes down to control and knowledge. You, your
team, your company, needs to do as much as possible on your own.
Self-reliance is king.

Build up your knowledge and therefore the team's knowledge. When you have
the ability to do everything yourself, you are in full control.

You can build electric cars, build rocket engines, or bore tunnels.

Don't largely rely on others, and be confident to just do stuff on your
own.

Dream big, and JUST DO IT!

PS. Don't get me wrong. You can still outsource work. Just do it in a
smart way by outsourcing small independent parts.

### Agile Frameworks

#### Scrum

There's an interesting Medium article with a lot of details
about Scrum: <https://medium.com/serious-scrum>

Also, this Scrum guide webpage has good info:
<https://www.scrumguides.org/scrum-guide.html>

#### OKR

I personally love OKR and have been using it for years. Especially for smaller
teams, OKR is great. You don't have a lot of overhead and get work done.
It helps you stay focused and look at the bigger picture.

I recommend doing a sync meeting every Monday. There you talk about what
happened last week and what you are going to work on this week.

I talked about this in this podcast:
<https://anchor.fm/andreaskayy/embed/episodes/Agile-Development-Is-Important-But-Please-Dont-Do-Scrum--PoDS-041-e2e2j4>

There is also this awesome 1,5-hour startup guide from Google:
<https://youtu.be/mJB83EZtAjc> I really love this video; I rewatched it
multiple times.

### Software Engineering Culture

The software engineering and development culture is super important. How
does a company handle product development with hundreds of developers?
Check out this podcast:

| Podcast episode: #070 Engineering Culture At Spotify
|------------------
|In this podcast, we look at the engineering culture at Spotify, my favorite music streaming service. The process behind the development of Spotify is really awesome.
  |Watch on YouTube \ Listen on Anchor|


**Some interesting slides:**

<https://labs.spotify.com/2014/03/27/spotify-engineering-culture-part-1/>

<https://labs.spotify.com/2014/09/20/spotify-engineering-culture-part-2/>

Learn How a Computer Works
--------------------------

### CPU,RAM,GPU,HDD

### Differences Between PCs and Servers

I talked about computer hardware and GPU processing in this podcast:
<https://anchor.fm/andreaskayy/embed/episodes/Why-the-hardware-and-the-GPU-is-super-important--PoDS-030-e23rig>

Data Network Transmission
---------------------------------------

### OSI Model

The OSI Model describes how data flows through the network. It
consists of layers starting from physical layers, basically how the data
is transmitted over the line or optic fiber.

Check out this article for a deeper understanding of the layers and processes outlined in the OSI model:
<https://www.studytonight.com/computer-networks/complete-osi-model>

The Wikipedia page is also very good:
<https://en.wikipedia.org/wiki/OSI_model>

###### Which Protocol Lives on Which Layer?

Check out this network protocol map. Unfortunately, it is really hard to
find it theses days:
<https://www.blackmagicboxes.com/wp-content/uploads/2016/12/Network-Protocols-Map-Poster.jpg>

### IP Subnetting

Check out this IP address and subnet guide from Cisco:
<https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13788-3.html>

A calculator for subnets:
<https://www.calculator.net/ip-subnet-calculator.html>

### Switch, Layer-3 Switch

For an introduction to how ethernet went from broadcasts, to bridges, to
Ethernet MAC switching, to ethernet & IP (layer 3) switching, to
software-defined networking, and to programmable data planes that can
switch on any packet field and perform complex packet processing, see
this video: <https://youtu.be/E0zt_ZdnTcM?t=144>

### Router

### Firewalls

I talked about network infrastructure and techniques in this podcast:
<https://anchor.fm/andreaskayy/embed/episodes/IT-Networking-Infrastructure-and-Linux-031-PoDS-e242bh>

Security and Privacy
--------------------

### SSL Public and Private Key Certificates


<https://www.cloudflare.com/learning/ssl/how-does-ssl-work/>

<https://www.kaspersky.com/resource-center/definitions/what-is-a-ssl-certificate>

<https://www.ssl.com/faqs/what-is-a-certificate-authority/>


### JSON Web Tokens

Link to the Wiki page: <https://en.wikipedia.org/wiki/JSON_Web_Token>

### GDPR Regulations

The EU created the GDPR \"General Data Protection Regulation\" to
protect your personal data like: name, age, address, and so
on.

It's huge and quite complicated. If you want to do online business in
the EU, you need to apply these rules. The GDPR is applicable since May
25th, 2018. So, if you haven't looked into it, now is the time.

The penalties can be crazy high if you make mistakes here.

Check out the full GDPR regulation here: <https://gdpr-info.eu>

By the way, if you do profiling or analyse big data in general, look
into it. There are some important regulations, unfortunately.

I spend months with GDPR compliance. Super fun. Not! Hahaha

### Privacy by Design

When should you look into privacy regulations and solutions?

Creating the product or service first and then bolting on the privacy is
a bad choice. The best way is to start implementing privacy right away
in the engineering phase.

This is called privacy by design. Privacy is an integral part of your
business, not just something optional.

Check out the Wikipedia page to get a feeling for the important
principles: <https://en.wikipedia.org/wiki/Privacy_by_design>

Linux
-----

Linux is very important to learn, at least the basics. Most big-data
tools or NoSQL databases run on Linux.

From time to time, you need to modify stuff through the operating system,
especially if you run an infrastructure as a service solution like
Cloudera CDH, Hortonworks, or a MapR Hadoop distribution.

### OS Basics

Show all historic commands:

    history | grep docker

### Shell scripting

Ah, creating shell scripts in 2019? Believe it or not, scripting in the
command line is still important.

Start a process, automatically rename, move or do a quick compaction of
log files. It still makes a lot of sense.

Check out this cheat sheet to get started with scripting in Linux:
<https://devhints.io/bash>

There's also this Medium article with a super-simple example for
beginners:
<https://medium.com/@saswat.sipun/shell-scripting-cheat-sheet-c0ecfb80391>

### Cron Jobs

Cron jobs are super important to automate simple processes or jobs in
Linux. You need this here and there, I promise. Check out these three
guides:

<https://linuxconfig.org/linux-crontab-reference-guide>

<https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/>

And, of course, Wikipedia, which is surprisingly good:
<https://en.wikipedia.org/wiki/Cron>

Pro tip: Don't forget to end your cron files with an empty line or a
comment, otherwise it will not work.

### Packet Management

Linux tips are the second part of this podcast:
<https://anchor.fm/andreaskayy/embed/episodes/IT-Networking-Infrastructure-and-Linux-031-PoDS-e242bh>


Docker
------

### What is Docker, and What Do You Use It for?

Have you played around with Docker yet? If you're a data science learner
or a data scientist, you need to check it out!

It's awesome because it simplifies the way you can set up development
environments for data science. If you want to set up a dev environment,
you usually have to install a lot of packages and tools.

#### Don't Mess Up Your System

What this does is basically mess up your operating system. If you're
just starting out, you don't know which packages you need to install. You don't
know which tools you need to install.

If you want to, for instance, start with Jupyter Notebooks, you need to
install that on your PC somehow. Or, you need to start installing tools
like PyCharm or Anaconda.

All that gets added to your system, and so you mess up your system more
and more and more. What Docker brings you, especially if you're on a Mac
or a Linux system, is simplicity.

#### Preconfigured Images

Because it is so easy to install on those systems, another cool thing
about Docker images is you can just search them in the Docker store,
download them, and install them on your system.

Running them in a completely pre-configured environment, you don't need
to think about stuff. You go to the Docker library, and you search for Deep
Learning, GPU and Python.

You get a list of images you can download. You download one, start it
up, go to the browser and hit up the URL, and just start coding.

Start doing the work. The only other thing you need to do is bind some
drives to that instance so you can exchange files. And, then that's it!

There is no way that you can crash or mess up your system. It's all
encapsulated into Docker. Why this works is because Docker has native
access to your hardware.

#### Take It With You

It's not a completely virtualized environment like a VirtualBox. An
image has the upside that you can take it wherever you want. So, if
you're on your PC at home, use that there.

Make a quick build, take the image, and go somewhere else. Install the
image, which is usually quite fast, and just use it like you're at home.

It's that awesome!

### Kubernetes Container Deployment

I am getting into Docker a lot more myself. For a some different reasons.

What I'm looking for is using Docker with Kubernetes. With Kubernetes,
you can automate the whole container deployment process.

The idea is that you have a cluster of machines. Lets say you have
a 10-server cluster and you run Kubernetes on it.

Kubernetes lets you spin up Docker containers on demand to execute
tasks. You can set up how much resources like CPU, RAM, and network your
Docker container can use.

You can basically spin up containers, on the cluster on demand, whenever
you need to do an analytics task.

That's perfect for data science.


### How to Create, Start, Stop a Container

### Docker Micro-Services?

### Kubernetes

### Why and How to Do Docker Container Orchestration

Podcast about how data science learners use Docker (for data
scientists):
<https://anchor.fm/andreaskayy/embed/episodes/Learn-Data-Science-Go-Docker-e10n7u>

### Useful Docker Commands

Create a container:

    docker run CONTAINER --network NETWORK

Start a stopped container:

    docker start CONTAINER NAME

Stop a running container:

    docker stop

List all running containers:

    docker ps

List all containers including stopped ones:

    docker ps -a

Inspect the container configuration (e.g. network settings, etc.):

    docker inspect CONTAINER

List all available virtual networks:

    docker network ls

Create a new network:

    docker network create NETWORK --driver bridge

Connect a running container to a network:

    docker network connect NETWORK CONTAINER

Disconnect a running container from a network:

    docker network disconnect NETWORK CONTAINER

Remove a network:

    docker network rm NETWORK


The Cloud
---------

### IaaS vs. PaaS vs. SaaS

Check out this podcast. It will help you understand the
difference and how to decide what to use.

| Podcast episode: #082 Reading Tweets With Apache Niﬁ & IaaS vs PaaS vs SaaS
|------------------|
|In this episode, we talk about the differences between infrastructure as a service, platform as a service, and application as a service. Then, we install the Niﬁ Docker container and look into how we can extract the twitter data.
| Watch on YouTube \ Listen on Anchor|


### AWS, Azure, IBM, Google

Each of these have their own answer to IaaS, Paas, and SaaS. Pricing and
pricing models vary greatly between each provider. Likewise, each
provider's service may have limitations and strengths.

#### AWS

Here is the full list of AWS services. Studying for the AWS Certified Cloud Practitioner and/or AWS Certified Solutions Architect exams can be helpful to quickly gain an understanding of all these services.
Here are links for free digital training for the AWS Certified Cloud Practitioner and AWS Certified Solutions Architect Associate.

Here is a free 17 hour Data Analytics Learning plan for AWS's Analytics/Data Engineering services.

#### Azure
Full list of Azure services.
Get started with mini courses.

#### IBM

#### Google

Google Cloud Platform offers a wide, ever-evolving variety of services.
List of GCP services with brief description. In
recent years, documentation and tutorials have com a long way to help
[getting started with
GCP](https://cloud.google.com/gcp/getting-started/). You can start with
a free account, but to use many of the services, you will need to turn on
billing. Once you do enable billing, always remember to turn off services
that you have spun up for learning purposes. It is also a good idea to
turn on billing limits and alerts.

### Cloud vs. On-Premises

| Podcast episode: #076 Cloud vs. On-Premise
|------------------|
|How to choose between cloud and on-premises, pros and cons and what you have to think about. There are good reasons to not go cloud. Also, thoughts on how to choose between the cloud providers by just comparing instance prices. Otherwise, the comparison will drive you insane. My suggestion: Basically use them as IaaS and something like Cloudera as PaaS. Then build your solution on top of that.  
| Watch on YouTube \ Listen on Anchor|


### Security

Listen to a few thoughts about the cloud in this podcast:
<https://anchor.fm/andreaskayy/embed/episodes/Dont-Be-Arrogant-The-Cloud-is-Safer-Then-Your-On-Premise-e16k9s>

### Hybrid Clouds

Hybrid clouds are a mixture of on-premises and cloud deployment. A very
interesting example for this is Google Anthos:

<https://cloud.google.com/anthos/>


# Data Scientists and Machine Learning

Data scientists aren't like every other scientist.

Data scientists do not wear white coats or work in high tech labs full
of science fiction movie equipment. They work in offices just like you
and me.

What differs them from most of us is that they are math experts. They
use linear algebra and multivariable calculus to create new insight from
existing data.

How exactly does this insight look?

Here's an example:

An industrial company produces a lot of products that need to be tested
before shipping.

Usually such tests take a lot of time because there are hundreds of
things to be tested. All to make sure that your product is not broken.

Wouldn't it be great to know early if a test fails ten steps down the
line? If you knew that you could skip the other tests and just trash the
product or repair it.

That's exactly where a data scientist can help you, big-time. This field
is called predictive analytics and the technique of choice is machine
learning.

Machine what? Learning?

Yes, machine learning, it works like this:

You feed an algorithm with measurement data. It generates a model and
optimises it based on the data you fed it with. That model basically
represents a pattern of how your data is looking. You show that model
new data and the model will tell you if the data still represents the
data you have trained it with. This technique can also be used for
predicting machine failure in advance with machine learning. Of course
the whole process is not that simple.

The actual process of training and applying a model is not that hard. A
lot of work for the data scientist is to figure out how to pre-process
the data that gets fed to the algorithms.

In order to train an algorithm you need useful data. If you use any data
for the training the produced model will be very unreliable.

An unreliable model for predicting machine failure would tell you that
your machine is damaged even if it is not. Or even worse: It would tell
you the machine is ok even when there is a malfunction.

Model outputs are very abstract. You also need to post-process the model
outputs to receive the outputs you desire

![The Machine Learning Pipeline](/images/Machine-Learning-Pipeline.jpg)


## Machine Learning Workflow

![The Machine Learning Workflow](/images/Machine-Learning-Workflow.jpg)

Data Scientists and Data Engineers. How does that all fit together?

You have to look at the data science process. How stuff is created and how data
science is done. How machine learning is
done.

The machine learning process shows, that you start with a training phase. A phase where you are basically training the algorithms to create the right output.

In the learning phase you are having the input parameters. Basically the configuration of the model and you have the input data.

What you're doing is you are training the algorithm. While training the algorithm modifies the training
parameters. It also modifies the used data and then you are getting to an output.

Once you get an output you are evaluating. Is that output okay, or is that output not the desired output?

if the output is not what you were looking for? Then you are continuing with the training phase.

You're trying to retrain the model hundreds, thousands, hundred thousands of times. Of course all this is being done automatically.

Once you are satisfied with the output, you are putting the model into production. In production it is no longer fed with training
data it's fed with the live data.

It's evaluating the input data live and putting out live results.

So, you went from training to production and then what?

What you do is monitoring the output. If the output keeps making sense, all good!

If the output of the model changes and it's on longer what you have expected, it means the model doesn't work anymore.

You need to trigger a retraining of the model. It basically gets to getting trained again.

Once you are again satisfied with the output, you put it into production again. It replaces the one in production.

This is the overall process how machine learning. It's how the learning part of data science is working.


## Machine Learning Model and Data

![The Machine Learning Model](/images/Machine-Learning-Model.jpg)

Now that's all very nice.

When you look at it, you have two very important places where you have data.

You have in the training phase two types of data:
Data that you use for the training. Data that basically configures the model, the hyper parameter configuration.

Once you're in production you have the live data that is streaming in. Data that is coming in from from an app, from
a IoT device, logs, or whatever.

A data catalog is also important. It explains which features are available and how different data sets are labeled.

All different types of data. Now, here comes the engineering part.

The Data Engineers part, is making this data available. Available to the data scientist and the machine learning process.

So when you look at the model, on the left side you have your hyper parameter configuration. You need to store and manage these configurations somehow.

Then you have the actual training data.

There's a lot going on with the training data:

Where does it come from? Who owns it? Which is basically data governance.

What's the lineage? Have you modified this data? What did you do, what was the basis, the raw data?

You need to access all this data somehow. In training and in production.

In production you need to have access to the live data.

All this is the data engineers job. Making the data available.

First an architect needs to build the platform. This can also be a good data engineer.

Then the data engineer needs to build the pipelines. How is the data coming in and how is the platform
connecting to other systems.

How is that data then put into the storage. Is there a pre processing for the algorithms necessary? He'll do it.

Once the data and the systems are available, it's time for the machine learning part.

It is ready for processing. Basically ready for the data scientist.

Once the analytics is done the data engineer needs to build pipelines to make it then accessible again. For instance for other analytics processes, for APIs, for front ends and so on.

All in all, the data engineer's part is a computer science part.

That's why I love it so much :)


---


Advanced Data Engineering Skills
================================

## Contents

- Data Science Platform
  - Why a Good Data Platform Is Important
  - Big Data vs Data Science and Analytics
  - The 4 Vs of Big Data
  - Why Big Data
    - Planning is Everything
    - The Problem with ETL
    - Scaling Up
    - Scaling Out
    - When not to Do Big Data
- 81 Platform & Pipeline Design Questions
  - Data Source Questions
  - Goals and Destination Questions
- Connect
  - REST APIs
    - API Design
    - Implementation Frameworks
    - Security
  - Apache Nifi
  - Logstash
- Buffer
  - Apache Kafka
    - Why a Message Queue Tool?
    - Kafka Architecture
    - Kafka Topics
    - Kafka and Zookeeper
    - How to Produce and Consume Messages
    - Kafka Commands
  - Apache Redis Pub-Sub
  - AWS Kinesis
  - Google Cloud PubSub
- Processing Frameworks
  - Lambda and Kappa Architecture
  - Batch Processing
  - Stream Processing
    - Three Methods of Streaming
    - At Least Once
    - At Most Once
    - Exactly Once
    - Check The Tools
  - Should You do Stream or Batch Processing
  - Is ETL still relevant for Analytics?
  - MapReduce
    - How Does MapReduce Work
    - MapReduce
    - MapReduce Example
    - MapReduce Limitations
  - Apache Spark
    - What is the Difference to MapReduce?
    - How Spark Fits to Hadoop
    - Spark vs Hadoop
    - Spark and Hadoop a Perfect Fit
    - Spark on YARn
    - My Simple Rule of Thumb
    - Available Languages
    - Spark Driver Executor and SparkContext
    - Spark Batch vs Stream processing
    - How Spark uses Data From Hadoop
    - What are RDDs and How to Use Them
    - SparkSQL How and Why to Use It
    - What are Dataframes and How to Use Them
    - Machine Learning on Spark (TensorFlow)
    - MLlib
    - Spark Setup
    - Spark Resource Management
  - AWS Lambda  
  - Apache Flink
  - Elasticsearch
  - Apache Drill
  - StreamSets
- Store
  - Analytical Data Stores
    - Data Warehouse vs Data Lake
    - Snowflake and dbt
  - Transactional Data Stores
    - SQL Databases
      - PostgreSQL DB
      - Database Design
      - SQL Queries
      - Stored Procedures
      - ODBC/JDBC Server Connections
    - NoSQL Stores
      - HBase KeyValue Store
      - HDFS Document Store
      - MongoDB Document Store
      - Elasticsearch Document Store
      - Graph Databases (Neo4j)
      - Impala
      - Kudu
      - Apache Druid
      - InfluxDB Time Series Database
      - Greenplum MPP Database
    - NoSQL Data Warehouses
      - Hive Warehouse
      - Impala
- Visualize
  - Android and IOS
  - API Design for Mobile Apps
  - Dashboards
    - Grafana
    - Kibana
  - Webservers
    - Tomcat
    - Jetty
    - NodeRED
    - React
  - Business Intelligence Tools
    - Tableau
    - Power BI
    - Quliksense
  - Identity & Device Management
    - What Is A Digital Twin
    - Active Directory
- Machine Learning
  - How to do Machine Learning in production
  - Why machine learning in production is harder then you think
  - Models Do Not Work Forever
  - Where are The Platforms That Support Machine Learning
  - Training Parameter Management
  - How to Convince People That Machine Learning Works
  - No Rules No Physical Models
  - You Have The Data. Use It!
  - Data is Stronger Than Opinions
  - AWS Sagemaker



## Data Science Platform

### Why a Good Data Platform Is Important

| Podcast Episode: #066 How To Do Data Science From A Data Engineers Perspective  
|------------------|
|A simple introduction how to do data science in the context of the internet of things.
| [Watch on YouTube](https://youtu.be/yp_cc4R0mGQ) \ [Listen on Anchor](https://anchor.fm/andreaskayy/episodes/066-How-To-Do-Data-Science-From-A-Data-Engineers-Perspective-e45imt)|

### Big Data vs Data Science and Analytics

I talked about the difference in this podcast:
<https://anchor.fm/andreaskayy/embed/episodes/BI-vs-Data-Science-vs-Big-Data-e199hq>

### The 4 Vs of Big Data

It is a complete misconception. Volume is only one part of the often
called four V's of big data: Volume, velocity, variety and veracity.

**Volume** is about the size - How much data you have

**Velocity** is about the speed - How fast data is getting to you

How much data in a specific time needs to get processed or is coming
into the system. This is where the whole concept of streaming data and
real-time processing comes in to play.

**Variety** is about the variety - How different your data is

Like CSV files, PDFs that you have and stuff in XML. That you also have
JSON logfiles, or data in some kind of a key-value store.

It's about the variety of data types from different sources that you
basically want to join together. All to make an analysis based on that
data.

**Veracity** is about the credibility - How reliable your data is

The issue with big data is, that it is very unreliable.

You cannot really trust the data. Especially when you're coming from the
Internet of Things (IoT) side. Devices use sensors for measurement of
temperature, pressure, acceleration and so on.

You cannot always be hundred percent sure that the actual measurement is
right.

When you have data that is from for instance SAP and it contains data
that is created by hand you also have problems. As you know we humans
are bad at inputting stuff.

Everybody articulates differently. We make mistakes, down to the spelling
and that can be a very difficult issue for analytics.

I talked about the 4Vs in this podcast:
<https://anchor.fm/andreaskayy/embed/episodes/4-Vs-Of-Big-Data-Are-Enough-e1h2ra>

### Why Big Data?

What I always emphasize is that the four V's are quite nice. They give you a
general direction.

There is a much more important issue: Catastrophic Success.

What I mean by catastrophic success is, that your project, your startup
or your platform has more growth that you anticipated. Exponential
growth is what everybody is looking for.

Because with exponential growth there is the money. It starts small and
gets very big very fast. The classic hockey stick curve:

1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384,
.... BOOM!

Think about it. It starts small and quite slow, but gets very big very
fast.

You get a lot of users or customers who are paying money to use your
service, the platform or whatever. If you have a system that is not
equipped to scale and process the data the whole system breaks down.

That's catastrophic success. You are so successful and grow so fast that
you cannot fulfill the demand anymore. And so you fail and it's all
over.

It's now like you just can make that up while you go. That you can
foresee in a few months or weeks the current system doesn't work
anymore.

### Planning is Everything

It's all happens very very fast and you cannot react anymore. There's a
necessary type of planning and analyzing the potential of your business
case necessary.

Then you need to decide if you actually have big data or not.

You need to decide if you use big data tools. This means when you
conceptualize the whole infrastructure it might look ridiculous to
actually focus on big data tools.

But in the long run it will help you a lot. Good planning will get a lot
of problems out of the way, especially if you think about streaming data
and real-time analytics.

### The problem with ETL

A typical old-school platform deployment would look like the picture
below. Devices use a data API to upload data that gets stored in a SQL
database. An external analytics tool is querying data and uploading the
results back to the SQL DB. Users then use the user interface to display
data stored in the database.

![Common SQL Platform Architecture](/images/Common-SQL-Architecture.jpg)

Now, when the front end queries data from the SQL database the following
three steps happen:

\- The database extracts all the needed rows from the storage. (E) - The
extracted data gets transformed, for instance sorted by timestamp or
something a lot more complex. (T) - The transformed data is loaded to
the destination (the user interface) for chart creation. (L)

With exploding amounts of stored data the ETL process starts being a
real problem.

Analytics is working with large data sets, for instance whole days,
weeks, months or more. Data sets are very big like 100GB or Terabytes.
That means Billions or Trillions of rows.

This has the result that the ETL process for large data sets takes
longer and longer. Very quickly the ETL performance gets so bad it won't
deliver results to analytics anymore.

A traditional solution to overcome these performance issues is trying to
increase the performance of the database server. That's what's called
scaling up.

### Scaling Up

To scale up the system and therefore increase ETL speeds administrators
resort to more powerful hardware by:

Speeding up the extract performance by adding faster disks to physically
read the data faster. Increasing RAM for row caching. What is already in
memory does not have to be read by slow disk drives. Using more powerful
CPU's for better transform performance (more RAM helps here as well).
Increasing or optimising networking performance for faster data delivery
to the front end and analytics.

In summary: Scaling up the system is fairly easy.

![Scaling up a SQL Database](/images/SQL-Scaling-UP.jpg)

But with exponential growth it is obvious that sooner or later (more
sooner than later) you will run into the same problems again. At some
point you simply cannot scale up anymore because you already have a
monster system, or you cannot afford to buy more expensive hardware.

The next step you could take would be scaling out.

### Scaling Out

Scaling out is the opposite of scaling up. Instead of building bigger
systems the goal is to distribute the load between many smaller systems.

The easiest way of scaling out an SQL database is using a storage area
network (SAN) to store the data. You can then use up to eight SQL
servers (explain), attach them to the SAN and let them handle queries.
This way load gets distributed between those eight servers.

![Scaling out a SQL Database](/images/SQL-Scaling-Out.jpg)

One major downside of this setup is that, because the storage is shared
between the SQL servers, it can only be used as an read only database.
Updates have to be done periodically, for instance once a day. To do
updates all SQL servers have to detach from the database. Then, one is
attaching the DB in read-write mode and refreshing the data. This
procedure can take a while if a lot of data needs to be uploaded.

This Link (missing) to a Microsoft MSDN page has more options of scaling
out an SQL database for you.

I deliberately don't want to get into details about possible scaling out
solutions. The point I am trying to make is that while it is possible to
scale out SQL databases it is very complicated.

There is no perfect solution. Every option has its up- and downsides.
One common major issue is the administrative effort that you need to
take to implement and maintain a scaled out solution.

### Please don't go Big Data

If you don't run into scaling issues please, do not use big data tools!

Big data is an expensive thing. A Hadoop cluster for instance needs at
least five servers to work properly. More is better.

Believe me this stuff costs a lot of money.

Especially when you are talking about maintenance and development on top
big data tools into account.

If you don't need it it's making absolutely no sense at all!

On the other side: If you really need big data tools they will save your
ass :)

## 81 Platform and Pipeline Design Questions
Many people ask: "How do you select the platform, tools and design the pipelines?"
The options seem infinite. Technology however should never dictate the decisions.

Here are 81 questions that you should answer when starting a project


### Data Source Questions

#### Data Origin and Structure
- **What is the source?** Understand the "device."
- **What is the format of the incoming data?** (e.g., JSON, CSV, Avro, Parquet)
- **What’s the schema?**
- **Is the data structured, semi-structured, or unstructured?**
- **What is the data type?** Understand the content of the data.
- **Is the schema well-defined, or is it dynamic?**
- **How are changes in the data structure from the source (schema evolution) handled?**

#### Data Volume & Velocity
- **How much data is transmitted per transmission?**
- **How fast is the data coming in?** (e.g., messages per minute)
- **What is the maximum data volume expected per source per day?**
- **What scaling of sources/data is expected?**
- **Are there peaks for incoming data?**
- **How much data is posted per day across all sources?**
- **How does the data volume fluctuate?** (e.g., seasonal peaks, hourly/daily variations)
- **How will the system handle bursts of data?** (e.g., throttling or buffering)

#### Source Reliability & Redundancy
- **Is there data arriving late?**
- **Is there a risk of duplicate data from the source?** How will we handle de-duplication?
- **How reliable are the sources?** What’s the expected failure rate?
- **How do we handle data corruption or loss during transmission?**
- **What happens if a source goes offline?** Is there a fallback or failover source?
- **Do we need to retry failed transmissions or have fault-tolerance mechanisms in place?**

#### Data Extraction & New Sources
- **Do we need to extract the data from the sources?**
- **How many sources are there?**
- **Will new sources be implemented?**

#### Data Source Connectivity & Authentication
- **How is the data arriving?** (API, bucket, etc.)
- **How is the authentication done?**
- **What kind of connection is required for the data source?** (e.g., streaming, batch, API)
- **What protocols are used for data ingestion?** (e.g., REST, WebSocket, FTP)
- **Are there any rate limits or quotas imposed by the data source?**
- **How do we handle credentials?** Is there an API?
- **What is the retry strategy if data fails to be processed or transmitted?**

#### Data Security & Compliance
- **Does the data need to be encrypted at the source before being transmitted?**
- **Are there any compliance frameworks (e.g., GDPR, HIPAA) that the source data must adhere to?**
- **Is there a requirement for data masking or obfuscation at the source?**

#### Metadata & Audit
- **Is there metadata for the client transmission stored somewhere?**
- **What metadata should be captured for each transmission?** (e.g., record counts, latency)
- **How do we track and log data ingestion events for audit purposes?**
- **Is there a need for tracking data lineage?** (i.e., source origin and changes over time)

---

### Goals and Destination Questions

#### Use Case & Data Consumption
- **What kind of use case is this?** (Analytics, BI, ML, Transactional processing, Visualization, User Interfaces, APIs)
- **What are the typical use cases that require this data?** (e.g., predictive analytics, operational dashboards)
- **What are the downstream systems or platforms that will consume this data?**
- **How critical is real-time data versus historical data in this use case?**

#### Data Query & Delivery
- **How is the data visualized?** (raw data, aggregated data)
- **How much raw data is processed at once?**
- **How much data is cold data, and how often is cold data queried?**
- **How fast do the results need to appear?**
- **How much data is going to be queried at once?**
- **How fresh does the data need to be?**
- **How often is the data queried?** (frequency)
- **What are the SLAs for delivering data to downstream systems or applications?**

#### Aggregation & Modeling
- **How is the data aggregated?** (by devices, topic, time)
- **When does the aggregation happen?** (on query, on schedule, while streaming)
- **What kind of data models are needed for this use case?** (e.g., star schema, snowflake schema)
- **Is there a need for pre-aggregations to speed up queries?**
- **Should partitioning or indexing strategies be implemented to optimize query performance?**

#### Performance & Availability
- **What is the processing time requirement?**
- **What is the availability of analytics output?** (input vs output delay)
- **How fresh does the data need to be?**
- **What are the performance expectations for query speed?**
- **What is the acceptable query response time for end-users?**
- **How will the system handle an increase in concurrent queries from multiple users?**
- **What is the expected lag between data ingestion and availability for querying?**
- **Do we need horizontal scaling for query engines or databases?**

#### Data Lifecycle & Retention
- **What’s the data retention time?**
- **How often is data archived or moved to lower-cost storage?**
- **Will old data need to be transformed or reprocessed for new use cases?**
- **What are the data retention policies?** (e.g., hot vs cold storage)
- **How will the use case evolve as the data grows?** Will this affect how data is consumed or visualized?

#### Monitoring & Debugging
- **How will data delivery to the destination be monitored?** (e.g., time-to-load, query failures)
- **How will we monitor data pipeline health at the destination?** (e.g., throughput, latency)
- **What tools or methods will be used for debugging data delivery failures or performance bottlenecks?**
- **What metrics should be tracked to ensure data pipeline health?** (e.g., latency, throughput)
- **How do we handle issues such as data corruption or incomplete data at the destination?**

#### Data Access & Permissions
- **Who is working with the platform, and who has access to query or visualize the data?**
- **Which tools are used to query the data?**
- **What kind of data export capabilities are required?** (e.g., CSV, API, direct database access)
- **Is role-based access control (RBAC) needed to segment data views for different users?**
- **How will access to sensitive data be managed?** (e.g., row-level security, encryption)

#### Scaling & Future Requirements
- **What are the scalability requirements for the data platform as data volume grows?**
- **How will future business goals or scalability needs affect the design of data aggregation and retention strategies?**
- **How will the system handle an increasing load as more users query data or as data volume grows?**


## Connect

### REST APIs

APIs or Application Programming Interfaces are the cornerstones of any
great data platform.

| Podcast Episode: #033 How APIs Rule The World
|------------------|
|Strong APIs make a good platform. In this episode I talk about why you need APIs and why Twitter is a great example. Especially JSON APIs are my personal favorite. Because JSON is also important in the Big Data world, for instance in log analytics. How? Check out this episode!  
| [Listen on Anchor](https://anchor.fm/andreaskayy/episodes/How-APIs-Rule-The-World--PoDS-033-e24ttq)|

#### API Design

In this podcast episode we look into the Twitter API. It's a great
example how to build an API

| Podcast Episode: #081 Twitter API Research Data Engineering Course Part 5
|------------------|
|In this episode we look into the Twitter API documentation, which I love by the way. How can we get old tweets for a certain hashtags and how to get current live tweets for these hashtags?
| [Watch on YouTube](https://youtu.be/UnAXKxeIlyg) \ [Listen on Anchor](https://anchor.fm/andreaskayy/episodes/081-How-to-get-tweets-from-the-Twitter-API-e45j32)|


#### Payload compression attacks

How to defend your Server with zip Bombs
https://www.sitepoint.com/how-to-defend-your-website-with-zip-bombs/

#### Implementation Frameworks

Jersey:

<https://eclipse-ee4j.github.io/jersey.github.io/documentation/latest/getting-started.html>

Tutorial – REST API design and implementation in Java with Jersey and Spring:
https://www.codepedia.org/ama/tutorial-rest-api-design-and-implementation-in-java-with-jersey-and-spring/

Swagger:

<https://github.com/swagger-api/swagger-core/wiki/Swagger-2.X---Getting-started>

Jersey vs Swagger:

<https://stackoverflow.com/questions/36997865/what-is-the-difference-between-swagger-api-and-jax-rs>

Spring Framework:

<https://spring.io/>

When to use Spring or Jersey:

<https://stackoverflow.com/questions/26824423/what-is-the-difference-among-spring-rest-service-and-jersey-rest-service-and-spr>

#### OAuth security

### Apache Nifi

Nifi is one of these tools that I identify as high potential tools. It
allows you to create a data pipeline very easily.

Read data from a RestAPI and post it to Kafka? No problem Read data from
Kafka and put it into a database? No problem

It's super versatile and you can do everything on the UI.

I use it in Part 3 of this Document. Check it out.

Check out the Apache Nifi FAQ website. Also look into the documentation
to find all possible data sources and sinks of Nifi:

<https://nifi.apache.org/faq.html>

Here's a great blog about Nifi:

<https://www.datainmotion.dev>

### Logstash

<https://www.elastic.co/products/logstash>

### FluentD

Data Collector

https://www.fluentd.org/

### Apache Flume

https://flume.apache.org/

### Sqoop

https://sqoop.apache.org/

### Azure IoTHub

https://azure.microsoft.com/en-us/services/iot-hub/



## Buffer

### Apache Kafka

#### Why a message queue tool?

#### Kafka architecture

#### What are topics

#### What does Zookeeper have to do with Kafka

#### How to produce and consume messages

My YouTube video how to set up Kafka at home:
<https://youtu.be/7F9tBwTUSeY>

My YouTube video how to write to Kafka: <https://youtu.be/RboQBZvZCh0>

#### KAFKA Commands

Start Zookeeper container for Kafka:

    docker run -d --name zookeeper-server   \
        --network app-tier   \
        -e ALLOW_ANONYMOUS_LOGIN=yes    \
        bitnami/zookeeper:latest

Start Kafka container:

    docker run -d --name kafka-server  \
        --network app-tier  \
        -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper-server:2181  \
        -e ALLOW_PLAINTEXT_LISTENER=yes  \
        bitnami/kafka:latest

### Redis Pub-Sub

### AWS Kinesis

### Google Cloud PubSub

## Processing Frameworks

### Lambda and Kappa Architecture

| Podcast Episode: #077 Lambda Architecture and Kappa Architecture
|------------------|
|In this stream we talk about the lambda architecture with stream and batch processing as well as a alternative the Kappa Architecture that consists only of streaming. Also Data engineer vs data scientist and we discuss Andrew Ng’s AI Transformation Playbook.  
| [Watch on YouTube](https://youtu.be/iUOQPyHN9-0) \ [Listen on Anchor](https://anchor.fm/andreaskayy/episodes/077-Lambda--Kappa-Architecture-e45j0r)|


### Batch Processing

Ask the big questions. Remember your last yearly tax statement?

You break out the folders. You run around the house searching for the
receipts.

All that fun stuff.

When you finally found everything you fill out the form and send it on
its way.

Doing the tax statement is a prime example of a batch process.

Data comes in and gets stored, analytics loads the data from storage and
creates an output (insight):

![Batch Processing Pipeline](/images/Simple-Batch-Processing-Workflow.jpg)

Batch processing is something you do either without a schedule or on a
schedule (tax statement). It is used to ask the big questions and gain
the insights by looking at the big picture.

To do so, batch processing jobs use large amounts of data. This data is
provided by storage systems like Hadoop HDFS.

They can store lots of data (petabytes) without a problem.

Results from batch jobs are very useful, but the execution time is high.
Because the amount of used data is high.

It can take minutes or sometimes hours until you get your results.

### Stream Processing

Gain instant insight into your data.

Streaming allows users to make quick decisions and take actions based on
"real-time" insight. Contrary to batch processing, streaming processes
data on the fly, as it comes in.

With streaming you don't have to wait minutes or hours to get results.
You gain instant insight into your data.

In the batch processing pipeline, the analytics was after the data
storage. It had access to all the available data.

Stream processing creates insight before the data storage. It has only
access to fragments of data as it comes in.

As a result the scope of the produced insight is also limited. Because
the big picture is missing.

![Stream Processing Pipeline](/images/Simple-Stream-Processing-Workflow.jpg)

Only with streaming analytics you are able to create advanced services
for the customer. Netflix for instance incorporated stream processing
into Chuckwa V2.0 and the new Keystone pipeline.

One example of advanced services through stream processing is the
Netflix "Trending Now" feature. Check out the Netflix case study.

#### Three methods of streaming

In stream processing sometimes it is ok to drop messages, other times it
is not. Sometimes it is fine to process a message multiple times, other
times that needs to be avoided like hell.

Today's topic are the different methods of streaming: At most once, at
least once and exactly once.

What this means and why it is so important to keep them in mind when
creating a solution. That is what you will find out in this article.

#### At Least Once

At least once, means a message gets processed in the system once or
multiple times. So with at least once it's not possible that a message
gets into the system and is not getting processed.

It's not getting dropped or lost somewhere in the system.

One example where at least once processing can be used is when you think
about a fleet management of cars. You get GPS data from cars and that
data is transmitted with a timestamp and the GPS coordinates.

It's important that you get the GPS data at least once, so you know
where the car is. If you're processing this data multiple times, it
always has the the timestamp with it.

Because of that it does not matter that it gets processed multiple
times, because of the timestamp. Or that it would be stored multiple
times, because it would just override the existing one.

#### At Most Once

The second streaming method is at most once. At most once means that
it's okay to drop some information, to drop some messages.

But it's important that a message is only processed once as a
maximum.

A example for this is event processing. Some event is happening and that
event is not important enough, so it can be dropped. It doesn't have any
consequences when it gets dropped.

But when that event happens it's important that it does not get
processed multiple times. Then it would look as if the event happened
five or six times instead of only one.

Think about engine misfires. If it happens once, no big deal. But if the
system tells you it happens a lot you will think you have a problem with
your engine.

#### Exactly Once

Another thing is exactly once, this means it's not okay to drop data,
it's not okay to lose data and it's also not okay to process data
multiple times.

An example for this is banking. When you think about credit card
transactions it's not okay to drop a transaction.

When dropped, your payment is not going through. It's also not okay to
have a transaction processed multiple times, because then you are paying
multiple times.

#### Check The Tools!

All of this sounds very simple and logical. What kind of processing is
done has to be a requirement for your use case.

It needs to be thought about in the design process, because not every
tool is supporting all three methods. Very often you need to code your
application very differently based on the streaming method.

Especially exactly once is very hard to do.

So, the tool of data processing needs to be chosen based on if you need
exactly once, at least once or if you need at most once.


### Should you do stream or batch processing?

It is a good idea to start with batch processing. Batch processing is
the foundation of every good big data platform.

A batch processing architecture is simple, and therefore quick to set
up. Platform simplicity means, it will also be relatively cheap to run.

A batch processing platform will enable you to quickly ask the big
questions. They will give you invaluable insight into your data and
customers.

When the time comes and you also need to do analytics on the fly, then
add a streaming pipeline to your batch processing big data platform.

### Is ETL still relevant for Analytics?

| Podcast Episode: #039 Is ETL Dead For Data Science & Big Data?
|------------------|
|Is ETL dead in Data Science and Big Data? In today’s podcast I share with you my views on your questions regarding ETL (extract, transform, load). Is ETL still practiced or did pre-processing & cleansing replace it. What would replace ETL in Data Engineering.
| [Watch on YouTube](https://youtu.be/leSOWPaNkl4) \ [Listen on Anchor](https://anchor.fm/andreaskayy/episodes/Is-ETL-Dead-For-Data-Science--Big-Data---PoDS-039-e2b604)|

### MapReduce

Since the early days of the Hadoop eco system, the MapReduce framework
is one of the main components of Hadoop alongside HDFS.

Google for instance used MapReduce to analyse stored HTML content of
websites through counting all the HTML tags and all the words and
combinations of them (for instance headlines). The output was then used
to create the page ranking for Google Search.

That was when everybody started to optimise his website for the google
search. Serious search engine optimisation was born. That was the year
2004.

How MapReduce is working is, that it processes data in two phases: The
map phase and the reduce phase.

In the map phase, the framework is reading data from HDFS. Each dataset
is called an input record.

Then there is the reduce phase. In the reduce phase, the actual
computation is done and the results are stored. The storage target can
either be a database or back HDFS or something else.

After all it's Java -- so you can implement what you like.

The magic of MapReduce is how the map and reduce phase are implemented
and how both phases are working together.

The map and reduce phases are parallelised. What that means is, that you
have multiple map phases (mappers) and reduce phases (reducers) that can
run in parallel on your cluster machines.

Here's an example how such a map and reduce process works with data:

![Mapping of input files and reducing of mapped records](/images/MapReduce-Process-Detailed.jpg)

#### How does MapReduce work

First of all, the whole map and reduce process relies heavily on using
key-value pairs. That's what the mappers are for.

In the map phase input data, for instance a file, gets loaded and
transformed into key-value pairs.

When each map phase is done it sends the created key-value pairs to the
reducers where they are getting sorted by key. This means, that an input
record for the reduce phase is a list of values from the mappers that
all have the same key.

Then the reduce phase is doing the computation of that key and its
values and outputting the results.

How many mappers and reducers can you use in parallel? The number of
parallel map and reduce processes depends on how many CPU cores you have
in your cluster. Every mapper and every reducer is using one core.

This means that the more CPU cores you actually have, the more mappers
you can use, the faster the extraction process can be done. The more
reducers you are using the faster the actual computation is being done.

To make this more clear, I have prepared an example:

#### Example

As I said before, MapReduce works in two stages, map and reduce. Often
these stages are explained with a word count task.

Personally, I hate this example because counting stuff is to trivial and
does not really show you what you can do with MapReduce. Therefore, we
are going to use a more real world use-case from the IoT world.

IoT applications create an enormous amount of data that has to be
processed. This data is generated by physical sensors who take
measurements, like room temperature at 8 o'clock.

Every measurement consists of a key (the timestamp when the measurement
has been taken) and a value (the actual value measured by the sensor).

Because you usually have more than one sensor on your machine, or
connected to your system, the key has to be a compound key. Compound
keys contain in addition to the measurement time information about the
source of the signal.

But, let's forget about compound keys for now. Today we have only one
sensor. Each measurement outputs key-value pairs like: Timestamp-Value.

The goal of this exercise is to create average daily values of that
sensor's data.

The image below shows how the map and reduce process works.

First, the map stage loads unsorted data (input records) from the source
(e.g. HDFS) by key and value (key:2016-05-01 01:02:03, value:1).

Then, because the goal is to get daily averages, the hour:minute:second
information is cut from the timestamp.

That is all that happens in the map phase, nothing more.

After all parallel map phases are done, each key-value pair gets sent to
the one reducer who is handling all the values for this particular key.

Every reducer input record then has a list of values and you can
calculate (1+5+9)/3, (2+6+7)/3 and (3+4+8)/3. That's all.

![MapReduce Example of Time Series Data](/images/MapReduce-Time-Series-example.jpg)

What do you think you need to do to generate minute averages?

Yes, you need to cut the key differently. You then would need to cut it
like this: "2016-05-01 01:02", keeping the hour and minute information
in the key.

What you can also see is, why map reduce is so great for doing parallel
work. In this case, the map stage could be done by nine mappers in
parallel because each map is independent from all the others.

The reduce stage could still be done by three tasks in parallel. One for
orange, one for blue and one for green.

That means, if your dataset would be 10 times as big and you'd have 10
times the machines, the time to do the calculation would be the same.

#### What is the limitation of MapReduce?

MapReduce is awesome for simpler analytics tasks, like counting stuff.
It just has one flaw: It has only two stages Map and Reduce.

![The Map Reduce Process](/images/MapReduce-Process.jpg)

First MapReduce loads the data from HDFS into the mapping function.
There you prepare the input data for the processing in the reducer.
After the reduce is finished the results get written to the data store.

The problem with MapReduce is that there is no simple way to chain
multiple map and reduce processes together. At the end of each reduce
process the data must be stored somewhere.

This fact makes it very hard to do complicated analytics processes. You
would need to chain MapReduce jobs together.

Chaining jobs with storing and loading intermediate results just makes
no sense.

Another issue with MapReduce is that it is not capable of streaming
analytics. Jobs take some time to spin up, do the analytics and shut
down. Basically Minutes of wait time are totally normal.

This is a big negative point in a more and more real time data
processing world.

### Apache Spark

I talked about the three methods of data streaming in this podcast:
<https://anchor.fm/andreaskayy/embed/episodes/Three-Methods-of-Streaming-Data-e15r6o>

#### What is the difference to MapReduce?

Spark is a complete in-memory framework. Data gets loaded from, for
instance HDFS, into the memory of workers.

There is no longer a fixed map and reduce stage. Your code can be as
complex as you want.

Once in memory, the input data and the intermediate results stay in
memory (until the job finishes). They do not get written to a drive like
with MapReduce.

This makes Spark the optimal choice for doing complex analytics. It
allows you for instance to do iterative processes. Modifying a dataset
multiple times in order to create an output is totally easy.

Streaming analytics capability is also what makes Spark so great. Spark
has natively the option to schedule a job to run every X seconds or X
milliseconds.

As a result, Spark can deliver you results from streaming data in "real
time".

#### How does Spark fit to Hadoop?

There are some very misleading articles out there titled \"Spark or
Hadoop\", \"Spark is better than Hadoop\" or even \"Spark is replacing
Hadoop\".

So, it's time to show you the differences between Spark and Hadoop.
After this you will know when and for what you should use Spark and
Hadoop.

You'll also understand why \"Hadoop or Spark\" is the totally wrong
question.

#### Where's the difference?

To make it clear how Hadoop differs from Spark I created this simple
feature table:

![Hadoop vs Spark capabilities](/images/Table-Hadoop-and-Spark.jpg)

Hadoop is used to store data in the Hadoop Distributed File System
(HDFS). It can analyse the stored data with MapReduce and manage
resources with YARN.

However, Hadoop is more than just storage, analytics and resource
management. There's a whole eco system of tools around the Hadoop core.
I've written about its eco system in this article: [missing](missing)
What is Hadoop and why is it so freakishly popular. You should check it
out as well.

Compared to Hadoop, Spark is "just" an analytics framework. It has no
storage capability. Although it has a standalone resource management,
you usually don't use that feature.

#### Spark and Hadoop is a perfect fit

So, if Hadoop and Spark are not the same things, can they work together?

Absolutely! Here's how the first picture will look if you combine Hadoop
with Spark:

missing

As Storage you use HDFS. Analytics is done with Apache Spark and YARN is
taking care of the resource management.

Why does that work so well together?

From a platform architecture perspective, Hadoop and Spark are usually
managed on the same cluster. This means on each server where a HDFS data
node is running, a Spark worker thread runs as well.

In distributed processing, network transfer between machines is a large
bottle neck. Transferring data within a machine reduces this traffic
significantly.

Spark is able to determine on which data node the needed data is stored.
This allows a direct load of the data from the local storage into the
memory of the machine.

This reduces network traffic a lot.

#### Spark on YARN:

You need to make sure that your physical resources are distributed
perfectly between the services. This is especially the case when you run
Spark workers with other Hadoop services on the same machine.

It just would not make sense to have two resource managers managing the
same server's resources. Sooner or later they will get in each others
way.

That's why the Spark standalone resource manager is seldom used.

So, the question is not Spark or Hadoop. The question has to be: Should
you use Spark or MapReduce alongside Hadoop's HDFS and YARN.

#### My simple rule of thumb:

If you are doing simple batch jobs like counting values or doing
calculating averages: Go with MapReduce.

If you need more complex analytics like machine learning or fast stream
processing: Go with Apache Spark.

#### Available Languages

Spark jobs can be programmed in a variety of languages. That makes
creating analytic processes very user-friendly for data scientists.

Spark supports Python, Scala and Java. With the help of SparkR you can
even connect your R program to a Spark cluster.

If you are a data scientist who is very familiar with Python just use
Python, its great. If you know how to code Java I suggest you start
using Scala.

Spark jobs are easier to code in Scala than in Java. In Scala you can
use anonymous functions to do processing.

This results in less overhead, it is a much cleaner, simpler code.

With Java 8 simplified function calls were introduced with lambda
expressions. Still, a lot of people, including me prefer Scala over
Java.

#### How Spark works: Driver, Executor, Sparkcontext

| Podcast Episode: #100 Apache Spark Week Day 1
|------------------|
|Is ETL dead in Data Science and Big Data? In today’s podcast I share with you my views on your questions regarding ETL (extract, transform, load). Is ETL still practiced or did pre-processing & cleansing replace it. What would replace ETL in Data Engineering.
| [Watch on YouTube](https://youtu.be/qD6Wi2pfCx0)


#### Spark batch vs stream processing

#### How does Spark use data from Hadoop

Another thing is data locality. I always make the point, that processing
data locally where it is stored is the most efficient thing to do.

That's exactly what Spark is doing. You can and should run Spark workers
directly on the data nodes of your Hadoop cluster.

Spark can then natively identify on what data node the needed data is
stored. This enables Spark to use the worker running on the machine
where the data is stored to load the data into the memory.

![Spark Using Hadoop Data Locality](/images/Spark-Data-Locality.jpg)

The downside of this setup is that you need more expensive servers.
Because Spark processing needs stronger servers with more RAM and CPUs
than a "pure" Hadoop setup.

#### What are RDDs and how to use them

RDDs are the core part of Spark. I learned and used RDDs first. It felt
familiar coming from MapReduce. Nowadays you use Dataframes or Datasets.

I still find it valuable to learn how RDDs and therefore Spark works at
a lower level.

| Podcast Episode: #101 Apache Spark Week Day 2
|------------------|
|On day two of the Apache Spark week we take a look at major Apache Spark concepts: RDDs, transformations and actions, caching and broadcast variables.
| [Watch on YouTube](https://youtu.be/9I6mA2W6_HU)


#### How and why to use SparkSQL?

When you use Apache Zeppelin notebooks to learn Spark you automatically
come across SparkSQL. SparkSQL allows you to access Dataframes with SQL
like queries.

Especially when you work with notebooks it is very handy to create
charts from your data. You can learn from mistakes easier than just
deploying Spark applications.

| Podcast Episode: #102 Apache Spark Week Day 3
|------------------|
| We continue the Spark week, hands on. We do a full example from reading a csv, doing maps and ﬂatmaps, to writing to disk. We also use SparkSQL to visualize the data.
| [Watch on YouTube](https://youtu.be/Fk-s8eKD4ZI)

#### What are DataFrames how to use them

As I said before. Dataframes are the successors to RDDs. It's the new
Spark API.

Dataframes are basically lake Tables in a SQL Database or like an Excel
sheet. This makes them very simple to use and manipulate with SparkSQL.
I highly recommend to go this route.

Processing with Dataframes is even faster then with RDDs, because it
uses optimization alogrithms for the data processing.

| Podcast Episode: #103 Apache Spark Week Day 4
|------------------|
|We look into Dataframes, Dataframes and Dataframes.
| [Watch on YouTube](https://youtu.be/9I6mA2W6_HU)

#### Machine Learning on Spark? (Tensor Flow)

Wouldn't it be great to use your deep learning TensorFlow applications
on Spark? Yes, it is already possible. Check out these Links:

Why do people integrate Spark with TensorFlow even if there is a
distributed TensorFlow framework?
<https://www.quora.com/Why-do-people-integrate-Spark-with-TensorFlow-even-if-there-is-a-distributed-TensorFlow-framework>

TensorFlow On Spark: Scalable TensorFlow Learning on Spark Clusters:
<https://databricks.com/session/tensorflow-on-spark-scalable-tensorflow-learning-on-spark-clusters>

Deep Learning with Apache Spark and TensorFlow:
<https://databricks.com/blog/2016/01/25/deep-learning-with-apache-spark-and-tensorflow.html>

#### MLlib:

The machine learning library MLlib is included in Spark so there is
often no need to import another library.

I have to admit because I am not a data scientist I am not an expert in
machine learning.

From what I have seen and read though the machine learning framework
MLlib is a nice treat for data scientists wanting to train and apply
models with Spark.

#### Spark Setup

From a solution architect's point of view Spark is a perfect fit for
Hadoop big data platforms. This has a lot to do with cluster deployment
and management.

Companies like Cloudera, MapR or Hortonworks include Spark into their
Hadoop distributions. Because of that, Spark can be deployed and managed
with the clusters Hadoop management web fronted.

This makes the process for deploying and configuring a Spark cluster
very quick and admin friendly.

#### Spark Resource Management

When running a computing framework you need resources to do computation:
CPU time, RAM, I/O and so on. Out of the box Spark can manage resources
with it's stand-alone resource manager.

If Spark is running in an Hadoop environment you don't have to use
Spark's own stand-alone resource manager. You can configure Spark to use
Hadoop's YARN resource management.

Why would you do that? It allows YARN to efficiently allocate resources
to your Hadoop and Spark processes.

Having a single resource manager instead of two independent ones makes
it a lot easier to configure the resource management.

![Spark Resource Management With YARN](/images/Spark-Yarn.jpg)

### Samza

[Link to Apache Samza Homepage](http://samza.apache.org/)

### AWS Lambda

[Link to AWS Lambda Homepage](https://aws.amazon.com/lambda/)


### Apache Flink

[Link to Apache Flink Homepage](https://flink.apache.org/)


### Elasticsearch

[Link to Elatsicsearch Homepage](https://www.elastic.co/products/elastic-stack)

### Graph DB

Graph databases store data in terms of nodes and relationships.
Each node represents an entity (people, movies, things and other
data points) and a relationship represents how the nodes are related.
They are designed to store and treat the relationships with the same
importance of that of the data (or nodes in this case). This
relationship-first approach makes a lot of difference as the relationship
between data need not be inferred anymore with foreign and primary keys.

Graph databases are especially useful when applications require
navigating through multiple and multi-level relationships between
various data points.

#### Neo4j

Neo4j is currently the most popular graph database management system.
It is ACID compliant and provides its own implementation of a graph database.
In addition to nodes and relationships, neo4j has the following components
to enrich the data model with information.

• Labels. These are used to group nodes, and each node can be assigned
multiple labels. Labels are indexed to speed up finding nodes in a graph.
• Properties. These are attributes of both nodes and relationships.
Neo4j allows for storing data as key-value pairs, which means properties
can have any value (string, number, or boolean).

##### Advantages

• Neo4j is schema-free
• Highly available and provides transactional guarantees
• Cypher is a declarative query language which makes it very easy to navigate the graph
• Neo4j is fast and easily traversible because the data is connected and is very easy to query, retrieve and navigate the graph
• For the same reason as above, there are no joins in Neo4j

##### Disadvantages

• Neo4j is not the best for any kind of aggregations or sorting, in comparison with a relational database
• While doable, they are not the best to handle transactional data like accounting
• Sharding is currently not supported

##### Use Cases

https://neo4j.com/use-cases/

### Apache Solr

[Link to Solr Homepage](https://solr.apache.org)


### Apache Drill

[Link to Apache Drill Homepage](https://drill.apache.org)


### Apache Storm

https://storm.apache.org/

### StreamSets

<https://youtu.be/djt8532UWow>

<https://www.youtube.com/watch?v=Qm5e574WoCU&t=2s>


<https://streamsets.com/blog/streaming-data-twitter-analysis-spark/>

## Store

### Analytical Data Stores

#### Data Warehouse vs Data Lake

| Podcast Episode: #055 Data Warehouse vs Data Lake
|------------------|
|On this podcast we are going to talk about data warehouses and data lakes? When do people use which? What are the pros and cons of both? Architecture examples for both Does it make sense to completely move to a data lake?
| [Watch on YouTube](https://youtu.be/8gNQTrUUwMk) \ [Listen on Anchor](https://anchor.fm/andreaskayy/episodes/055-Data-Warehouse-vs-Data-Lake-e45iem)|

#### Snowflake and dbt

![Snowlfake thumb](/images/03/Snowflake-dbt-thumbnail.jpeg)

In the rapidly evolving landscape of data engineering, staying ahead means continuously expanding your skill set with the latest tools and technologies. Among the myriad of options available, dbt (data build tool) and Snowflake have emerged as indispensable for modern data engineering workflows. Understanding and leveraging these tools can significantly enhance your ability to manage and transform data, making you a more effective and valuable data engineer. Let's dive into why dbt and Snowflake should be at the top of your learning list and explore how the "dbt for Data Engineers" and "Snowflake for Data Engineers" courses from the Learn Data Engineering Academy can help you achieve mastery in these tools.

##### The Power of Snowflake in Data Engineering

Snowflake has revolutionized the data warehousing space with its cloud-native architecture. It offers a scalable, flexible, and highly performant platform that simplifies data management and analytics. Here’s why Snowflake is a critical skill for data engineers:

1. **Cloud-Native Flexibility:** Snowflake’s architecture allows you to scale resources up or down based on your needs, ensuring optimal performance and cost-efficiency.
2. **Unified Data Platform:** It unifies data silos, enabling seamless data sharing and collaboration across the organization.
3. **Integration Capabilities:** Snowflake integrates with various data tools and platforms, enhancing its versatility in different data workflows.
4. **Advanced Analytics:** With its robust support for data querying, transformation, and integration, Snowflake is ideal for complex analytical workloads.

The "Snowflake for Data Engineers" course in my Learn Data Engineering Academy provides comprehensive training on Snowflake. From the basics of setting up your Snowflake environment to advanced data automation with Snowpipes, the course equips you with practical skills to leverage Snowflake effectively in your data projects.

Learn more about the course [here](https://learndataengineering.com/p/snowflake-for-data-engineers).

![Snowlfake thumb](/images/03/Snowflake-ui.jpeg)


##### Why dbt is a Game-Changer for Data Engineers

dbt is a powerful transformation tool that allows data engineers to transform, test, and document data directly within their data warehouse using simple SQL. Unlike traditional ETL tools, dbt operates on the principle of ELT (Extract, Load, Transform), which aligns perfectly with modern cloud data warehousing paradigms. Here are a few reasons why dbt is a must-have skill for data engineers:

1. **SQL-First Approach:** dbt allows you to write transformations in SQL, the lingua franca of data manipulation, making it accessible to a broad range of data professionals.
2. **Collaboration:** Teams can collaborate seamlessly, creating trusted datasets for reporting, machine learning, and operational workflows.
3. **Ease of Use:** With dbt, you can transform, test, and document your data with ease, streamlining the data pipeline process.
4. **Integration:** dbt integrates effortlessly with your existing data warehouse, such as Snowflake, making it a versatile addition to your toolkit.

In my Learn Data Engineering Academy you find the perfect starting point for mastering dbt with the course "dbt for Data Engineers". The course covers everything from the basics of ELT processes to advanced features like continuous integration and deployment (CI/CD) pipelines. With hands-on training, you'll learn to create data pipelines, configure dbt materializations, test dbt models, and much more.

Learn more about the course [here](https://learndataengineering.com/p/dbt-for-data-engineers).

![Snowlfake thumb](/images/03/dbt-ui.jpeg)

##### dbt and Snowflake: A Winning Combination

When used together, dbt and Snowflake offer a powerful combination for data engineering. Here’s why:

1. **Seamless Integration:** dbt’s SQL-first transformation capabilities integrate perfectly with Snowflake’s scalable data warehousing, creating a streamlined ELT workflow.
2. **Efficiency:** Together, they enhance the efficiency of data transformation and analytics, reducing the time and effort required to prepare data for analysis.
3. **Scalability:** The combined power of dbt’s model management and Snowflake’s dynamic scaling ensures that your data pipelines can handle large and complex datasets with ease.
4. **Collaboration and Documentation:** dbt’s ability to document and test data transformations directly within Snowflake ensures that data workflows are transparent, reliable, and collaborative.
Get right into it with our Academy!

By integrating Snowflake and dbt into your skill set, you position yourself at the forefront of data engineering innovation. These tools not only simplify and enhance your data workflows but also open up new possibilities for data transformation and analysis.

### Transactional Data Stores
#### SQL Databases

##### PostgreSQL DB

Homepage:

<https://www.postgresql.org/>

PostgreSQL vs MongoDB:

<https://blog.panoply.io/postgresql-vs-mongodb>

##### Database Design

##### SQL Queries

##### Stored Procedures

##### ODBC/JDBC Server Connections

#### NoSQL Stores

##### KeyValue Stores (HBase)


  | Podcast Episode: #056 NoSQL Key Value Stores Explained with HBase
  |------------------|
  |What is the diﬀerence between SQL and NoSQL? In this episode I show you on the example of HBase how a key/value store works.
  | [Watch on YouTube](https://youtu.be/67hIkbpzFc8) \ [Listen on Anchor](https://anchor.fm/andreaskayy/episodes/056-NoSQL-Key-Value-Stores-Explained-With-HBase-e45ifb)|


##### Document Store HDFS

The Hadoop distributed file system, or HDFS, allows you to store files
in Hadoop. The difference between HDFS and other file systems like NTFS
or EXT is that it is a distributed one.

What does that mean exactly?

A typical file system stores your data on the actual hard drive. It is
hardware dependent.

If you have two disks then you need to format every disk with its own
file system. They are completely separate.

You then decide on which disk you physically store your data.

HDFS works different to a typical file system. HDFS is hardware
independent.

Not only does it span over many disks in a server. It also spans over
many servers.

HDFS will automatically place your files somewhere in the Hadoop server
collective.

It will not only store your file, Hadoop will also replicate it two or
three times (you can define that). Replication means replicas of the
file will be distributed to different servers.

![HDFS Master and Data Nodes](/images/HDFS-Master-DataNodes.jpg)

This gives you superior fault tolerance. If one server goes down, then
your data stays available on a different server.

Another great thing about HDFS is, that there is no limit how big the
files can be. You can have server log files that are terabytes big.

How can files get so big? HDFS allows you to append data to files.
Therefore, you can continuously dump data into a single file without
worries.

HDFS physically stores files different then a normal file system. It
splits the file into blocks.

These blocks are then distributed and replicated on the Hadoop cluster.
The splitting happens automatically.

![Distribution of Blocks for a 512MB File](/images/HDFS-Distributed-FileSystem.jpg)

In the configuration you can define how big the blocks should be. 128
megabyte or 1 gigabyte?

No problem at all.

This mechanic of splitting a large file in blocks and distributing them
over the servers is great for processing. See the MapReduce section for
an example.

##### Document Store MongoDB


  | Podcast Episode: #093 What is MongoDB
  |------------------|
  |What is the diﬀerence between SQL and NoSQL? In this episode I show you on the example of HBase how a key/value store works.
  | [Watch on YouTube](https://youtu.be/U05knQN29FA)


**Links:**

What is MongoDB:

<https://www.guru99.com/what-is-mongodb.html#4>

Or directly from MongoDB.com:

<https://www.mongodb.com/what-is-mongodb>

Storage in BSON files:

<https://en.wikipedia.org/wiki/BSON>

Hello World in MongoDB:

<https://www.mkyong.com/mongodb/mongodb-hello-world-example>

Real-Time Analytics on MongoDB Data in Power BI:

<https://dzone.com/articles/real-time-analytics-on-mongodb-data-in-power-bi>

Spark and MongoDB:

<https://www.mongodb.com/scale/when-to-use-apache-spark-with-mongodb>

MongoDB vs Time Series Database:

<https://blog.timescale.com/how-to-store-time-series-data-mongodb-vs-timescaledb-postgresql-a73939734016/>

Fun article titled why you should never use mongodb:

<http://www.sarahmei.com/blog/2013/11/11/why-you-should-never-use-mongodb/>

MongoDB vs Cassandra:

<https://blog.panoply.io/cassandra-vs-mongodb>

##### Elasticsearch Search Engine and Document Store

Elasticsearch is not a DB but firstly a search engine that indexes JSON
documents.

| Podcast Episode: #095 What is Elasticsearch & Why is It So Popular?
|------------------|
|Elasticsearch is a super popular tool for indexing and searching data. On this stream we check out how it works, architectures and what to use it for. There must be a reason why it is so popular.  
| [Watch on YouTube](https://youtu.be/hNb5zB4OPXM)


Links:

Great example for architecture with Elasticsearch, Logstash and Kibana:\
<https://www.elastic.co/pdf/architecture-best-practices.pdf>

Introduction to Elasticsearch in the documentation:\
<https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html>

Working with JSON documents:\
<https://www.slideshare.net/openthinklabs/03-elasticsearch-data-in-data-out>

JSONs need to be flattened heres how to work with nested objects in the
JSON:\
<https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html>

Indexing basics:\
<https://www.slideshare.net/knoldus/deep-dive-into-elasticsearch>

How to do searches with search API:\
<https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html>

General recommendations when working with Elasticsearch:\
<https://www.elastic.co/guide/en/elasticsearch/reference/current/general-recommendations.html>

JSON document example and intro to Kibana:\
<https://www.slideshare.net/objectrocket/an-intro-to-elasticsearch-and-kibana>

How to connect Tableau to Elasticsearch:\
<https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-client-apps-tableau.html>

Benchmarks how fast Elasticsearch is:\
<https://medium.appbase.io/benchmarking-elasticsearch-1-million-writes-per-sec-bf37e7ca8a4c>

Elasticsearch vs MongoDB quick overview:\
<https://db-engines.com/en/system/Elasticsearch%3BMongoDB>

Logstash overview (preprocesses data before insert into Elasticsearch)
<https://www.elastic.co/products/logstash>

X-Pack Security for Elasticsearch:\
<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api.html>

Google Trends Grafana vs Kibana:\
<https://trends.google.com/trends/explore?geo=US&q=%2Fg%2F11fy132gmf,%2Fg%2F11cknd0blr>


##### Apache Impala

[Apache Impala Homepage](https://impala.apache.org/)

##### Kudu

##### Apache Druid

| Podcast Episode: Druid NoSQL DB and Analytics DB Introduction
|------------------|
|In this video I explain what Druid is and how it works. We look into the architecture of a Druid cluster and check out how Clients access the data.
|[Watch on YouTube](https://youtu.be/EiEIeBXSWjM)


##### InfluxDB Time Series Database

What is time-series data?

<https://questdb.io/blog/what-is-time-series-data/>

Key concepts:

<https://docs.influxdata.com/influxdb/v1.7/concepts/key_concepts/>

InfluxDB and Spark Streaming

<https://towardsdatascience.com/processing-time-series-data-in-real-time-with-influxdb-and-structured-streaming-d1864154cf8b>

Building a Streaming application with spark, grafana, chronogram and
influx:

<https://medium.com/@xaviergeerinck/building-a-real-time-streaming-dashboard-with-spark-grafana-chronograf-and-influxdb-e262b68087de>

Performance Dashboard Spark and InfluxDB:

<https://db-blog.web.cern.ch/blog/luca-canali/2019-02-performance-dashboard-apache-spark>

Other alternatives for time series databases are: DalmatinerDB,
QuestDB, Prometheus, Riak TS, OpenTSDB, KairosDB

##### MPP Databases (Greenplum)

##### Azure Cosmos DB

https://azure.microsoft.com/en-us/services/cosmos-db/

##### Azure Table-Storage

https://azure.microsoft.com/en-us/services/storage/tables/

#### NoSQL Data warehouse

##### Hive Warehouse

##### Impala

## Visualize

### Android & IOS

### How to design APIs for mobile apps

### How to use Webservers to display content

### Dashboards

#### Grafana

#### Kibana

#### Tomcat

#### Jetty

#### NodeRED

#### React

### Business Intelligence Tools

#### Tableau

#### PowerBI

#### Quliksense

### Identity & Device Management

#### What is a digital twin?

#### Active Directory


Machine Learning
----------------

| Podcast Episode: Machine Learning In Production
|------------------|
|Doing machine learning in production is very diﬀerent than for proof of concepts or in education. One of the hardest parts is keeping models updated.  
| [Listen on Anchor](https://anchor.fm/andreaskayy/episodes/Machine-Learning-In-Production-e11bbk)

### How to do Machine Learning in production

Machine learning in production is using stream and batch processing. In
the batch processing layer you are creating the models, because you have
all the data available for training.

In the stream in processing layer you are using the created models, you
are applying them to new data.

The idea that you need to incorporate is that it is a constant cycle.
Training, applying, re-training, pushing into production and applying.

What you don't want to do is doing this manually. You need to figure out
a process of automatic retraining and automatic pushing to into
production of models.

In the retraining phase the system automatically evaluates the training.
If the model no longer fits it works as long as it needs to create a
good model.

After the evaluation of the model is complete and it's good, the model
gets pushed into production. Into the stream processing.

### Why machine learning in production is harder then you think

How to automate machine learning is something that drives me day in and
day out.

What you do in development or education is, that you create a model and
fit it to the data. Then that model is basically done forever.

Where I'm coming from, the IoT world, the problem is that machines are
very different. They behave very different and experience wear.

### Models Do Not Work Forever

Machines have certain processes that decrease the actual health of the
machine. Machine wear is a huge issue. Models that that are built on top
of a good machine don't work forever.

When the Machine wears out, the models need to be adjusted. They need to
be maintained, retrained.

### Where The Platforms That Support This?

Automatic re-training and re-deploying is a very big issue, a very big
problem for a lot of companies. Because most existing platforms don't
have this capability (I actually haven't seen one until now).

Look at AWS machine learning for instance. The process is: build, train,
tune deploy. Where's the loop of retraining?

You can create models and then use them in production. But this loop is
almost nowhere to be seen.

It is a very big issue that needs to be solved. If you want to do
machine learning in production you can start with manual interaction of
the training, but at some point you need to automate everything.

### Training Parameter Management

To train a model you are manipulating input parameters of the models.

Take deep learning for instance.

To train you are manipulating for instance:

\- How many layers do you use. - The depth of the layers, which means
how many neurons you have in a layer. - What activation function you
use, how long are you training and so on.

You also need to keep track of what data you used to train which model.

All those parameters need to be manipulated automatically, models
trained and tested.

To do all that, you basically need a database that keeps track of those
variables.

How to automate this, for me, is like the big secret. I am still working
on figuring it out.

### What's Your Solution?

Did you already have the problem of automatic re-training and deploying
of models as well?

Were you able to use a cloud platform like Google, AWS or Azure?

It would be really awesome if you share your experience :)

### How to convince people machine learning works

Many people still are not convinced that machine learning works
reliably. But they want analytics insight and most of the time machine
learning is the way to go.

This means, when you are working with customers you need to do a lot of
convincing. Especially if they are not into machine learning themselves.

But it's actually quite easy.

### No Rules, No Physical Models

Many people are still under the impression that analytics only works
when it's based on physics. When there are strict mathematical rules to
a problem.

Especially in engineering heavy countries like Germany this is the norm:

"Sere has to be a Rule for Everysing!" (imagine a German accent). When
you're engineering you are calculating stuff based on physics and not
based on data. If you are constructing an airplane wing, you better make
sure to use calculations so it doesn't fall off.

And that's totally fine.

Keep doing that!

Machine learning has been around for decades. It didn't quite work as
good as people hoped. We have to admit that. But there is this
preconception that it still doesn't work.

Which is not true: Machine learning works.

Somehow you need to convince people that it is a viable approach. That
learning from data to make predictions is working perfectly.

### You Have The Data. USE IT!

As a data scientist you have one ace up your sleeve, it's the obvious
one:

It's the data and it's statistics.

You can use that data and those statistics to counter peoples
preconceptions. It's very powerful if someone says: "This doesn't work"

You bring the data. You show the statistics and you show that it works
reliably.

A lot of discussions end there.

Data doesn't lie. You can't fight data. The data is always right.

### Data is Stronger Than Opinions

This is also why I believe that autonomous driving will come quicker
than many of us think. Because a lot of people say, they are not safe.
That you cannot rely on those cars.

The thing is: When you have the data you can do the statistics.

You can show people that autonomous driving really works reliably. You
will see, the question of \"Is this allowed or is this not allowed?\"
will be gone quicker than you think.

Because government agencies can start testing the algorithms based on
predefined scenarios. They can run benchmarks and score the cars
performance.

All those opinions, if it works, or if it doesn't work, they will be
gone.

The motor agency has the statistics. The stats show people how good cars
work.

Companies like Tesla, they have it very easy. Because the data is
already there.

**They just need to show us that the algorithms work. The end.**

### AWS Sagemaker

Train and apply models online with Sagemaker

Link to the OLX Slideshare with pros, cons and how to use Sagemaker:
<https://www.slideshare.net/mobile/AlexeyGrigorev/image-models-infrastructure-at-olx>


---

Data Engineering Course: Building A Data Platform
=================================================

## Contents

- GenAI Retrieval Augmented Generation with Ollama and Elasticsearch
- Free Data Engineering Course with AWS, TDengine, Docker and Grafana
- Monitor your data in dbt & detect quality issues with Elementary
- Solving Engineers 4 Biggest Airflow Problems
- The best alternative to Airlfow? Mage.ai

## GenAI Retrieval Augmented Generation with Ollama and Elasticsearch

- This how-to is based on this one from Elasticsearch: https://www.elastic.co/search-labs/blog/rag-with-llamaIndex-and-elasticsearch
- Instead of Elasticsearch cloud we're going to run everything locally
- The simplest way to get this done is to just clone this GitHub Repo for the code and docker setup
- I've tried this on a M1 Mac. Changes for Windows with WSL will come later.
- The biggest problems that I had were actually installing the dependencies rather than the code itself.

### Install Ollama
1. Download Ollama from here https://ollama.com/download/mac
2. Unzip, drag into applications and install
3. do `ollama run mistral` (It's going to download the Mistral 7b model, 4.1GB size)
4. Create a new folder in Documents "Elasticsearch-RAG"
5. Open that folder in VSCode

### Install Elasticsearch & Kibana (Docker)
1. Use the docker-compose file from this repo: https://github.com/andkret/Cookbook/blob/master/Code%20Examples/GenAI-RAG/docker-compose.yml
2. Download Docker Desktop from here: https://www.docker.com/products/docker-desktop/
3. Install docker desktop and sign in in the app/create a user -> sends you to the browser

**For Windows Users**
Configure WSL2 to use max only 4GB of ram:
```
wsl --shutdown
notepad "$env:USERPROFILE/.wslconfig"
```
.wslconfig file:
```
[wsl2]
memory=4GB   # Limits VM memory in WSL 2 up to 4GB
```
**Modify the Linux kernel map count in WSL**
Do this before the start because Elasticsearch requires a higher value to work
`sudo sysctl -w vm.max_map_count=262144`

4. go to the Elasticsearch-RAG folder and do `docker compose up`
5. make sure you have Elasticsearch 8.11 or later (we use 8.16 here in this project) if you want to use your own Elasticsearch image
6. if you get this error on a mac then just open the console in the docker app: *error getting credentials - err: exec: docker-credential-desktop: executable file not found in $PATH, out:*
7. Install xcode command line tools: `xcode-select --install`
8. make sure you're at python 3.8.1 or larger -> installed 3.13.0 from https://www.python.org/downloads/

### Setup the virtual Python environment

#### preparation on a Mac
##### install brew
which brew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
export PATH="/opt/homebrew/bin:$PATH"
brew --version
brew install pyenv
brew install pyenv-virtualenv

##### install pyenv
```
brew install pyenv
brew install pyenv-virtualenv
```

Modify the path so that pyenv is in the path variable
`nano ~/.zshrc`

```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

install dependencies for building python versions
`brew install openssl readline sqlite3 xz zlib`

Reload to apply changes
`source ~/.zshrc`

install python
```
pyenv install 3.11.6
pyenv version
```

Set Python version system wide
`pyenv global 3.11.6`

```
pyenv virtualenv <python-version> <new-virtualenv-name>
pyenv activate <your-virtualenv-name>
pyenv virtualenv-delete <your-virtualenv-name>
```

#### Windows without pyenv
setup virtual python environment - go to the Elasticsearch-RAG folder and do
`python3 -m venv .elkrag`
enable the environment
`source .elkrag/bin/activate`


### Install required libraries (do one at a time so you see errors):
```
pip install llama-index (optional python3 -m pip install package name)
pip install llama-index-embeddings-ollama
pip install llama-index-llms-ollama
pip install llama-index-vector-stores-elasticsearch
pip install python-dotenv
```

### Write the data to Elasticsearch
1. create / copy in the index.py file
2. download the conversations.json file from the folder code examples/GenAI-RAG
3. if you get an error with the execution then check if pedantic version is <2.0 `pip show pydantic` if not do this: `pip install "pydantic<2.0`
4. run the program index.py: https://github.com/andkret/Cookbook/blob/master/Code%20Examples/GenAI-RAG/index.py

### Check the data in Elasticsearch
1. go to kibana http://localhost:5601/app/management/data/index_management/indices and see the new index called calls
2. go to dev tools and try out this query `GET calls/_search?size=1 http://localhost:5601/app/dev_tools#/console/shell`

### Query data from elasticsearch and create an output with Mistral
1. if everything is good then run the query.py file https://github.com/andkret/Cookbook/blob/master/Code%20Examples/GenAI-RAG/query.py
2. try a few queries :)

### Install libraries to extract text from pdfs


### Extract data from CV and put it into Elasticsearch
I created a CV with ChatGPT https://github.com/andkret/Cookbook/blob/master/Code%20Examples/GenAI-RAG/Liam_McGivney_CV.pdf

Install the library to extract text from the pdf
`pip install PyMuPDF`
I had to Shift+Command+p then python clear workspace cache and reload window. Then it saw it :/

The file cvpipeline.py has the python code for the indexing. It's not working right now though!
https://github.com/andkret/Cookbook/blob/master/Code%20Examples/GenAI-RAG/cvpipeline.py


I'll keep developing this and update it once it's working.


## Free Data Engineering Course with AWS TDengine Docker and Grafana

**Free hands-on course:** [Watch on YouTube](https://youtu.be/eoj-CnrR9jA)

In this detailed tutorial video, Andreas guides viewers through creating an end-to-end data pipeline using time series data. The project focuses on fetching weather data from a Weather API, processing it on AWS, storing it in TDengine (a time series database), and visualizing the data with Grafana. Here's a concise summary of what the video covers:

1. **Introduction and Setup:**
  - The project is introduced along with a GitHub repository containing all necessary resources and a step-by-step guide.
  - The pipeline architecture includes an IoT weather station, a Weather API, AWS for processing, TDengine for data storage, and Grafana for visualization.
2. **Project Components:**
  - **Weather API:** Utilizes weatherapi.com to fetch weather data.
  - **AWS Lambda:** Processes the data fetched from the Weather API.
  - **TDengine:** Serves as the time series database to store processed data. It's highlighted for its performance and simplicity, especially for time series data.
  - **Grafana:** Used for creating dashboards to visualize the time series data.
3. **Development and Deployment:**
  - The local development environment setup includes Python, Docker, and VS Code.
  - The tutorial covers the creation of a Docker image for the project and deploying it to AWS Elastic Container Registry (ECR).
  - AWS Lambda is then configured to use the Docker image from ECR.
  - AWS EventBridge is used to schedule the Lambda function to run at specified intervals.
4. **Time Series Data:**
  - The importance of time series data and the benefits of using a time series database like TDengine over traditional relational databases are discussed.
  - TDengine's features such as speed, scaling, data retention, and built-in functions for time series data are highlighted.
5. **Building the Pipeline:**
  - Detailed instructions are provided for setting up each component of the pipeline:
    - Fetching weather data from the Weather API.
    - Processing and sending the data to TDengine using an AWS Lambda function.
    - Visualizing the data with Grafana.
  - Each step includes code snippets and configurations needed to implement the pipeline.
6. **Conclusion:**
  - The video concludes with a demonstration of the completed pipeline, showing weather data visualizations in Grafana.
  - Viewers are encouraged to replicate the project using the resources provided in the GitHub repository linked in the video description.

This video provides a comprehensive guide to building a data pipeline with a focus on time series data, demonstrating the integration of various technologies and platforms to achieve an end-to-end solution.

## Monitor your data in dbt and detect quality issues with Elementary

**Free hands-on tutorial:** [Watch on YouTube](https://youtu.be/6fnU91Q2gq0)

In this comprehensive tutorial, Andreas delves into the integration of dbt (data build tool) with Elementary to enhance data monitoring and quality detection within Snowflake databases. The tutorial is structured to guide viewers through a hands-on experience, starting with an introduction to a sample project setup and the common challenges faced in monitoring dbt jobs. It then transitions into how Elementary can be utilized to address these challenges effectively.

Key learning points and tutorial structure include:

1. **Introduction to the Sample Project:** Andreas showcases a project setup involving Snowflake as the data warehouse, dbt for data modeling and testing, and a visualization tool for data analysis. This setup serves as the basis for the tutorial.
2. **Challenges in Monitoring dbt Jobs:** Common issues in monitoring dbt jobs are discussed, highlighting the limitations of the dbt interface in providing comprehensive monitoring capabilities.
3. **Introduction to Elementary:** Elementary is introduced as a dbt-native data observability tool designed to enhance the monitoring and analysis of dbt jobs. It offers both open-source and cloud versions, with the tutorial focusing on the cloud version.
4. **Setup Requirements:** The tutorial covers the necessary setup on both the Snowflake and dbt sides, including schema creation, user and role configuration in Snowflake, and modifications to the dbt project for integrating with Elementary.
5. **Elementary's User Interface and Features:** A thorough walkthrough of Elementary's interface is provided, showcasing its dashboard, test results, model runs, data catalog, and data lineage features. The tool's ability to automatically run additional tests, like anomaly detection and schema change detection, is also highlighted.
6. **Advantages of Using Elementary:** The presenter outlines several benefits of using Elementary, such as easy implementation, native test integration, clean and straightforward UI, and enhanced privacy due to data being stored within the user's data warehouse.
7. **Potential Drawbacks:** Some potential drawbacks are discussed, including the additional load on dbt job execution due to more models being run and limitations in dashboard customization.
8. **Summary and Verdict:** The tutorial concludes with a summary of the key features and benefits of using Elementary with dbt, emphasizing its value in improving data quality monitoring and detection.

Overall, viewers are guided through setting up and utilizing Elementary for dbt data monitoring, gaining insights into its capabilities, setup process, and the practical benefits it offers for data quality assurance.


## Solving Engineers 4 Biggest Airflow Problems

**Free hands-on tutorial:** [Watch on YouTube](https://youtu.be/b9bMNEh8bes)

In this informative video, Andreas discusses the four major challenges engineers face when working with Apache Airflow and introduces Astronomer, a managed Airflow service that addresses these issues effectively. Astronomer is highlighted as a solution that simplifies Airflow deployment and management, making it easier for engineers to develop, deploy, and monitor their data pipelines. Here's a summary of the key points discussed for each challenge and how Astronomer provides solutions:

1. Managing Airflow Deployments:
  - **Challenge:** Setting up and maintaining Airflow deployments is complex and time-consuming, involving configuring cloud instances, managing resources, scaling, and updating the Airflow system.
  - **Solution with Astronomer:** Offers a straightforward deployment process where users can easily configure their deployments, choose cloud providers (GCP, AWS, Azure), and set up scaling with just a few clicks. Astronomer handles the complexity, making it easier to manage production and quality environments.
2. Development Environment and Deployment:
  - **Challenge:** Local installation of Airflow is complicated due to its dependency on multiple Docker containers and the need for extensive configuration.
  - **Solution with Astronomer:** Provides a CLI tool for setting up a local development environment with a single command, simplifying the process of developing, testing, and deploying pipelines. The Astronomer CLI also helps in initializing project templates and deploying Dags to the cloud effortlessly.
3. Source Code Management and CI/CD Pipelines:
  - **Challenge:** Collaborative development and continuous integration/deployment (CI/CD) are essential but challenging to implement effectively with Airflow alone.
  - **Solution with Astronomer:** Facilitates easy integration with GitHub for source code management and GitHub Actions for CI/CD. This allows automatic testing and deployment of pipeline code, ensuring a smooth workflow for teams working on pipeline development.
4. Observing Pipelines and Alarms:
  - **Challenge:** Monitoring data pipelines and getting timely alerts when issues occur is crucial but often difficult to achieve.
  - **Solution with Astronomer:** The Astronomer platform provides a user-friendly interface for monitoring pipeline status and performance. It also offers customizable alerts for failures or prolonged task durations, with notifications via email, PagerDuty, or Slack, ensuring immediate awareness and response to issues.

Overall, the video shows Astronomer as a powerful and user-friendly platform that addresses the common challenges of using Airflow, from deployment and development to collaboration, CI/CD, and monitoring. It suggests that Astronomer can significantly improve the experience of engineers working with Airflow, making it easier to manage, develop, and monitor data pipelines.


## The best alternative to Airlfow? Mage.ai

**Free hands-on tutorial:** [Watch on YouTube](https://youtu.be/3gXsFEC3aYA)

In this insightful video, Andreas introduces Mage, a promising alternative to Apache Airflow, focusing on its simplicity, user-friendliness, and scalability. The video provides a comprehensive walkthrough of Mage, highlighting its key features and advantages over Airflow. Here's a breakdown of what viewers can learn and expect from the video:

1. **Deployment Ease:** Mage offers a stark contrast to Airflow's complex setup process. It simplifies deployment to a single Docker image, making it straightforward to install and start on any machine, whether it's local or cloud-based on AWS, GCP, or Azure. This simplicity extends to scaling, which Mage handles horizontally, particularly beneficial in Kubernetes environments where performance scales with the number of pipelines.
2. **User Interface (UI):** Mage shines with its UI, presenting a dark mode interface that's not only visually appealing but also simplifies navigation and pipeline management. The UI facilitates easy access to pipelines, scheduling, and monitoring of pipeline runs, offering a more intuitive experience compared to Airflow.
3. **Pipeline Creation and Modification:** Mage streamlines the creation of ETL pipelines, allowing users to easily add data loaders, transformers, and exporters through its UI. It supports direct interaction with APIs for data loading and provides a visual representation of the data flow, enhancing the overall pipeline design experience.
4. **Data Visualization and Exploration:** Beyond simple pipeline creation, Mage enables in-depth data exploration within the UI. Users can generate various charts, such as histograms and bar charts, to analyze the data directly, a feature that greatly enhances the tool's utility.
5. **Testing and Scheduling:** Testing pipelines in Mage is straightforward, allowing for quick integration of tests to ensure data quality and pipeline reliability. Scheduling is also versatile, supporting standard time-based triggers, event-based triggers for real-time data ingestion, and API calls for on-demand pipeline execution.
6. **Support for Streaming and ELT Processes:** Mage is not limited to ETL workflows but also supports streaming and ELT processes. It integrates seamlessly with DBT models for in-warehouse transformations and Spark for big data processing, showcasing its versatility and scalability.
7. **Conclusion and Call to Action:** Andreas concludes by praising the direction in which the industry is moving, with tools like Mage simplifying data engineering processes. He encourages viewers to try Mage and engage with the content by liking, subscribing, and commenting on their current tools and the potential impact of Mage.

Overall, the video shows Mage as a highly user-friendly, scalable, and versatile tool for data pipeline creation and management, offering a compelling alternative to traditional tools like Airflow.


---

Case Studies
============

## Contents

- Data Science @Airbnb
- Data Science @Amazon
- Data Science @Baidu
- Data Science @Blackrock
- Data Science @BMW
- Data Science @Booking.com
- Data Science @CERN
- Data Science @Disney
- Data Science @DLR
- Data Science @Drivetribe
- Data Science @Dropbox
- Data Science @Ebay
- Data Science @Expedia
- Data Science @Facebook
- Data Science @Google
- Data Science @Grammarly
- Data Science @ING Fraud
- Data Science @Instagram
- Data Science @LinkedIn
- Data Science @Lyft
- Data Science @NASA
- Data Science @Netflix
- Data Science @OLX
- Data Science @OTTO
- Data Science @Paypal
- Data Science @Pinterest
- Data Science @Salesforce
- Data Science @Siemens Mindsphere
- Data Science @Slack
- Data Science @Spotify
- Data Science @Symantec
- Data Science @Tinder
- Data Science @Twitter
- Data Science @Uber
- Data Science @Upwork
- Data Science @Woot
- Data Science @Zalando



How I do Case Studies
---------------------

### Data Science at Airbnb

| Podcast Episode: #063 Data Engineering At Airbnb Case Study
|------------------|
|How Airbnb is doing data engineering? Let’s check it out.
| Watch on YouTube \ Listen on Anchor|


**Slides:**

<https://medium.com/airbnb-engineering/airbnb-engineering-infrastructure/home>

Airbnb Engineering Blog: <https://medium.com/airbnb-engineering>

Data Infrastructure:
<https://medium.com/airbnb-engineering/data-infrastructure-at-airbnb-8adfb34f169c>

Scaling the serving tier:
<https://medium.com/airbnb-engineering/unlocking-horizontal-scalability-in-our-web-serving-tier-d907449cdbcf>

Druid Analytics:
<https://medium.com/airbnb-engineering/druid-airbnb-data-platform-601c312f2a4c>

Spark Streaming for logging events:
<https://medium.com/airbnb-engineering/scaling-spark-streaming-for-logging-event-ingestion-4a03141d135d>

-Druid Wiki: <https://en.wikipedia.org/wiki/Apache_Druid>

### Data Science at Amazon

<https://aws.amazon.com/solutions/case-studies/amazon-migration-analytics/>

### Data Science at Baidu

<https://www.slideshare.net/databricks/spark-sql-adaptive-execution-unleashes-the-power-of-cluster-in-large-scale-with-chenzhao-guo-and-carson-wang>

### Data Science at Blackrock

<https://www.slideshare.net/DataStax/maintaining-consistency-across-data-centers-randy-fradin-blackrock-cassandra-summit-2016>

### Data Science at BMW

<https://www.unibw.de/code/events-u/jt-2018-workshops/ws3_bigdata_vortrag_widmann.pdf>

### Data Science at Booking.com

| Podcast Episode: #064 Data Engineering at Booking.com Case Study
|------------------|
|How Booking.com is doing data engineering? Let’s check it out.
| Watch on YouTube \ Listen on Anchor|

**Slides:**

<https://www.slideshare.net/ConfluentInc/data-streaming-ecosystem-management-at-bookingcom?ref=https://www.confluent.io/kafka-summit-sf18/data-streaming-ecosystem-management>

<https://www.slideshare.net/SparkSummit/productionizing-behavioural-features-for-machine-learning-with-apache-spark-streaming-with-ben-teeuwen-and-roman-studenikin>

<https://www.slideshare.net/ConfluentInc/data-streaming-ecosystem-management-at-bookingcom?ref=https://www.confluent.io/kafka-summit-sf18/data-streaming-ecosystem-management>

Druid:
<https://towardsdatascience.com/introduction-to-druid-4bf285b92b5a>

Kafka Architecture:
<https://data-flair.training/blogs/kafka-architecture/>

Confluent Platform:
<https://www.confluent.io/product/confluent-platform/>

### Data Science at CERN

| Podcast Episode: #065 Data Engineering At CERN Case Study
|------------------|
|How is CERN doing Data Engineering? They must get huge amounts of data from the Large Hadron Collider. Let’s check it out.
| Watch on YouTube \ Listen on Anchor|


**Slides:**

<https://en.wikipedia.org/wiki/Large_Hadron_Collider>

<http://www.lhc-facts.ch/index.php?page=datenverarbeitung>


<https://www.slideshare.net/SparkSummit/next-cern-accelerator-logging-service-with-jakub-wozniak>

<https://databricks.com/session/the-architecture-of-the-next-cern-accelerator-logging-service>

<http://opendata.cern.ch>

<https://gobblin.apache.org>

<https://www.slideshare.net/databricks/cerns-next-generation-data-analysis-platform-with-apache-spark-with-enric-tejedor>

<https://www.slideshare.net/SparkSummit/realtime-detection-of-anomalies-in-the-database-infrastructure-using-apache-spark-with-daniel-lanza-and-prasanth-kothuri>

### Data Science at Disney

<https://medium.com/disney-streaming/delivering-data-in-real-time-via-auto-scaling-kinesis-streams-72a0236b2cd9>

### Data Science at DLR

<https://www.unibw.de/code/events-u/jt-2018-workshops/ws3_bigdata_vortrag_bamler.pdf>

### Data Science at Drivetribe

<https://berlin-2017.flink-forward.org/kb_sessions/drivetribes-kappa-architecture-with-apache-flink/>

<https://www.slideshare.net/FlinkForward/flink-forward-berlin-2017-aris-kyriakos-koliopoulos-drivetribes-kappa-architecture-with-apache-flink>

### Data Science at Dropbox

<https://blogs.dropbox.com/tech/2019/01/finding-kafkas-throughput-limit-in-dropbox-infrastructure/>

### Data Science at Ebay

<https://www.slideshare.net/databricks/moving-ebays-data-warehouse-over-to-apache-spark-spark-as-core-etl-platform-at-ebay-with-kim-curtis-and-brian-knauss>
<https://www.slideshare.net/databricks/analytical-dbms-to-apache-spark-auto-migration-framework-with-edward-zhang-and-lipeng-zhu>

### Data Science at Expedia

<https://www.slideshare.net/BrandonOBrien/spark-streaming-kafka-best-practices-w-brandon-obrien>
<https://www.slideshare.net/Naveen1914/brandon-obrien-streamingdata>

### Data Science at Facebook

<https://code.fb.com/core-data/apache-spark-scale-a-60-tb-production-use-case/>

### Data Science at Google

<http://www.unofficialgoogledatascience.com/>\
<https://ai.google/research/teams/ai-fundamentals-applications/>\
<https://cloud.google.com/solutions/big-data/>\
<https://datafloq.com/read/google-applies-big-data-infographic/385>

### Data Science at Grammarly

<https://www.slideshare.net/databricks/building-a-versatile-analytics-pipeline-on-top-of-apache-spark-with-mikhail-chernetsov>

### Data Science at ING Fraud

<https://sf-2017.flink-forward.org/kb_sessions/streaming-models-how-ing-adds-models-at-runtime-to-catch-fraudsters/>

### Data Science at Instagram

<https://www.slideshare.net/SparkSummit/lessons-learned-developing-and-managing-massive-300tb-apache-spark-pipelines-in-production-with-brandon-carl>

### Data Science at LinkedIn

| Podcast Episode: #073 Data Engineering At LinkedIn Case Study
|------------------|
|Let’s check out how LinkedIn is processing data :)
| Watch on YouTube \ Listen on Anchor|


**Slides:**

<https://engineering.linkedin.com/teams/data#0>

<https://www.slideshare.net/yaelgarten/building-a-healthy-data-ecosystem-around-kafka-and-hadoop-lessons-learned-at-linkedin>

<https://thirdeye.readthedocs.io/en/latest/about.html>

<http://samza.apache.org>

<https://www.slideshare.net/ConfluentInc/more-data-more-problems-scaling-kafkamirroring-pipelines-at-linkedin?ref=https://www.confluent.io/kafka-summit-sf18/more_data_more_problems>

<https://www.slideshare.net/KhaiTran17/conquering-the-lambda-architecture-in-linkedin-metrics-platform-with-apache-calcite-and-apache-samza>

<https://www.slideshare.net/Hadoop_Summit/unified-batch-stream-processing-with-apache-samza>

<http://druid.io/docs/latest/design/index.html>

### Data Science at Lyft

<https://eng.lyft.com/running-apache-airflow-at-lyft-6e53bb8fccff>

### Data Science at NASA

| Podcast Episode: #067 Data Engineering At NASA Case Study
|------------------|
|A look into how NASA is doing data engineering.
| Watch on YouTube \ Listen on Anchor|


**Slides:**

<https://esip.figshare.com/articles/Apache_Science_Data_Analytics_Platform/5786421>

<http://www.socallinuxexpo.org/sites/default/files/presentations/OnSightCloudArchitecture-scale14x.pdf>

<https://www.slideshare.net/SparkSummit/spark-at-nasajplchris-mattmann?qid=90968554-288e-454a-b63a-21a45cfc897d&v=&b=&from_search=4>

<https://en.m.wikipedia.org/wiki/Hierarchical_Data_Format>

### Data Science at Netflix

| Podcast Episode: #062 Data Engineering At Netﬂix Case Study
|------------------|
|How Netﬂix is doing Data Engineering using their Keystone platform.
| Watch on YouTube \ Listen on Anchor|


Netflix revolutionized how we watch movies and TV. Currently over 75
million users watch 125 million hours of Netflix content every day!

Netflix's revenue comes from a monthly subscription service. So, the
goal for Netflix is to keep you subscribed and to get new subscribers.

To achieve this, Netflix is licensing movies from studios as well as
creating its own original movies and TV series.

But offering new content is not everything. What is also very important
is, to keep you watching content that already exists.

To be able to recommend you content, Netflix is collecting data from
users. And it is collecting a lot.

Currently, Netflix analyses about 500 billion user events per day. That
results in a stunning 1.3 Petabytes every day.

All this data allows Netflix to build recommender systems for you. The
recommenders are showing you content that you might like, based on your
viewing habits, or what is currently trending.

###### The Netflix batch processing pipeline

When Netflix started out, they had a very simple batch processing system
architecture.

The key components were Chuckwa, a scalable data collection system,
Amazon S3 and Elastic MapReduce.

![Old Netflix Batch Processing Pipeline[]{label="fig:Bild1"}](/images/Netflix-Chuckwa-Pipeline.jpg){#fig:Bild1
width="90%"}

Chuckwa wrote incoming messages into Hadoop sequence files, stored in
Amazon S3. These files then could be analysed by Elastic MapReduce jobs.

Netflix batch processing pipeline Jobs were executed regularly on a
daily and hourly basis. As a result, Netflix could learn how people used
the services every hour or once a day.

###### Know what customers want:

Because you are looking at the big picture you can create new products.
Netflix uses insight from big data to create new TV shows and movies.

They created House of Cards based on data. There is a very interesting
TED talk about this you should watch:

[How to use data to make a hit TV show \| Sebastian
Wernicke](https://www.youtube.com/watch?v=vQILP19qABk)

Batch processing also helps Netflix to know the exact episode of a TV
show that gets you hooked. Not only globally but for every country where
Netflix is available.

Check out the article from TheVerge

They know exactly what show works in what country and what show does
not.

It helps them create shows that work in everywhere or select the shows
to license in different countries. Germany for instance does not have
the full library that Americans have :(

We have to put up with only a small portion of TV shows and movies. If
you have to select, why not select those that work best.

###### Batch processing is not enough

As a data platform for generating insight the Cuckwa pipeline was a good
start. It is very important to be able to create hourly and daily
aggregated views for user behavior.

To this day Netflix is still doing a lot of batch processing jobs.

The only problem is: With batch processing you are basically looking
into the past.

For Netflix, and data driven companies in general, looking into the past
is not enough. They want a live view of what is happening.

###### The trending now feature

One of the newer Netflix features is "Trending now". To the average user
it looks like that "Trending Now" means currently most watched.

This is what I get displayed as trending while I am writing this on a
Saturday morning at 8:00 in Germany. But it is so much more.

What is currently being watched is only a part of the data that is used
to generate "Trending Now".

![Netflix Trending Now Feature[]{label="fig:Bild1"}](/images/Netflix-Trending-Now-Screenshot.jpg){#fig:Bild1
width="90%"}

"Trending now" is created based on two types of data sources: Play
events and Impression events.

What messages those two types actually include is not really
communicated by Netflix. I did some research on the Netflix Techblog and
this is what I found out:

Play events include what title you have watched last, where you did stop
watching, where you used the 30s rewind and others. Impression events
are collected as you browse the Netflix Library like scroll up and down,
scroll left or right, click on a movie and so on.

Basically, play events log what you do while you are watching.
Impression events are capturing what you do on Netflix, while you are
not watching something.

###### Netflix real-time streaming architecture

Netflix uses three internet facing services to exchange data with the
client's browser or mobile app. These services are simple Apache Tomcat
based web services.

The service for receiving play events is called "Viewing History".
Impression events are collected with the "Beacon" service.

The "Recommender Service" makes recommendations based on trend data
available for clients.

Messages from the Beacon and Viewing History services are put into
Apache Kafka. It acts as a buffer between the data services and the
analytics.

Beacon and Viewing History publish messages to Kafka topics. The
analytics subscribes to the topics and gets the messages automatically
delivered in a first in first out fashion.

After the analytics the workflow is straight forward. The trending data
is stored in a Cassandra Key-Value store. The recommender service has
access to Cassandra and is making the data available to the Netflix
client.

![Netflix Streaming Pipeline[]{label="fig:Bild1"}](/images/Netflix-Streaming-Pipeline.jpg){#fig:Bild1
width="90%"}

The algorithms how the analytics system is processing all this data is
not known to the public. It is a trade secret of Netflix.

What is known, is the analytics tool they use. Back in Feb 2015 they
wrote in the tech blog that they use a custom made tool.

They also stated, that Netflix is going to replace the custom made
analytics tool with Apache Spark streaming in the future. My guess is,
that they did the switch to Spark some time ago, because their post is
more than a year old.

### Data Science at OLX

| Podcast Episode: #083 Data Engineering at OLX Case Study
|------------------|
|This podcast is a case study about OLX with Senior Data Scientist Alexey Grigorev as guest. It was super fun.
| Watch on YouTube \ Listen on Anchor|


**Slides:**

<https://www.slideshare.net/mobile/AlexeyGrigorev/image-models-infrastructure-at-olx>

### Data Science at OTTO

<https://www.slideshare.net/SparkSummit/spark-summit-eu-talk-by-sebastian-schroeder-and-ralf-sigmund>

### Data Science at Paypal

<https://www.paypal-engineering.com/tag/data/>

### Data Science at Pinterest

| Podcast Episode: #069 Engineering Culture At Pinterest
|------------------|
|In this podcast we look into data platform and processing at Pinterest.
| Watch on YouTube \ Listen on Anchor|

**Slides:**

<https://www.slideshare.net/ConfluentInc/pinterests-story-of-streaming-hundreds-of-terabytes-of-pins-from-mysql-to-s3hadoop-continuously?ref=https://www.confluent.io/kafka-summit-sf18/pinterests-story-of-streaming-hundreds-of-terabytes>

<https://www.slideshare.net/ConfluentInc/building-pinterest-realtime-ads-platform-using-kafka-streams?ref=https://www.confluent.io/kafka-summit-sf18/building-pinterest-real-time-ads-platform-using-kafka-streams>

<https://medium.com/@Pinterest_Engineering/building-a-real-time-user-action-counting-system-for-ads-88a60d9c9a>

<https://medium.com/pinterest-engineering/goku-building-a-scalable-and-high-performant-time-series-database-system-a8ff5758a181>

<https://medium.com/pinterest-engineering/building-a-dynamic-and-responsive-pinterest-7d410e99f0a9>

<https://medium.com/@Pinterest_Engineering/building-pin-stats-25ec8460e924>

<https://medium.com/@Pinterest_Engineering/improving-hbase-backup-efficiency-at-pinterest-86159da4b954>

<https://medium.com/@Pinterest_Engineering/pinterest-joins-the-cloud-native-computing-foundation-e3b3e66cb4f>

<https://medium.com/@Pinterest_Engineering/using-kafka-streams-api-for-predictive-budgeting-9f58d206c996>

<https://medium.com/@Pinterest_Engineering/auto-scaling-pinterest-df1d2beb4d64>

### Data Science at Salesforce

<https://engineering.salesforce.com/building-a-scalable-event-pipeline-with-heroku-and-salesforce-2549cb20ce06>

### Data Science at Siemens Mindsphere

| Podcast Episode: #059 What Is The Siemens Mindsphere IoT Platform?
|------------------|
|The Internet of things is a huge deal. There are many platforms available. But, which one is actually good? Join me on a 50 minute dive into the Siemens Mindsphere online documentation. I have to say I was super unimpressed by what I found. Many limitations, unclear architecture and no pricing available? Not good!
| Watch on YouTube \ Listen on Anchor|

### Data Science at Slack

<https://speakerdeck.com/vananth22/streaming-data-pipelines-at-slack>

### Data Science at Spotify

| Podcast Episode: #071 Data Engineering At Spotify Case Study
|------------------|
|In this episode we are looking at data engineering at Spotify, my favorite music streaming service. How do they process all that data?
| Watch on YouTube \ Listen on Anchor|


**Slides:**

<https://labs.spotify.com/2016/02/25/spotifys-event-delivery-the-road-to-the-cloud-part-i/>

<https://labs.spotify.com/2016/03/03/spotifys-event-delivery-the-road-to-the-cloud-part-ii/>

<https://labs.spotify.com/2016/03/10/spotifys-event-delivery-the-road-to-the-cloud-part-iii/>

<https://www.slideshare.net/InfoQ/scaling-the-data-infrastructure-spotify>

<https://www.datanami.com/2018/05/16/big-data-file-formats-demystified/>

<https://labs.spotify.com/2017/04/26/reliable-export-of-cloud-pubsub-streams-to-cloud-storage/>

<https://labs.spotify.com/2017/11/20/autoscaling-pub-sub-consumers/>

### Data Science at Symantec

<https://www.slideshare.net/planetcassandra/symantec-cassandra-data-modelling-techniques-in-action>

### Data Science at Tinder

<https://www.slideshare.net/databricks/scalable-monitoring-using-apache-spark-and-friends-with-utkarsh-bhatnagar>

### Data Science at Twitter

| Podcast Episode: #072 Data Engineering At Twitter Case Study
|------------------|
|How is Twitter doing data engineering? Oh man, they have a lot of cool things to share these tweets.
| Watch on YouTube \ Listen on Anchor|


**Slides:**

<https://www.slideshare.net/sawjd/real-time-processing-using-twitter-heron-by-karthik-ramasamy>

<https://www.slideshare.net/sawjd/big-data-day-la-2016-big-data-track-twitter-heron-scale-karthik-ramasamy-engineering-manager-twitter>

<https://techjury.net/stats-about/twitter/>

<https://developer.twitter.com/en/docs/tweets/post-and-engage/overview>

<https://www.slideshare.net/prasadwagle/extracting-insights-from-data-at-twitter>

<https://blog.twitter.com/engineering/en_us/topics/insights/2018/twitters-kafka-adoption-story.html>

<https://blog.twitter.com/engineering/en_us/topics/infrastructure/2017/the-infrastructure-behind-twitter-scale.html>

<https://blog.twitter.com/engineering/en_us/topics/infrastructure/2019/the-start-of-a-journey-into-the-cloud.html>

<https://www.slideshare.net/billonahill/twitter-heron-in-practice>

<https://medium.com/@kramasamy/introduction-to-apache-heron-c64f8c7c0956>

<https://www.youtube.com/watch?v=3QHGhnHx5HQ>

<https://hbase.apache.org>

<https://db-engines.com/en/system/Amazon+DynamoDB%3BCassandra%3BGoogle+Cloud+Bigtable%3BHBase>

### Data Science at Uber

<https://eng.uber.com/uber-big-data-platform/>

<https://eng.uber.com/aresdb/>

<https://www.uber.com/us/en/uberai/>

### Data Science at Upwork

<https://www.slideshare.net/databricks/how-to-rebuild-an-endtoend-ml-pipeline-with-databricks-and-upwork-with-thanh-tran>

### Data Science at Woot

<https://aws.amazon.com/de/blogs/big-data/our-data-lake-story-how-woot-com-built-a-serverless-data-lake-on-aws/>

### Data Science at Zalando

| Podcast Episode: #087 Data Engineering At Zalando Case Study Talk
|------------------|
|I had a great conversation about data engineering for online retailing with Michal Gancarski and Max Schultze. They showed Zalando’s data platform and how they build data pipelines. Super interesting especially for AWS users.
| Watch on YouTube

Do me a favor and give these guys a follow on LinkedIn:

LinkedIn of Michal: <https://www.linkedin.com/in/michalgancarski/>

LinkedIn of Max: <https://www.linkedin.com/in/max-schultze-b11996110/>

Zalando has a tech blog with more infos and there is also a meetup in
Berlin:

Zalando Blog: <https://jobs.zalando.com/tech/blog/>

Next Zalando Data Engineering Meetup:
<https://www.meetup.com/Zalando-Tech-Events-Berlin/events/262032282/>

Interesting tools:

AWS CDK: <https://docs.aws.amazon.com/cdk/latest/guide/what-is.html>

Delta Lake: <https://delta.io/>

AWS Step Functions:
https://aws.amazon.com/step-functions/ AWS State Language: https://states-language.net/spec.html

Youtube channel of the meetup:
https://www.youtube.com/channel/UCxwul7aBm2LybbpKGbCOYNA/playlists talk at Spark+AI

Summit about Zalando's Processing Platform:
<https://databricks.com/session/continuous-applications-at-scale-of-100-teams-with-databricks-delta-and-structured-streaming>

Talk at Strata London slides:
<https://databricks.com/session/continuous-applications-at-scale-of-100-teams-with-databricks-delta-and-structured-streaming>

<https://jobs.zalando.com/tech/blog/what-is-hardcore-data-science--in-practice/?gh_src=4n3gxh1>

<https://jobs.zalando.com/tech/blog/complex-event-generation-for-business-process-monitoring-using-apache-flink/>


---

Best Practices Cloud Platforms
=============================

This section is a collection of best practices on how you can arrange the tools together to a platform.  
It's here especially to help you start your own project in the cloud on AWS, Azure and GCP.

Like the advanced skills section this section also follows my My Data Science Platform Blueprint.
In the blueprint I divided the platform into sections: Connect, Buffer, Processing, Store and Visualize.

This order will help you learn how to connect the right tools together.
Take your time and research the tools and learn how they work.

Right now the Azure section has a lot of links to platform examples.
They are also useful for AWS and GCP, just try to change out the tools.

As always, I am going to add more stuff to this over time.

Have fun!

## Contents

- Amazon Web Services (AWS)
  - Connect
  - Buffer
  - Processing
  - Store
  - Visualize
  - Containerization
  - Best Practices
  - More Details
- Microsoft Azure
  - Connect
  - Buffer
  - Processing
  - Store
  - Visualize
  - Containerization
  - Best Practices
- Google Cloud Platform (GCP)
  - Connect
  - Buffer
  - Processing
  - Store
  - Visualize
  - Containerization
  - Best Practices

# AWS
## Connect
- Elastic Beanstalk (very old)
- SES Simple Email Service
- API Gateway
## Buffer
- Kinesis
- Kinesis Data Firehose
- Managed Streaming for Kafka (MSK)
- MQ
- Simple Queue Service (SQS)
- Simple Notification Service (SNS)
## Processing
- EC2
- Athena
- EMR
- Elasticsearch
- Kinesis Data Analytics
- Glue
- Step Functions
- Fargate
- Lambda
- SageMaker
## Store
- Simple Storage Service (S3)
- Redshift
- Aurora
- RDS
- DynamoDB
- ElastiCache
- Neptune Graph DB
- Timestream
- DocumentDB (MongoDB compatible)
## Visualize
- Quicksight

## Containerization
- Elastic Container Service (ECS)
- Elastic Container Registry (ECR)
- Elastic Kubernetes Service (EKS)

## Best Practices
Deploying a Spring Boot Application on AWS Using AWS Elastic Beanstalk:

[https://aws.amazon.com/de/blogs/devops/deploying-a-spring-boot-application-on-aws-using-aws-elastic-beanstalk/](https://aws.amazon.com/de/blogs/devops/deploying-a-spring-boot-application-on-aws-using-aws-elastic-beanstalk/)

How to deploy a Docker Container on AWS:

[https://aws.amazon.com/getting-started/hands-on/deploy-docker-containers/](https://aws.amazon.com/getting-started/hands-on/deploy-docker-containers/)


#### AWS platform architecture for GenAI

![Imagetitle](/images/06/genai-enterprise.png)
▶ [Click here to watch](https://youtu.be/2yX6G4ZURbc)

I recorded a reaction video to an AWS platform architecture for GenAI called Tailwinds. Presented by John from Innovative Solutions and Josh from AWS, it has two main flows: indexing and consumer.

Data enters through S3 buckets or an API gateway, processed by AWS Lambda or Glue, and stored in a vector or graph database, then indexed in OpenSearch. Applications like chatbots use an API gateway to trigger Lambda functions for data retrieval and processing. This flexible serverless setup supports various data formats and uses tools like SAM and Terraform.

Amazon Bedrock helps customers choose and evaluate models. The architecture is flexible but requires effort to create the necessary Lambda functions. Check out the video and share your thoughts!

▶ [Click here to watch](https://youtu.be/2yX6G4ZURbc)

#### Generative AI enabled job search engine

![Imagetitle](/images/06/job-search.png)

▶ [Click here to watch](https://youtu.be/dOWqasmqfHQ)

Hey everyone, I recorded a reaction video to an AWS platform architecture for a Gen AI job search engine. Presented by Andrea from AWS and Bill from Healthy Careers, this setup uses generative AI to enhance job searches for healthcare professionals.

The architecture uses Elastic Container Service (ECS) to handle user queries, processed by Claude II for prompt checks and geolocation. Cleaned prompts are vectorized using Amazon's Titan model, with user search history fetched from an SQL database. Search results are stored in Elasticsearch, updating every six hours. Finally, Claude II generates a response from the search results and sends it back to the user.

I found the use of Claude II for prompt sanitization and geolocation, and the integration of multiple AI models through AWS Bedrock, particularly interesting. This setup keeps data private and provides a flexible, efficient job search experience.

Check out the video and share your thoughts!


#### Voice transcription and analysis on AWS

![Imagetitle](/images/06/voice-transcription.png)

▶ [Click here to watch](https://youtu.be/RGXRjOTQuBM)

Hey everyone, I recorded a reaction video to an AWS architecture for voice transcription and analysis. Presented by Nuan from AWS and Ben from Assembly AI, this system is designed to handle large-scale audio data processing.

Users upload audio data via an API to an ECS container. The data is then managed by an orchestrator that decides which models to use and in what order. The orchestrator sends tasks to SQS, which triggers various ML models running on ECS. These models handle tasks like speech-to-text conversion, sentiment analysis, and speaker labeling. Results are stored in S3 and users are notified via SNS and a Lambda function when processing is complete.

I found the use of ECS for containerized applications and the flexibility of swapping models through ECR particularly interesting. This architecture ensures scalability and efficiency, making it ideal for handling millions of requests per day.

Check out the video and share your thoughts!


#### GeoSpatial Data Analysis

![Imagetitle](/images/06/geo-spacial.png)

▶ [Click here to watch](https://youtu.be/MxVJAvFSTXg)

Hey everyone, I recorded a reaction video to an AWS architecture for geospatial data analysis by TCS. Presented by David John and Suryakant from TCS, this platform is used in next-gen agriculture for tasks like crop health, yield, and soil moisture analysis.

The platform uses data from satellites, AWS open data, and field agents, processing it with Lambda, Sagemaker, and PostgreSQL. Data is stored and analyzed in S3 buckets and PostgreSQL, with results made accessible via EKS-deployed UIs on EC2 instances, buffered through CloudFront for efficiency.

Key aspects include:

- Lambda functions triggering Sagemaker jobs for machine learning.
- Sagemaker handling extensive processing tasks.
- PostgreSQL and S3 for storing processed data.
- CloudFront caching data to enhance user experience.
- I found the use of parallel Sagemaker jobs for scalability and the integration of open data for cost efficiency particularly interesting. This setup effectively meets the agricultural sector's data analysis needs.

Check out the video and share your thoughts!


#### Building a Self-Service Enterprise Data Engineering Platform

![Imagetitle](/images/06/enterprise-solution.png)

▶ [Click here to watch](https://youtu.be/E9JFCl7bk88)

Hey everyone, I recorded a reaction video to an AWS architecture for a self-service enterprise data engineering platform by ZS Associates. Presented by David John and Laken from ZS Associates, this platform is designed to streamline data integration, infrastructure provisioning, and data access for life sciences companies.

Key components:
- **Users and Interaction**: Data engineers and analysts interact through a self-service web portal, selecting infrastructure types and providing project details. This portal makes REST requests to EKS, which creates records in PostgreSQL and triggers infrastructure provisioning via SQS.
- **Infrastructure Provisioning**: EKS processes SQS messages to provision infrastructure such as EMR clusters, databases in Glue Catalog, S3 buckets, and EC2 instances with containerized services like Airflow or NiFi. IAM roles are configured for access control.
- **Data Governance and Security**: All data sets are accessed through the Glue Catalog, with governance workflows requiring approval from data owners via SES notifications. EKS updates IAM roles and Ranger policies for fine-grained access control.
- **Scalability and Efficiency**: EKS hosts 100+ microservices supporting workflows and UI portals. The platform handles millions of API requests and hundreds of data access requests monthly, with auto-scaling capabilities to manage costs.

This architecture effectively reduces time to market, enhances security at scale, and optimizes costs by automating data access and infrastructure provisioning. It also ensures data governance and security through controlled access and approval processes.

Check out the video and share your thoughts!


#### Customer Support Platform

![Imagetitle](/images/06/customer-support.png)

▶ [Click here to watch](https://youtu.be/sCIFpOuryFU)

Hey everyone, I recorded a reaction video to an AWS architecture for a personalized customer support platform by Traeger. Presented by David John and Lizzy from Traeger, this system enhances customer support by leveraging data from Shopify, EventBridge, Kinesis Data Firehose, S3, Lambda, DynamoDB, and Amazon Connect.

Key components:
- **Order Processing**: Customer order data from Shopify flows into EventBridge, then to Kinesis Data Firehose, which writes it to S3. An event trigger in S3 invokes a Lambda function that stores specific order metadata in DynamoDB.
- **Personalized Customer Support**: When a customer calls, Amazon Connect uses Pinpoint to determine the call's origin, personalizing the language options. Connect triggers a Lambda function to query DynamoDB for customer metadata based on the phone number. This data is used to inform the customer support agent.
- **Reason for Contact**: Amazon Lex bot asks the customer the reason for their call, and this information, along with customer metadata, routes the call to a specialized support queue.

I found the use of DynamoDB for storing customer metadata and the integration with Amazon Connect and Lex for personalized support particularly interesting. The architecture is scalable and ensures a personalized experience for customers.

Check out the video and share your thoughts!


#### League of Legends Data Platform on AWS

![Imagetitle](/images/06/league.jpg)

▶ [Click here to watch](https://youtu.be/FX_ZUJk_WoE)

Hey everyone, I recorded a reaction video to an AWS architecture for the data platform that powers League of Legends by Riot Games. Presented by David John and the team at Riot Games, this system handles massive amounts of data generated by millions of players worldwide.

Key components:
- **Player Interaction**: Players connect to game servers globally. The game client communicates with an API running in EKS. This setup ensures low latency and optimal performance.
- **Data Ingestion**: The game client and server send data about player interactions to EKS, which flows into MSK (Managed Streaming for Kafka). Local Kafka clusters buffer the data before it’s replicated to regional MSK clusters using MirrorMaker.
- **Data Processing**: Spark Streaming jobs process the data from MSK and store it in Delta Lake on S3. This setup ensures efficient data handling and reduces latency in data availability.
- **Data Storage and Access**: Glue serves as the data catalog, managing metadata and permissions. Data consumers, including analysts, designers, engineers, and executives, access this data through Databricks, leveraging Glue for structured queries.

I found the use of MSK and Spark for scalable data ingestion and processing particularly interesting. This architecture supports real-time analytics, allowing Riot Games to quickly assess the impact of new patches and gameplay changes.

Check out the video and share your thoughts!



#### Platform Connecting 70 Million Cars

![Imagetitle](/images/06/70m-cars.png)

▶ [Click here to watch](https://youtu.be/1nifzmvOGHs)

Hey everyone, I recorded a reaction video to an AWS architecture for a connected car platform by Mobileye. Presented by David John and the team at Mobileye, this system connects 70 million cars, collecting and processing data to offer digital services and fleet analysis.

Key components:
- **Data Collection**: Cars collect anonymized data using sensors and visual inspections, sending it to a REST API and storing it in S3.
- **Data Processing**: The data is pulled from S3 into SQS and processed by EKS workers, which scale according to the queue size. Processed data is stored back in S3 and further analyzed using step functions and Lambda for tasks like extracting construction zones and clustering observations.
- **Data Storage**: Processed data is stored in S3, Elasticsearch, and CockroachDB. Elasticsearch handles document-based data with self-indexing, while CockroachDB supports frequent updates.
- **Data Consumption**: EKS hosts a secured REST API and web application, allowing customers like city planners to access insights on pedestrian and bicycle traffic.

Future plans include enabling cloud image processing on EKS with GPU instances and focusing on cost reduction as data flow increases.

I found the use of EKS for scalable data processing and the combination of Elasticsearch and CockroachDB for different data needs particularly interesting. This architecture efficiently handles large-scale data from millions of connected cars.

Check out the video and share your thoughts!


#### 55TB A Day: Nielsen AWS Data Architecture

![Imagetitle](/images/06/55-tb.png)

▶ [Click here to watch](https://youtu.be/WCQe1VP_q5A)

Hey everyone, I recorded a reaction video to an AWS architecture for Nielsen Marketing Cloud, which processes 55TB of data daily. Presented by David John, this system handles marketing segmentation data for campaigns.

Key components:
- **Data Ingestion**: Marketing data comes in files, written to S3. Spark on EMR processes and transforms the data, writing the output to another S3 bucket.
- **Data Processing**: Lambda functions handle the final formatting and upload the data to over 100 ad networks. Metadata about file processing is managed in a PostgreSQL RDS database.
- **Metadata Management**: A work manager Lambda reads metadata from RDS, triggers processing jobs in EMR, and updates the metadata post-processing.
- **Scaling and Rate Limiting**: The serverless architecture allows automatic scaling. However, rate limiting is implemented to prevent overloading ad networks, ensuring they handle data bursts smoothly.

Challenges and Solutions:
- **Scale**: The system handles 250 billion events per day, scaling up and down automatically to manage peak loads.
- **Rate Limiting**: To avoid overwhelming ad networks, a rate-limiting mechanism was introduced, managing data flow based on network capacity.
- **Back Pressure Management**: SQS is used to buffer Lambda responses, preventing direct overload on the PostgreSQL database.

I found the use of SQS for metadata management and the serverless architecture for handling massive data loads particularly interesting. This setup ensures efficient data processing and smooth delivery to ad networks.

Check out the video and share your thoughts!


#### Orange Theory Fitness

![Image](/images/06/fitness-1.jpeg)

▶ [Click here to watch](https://youtu.be/ssaXRo5s1r4)

Hey, everybody! Today, I'm reacting to the AWS data infrastructure at Orange Theory Fitness, where they collect data from wristbands and training machines. Let's dive in and see how they manage it all.

### Key Components

1. **Local Server**: Aggregates data from in-studio equipment and mobile apps, ensuring resiliency if the cloud connection is lost.
2. **API Gateway and Cognito**: Handle authentication and route data to the cloud.
3. **Lambda Functions**: Process data.
4. **Aurora RDS (MySQL)**: Stores structured data like member profiles, class bookings, and studio information.
5. **DynamoDB**: Stores performance metrics and workout statistics for quick access.
6. **S3**: Serves as a data lake, storing telemetry data.
7. **Kinesis Firehose**: Streams telemetry data to S3.

### Challenges & Solutions

1. **Resiliency**
   - **Challenge**: Ensure operations continue if cloud connection is lost.
   - **Solution**: Local server aggregates data and syncs with the cloud once the connection is restored.

2. **Data Integration**
   - **Challenge**: Integrate data from various sources.
   - **Solution**: Use API Gateway and Cognito for unified authentication and data routing.

3. **Data Processing**
   - **Challenge**: Efficiently process and store different types of data.
   - **Solution**: Use Lambda for processing, Aurora RDS for structured data, DynamoDB for quick access to performance metrics, and Kinesis Firehose with S3 for streaming and storing large volumes of telemetry data.

This architecture leverages AWS tools for scalability, flexibility, and resilience, making it an excellent example of a well-thought-out data infrastructure for a fitness application.

Let me know your thoughts in the comments. What do you think of this architecture? Would you have done anything differently? If you have any questions, feel free to ask. And if you're interested in learning more about data engineering, check out my academy at learndataengineering.com. See you in the next video!


## More Details
AWS Whitepapers:

[https://d1.awsstatic.com/whitepapers/aws-overview.pdf](https://d1.awsstatic.com/whitepapers/aws-overview.pdf)


# Azure
## Connect
- Event Hub
- IoT Hub
## Buffer
- Data Factory
- Event Hub
- RedisCache (also Store)
## Processing
- Stream Analytics Service
- Azure Databricks
- Machine Learning
- Azure Functions
- Azure HDInsight (Hadoop PaaS)
## Store
- Blob
- CosmosDB
- MariaDB
- MySQL
- PostgreSQL
- SQL
- Azure Data lake
- Azure Storage (SQL Table?)
- Azure Synapse Analytics
## Visualize
- PowerBI
## Containerization
- Virtual Machines
- Virtual Machine Scale Sets
- Azure Container Service (AKS)
- Container Instances
- Azure Kubernetes Service
## Best Practices

Advanced Analytics Architecture:

[https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/advanced-analytics-on-big-data](https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/advanced-analytics-on-big-data)

Anomaly Detection in Real-time Data Streams:

[https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/anomaly-detection-in-real-time-data-streams](https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/anomaly-detection-in-real-time-data-streams)

Modern Data Warehouse Architecture:

[https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/modern-data-warehouse](https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/modern-data-warehouse)

CI/CD for Containers:

[https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/cicd-for-containers](https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/cicd-for-containers)

Real Time Analytics on Big Data Architecture:

[https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/real-time-analytics](https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/real-time-analytics)

Anomaly Detection in Real-time Data Streams:

[https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/anomaly-detection-in-real-time-data-streams](https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/anomaly-detection-in-real-time-data-streams)

IoT Architecture – Azure IoT Subsystems:

[https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/azure-iot-subsystems](https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/azure-iot-subsystems)

Tier Applications & Data for Analytics:

[https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/tiered-data-for-analytics](https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/tiered-data-for-analytics)

Extract, transform, and load (ETL) using HDInsight:

[https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/extract-transform-and-load-using-hdinsight](https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/extract-transform-and-load-using-hdinsight)

IoT using Cosmos DB:

[https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/iot-using-cosmos-db](https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/iot-using-cosmos-db)

Streaming using HDInsight:

[https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/streaming-using-hdinsight](https://docs.microsoft.com/en-us/azure/architecture/solution-ideas/articles/streaming-using-hdinsight)

# GCP
## Connect
- Cloud IoT Core
- App Engine
- Cloud Dataflow
## Buffer
- Pub/Sub
## Processing
- Compute Engine
- Cloud Functions
- Specialized tools:
  - Cloud Dataflow
  - Cloud Dataproc
  - Cloud Datalab
  - Cloud Dataprep
  - Cloud Composer
- App Engine
## Store
- Cloud Storage
- Cloud SQL
- Cloud Spanner
- Cloud Datastore
- Cloud BigTable
- Cloud Storage
- Cloud Memorystore
- BigQuery
## Visualize

## Containerization
- Kubernetes Engine
- Container Security
## Best Practices

Thanks to Ismail Holoubi for the following GCP links

Best practices for migrating virtual machines to Compute Engine:

https://cloud.google.com/solutions/best-practices-migrating-vm-to-compute-engine

Best practices for Cloud Storage:

https://cloud.google.com/storage/docs/best-practices

Moving a publishing workflow to BigQuery for new data insights:

https://cloud.google.com/blog/products/data-analytics/moving-a-publishing-workflow-to-bigquery-for-new-data-insights

Architecture: Optimizing large-scale ingestion of analytics events and logs:

https://cloud.google.com/solutions/architecture/optimized-large-scale-analytics-ingestion

Choosing the right architecture for global data distribution:

https://cloud.google.com/solutions/architecture/global-data-distribution

Best Practices for Operating Containers:

https://cloud.google.com/solutions/best-practices-for-operating-containers


Automating IoT Machine Learning: Bridging Cloud and Device Benefits with AI Platform:

https://cloud.google.com/solutions/automating-iot-machine-learning


---


100 Plus Data Sources Data Science
===================================

This is a section with links to data sources. During my data engineer coaching we need to find good data sets to work with.
So, I started this section to make it easier to find good sources.

I've taken these links from articles and blog posts. Why not only link the articles?
You know, these posts can go away at any time. I want to keep the links to the platforms either way.

I haven't had the chance to check each link myself. Please let me know if something isn't right.

You can find the articles on the bottom of this section to read more. They include even more data sources I haven't had time to add to this list.



## Contents

- Student Favorites
- Content Marketing
- Crime
- Drugs
- Education
- Entertainment
- Environmental And Weather Data
- Financial And Economic Data
- General And Academic
- Government And World
- Health
- Human Rights
- Labor And Employment Data
- Politics
- Retail
- Social
- Source Articles and Blog Posts
- Travel And Transportation
- Various Portals

## Student Favorites

In my Coaching program my students learn by doing a project. And the foundation of every project is selecting a dataset.
That can be an API or a file source, depending a lot on the student's goals and interests.

Working out goals for the dataset, figuring out the data modeling, creating the architecture and building it. 
It's a fun way to learn and get better at Data Engineering. 

Here's a list of my student's favorite datasets and APIs

Learn more about the Coaching program: [click here](https://learndataengineering.com/p/data-engineering-coaching)

### Datasets

- [Fraud detection](https://www.kaggle.com/datasets/kartik2112/fraud-detection)
- [Industrial equipment monitoring](https://www.kaggle.com/datasets/dnkumars/industrial-equipment-monitoring-dataset)
- [Energy demand & generation](https://www.kaggle.com/datasets/nicholasjhana/energy-consumption-generation-prices-and-weather?select=weather_features.csv)
- [Online Retail](https://www.kaggle.com/datasets/tunguz/online-retail)
- [Brazilian E-commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- [Beijing Air Quality](https://www.kaggle.com/datasets/sid321axn/beijing-multisite-airquality-data-set)
- [NYC Taxi](https://www.kaggle.com/datasets/diishasiing/revenue-for-cab-drivers)

### APIs

- [Bike sharing Bluebikes](https://bluebikes.com/system-data)
- [Bike sharing Divvy Bikes](https://divvybikes.com/system-data)
- [Weather API](https://www.weatherapi.com/docs/)
- [Bluesky API](https://docs.bsky.app/docs/advanced-guides/api-directory)
- [Guardian news API](https://open-platform.theguardian.com/)
- [Football API](https://www.api-football.com/)


## General And Academic

- [Amazon Public Data Sets](https://registry.opendata.aws/)
- [Datasets Subreddit](https://www.reddit.com/r/datasets)
- [Enigma Public](https://public.enigma.com/)
- [FiveThirtyEight](http://fivethirtyeight.com/)
- [Google Scholar](http://scholar.google.com/)
- [Pew Research](http://www.pewresearch.org/)
- [The Upshot by New York Times](http://www.nytimes.com/section/upshot)
- [UNData](http://data.un.org/)

## Content Marketing

- [Buffer](https://blog.bufferapp.com/)
- [Content Marketing Institute](http://contentmarketinginstitute.com/about/)
- [HubSpot](http://www.hubspot.com/marketing-statistics)
- [Moz](https://moz.com/blog)

## Crime

- [Bureau of Justice Statistics](http://www.bjs.gov/index.cfm?ty=dca)
- [FBI Crime Statistics](https://www.fbi.gov/stats-services/crimestats)
- [National Archive of Criminal Justice Data](https://www.icpsr.umich.edu/icpsrweb/NACJD/)
- [Uniform Crime Reporting Statistics](https://crime-data-explorer.fr.cloud.gov/)

## Drugs

- [Drug Data and Database by First Databank](http://www.fdbhealth.com/)
- [Drug War Facts](http://www.drugwarfacts.org/)
- [National Institute on Drug Abuse](https://www.drugabuse.gov/related-topics/trends-statistics)
- [U.S. Food and Drug Administration](http://www.fda.gov/Drugs/InformationOnDrugs/ucm079750.htm)
- [United Nations Office on Drugs and Crime](https://www.unodc.org/unodc/en/data-and-analysis/)

## Education

- [Education Data by the World Bank](http://data.worldbank.org/topic/education)
- [Education Data by Unicef](http://data.unicef.org/education/overview.html)
- [National Center for Education Statistics](https://nces.ed.gov/)

## Entertainment

- [Academic Rights Press](http://www.academicrightspress.com/entertainment/music)
- [BFI Film Forever](http://www.bfi.org.uk/education-research/film-industry-statistics-research)
- [BLS: Arts, Entertainment, and Recreation](http://www.bls.gov/iag/tgs/iag71.htm)
- [IFPI](http://www.ifpi.org/global-statistics.php)
- [Million Song Dataset](https://aws.amazon.com/datasets/million-song-dataset/)
- [Statista: Film Industry](http://www.statista.com/topics/964/film/)
- [Statista: Music Industry](http://www.statista.com/topics/1639/music/)
- [Statista: Video Game Industry](http://www.statista.com/topics/868/video-games/)
- [The Numbers](http://www.the-numbers.com/)

## Environmental And Weather Data

- [Environmental Protection Agency](https://www.epa.gov/data)
- [International Energy Agency Atlas](https://www.iea.org/data-and-statistics?country=WORLD&fuel=Energy%20supply&indicator=TPESbySource)
- [National Center for Environmental Health](http://www.cdc.gov/nceh/data.htm)
- [National Climatic Data Center](http://www.ncdc.noaa.gov/data-access/quick-links#loc-clim)
- [National Weather Service](http://www.weather.gov/help-past-weather)
- [Weather Underground](https://www.wunderground.com/)
- [WeatherBase](http://www.weatherbase.com/)

## Financial And Economic Data

- [Federal Reserve Economic Database](https://fred.stlouisfed.org/)
- [Financial Data Finder at OSU](./) - Missing link.
- [Global Financial Data](https://www.globalfinancialdata.com/index.html)
- [Google Finance](https://www.google.com/finance)
- [Google Public Data Explorer](http://www.google.com/publicdata/directory)
- [IMF Economic Data](https://data.imf.org/?sk=388dfa60-1d26-4ade-b505-a05a558d9a42)
- [National Bureau of Economic Research](http://www.nber.org/data/)
- [OpenCorporates](https://opencorporates.com/)
- [The Atlas of Economic Complexity](http://atlas.cid.harvard.edu/)
- [U.S. Bureau of Economic Analysis](http://www.bea.gov/)
- [U.S. Securities and Exchange Commission](https://www.sec.gov/dera/data/financial-statement-data-sets.html)
- [UN Comtrade Database](https://comtrade.un.org/labs/)
- [Visualizing Economics](http://visualizingeconomics.com/)
- [World Bank Doing Business Database](http://www.doingbusiness.org/rankings)
- [World Bank Open Data](http://data.worldbank.org/)

## Government And World

- [Data.gov](http://www.data.gov/)
- [European Union Open Data Portal](http://data.europa.eu/euodp/en/data/)
- [Gapminder](https://www.gapminder.org/data/)
- [Land Matrix (Transnational Land Database)](http://landmatrix.org/en/)
- [OECD Aid Database](http://www.oecd.org/dac/financing-sustainable-development/development-finance-data/)
- [Open Data Network](http://www.opendatanetwork.com/)
- [The CIA World Factbook](https://www.cia.gov/the-world-factbook/)
- [The World Bank’s World Development Indicators](http://data.worldbank.org/data-catalog/world-development-indicators)
- [U.S. Census Bureau](http://www.census.gov/)
- [UNDP’s Human Development Index](http://hdr.undp.org/en/data)

## Health

- [America’s Health Rankings](http://www.americashealthrankings.org/)
- [Centers for Disease Control and Prevention](http://www.cdc.gov/datastatistics/)
- [Health & Social Care Information Centre](http://www.hscic.gov.uk/home)
- [Health Services Research Information Central](https://www.nlm.nih.gov/hsrinfo/datasites.html)
- [HealthData.gov](https://www.healthdata.gov/)
- [Medicare Hospital Quality](https://data.medicare.gov/data/hospital-compare#)
- [MedicinePlus](https://www.nlm.nih.gov/medlineplus/healthstatistics.html)
- [National Center for Health Statistics](http://www.cdc.gov/nchs/)
- [SEER Cancer Incidence](http://seer.cancer.gov/faststats/selections.php?series=cancer)
- [World Health Organization](http://www.who.int/en/)

## Human Rights

- [Amnesty International](https://www.amnesty.org/en/search/?q=&documentType=Annual+Report)
- [Human Rights Data Analysis Group](https://hrdag.org/)
- [The Armed Conflict Database by Uppsala University](http://www.pcr.uu.se/research/UCDP/)

## Labor And Employment Data

- [Bureau of Labor Statistics](http://www.bls.gov/)
- [Department of Labor](https://www.dol.gov/general/topic/statistics/employment)
- [Employment by U.S. Census](http://www.census.gov/topics/employment.html)
- [U.S. Small Business Administration](https://www.sba.gov/starting-business/how-start-business/business-data-statistics/employment-statistics)

## Politics

- [California Field Poll](http://dlab.berkeley.edu/data-resources/california-polls)
- [Crowdpac](https://www.crowdpac.com/)
- [Gallup](http://www.gallup.com/home.aspx)
- [Open Secrets](https://www.opensecrets.org/)
- [Rand State Statistics](http://www.randstatestats.org/us/)
- [Real Clear Politics](http://guides.lib.berkeley.edu/Intro-to-Political-Science-Research/Stats)
- [Roper Center for Public Opinion Research](https://ropercenter.cornell.edu/)
- [US Voter Files](http://voterlist.electproject.org/) Note only some states are free, and most do not allow voter files to be used for commercial purposes - this map allows you to see the rules/cost for each state.

## Retail

- [Love the Sales](https://www.lovethesales.com/press/data-request)

## Social

- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Google Trends](http://www.google.com/trends/explore)
- [SocialMention](./) - Missing link.

## Travel And Transportation

- [Bureau of Transportation Statistics](https://www.bts.gov/browse-statistical-products-and-data)
- [Monthly Tourism Statistics – U.S. Travelers Overseas](http://travel.trade.gov/research/monthly/departures/)
- [Search the World](http://www.geoba.se/)
- [SkiftStats](https://skift.com/skiftx/skiftstats/)
- [U.S. Travel Association](https://www.ustravel.org/research)

## Various Portals

- [Ckan](https://ckan.org/)
- [Dataverse](https://dataverse.org/)
- [DBpedia](https://wiki.dbpedia.org/)
- [freeCodeCamp Open Data](https://github.com/freeCodeCamp/open-data)
- [Kaggle](https://www.kaggle.com/datasets)
- [LODUM](https://lodum.de/)
- [Open Data Ipact Map](http://opendataimpactmap.org/)
- [Open Data Kit](https://opendatakit.org/)
- [Open Data Monitor](https://opendatamonitor.eu/frontend/web/index.php?r=dashboard%2Findex)
- [Plenar.io](http://plenar.io/)
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)
- [Yelp Open Datasets](https://www.yelp.com/dataset)


## Source Articles and Blog Posts


- [100+ of the Best Free Data Sources For Your Next Project](https://www.columnfivemedia.com/100-best-free-data-sources-infographic)
- [15 Great Free Data Sources for 2016](https://medium.com/@Infogram/15-great-free-data-sources-for-2016-25cb455db257)
- [20 Awesome Sources of Free Data](https://www.searchenginejournal.com/free-data-sources/302601/#close)
- [30+ Free Data Sources Every Company Should Be Aware Of](https://www.bernardmarr.com/default.asp?contentID=960)
- [50 Amazing Free Data Sources You Should Know](https://infogram.com/blog/free-data-sources/)
- [50 Best Open Data Sources Ready to be Used Right Now](https://learn.g2.com/open-data-sources)
- [70 Amazing Free Data Sources You Should Know](https://www.kdnuggets.com/2017/12/big-data-free-sources.html)
- [Big Data: 33 Brilliant And Free Data Sources Anyone Can Use](https://www.forbes.com/sites/bernardmarr/2016/02/12/big-data-35-brilliant-and-free-data-sources-for-2016/#527557ffb54d)
- [These Are The Best Free Open Data Sources Anyone Can Use](https://www.freecodecamp.org/news/https-medium-freecodecamp-org-best-free-open-data-sources-anyone-can-use-a65b514b0f2d/)


---

1001 Data Engineering Interview Questions
=========================================

Hey everyone, this collection of questions and answers is a work in progress.
I'm going to keep adding Q&As, but you are invited to collaborate through [GitHub](https://github.com/andkret/Cookbook):
- Eiter clone this repo, make your changes and create a pull request
- or raise an issue on GitHub with your questions and answers and we'll add them

Andreas

## Contents:

- Python
- SQL
- Integrate
    - APIs
- Message Queues
    - Distributed Message Queues
    - Message Queues (Fifo)
    - Caches
- Data Processing
    - ETL
    - Stream Processing
    - Batch Processing
    - Processing Frameworks
        - Serverless
        - Distributed Processing Frameworks
    - Scheduling
        - Airflow
    - CI-CD
    - Docker
    - Kubernetes
- Data Storage
    - Relational Databases
    - NoSQL
    - Analytical Stores
    - Relational Modeling
    - Dimensional Data Modeling
    - Data Lakes
- Data Platforms
    - AWS
    - Azure
    - GCP
    - Snowflake


### Python

1. **What is Apache Spark, and how can you use it with Python?**
   - **Answer**: Apache Spark is a distributed data processing framework that allows for big data processing with in-memory computing capabilities. You can use it with Python through PySpark, which provides a Python API for Spark. PySpark enables data engineers to write Spark applications in Python.

2. **How do you perform data cleaning in Python?**
   - **Answer**: Data cleaning in Python can be performed using the `pandas` library. Common tasks include handling missing values (`dropna`, `fillna`), removing duplicates (`drop_duplicates`), converting data types, normalizing data, and handling outliers. Example:
     ```python
     import pandas as pd
     df = pd.read_csv('data.csv')
     df.dropna(inplace=True)  # Remove rows with missing values
     df['column'] = df['column'].astype(int)  # Convert column to integer type
     ```

3. **Explain how you would optimize a slow-running SQL query within a Python ETL pipeline.**
   - **Answer**: To optimize a slow-running SQL query, you can:
     - Analyze the query execution plan.
     - Add appropriate indexes.
     - Optimize the query by reducing complexity, such as using JOINs efficiently and avoiding unnecessary subqueries.
     - Partition large tables if applicable.
     - Use caching and materialized views for frequently accessed data.
     - Ensure that statistics are up to date.
     Example with SQLAlchemy:
     ```python
     from sqlalchemy import create_engine
     engine = create_engine('postgresql://user:password@localhost/dbname')
     with engine.connect() as connection:
         result = connection.execute('SELECT * FROM table WHERE condition')
         data = result.fetchall()
     ```

4. **What is the role of a workflow scheduler in data engineering, and can you name some common ones?**
   - **Answer**: A workflow scheduler automates and manages the execution of ETL jobs and data pipelines. It ensures tasks are executed in the correct order and handles retries, dependencies, and monitoring. Common workflow schedulers include Apache Airflow, Luigi, Prefect, and Apache NiFi.

5. **How do you handle schema changes in a data pipeline?**
   - **Answer**: Handling schema changes in a data pipeline involves:
     - Implementing schema evolution techniques.
     - Using tools like Apache Avro, which supports schema evolution.
     - Versioning schemas and ensuring backward compatibility.
     - Monitoring and validating incoming data against the schema.
     - Applying transformations to adapt to new schemas.
     Example with Avro:
     ```python
     from avro.datafile import DataFileReader
     from avro.io import DatumReader

     reader = DataFileReader(open("data.avro", "rb"), DatumReader())
     for record in reader:
         print(record)
     reader.close()
     ```

6. **What is data partitioning, and why is it important in data engineering?**
   - **Answer**: Data partitioning is the process of dividing a large dataset into smaller, more manageable pieces, often based on a key such as date, user ID, or geographic location. Partitioning improves query performance by reducing the amount of data scanned and allows for parallel processing. It also helps in managing large datasets and reducing I/O costs.

7. **How do you ensure data quality in your pipelines?**
   - **Answer**: Ensuring data quality involves:
     - Implementing data validation checks (e.g., constraints, data type checks).
     - Monitoring for data anomalies and inconsistencies.
     - Using data profiling tools to understand the data.
     - Creating unit tests for data processing logic.
     - Automating data quality checks and alerting mechanisms.
     Example with `pandas` for data validation:
     ```python
     import pandas as pd

     df = pd.read_csv('data.csv')
     assert df['column'].notnull().all(), "Missing values found in column"
     assert (df['age'] >= 0).all(), "Negative ages found"
     ```

8. **What is the difference between batch processing and stream processing?**
   - **Answer**: Batch processing involves processing large volumes of data at once, usually at scheduled intervals. It is suitable for tasks that are not time-sensitive. Stream processing, on the other hand, involves processing data in real-time as it arrives, which is suitable for time-sensitive applications such as real-time analytics, monitoring, and alerts.

9. **How do you implement logging and monitoring in your data pipelines?**
   - **Answer**: Logging and monitoring can be implemented using:
     - Logging libraries like Python's `logging` module to capture and store logs.
     - Monitoring tools like Prometheus, Grafana, or ELK Stack (Elasticsearch, Logstash, Kibana) to visualize and monitor logs.
     - Setting up alerts for failures or anomalies.
     Example with Python's `logging` module:
     ```python
     import logging

     logging.basicConfig(filename='pipeline.log', level=logging.INFO)
     logging.info('This is an informational message')
     logging.error('This is an error message')
     ```

10. **What are some common challenges you face with distributed data processing, and how do you address them?**
    - **Answer**: Common challenges with distributed data processing include data consistency, fault tolerance, data shuffling, and latency. To address these:
      - Use distributed processing frameworks like Apache Spark, which handle many of these issues internally.
      - Implement robust error handling and retries.
      - Optimize data shuffling by partitioning data effectively.
      - Use caching mechanisms to reduce latency.
      - Ensure proper resource allocation and scaling to handle large data volumes.

## SQL

## Integrate
### APIs

These questions cover a range of topics related to APIs, including their concepts, security, best practices, and specific implementation details.

1. **What is an API and how does it work?**
   - **Answer**: An API (Application Programming Interface) is a set of rules and protocols for building and interacting with software applications. It allows different software systems to communicate with each other. APIs define the methods and data formats that applications can use to request and exchange data.

2. **What are the different types of APIs?**
   - **Answer**: The main types of APIs include:
     - **Open APIs (Public APIs)**: Available to developers and other users with minimal restrictions.
     - **Internal APIs (Private APIs)**: Used within an organization to connect systems and data internally.
     - **Partner APIs**: Shared with specific business partners and offer more control over how data is exposed.
     - **Composite APIs**: Combine multiple API requests into a single call, allowing multiple data or service requests in one API call.

3. **What is REST and how does it differ from SOAP?**
   - **Answer**: REST (Representational State Transfer) and SOAP (Simple Object Access Protocol) are two different approaches to building APIs. REST uses standard HTTP methods (GET, POST, PUT, DELETE) and is stateless, meaning each request from a client to a server must contain all the information needed to understand and process the request. SOAP, on the other hand, is a protocol that relies on XML-based messaging and includes built-in rules for security and transactions.

4. **Explain the concept of RESTful services.**
   - **Answer**: RESTful services are web services that follow the principles of REST. These principles include:
     - **Statelessness**: Each request from a client must contain all the information needed by the server to process the request.
     - **Client-Server Architecture**: The client and server are separate entities, and they communicate over a network via standard HTTP.
     - **Cacheability**: Responses from the server can be cached by the client or intermediate proxies to improve performance.
     - **Uniform Interface**: Resources are identified in the request (usually via URIs), and actions are performed using standard HTTP methods.

5. **What is an API gateway and why is it used?**
   - **Answer**: An API gateway is a server that acts as an intermediary for requests from clients seeking resources from backend services. It provides various functions such as request routing, composition, protocol translation, and handling of cross-cutting concerns like authentication, authorization, logging, monitoring, and rate limiting. It simplifies the client interface and improves security, scalability, and manageability of API services.

6. **How do you ensure the security of an API?**
   - **Answer**: Ensuring API security involves several practices, including:
     - **Authentication**: Verify the identity of the user or system making the request (e.g., using OAuth, JWT).
     - **Authorization**: Ensure the authenticated user or system has permission to perform the requested action.
     - **Encryption**: Use HTTPS to encrypt data in transit between the client and server.
     - **Rate Limiting**: Prevent abuse by limiting the number of requests a client can make in a given time period.
     - **Input Validation**: Validate and sanitize all inputs to prevent injection attacks.
     - **Logging and Monitoring**: Track API usage and monitor for unusual or suspicious activity.

7. **What is versioning in APIs and how is it typically managed?**
   - **Answer**: API versioning is the practice of managing changes to an API without disrupting existing clients. It can be managed in several ways, including:
     - **URI Versioning**: Including the version number in the URI path (e.g., `/v1/resource`).
     - **Query Parameter Versioning**: Including the version number as a query parameter (e.g., `/resource?version=1`).
     - **Header Versioning**: Including the version number in the HTTP headers (e.g., `Accept: application/vnd.example.v1+json`).

8. **What are HTTP status codes and why are they important in API responses?**
   - **Answer**: HTTP status codes are standardized codes returned by a server to indicate the result of a client's request. They are important because they provide meaningful feedback to the client about what happened with their request. Common status codes include:
     - **200 OK**: The request was successful.
     - **201 Created**: A resource was successfully created.
     - **400 Bad Request**: The request was invalid or cannot be processed.
     - **401 Unauthorized**: Authentication is required and has failed or has not yet been provided.
     - **404 Not Found**: The requested resource could not be found.
     - **500 Internal Server Error**: An error occurred on the server.

9. **Explain the concept of idempotency in RESTful APIs.**
   - **Answer**: Idempotency refers to the property of certain operations whereby performing the same operation multiple times results in the same outcome. In RESTful APIs, methods like GET, PUT, and DELETE are idempotent because making the same request multiple times has the same effect as making it once. POST is not idempotent because multiple requests could create multiple resources.

10. **How do you handle pagination in APIs?**
    - **Answer**: Pagination is used to split large sets of data into manageable chunks. Common methods for handling pagination include:
      - **Offset and Limit**: Using query parameters to specify the starting point and number of records to return (e.g., `?offset=0&limit=10`).
      - **Page Number and Size**: Using query parameters to specify the page number and the number of records per page (e.g., `?page=1&size=10`).
      - **Cursor-Based Pagination**: Using a cursor (a pointer to a specific record) to fetch the next set of results (e.g., `?cursor=abc123`).


These additional questions cover more advanced topics related to APIs, including security, design principles, best practices, and tooling.
11. **What is the difference between synchronous and asynchronous API calls?**
    - **Answer**: Synchronous API calls wait for the response before continuing, blocking the execution of code until the operation completes. Asynchronous API calls, on the other hand, do not block the execution; they allow the code to continue running and handle the response once it arrives, typically through callbacks, promises, or async/await patterns.

12. **What is a webhook, and how does it differ from an API endpoint?**
    - **Answer**: A webhook is a way for an application to provide other applications with real-time information. A webhook is a "callback" that allows the sending application to push data to the receiving application when an event occurs. Unlike traditional API endpoints, which require the client to periodically check for data (polling), webhooks enable the server to push data to the client when an event occurs.

13. **What is CORS, and why is it important in the context of APIs?**
    - **Answer**: CORS (Cross-Origin Resource Sharing) is a security feature implemented in web browsers that restricts web pages from making requests to a different domain than the one that served the web page. It is important in APIs to control how resources on a server are accessed by external domains. Proper CORS configuration ensures that only authorized domains can access API resources.

14. **What is the purpose of API documentation, and what should it include?**
    - **Answer**: API documentation provides developers with the information they need to use and integrate with an API effectively. It should include:
      - An overview of the API and its purpose.
      - Authentication and authorization methods.
      - Endpoint definitions and available methods (GET, POST, PUT, DELETE).
      - Request and response formats (including headers, query parameters, and body data).
      - Error codes and their meanings.
      - Examples of requests and responses.
      - Rate limits and usage policies.

15. **What are API gateways, and what role do they play in API management?**
    - **Answer**: API gateways act as intermediaries between clients and backend services. They provide various functions such as request routing, load balancing, security (authentication and authorization), rate limiting, logging, monitoring, and transforming requests and responses. API gateways simplify client interactions with microservices and help manage and secure APIs.

16. **How do you handle authentication and authorization in APIs?**
    - **Answer**: Authentication verifies the identity of a user or application, while authorization determines what resources and operations they have access to. Common methods for handling authentication and authorization in APIs include:
      - API keys: Simple tokens provided to access the API.
      - OAuth: An open standard for token-based authentication and authorization.
      - JWT (JSON Web Tokens): A compact, URL-safe means of representing claims to be transferred between two parties.
      - Basic Auth: A simple method using a username and password encoded in base64.

17. **What is the concept of rate limiting in APIs, and why is it important?**
    - **Answer**: Rate limiting controls the number of requests a client can make to an API within a specified time period. It is important for:
      - Preventing abuse and overuse of API resources.
      - Ensuring fair usage among clients.
      - Protecting the backend services from being overwhelmed.
      - Managing and maintaining service quality and performance.

18. **Explain the concept of API throttling.**
    - **Answer**: API throttling is the process of controlling the usage rate of an API by limiting the number of requests a client can make within a certain timeframe. Throttling helps prevent abuse, protects resources, and ensures that the service remains available and responsive to all users. It can be implemented using techniques such as rate limits, quotas, and burst control.

19. **What is HATEOAS and how does it relate to RESTful APIs?**
    - **Answer**: HATEOAS (Hypermedia As The Engine Of Application State) is a constraint of RESTful APIs where hypermedia links are included in the responses to guide clients through the API. It allows clients to dynamically discover available actions and navigate the API without hardcoding the structure. For example, a response to a GET request for a user resource might include links to update or delete the user.

20. **What are some common tools and platforms for testing and documenting APIs?**
    - **Answer**: Common tools and platforms for testing and documenting APIs include:
      - **Postman**: A popular tool for developing, testing, and documenting APIs.
      - **Swagger/OpenAPI**: A framework for designing, building, and documenting RESTful APIs, often used with tools like Swagger UI and Swagger Editor.
      - **Insomnia**: An API client for testing RESTful and GraphQL APIs.
      - **Apigee**: An API management platform providing tools for API design, security, analytics, and monitoring.
      - **Paw**: A macOS-based API client for testing and documenting APIs.
      - **RAML (RESTful API Modeling Language)**: A language for designing and documenting APIs.


## Message queues
### Distributed Message Queues
### Message Queues (Fifo)
### Caches

## Data Processing
### ETL
### Stream processing
### Batch processing
### Processing Frameworks
#### Serverless
#### Distributed Processing frameworks
### Scheduling
#### Airflow
### Docker and Kubernetes
### CI-CD

## Data Storage
### Relational Databases
### NoSQL
### Analytical Stores
### Relational Modeling
### Dimensional Data Modeling
### Data Lakes

## Data Platforms
### AWS
### GCP
### Azure
### Snowflake





Looking for a job or just want to know what people find important? In
this chapter you can find a lot of interview questions we collect on the
stream.

Ultimately this should reach at least one thousand and one questions.

**But Andreas, where are the answers??** Answers are for losers. I have
been thinking a lot about this and the best way for you to prepare and
learn is to look into these questions yourself.

This cookbook or Google will help you a long way. Some questions we
discuss directly on the live stream.

Live Streams
------------

First live stream where we started to collect these questions.

| Podcast Episode: #096 1001 Data Engineering Interview Questions
|------------------|
|First live stream where we collect and try to answer as many interview questions as possible. If this helps people and is fun we do this regularly until we reach 1000 and one.
| [Watch on YouTube](https://youtu.be/WbqRH2r3N40)

All Interview Questions
-----------------------

The interview questions are roughly structured like the sections in the
\"Basic data engineering skills\" part. This makes it easier to navigate
this document. I still need to sort them accordingly.

### SQL DBs

-   What are windowing functions?

-   What is a stored procedure?

-   Why would you use them?

-   What are atomic attributes?

-   Explain ACID props of a database

-   How to optimize queries?

-   What are the different types of JOIN (CROSS, INNER, OUTER)?

-   What is the difference between Clustered Index and Non-Clustered
    Index - with examples?

### The Cloud

-   What is serverless?

-   What is the difference between IaaS, PaaS and SaaS?

-   How do you move from the ingest layer to the Cosumption layer? (In
    Serverless)

-   What is edge computing?

-   What is the difference between cloud and edge and on-premise?

### Linux

-   What is crontab?

### Big Data

-   What are the 4 V's?

-   Which one is most important?

### Kafka

-   What is a topic?

-   How to ensure FIFO?

-   How do you know if all messages in a topic have been fully consumed?

-   What are brokers?

-   What are consumergroups?

-   What is a producer?

### Coding

-   What is the difference between an object and a class?

-   Explain immutability

-   What are AWS Lambda functions and why would you use them?

-   Difference between library, framework and package

-   How to reverse a linked list

-   Difference between args and kwargs

-   Difference between OOP and functional programming

### NoSQL DBs

-   What is a key-value (rowstore) store?

-   What is a columnstore?

-   Diff between Row and col.store

-   What is a document store?

-   Difference between Redshift and Snowflake

### Hadoop

-   What file formats can you use in Hadoop?

-   What is the difference between a namenode and a datanode?

-   What is HDFS?

-   What is the purpose of YARN?

### Lambda Architecture

-   What is streaming and batching?

-   What is the upside of streaming vs batching?

-   What is the difference between lambda and kappa architecture?

-   Can you sync the batch and streaming layer and if yes how?


### Data Warehouse & Data Lake

-   What is a data lake?

-   What is a data warehouse?

-   Are there data lake warehouses?

-   Two data lakes within single warehouse?

-   What is a data mart?

-   What is a slow changing dimension (types)?

-   What is a surrogate key and why use them?

### APIs (REST)

-   What does REST mean?

-   What is idempotency?

-   What are common REST API frameworks (Jersey and Spring)?

### Apache Spark

-   What is an RDD?

-   What is a dataframe?

-   What is a dataset?

-   How is a dataset typesafe?

-   What is Parquet?

-   What is Avro?

-   Difference between Parquet and Avro

-   Tumbling Windows vs. Sliding Windows

-   Difference between batch and stream processing

-   What are microbatches?

### MapReduce

-   What is a use case of mapreduce?

-   Write a pseudo code for wordcount

-   What is a combiner?

### Docker & Kubernetes

-   What is a container?

-   Difference between Docker Container and a Virtual PC

-   What is the easiest way to learn kubernetes fast?

### Data Pipelines

-   What is an example of a serverless pipeline?

-   What is the difference between at most once vs at least once vs
    exactly once?

-   What systems provide transactions?

-   What is a ETL pipeline?

### Airflow

-   What is a DAG (in context of airflow/luigi)?

-   What are hooks/is a hook?

-   What are operators?

-   How to branch?

### DataVisualization

-   What is a BI tool?

### Security/Privacy

-   What is Kerberos?

-   What is a firewall?

-   What is GDPR?

-   What is anonymization?

### Distributed Systems

-   How clusters reach consensus (the answer was using consensus
    protocols like Paxos or Raft). Good I didnt have to explain paxos

-   What is the cap theorem / explain it (What factors should be
    considered when choosing a DB?)

-   How to choose right storage for different data consumers? It's
    always a tricky question

### Apache Flink

-   What is Flink used for?

-   Flink vs Spark?

### GitHub

-   What are branches?

-   What are commits?

-   What's a pull request?

### Dev/Ops

-   What is continuous integration?

-   What is continuous deployment?

-   Difference CI/CD

### Development / Agile

-   What is Scrum?

-   What is OKR?

-   What is Jira and what is it used for?





---

Recommended Books, Courses, and Podcasts
=============================

## Contents
- About Books and Courses
- Books
  - Languages
  - Data Science Tools
  - Business
  - Community Recommendations
- Online Courses
    - Preparation courses
    - Data engineering courses
- Certifications
- Podcasts


## About Books, Courses, and Podcasts

This is a collection of books and courses I can recommend personally.
They are great for every data engineering learner.

I either have used or own these books during my professional work.

I also looked into every online course personally.

If you want to buy a book or course and support my work, please use one of my links below. They are all affiliate marketing links that help me fund this passion.

Of course all this comes at no additional expense to you, but it helps me a lot.

You can find even more interesting books and my whole podcast equipment on my Amazon store:

[Go to the Amazon store](https://www.amazon.com/shop/plumbersofdatascience)



PS: Don't just get a book and expect to learn everything
  - Course certificates alone help you nothing
  - Have a purpose in mind, like a small project
  - Great for use at work

## Books

### Languages

#### Java

[Learning Java: A Bestselling Hands-On Java Tutorial](https://amzn.to/2MgYp8h)

#### Python

[Learning Python, 5th Edition](https://amzn.to/2MdpM34)


#### Scala

[Programming Scala: Scalability = Functional Programming + Objects](https://amzn.to/2VIpww5)


#### Swift

[Learning Swift: Building Apps for macOS, iOS, and Beyond](https://amzn.to/31hDN4e)


### Data Science Tools

#### Apache Spark

[Learning Spark: Lightning-Fast Big Data Analysis](https://amzn.to/31mtAUg)


#### Apache Kafka

[Kafka Streams in Action: Real-time apps and microservices with the Kafka Streams API](https://amzn.to/35uiSOJ)


#### Apache Hadoop

[Hadoop: The Definitive Guide: Storage and Analysis at Internet Scale](https://amzn.to/2VNzf4n)


#### Apache HBase

[HBase: The Definitive Guide: Random Access to Your Planet-Size Data](https://amzn.to/2BbiyGz)


### Business

#### The Lean Startup

[The Lean Startup: How Today's Entrepreneurs Use Continuous Innovation to Create Radically Successful Businesses](https://amzn.to/2Meyv5e)

#### Zero to One

[Zero to One: Notes on Startups, or How to Build the Future](https://amzn.to/2BbBwgr)


#### The Innovators Dilemma

[The Innovator's Dilemma: When New Technologies Cause Great Firms to Fail (Management of Innovation and Change)](https://amzn.to/31eGZ0k)


#### Crossing the Chasm

[Crossing the Chasm, 3rd Edition (Collins Business Essentials)](https://amzn.to/2IU7QZs)


#### Crush It!

[Crush It!: Why Now Is The Time To Cash In On Your Passion](https://amzn.to/33xe7Su)

### Community Recommendations

#### Designing Data-Intensive Applications

"In my opinion, the knowledge contained in this book differentiates a data engineer from a software engineer or a developer. The book strikes a good balance between breadth and depth of discussion on data engineering topics, as well as the tradeoffs we must make due to working with massive amounts of data." -- David Lee on LinkedIn

[Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems](https://amzn.to/2MIqTqJ)


## Online Courses

### Preparation courses

| Course name | Course description | Course URL |
|---|---|---|
| The Bits and Bytes of Computer Networking | This course is designed to provide a full overview of computer networking. We’ll cover everything from the fundamentals of modern networking technologies and protocols to an overview of the cloud to practical applications and network troubleshooting. | https://www.coursera.org/learn/computer-networking |
| Learn SQL \| Codecademy | In this SQL course, you'll learn how to manage large datasets and analyze real data using the standard data management language. | https://www.codecademy.com/learn/learn-sql |
| Learn Python 3 \| Codecademy | Learn the basics of Python 3, one of the most powerful, versatile, and in-demand programming languages today. | https://www.codecademy.com/learn/learn-python-3 |

### Data engineering courses

| Course name | Course description | Course URL |
|---|---|---|
| **1. Data Engineering Basics** |  |  |
| Introduction to Data Engineering | Introduction to Data Engineering with over 1 hour of videos including my journey here. | https://learndataengineering.com/p/introduction-to-data-engineering |
| Computer Science Fundamentals | A complete guide of topics and resources you should know as a Data Engineer. | https://learndataengineering.com/p/data-engineering-fundamentals |
| Introduction to Python | Learn all the fundamentals of Python to start coding quick | https://learndataengineering.com/p/introduction-to-python |
| Python for Data Engineers | Learn all the Python topics a Data Engineer needs even if you don't have a coding background | https://learndataengineering.com/p/python-for-data-engineers |
| Docker Fundamentals | Learn all the fundamental Docker concepts with hands-on examples | https://learndataengineering.com/p/docker-fundamentals |
| Successful Job Application | Everything you need to get your dream job in Data Engineering. | https://learndataengineering.com/p/successful-job-application |
| Data Preparation & Cleaning for ML | All you need for preparing data to enable Machine Learning. | https://learndataengineering.com/p/data-preparation-and-cleaning-for-ml |
| **2. Platform & Pipeline Design Fundamentals** |  |  |
| Data Platform And Pipeline Design | Learn how to build data pipelines with templates and examples for Azure, GCP and Hadoop. | https://learndataengineering.com/p/data-pipeline-design |
| Platform & Pipelines Security | Learn the important security fundamentals for Data Engineering | https://learndataengineering.com/p/platform-pipeline-security |
| Choosing Data Stores | Learn the different types of data stores and when to use which. | https://learndataengineering.com/p/choosing-data-stores |
| Schema Design Data Stores | Learn how to design schemas for SQL, NoSQL and Data Warehouses. | https://learndataengineering.com/p/data-modeling |
| **3. Fundamental Tools** |  |  |
| Building APIs with FastAPI | Learn the fundamentals of designing, creating and deploying APIs with FastAPI and Docker | https://learndataengineering.com/p/apis-with-fastapi-course |
| Apache Kafka Fundamentals | Learn the fundamentals of Apache Kafka | https://learndataengineering.com/p/apache-kafka-fundamentals |
| Apache Spark Fundamentals | Apache Spark quick start course in Python with Jupyter notebooks, DataFrames, SparkSQL and RDDs. | https://learndataengineering.com/p/learning-apache-spark-fundamentals |
| Data Engineering on Databricks | Everything you need to get started with Databricks. From setup to building ETL pipelines &amp; warehousing. | https://learndataengineering.com/p/data-engineering-on-databricks |
| MongoDB Fundamentals | Learn how to use MongoDB | https://learndataengineering.com/p/mongodb-fundamentals-course |
| Log Analysis with Elasticsearch | Learn how to monitor and debug your data pipelines | https://learndataengineering.com/p/log-analysis-with-elasticsearch |
| Airflow Workflow Orchestration | Learn how to orchestrate your data pipelines with Apache Airflow | https://learndataengineering.com/p/learn-apache-airflow |
| Snowflake for Data Engineers | Everything you need to get started with Snowflake | https://learndataengineering.com/p/snowflake-for-data-engineers |
| dbt for Data Engineers | Everything you need to work with dbt and Snowflake | https://learndataengineering.com/p/dbt-for-data-engineers |
| **4. Full Hands-On Example Projects** |  |  |
| Data Engineering on AWS | Full 5 hours course with complete example project. Building stream and batch processing pipelines on AWS. | https://learndataengineering.com/p/data-engineering-on-aws |
| Data Engineering on Azure | Ingest, Store, Process, Serve and Visualize Streams of Data by Building Streaming Data Pipelines in Azure. | https://learndataengineering.com/p/build-streaming-data-pipelines-in-azure |
| Data Engineering on GCP | Everything you need to start with Google Cloud. | https://learndataengineering.com/p/data-engineering-on-gcp |
| Modern Data Warehouses & Data Lakes | How to integrate a Data Lake with a Data Warehouse and query data directly from files | https://learndataengineering.com/p/modern-data-warehouses |
| Machine Learning & Containerization On AWS | Build a app that analyzes the sentiment of tweets and visualizing them on a user interface hosted as container | https://learndataengineering.com/p/ml-on-aws |
| Contact Tracing with Elasticsearch | Track 100,000 users in San Francisco using Elasticsearch and an interactive Streamlit user interface | https://learndataengineering.com/p/contact-tracing-with-elasticsearch |
| Document Streaming Project | Document Streaming with FastAPI, Kafka, Spark Streaming, MongoDB and Streamlit | https://learndataengineering.com/p/document-streaming |
| Storing & Visualizing Time Series Data with InfluxDB and Grafana | Learn how to use InfluxDB to store time series data and visualize interactive dashboards with Grafana | https://learndataengineering.com/p/time-series-influxdb-grafana |
| Data Engineering with Hadoop | Hadoop Project with HDFS, YARN, MapReduce, Hive and Sqoop! | https://learndataengineering.com/p/data-engineering-with-hadoop |
| Dockerized ETL | Learn how quickly set up a simple ETL script with AWS TDengine & Grafana | https://learndataengineering.com/p/timeseries-etl-with-aws-tdengine-grafana |

## Certifications

Here's a list of great certifications that you can do on AWS and Azure. We left out GCP here, because the adoption of AWS and Azure is a lot higher and that's why I recommend to start with one of these. The costs are usually for doing the certification tests. We also added the level and prerequisites to make it easier for you make the decision which one fits for you.

| Platform | Certification Name                                      | Price | Level       | Prerequisite Experience                                                                  | URL                                                                                                          |
|----------|---------------------------------------------------------|-------|-------------|------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| AWS      | AWS Certified Cloud Practitioner (maybe)               | 100   | Beginner    | Familiarity with the AWS platform is recommended but not required.                       | [Link](https://aws.amazon.com/certification/certified-cloud-practitioner/)                                   |
| AWS      | AWS Certified Solutions Architect                      | 300   | Expert      | AWS Certified Solutions Architect - Professional is intended for individuals with two or more years of hands-on experience designing and deploying cloud architecture on AWS. | [Link](https://aws.amazon.com/certification/certified-solutions-architect-professional/?ch=sec&sec=rmg&d=1) |
| AWS      | AWS Certified Solutions Architect                      | 150   | Intermediate| This is an ideal starting point for candidates with AWS Cloud or strong on-premises IT experience. This exam does not require deep hands-on coding experience, although familiarity with basic programming concepts would be an advantage. | [Link](https://aws.amazon.com/certification/certified-solutions-architect-associate/)                        |
| AWS      | AWS Certified Data Engineer                            | 150   | Intermediate| The ideal candidate for this exam has the equivalent of 2-3 years of experience in data engineering or data architecture and a minimum of 1-2 years of hands-on experience with AWS services. | [Link](https://aws.amazon.com/certification/certified-data-engineer-associate/)                              |
| Azure    | Microsoft Certified: Azure Cosmos DB Developer Specialty| 165   | Intermediate|                                                                                          | [Link](https://learn.microsoft.com/en-us/credentials/certifications/azure-cosmos-db-developer-specialty/?practice-assessment-type=certification) |
| Azure    | Microsoft Certified: Azure Data Engineer Associate - DP 203| 165   | Intermediate|                                                                                          | [Link](https://learn.microsoft.com/en-us/credentials/certifications/azure-data-engineer/?practice-assessment-type=certification) |
| Azure    | Microsoft Certified: Azure Data Fundamentals           | 99    | Beginner    |                                                                                          | [Link](https://learn.microsoft.com/en-us/credentials/certifications/azure-data-fundamentals/?practice-assessment-type=certification) |
| Azure    | Microsoft Certified: Azure Database Administrator Associate| 165   | Intermediate|                                                                                          | [Link](https://learn.microsoft.com/en-us/credentials/certifications/azure-database-administrator-associate/?practice-assessment-type=certification) |
| Azure    | Microsoft Certified: Azure Developer Associate         | 165   | Intermediate|                                                                                          | [Link](https://learn.microsoft.com/en-us/credentials/certifications/azure-developer/?practice-assessment-type=certification) |
| Azure    | Microsoft Certified: Azure Fundamentals                | 99    | Beginner    |                                                                                          | [Link](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/?practice-assessment-type=certification) |
| Azure    | Microsoft Certified: Azure Solutions Architect Expert  | 165   | Expert      | Microsoft Certified: Azure Administrator Associate certification                        | [Link](https://learn.microsoft.com/en-us/credentials/certifications/azure-solutions-architect/)             |
| Azure    | Microsoft Certified: Fabric Analytics Engineer Associate| 165   | Intermediate|                                                                                          | [Link](https://learn.microsoft.com/en-us/credentials/certifications/fabric-analytics-engineer-associate/?practice-assessment-type=certification) |
| Azure    | Microsoft Certified: Fabric Data Engineer Associate    | 165   | Intermediate|                                                                                          | [Link](https://learn.microsoft.com/en-us/credentials/certifications/fabric-data-engineer-associate/)        |
| Azure    | Microsoft Certified: Power BI Data Analyst Associate   | 165   | Intermediate|                                                                                          | [Link](https://learn.microsoft.com/en-us/credentials/certifications/data-analyst-associate/?practice-assessment-type=certification) |


## Podcasts
Top five podcasts by the number of episodes created.

### Super Data Science

[The latest machine learning, A.I., and data career topics from across both academia and industry are brought to you by host Dr. Jon Krohn on the Super Data Science Podcast.](https://podcasts.apple.com/us/podcast/super-data-science/id1163599059)

### Data Skeptic

[The Data Skeptic Podcast features interviews and discussion of topics related to data science, statistics, machine learning, artificial intelligence and the like, all from the perspective of applying critical thinking and the scientific method to evaluate the veracity of claims and efficacy of approaches.](https://podcasts.apple.com/us/podcast/data-skeptic/id890348705)

### Data Engineering Podcast

[This show goes behind the scenes for the tools, techniques, and difficulties associated with the discipline of data engineering. Databases, workflows, automation, and data manipulation are just some of the topics that you will find here.](https://podcasts.apple.com/us/podcast/data-engineering-podcast/id1193040557?mt=2)

### Roaring Elephant BiteSized Big Tech

[A weekly community podcast about Big Technology with a focus on Open Source, Advanced Analytics and other modern magic.](https://roaringelephant.org/)

### SQL Data Partners Podcast

[Hosted by Carlos L Chacon, the SQL Data Partners Podcast focuses on Microsoft data platform related topics mixed with a sprinkling of professional development. Carlos and guests discuss new and familiar features and ideas and how you might apply them in your environments.](https://podcasts.apple.com/us/podcast/sql-data-partners-podcast/id1027394388)

### Complete list
| Host name               | Podcast name                                                                     | Access podcast                                                                                                                                                 |
|-------------------------|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Jon Krohn               | Super Data Science                                                               | https://www.superdatascience.com/podcast                                                                                                                       |
| Kyle Polich             | Data Skeptic                                                                     | https://dataskeptic.com/                                                                                                                                       |
| Tobias Macey            | Data Engineering Podcast                                                         | https://www.dataengineeringpodcast.com/                                                                                                                        |
| Dave Russell            | Roaring Elephant - Bite-Sized Big Tech                                           | https://roaringelephant.org/                                                                                                                                   |
| Carlos L Chacon         | SQL Data Partners Podcast                                                        | https://sqldatapartners.com/podcast/                                                                                                                           |
| Jason Himmelstein       | BIFocal - Clarifying Business Intelligence                                       | https://bifocal.show/                                                                                                                                          |
| Scott Hirleman          | Data Mesh Radio                                                                  | https://daappod.com/data-mesh-radio/                                                                                                                           |
| Jonathan Schwabish      | PolicyViz                                                                        | https://policyviz.com/podcast/                                                                                                                                 |
| Al Martin               | Making Data Simple                                                               | https://www.ibm.com/blogs/journey-to-ai/2021/02/making-data-simple-this-week-we-continue-our-discussion-on-data-framework-and-what-is-meant-by-data-framework/ |
| John David Ariansen     | How to Get an Analytics Job                                                      | https://www.silvertoneanalytics.com/how-to-get-an-analytics-job/                                                                                               |
| Moritz Stefaner         | Data Stories                                                                     | https://datastori.es/                                                                                                                                          |
| Hilary Parker           | Not So Standard Deviations                                                       | https://nssdeviations.com/                                                                                                                                     |
| Ben Lorica              | The Data Exchange with Ben Lorica                                                | https://thedataexchange.media/author/bglorica/                                                                                                                 |
| Juan Sequeda            | Catalog & Cocktails                                                              | https://data.world/resources/podcasts/                                                                                                                         |
| Wayne Eckerson          | Secrets of Data Analytics Leaders                                                | https://www.eckerson.com/podcasts/secrets-of-data-analytics-leaders                                                                                            |
| Guy Glantser            | SQL Server Radio                                                                 | https://www.sqlserverradio.com/                                                                                                                                |
| Eitan Blumin            | SQL Server Radio                                                                 | https://www.sqlserverradio.com/                                                                                                                                |
| Jason Tan               | The Analytics Show                                                               | https://ddalabs.ai/the-analytics-show/                                                                                                                         |
| Hugo Bowne-Anderson     | DataFramed                                                                       | https://www.datacamp.com/podcast                                                                                                                               |
| Kostas Pardalis         | The Data Stack Show                                                              | https://datastackshow.com/                                                                                                                                     |
| Eric Dodds              | The Data Stack Show                                                              | https://datastackshow.com/                                                                                                                                     |
| Catherine King          | The Business of Data Podcast                                                     | https://podcasts.apple.com/gb/podcast/the-business-of-data-podcast/id1528796448                                                                                |
|                         | The Business of Data                                                             | https://business-of-data.com/podcasts/                                                                                                                         |
| James Le                | Datacast                                                                         | https://datacast.simplecast.com/                                                                                                                               |
| Mike Delgado            | DataTalk                                                                         | https://podcasts.apple.com/us/podcast/datatalk/id1398548129                                                                                                    |
| Matt Housley            | Monday Morning Data Chat                                                         | https://podcasts.apple.com/us/podcast/monday-morning-data-chat/id1565154727                                                                                    |
| Francesco Gadaleta      | Data Science at Home                                                             | https://datascienceathome.com/                                                                                                                                 |
| Alli Torban             | Data Viz Today                                                                   | https://dataviztoday.com/                                                                                                                                      |
| Steve Jones             | Voice of the DBA                                                                 | https://voiceofthedba.com/                                                                                                                                     |
| Lea Pica                | The Present Beyond Measure Show: Data Storytelling, Presentation & Visualization | https://leapica.com/podcast/                                                                                                                                   |
| Samir Sharma            | The Data Strategy Show                                                           | https://podcasts.apple.com/us/podcast/the-data-strategy-show/id1515194422                                                                                      |
| Cindi Howson            | The Data Chief                                                                   | https://www.thoughtspot.com/data-chief/podcast                                                                                                                 |
| Cole Nussbaumer Knaflic | storytelling with data podcast                                                   | https://storytellingwithdata.libsyn.com/                                                                                                                       |
| Margot Gerritsen        | Women in Data Science                                                            | https://www.widsconference.org/podcast.html                                                                                                                    |
| Jonas Christensen       | Leaders of Analytics                                                             | https://www.leadersofanalytics.com/episode/the-future-of-analytics-leadership-with-john-thompson                                                               |
| Matt Brady              | ZUMA: Data For Good                                                              | https://www.youtube.com/@zuma-dataforgood                                                                                                                      |
| Julia Schottenstein     | The Analytics Engineering Podcast                                                | https://roundup.getdbt.com/s/the-analytics-engineering-podcast                                                                                                 |
|                         | Data Unlocked                                                                    | https://dataunlocked.buzzsprout.com/                                                                                                                           |
| Boris Jabes             | The Sequel Show                                                                  | https://www.thesequelshow.com/                                                                                                                                 |
|                         | Data Radicals                                                                    | https://www.alation.com/podcast/                                                                                                                               |
| Nicola Askham           | The Data Governance                                                              | https://www.nicolaaskham.com/podcast                                                                                                                           |
| Boaz Farkash            | The Data Engineering Show                                                        | https://www.dataengineeringshow.com/                                                                                                                           |
| Bob Haffner             | The Engineering Side of Data                                                     | https://podcasts.apple.com/us/podcast/the-engineering-side-of-data/id1566999533                                                                                |
| Dan Linstedt            | Data Vault Alliance                                                              | https://datavaultalliance.com/category/news/podcasts/                                                                                                          |
| Dustin Schimek          | Data Ideas                                                                       | https://podcasts.apple.com/us/podcast/data-ideas/id1650322207                                                                                                  |
| Alex Merced             | The datanation                                                                   | https://podcasts.apple.com/be/podcast/the-datanation-podcast-podcast-for-data-engineers/id1608638822                                                           |
| Thomas Bustos           | Let's Talk AI                                                                    | https://www.youtube.com/@lets-talk-ai                                                                                                                          |
| Jahanvee Narang         | Decoding Data Analytics                                                          | https://www.youtube.com/@decodingdataanalytics/videos                                                                                                          |


---

Updates
============

What's new? Here you can find a list of all the updates with links to the sections

- **2025-07-21**
  - Added a list of my students favorite datasets and APIs [click here](07-DataSources.md#Student-Favorites)


- **2025-06-11**
  - Released the first playable demo of the Spark Optimization Playground [click here](https://bit.ly/play-spark-optimization)


- **2025-03-25**
  - Added a detailed 14-week roadmap to Data Engineering for Data Scientists [click here](01-Introduction.md#roadmap-for-data-scientists)


- **2025-03-05**
  - Added a detailed 11-week roadmap to Data Engineering for Beginners [click here](01-Introduction.md#roadmap-for-beginners)


- **2025-03-04**
  - Added a detailed 10-week roadmap to Data Engineering for Data Analysts [click here](01-Introduction.md#roadmap-for-data-analysts)


- **2024-12-11**
  - Prepared the 81 most important questions for platform & pipeline design. Specifically looking at the data source and the goals [click here](03-AdvancedSkills.md#81-platform-and-pipeline-design-questions)


- **2024-11-28**
  - Prepared a GenAI RAG example project that you can run on your own computer without internet. It uses Ollama with Mistral model and Elasticsearch. Working on a way of creating embeddings from pdf files and inserting them into Elsaticsearch for queries [click here](04-HandsOnCourse.md#genai-retrieval-augmented-generation-with-ollama-and-elasticsearch)


- **2024-11-23**
  - Added an overview of AWS and Azure cloud certifications for Data Engineers. From beginners to experts [click here](09-BooksAndCourses.md#Certifications)


- **2024-07-31**
  - Added 10 platform architecture react videos I did to the "Best Practices" section. This way you get a better feeling of what companies are doing and which tools they use [click here](06-BestPracticesCloud.md#best-practices)


- **2024-07-17**
  - Added 20 API interview questoins and their answers [click here](08-InterviewQuestions.md#apis)
  - Added 10 Python interview questions and their answers [click here](03-AdvancedSkills.md#python)


- **2024-07-08**
  - Added large article about Snowflake and dbt for Data Engineers [click here](03-AdvancedSkills.md#analytical-data-stores)
  - Added new secton "Analytical Data Stores" to Advanced skills with the Snowflake & dbt infos.
  - Put SQL and NoSQL datastores into a new section "Transactional Data Stores"


- **2024-03-20**
  - Added roadmap for Software Engineers / Computer Scientists [click here](01-Introduction.md#roadmap-for-software-engineers)
  - Added many questions and answers from my interview on the Super Data Science Podcast (plus links to YouTube and the Podcast) [click here](01-Introduction.md#Interview-with-Andreas-on-the-Super-Data-Science-Podcast)


- **2024-03-13**
  - Added "How to become a Senior Data Engineer" live stream series as a blog post with images shown in the live streams and the links to the videos. [click here](01-Introduction.md#how-to-become-a-senior-data-engineer)


- **2024-03-08**
  - Included Data Engineering skills matrix into the introduction with link to the live stream. [click here](01-Introduction.md#data-engineers-skills-matrix)


- **2024-03-01**
  - Added updates section
  - Reworked the Hands-on courses section with 5 free courses / tutorials from Andreas on YouTube [click here](04-HandsOnCourse.md)


- **2024-02-28**
  - Added Data Engineering Roadmap for Data Scientists: [click here](01-Introduction.md#roadmap-for-data-scientists)


- **2024-02-25**
  - Data Engineering Roadmap for Software Engineers: [click here](01-Introduction.md#roadmap-for-software-engineers)


- **2024-02-20**
  - Data Engineering Roadmap for Data Analysts: [click here](01-Introduction.md#roadmap-for-data-analysts)



<!---
| Date | Topic | Link
|------------------|
| 2024-02-28 | Added updates section - sdfs | [click here](sections/01-Introduction.md#roadmap-for-data-scientists)
| 2024-02-28 | Data Engineering Roadmap for Data Scientists | [click here](sections/01-Introduction.md#roadmap-for-data-scientists)
| 2024-02-25 | Data Engineering Roadmap for Software Engineers | [click here](sections/01-Introduction.md#roadmap-for-software-engineers)
| 2024-02-20 | Data Engineering Roadmap for Data Analysts | [click here](sections/01-Introduction.md#roadmap-for-data-analysts)
--->


---

