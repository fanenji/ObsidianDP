---
title: "Data Engineering: Architectures & Strategies for Handling Sensitive Data"
source: https://medium.com/data-science-collective/data-engineering-architectures-strategies-for-handling-sensitive-data-0897ab9abc61
author:
  - "[[Hussein Jundi]]"
published: 2025-12-11
created: 2026-04-04
description: "Data Engineering: Architectures & Strategies for Handling Sensitive Data Strategies and architectures to handle sensitive data efficiently and securely according to an organization’s data maturity …"
tags:
  - clippings
  - data-governance
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)## [Data Science Collective](https://medium.com/data-science-collective?source=post_page---publication_nav-8993e01dcfd3-0897ab9abc61---------------------------------------)

[![Data Science Collective](https://miro.medium.com/v2/resize:fill:76:76/1*0nV0Q-FBHj94Kggq00pG2Q.jpeg)](https://medium.com/data-science-collective?source=post_page---post_publication_sidebar-8993e01dcfd3-0897ab9abc61---------------------------------------)

Advice, insights, and ideas from the Medium data science community

## Strategies and architectures to handle sensitive data efficiently and securely according to an organization’s data maturity level.

*Building an end-to-end secure data architecture? Looking for solution architectures that ensure compliance* *with the laws and regulations?*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*PKDIlPG3yjGepvRl)

Photo by Pierre Bamin on Unsplash

> *In this article, we will discuss strategies for sensitive data handling utilized by data practitioners architecting data solutions. We describe scenarios where specific solutions require different approaches, depending on the organization’s data maturity, and detail the necessary components shaping the final solution architecture.*

The growth of data has significantly increased the challenge for engineers and architects to balance between performance and security. On one hand making data available in a timely and flexible manner, on another maintaining compliance standards and security.

The emergence of laws and regulations like the General Data Protection Regulation (GDPR) and California Consumer Privacy (CCPA) contributed to this complexity. Data solutions are expected to meet all these requirements, fulfilling thus consumers’ expectations when it comes to privacy, and minimizing the consequences of any potential data leaks.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*SEGOuhZ4Mvb89CqS.png)

Image by Author

Numerous robust approaches for data de-identifications exist. To narrow down our list of options, we can also look at recommendations provided by the protection regulations and acts for handling personal data. It’s not the lack of approaches and algorithms that make the process of de-identification of data complex, but the conflicting requirements, SLAs, and data maturity of an organization.

Constraints such as tight deadlines, limited resources, and expertise can lead to skipping the stage for incorporating a de-identification within a data architecture. Given the impact data leaks have on an organization, it’s clear that implementing the simplest de-identification techniques can mitigate substantial risks.

The diagram below gives an overview of what to expect in the coming sections. If you’re familiar with such architecture diagrams, it is clear that some details are taken out to hold the focus on the sections discussed later. I leave out detailing specific sections to my other existing articles.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*6aP9ZBOhZGsBRwLC.png)

Data Solution architecture — Image by Author

The focus in this story will be on data de-identification techniques, and their integration into a data solution architecture. We consider the important role an organization’s data maturity stage plays, ranging from small organizations to multi-national enterprises on the final solution.

> *Note that three different maturity levels are presented. In reality, depending on the data maturity models or framework you adopt, it can vary significantly.*

## Maturity Level 1

**Data Maturity Description:** This level represents the initial first stage for data maturity within this article. This level’s organization is characterized by:

- No established data management practices
- Undefined data roles.
- Data warehouse is in the early stages of development and not fully modeled
- Data is provided “as-is” to analysts to report on needed KPIs
- Small data infrastructure team, potentially standing for multiple roles.

**Recommendation:** Within this maturity level, it becomes obvious that many limitations are present to bring a full best practices solution to deliver on all data requests. In order to achieve full compliance for the organization’s data platform and reporting architecture, it is best to reduce the effort required to achieve laws and regulation compliance. This includes fully anonymizing the data where required using Data Masking, or further excluding any personally identifiable columns from each reporting infrastructure. This will allow continued scoped Analytics and BI delivery for necessary KPIs until the organization levels its data maturity.

**Data De-identification Technique Description:** Data Masking

Described as replacing personally identifiable information with meaningless characters in a way that cannot be reverse-engineered.

**Advantages**

- Complaint data architecture
- Requires low effort

**Disadvantages**

- Limitations in Customer Analytics & BI Capabilities

**Solution Architecture**

The architecture describes the required components to achieve compliance, spanning from data ingestion to data consumption. It identifies stages where data anonymization or exclusion can take place. The selection of services for data anonymization will depend on the organization’s tech stack, ranging from an ETL tool to a simple script.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*2rFFK2P8sUNdJJZQ.png)

Maturity Level 1 Solution Architecture — Image by Author

## Maturity Level 2

**Data Maturity Description:** This level represents an intermediate level of data maturity described by:

- Implementation of some data management practices.
- Undefined data roles.
- Manual Data Discovery & Cataloging.
- Partially modeled data warehouse.
- Small data infrastructure team consisting of -3 members.

**Recommendation:** This maturity level provides more opportunities for enhancing the architecture, adding additional components that enable data de-identification, with the possibility of re-identification. A Data Catalog for storing all important data assets (ideally all), along with classifications on selected tables and fields for de-identification, and a token store as an enabler to re-identify anonymized data. Both are crucial for a functional working sensitive data-handling solution.

**Data De-identification Technique Description:** Data Pseudonymization

Defined in Article 3 of the GDPR as:

“The processing of personal data in such a manner that the personal data can no longer be attributed to a specific data subject without the use of additional information, provided that such additional information is kept separately and is subject to technical and organizational measures to ensure that the personal data are not attributed to an identified or identifiable natural person.”

**Advantages**

- Complaint data architecture
- Medium effort
- Enhanced opportunities for customer analytics.

**Disadvantages**

- Manual data discovery and classification efforts
- Introduces added system complexity

**Solution Architecture**

This architecture evolves the previous solution with an additional Data Catalog and a Token Vault. With best-case scenarios having Data Catalogs populated automatically by data discovery and profiling tools, here we assume manual population by Data Stewards or Subject Matter Experts (SMEs). The Catalog can be accessed automatically by services, thus identifying sensitive data for applying the required anonymization technique before data reaches the consumption stages.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*8ivMx0fk0KAE7N7Q.png)

Maturity Level 2 Solution Architecture — Image by Author

Re-identification becomes possible through pseudonymization tokens that are stored in a separate token storage ensuring compliance. Access to the tokens is only granted to authorized access groups. In some situations this would require the users to access different storage solutions to fully utilize the data. Knowing that this may come as a requirement for the organization, many platforms support data federation, reducing the overhead of access management, and maintaining separation between both storage systems. (depending on the use case, data federation may not ensure the organization’s system Separation requirements).

**Note:** Some platforms embed such solutions in their product offerings, thus abstracting away complexities for consumers to implement them themselves. It could be nonetheless needed that such actions are taken before the data reaches the platforms.

## Maturity Level 3

**Data Maturity Description:** This level represents an advanced stage of data maturity

- Established data management and governance practices.
- Automated Data Discovery & Classification
- Data Products are fully modelled and tested
- Multi-national operating data teams

**Recommendation:** On this level, setting the stage for best practice solution architectures becomes feasible. with all necessary components in place. The aim is to ensure a fully automated and compliant solution.

**Data De-identification Technique Description:** Data pseudonymization & Encryption

As discussed in the previous level, Pseudonymization is sufficient to provide a compliant architecture by separating personal data from individual users, while encryption tackles data confidentiality, using keys and cryptographic algorithms for encrypting sensitive data. Accessibility to the data through decryption is only by authorized users with access to the keys. On this level, Encryption can be utilized as an extra security layer to ensure encrypted data transmission between systems. (depending on the organization’s sector, this may become a regulatory requirement)

**Advantages**

- Complaint data architecture
- Improved security
- Established full customer analytics capabilities
- Automation & processes

**Disadvantages**

- Increased architecture complexity

**Solution Architecture**

Two new components are introduced on this level. A data encryption stage during data transformation and automated data discovery and classification service *(Note: If cloud services are used, incurring additional costs can be justified to simplify implementation complexity)*. The automated service handles metadata collection and profiling across data sources, reducing previous manual input requirements into the Data Catalog. Though this provides an automated approach, the detection capabilities of these systems, may require further involvement from data stewards, where complex data assets present a challenge for these tools to capture accurately.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*lFrGE1D_kFvBpO8m.png)

Data Architecture — Image by Author

## Conclusion

Implementing solutions for handling sensitive as described, requires careful assessment of an organization’s data maturity regardless of the model used. Navigating between levels of complexity, available resources and the compliance level determines the team’s success and flexibility in implementing the right data solution architecture.

**Happy Designing!**

## References:

[https://www.k2view.com/blog/pseudonymization-vs-encryption/#Top-Use-Cases-for-Pseudonymization-vs-Encryption](https://www.k2view.com/blog/pseudonymization-vs-encryption/#Top-Use-Cases-for-Pseudonymization-vs-Encryption)

[Protecting Sensitive Data in Analytics: A Data Engineering Perspective | by QuantumBlack, AI by McKinsey | QuantumBlack, AI by McKinsey | Medium](https://medium.com/quantumblack/protecting-sensitive-data-in-analytics-a-data-engineering-perspective-c0ab95cd32cc)

[https://www.piiano.com/blog/pseudonymization-vs-tokenization](https://www.piiano.com/blog/pseudonymization-vs-tokenization)

## Responses (1)

S Parodi

What are your thoughts?  

```c
A well-structured perspective on how sensitive data handling is less about a single solution and more about aligning architecture with organizational maturity. The balance between accessibility and compliance is where most real-world systems…more
```

10