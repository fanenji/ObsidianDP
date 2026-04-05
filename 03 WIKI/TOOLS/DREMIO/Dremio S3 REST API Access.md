---
title: "Dremio S3 REST API Access"
type: conversation
topic: data-platform
created: 2026-02-13
tags:
  - dremio
  - s3
  - gemini
  - tools

---
**Source:** https://aistudio.google.com/u/1/prompts/1EUuK8n9-uazhK_es-_Ph-TdVb1Cilm6Y

## System Instructions

Optional tone and style instructions for the model

---

### User

Can Dremio expose the data in the underlying s3 storage via REST API?

---

### Model

Yes, Dremio can expose data in underlying S3 storage via its REST API, but it's important to understand how. Dremio doesn't directly expose S3's native REST API. Instead, Dremio acts as a query engine and semantic layer on top of your S3 data (and other sources).[1][2] You connect Dremio to your S3 buckets, and then you can query the data within those buckets using Dremio's SQL capabilities.[2] These queries can be executed via Dremio's REST API.[1]

Here's a breakdown:

Connecting Dremio to S3: You first configure S3 as a data source within Dremio.[2][3] This involves providing your AWS credentials and specifying the S3 buckets you want to access.[2] Dremio supports both Amazon S3 and S3-compatible storage.[2][4]

Querying via REST API: Once S3 is a connected source, you can use Dremio's REST API (typically v3) to execute SQL queries against the datasets that reside in S3.[1][5] The results of these queries are then returned through the API.

Semantic Layer: Dremio allows you to create virtual datasets, join data from different sources (including S3), and apply data transformations. These curated views can also be queried via the REST API, providing a more governed and user-friendly way to access the underlying S3 data.[1]

Metadata: Dremio's REST API can also be used to get metadata about your S3 data sources, datasets, and their organization within Dremio.[6]

In summary, while you're not directly hitting an S3 REST endpoint through Dremio in the sense of proxying S3's own API, Dremio provides its own REST API that allows you to query and access the data stored in S3 after you've configured S3 as a source in Dremio.[1] This approach allows Dremio to provide its query acceleration, semantic layer, and security features on top of your S3 data.

---

### User

what's the best way to expose the Dremio API to the internet for public access to open data

---

### Model

Exposing any API to the public internet, including Dremio's, requires careful consideration of security and manageability to protect your data and ensure reliable access for legitimate users. Here's a breakdown of best practices:

1. Authentication and Authorization:

Dedicated API User/Role for Public Access:

Create a specific user or role within Dremio for public API access.[1]

Grant this user/role the principle of least privilege, meaning it should only have read-only access (SELECT permissions) to the specific open data datasets, spaces, or views you intend to expose.[1] Do not grant administrative or write privileges.

Dremio uses a Role-Based Access Control (RBAC) model, allowing granular control over permissions.[1]

API Tokens:

Utilize Dremio's token-based authentication for API access. Dremio supports Personal Access Tokens (PATs) and OAuth access tokens.[2][3]

PATs can be generated via the Dremio console or REST API.[2][3] OAuth access tokens are generally recommended for improved security as they are typically short-lived.[2][3]

Ensure these tokens are securely managed and have appropriate expiration policies.

Anonymous Access (Use with Extreme Caution):

If you truly need unauthenticated public access (e.g., for a public data portal), this typically needs to be managed at a layer in front of Dremio (like an API Gateway) that then uses a pre-configured, highly restricted Dremio user/token to query the data. Direct anonymous access to Dremio's API endpoints is generally not a standard feature for public exposure due to security risks.

2. Network Security and Architecture:

API Gateway:

Highly Recommended. Place an API Gateway (e.g., AWS API Gateway, Azure API Management, Kong, Apigee) in front of your Dremio API endpoints.[4]

Benefits:

Request Throttling/Rate Limiting: Protect Dremio from abuse and ensure fair usage.

Authentication/Authorization Offload: The API Gateway can handle initial authentication (e.g., API key validation for public clients) before forwarding requests to Dremio with a secured token.

Request/Response Transformation: Modify requests or responses if needed.

Caching: Reduce load on Dremio for frequently requested data.

Logging and Monitoring: Centralized logging of API traffic.[5]

Security Policies: Enforce security policies like IP whitelisting/blacklisting.[4]

Web Application Firewall (WAF):

Deploy a WAF to protect against common web exploits (SQL injection, XSS, etc.) even though Dremio has its own security measures.[6]

Reverse Proxy:

A reverse proxy can provide an additional layer of security, load balancing, and SSL termination.

Network Segmentation:

Isolate your Dremio cluster in a private network (VPC). Do not expose Dremio coordinator or executor nodes directly to the public internet. The API Gateway should be the public-facing entry point.

Encryption:

Ensure all communication is over HTTPS (SSL/TLS) to encrypt data in transit.[7] Dremio itself can be configured for SSL.[8][9]

3. Dremio Configuration for Open Data:

Virtual Datasets (VDS):

Create specific VDS in Dremio for your open data. This allows you to:

Define a clear, stable API contract for your data consumers.

Apply necessary data masking, filtering, or transformations before exposing the data.

Decouple the public API from the underlying physical data storage and schema.

Data Masking and Row/Column Level Security:

If any part of the open data still contains sensitive elements, use Dremio's capabilities (potentially with integrations like PlainID or AWS Lake Formation) for fine-grained access control, data masking, and row/column-level security to ensure only appropriate data is exposed.[10][11][12]

4. Monitoring and Logging:[5][13]

Dremio Monitoring: Dremio provides tools and APIs to monitor job activity, catalog usage, and system health.[5][13]

API Gateway Logging: Your API Gateway will provide detailed logs of all incoming requests.

Security Monitoring: Implement security monitoring to detect and respond to suspicious activity. Dremio itself performs security scans and penetration tests on its software.[6]

Audit Logging: Dremio provides audit logging capabilities.[14]

5. Data Governance and Compliance:

Clear Data Usage Policies: Define and publish clear terms of use for your open data API.

Compliance: Ensure your data exposure practices comply with relevant data privacy regulations, even for open data (e.g., anonymization standards). Dremio supports various compliance frameworks.[6][14]

Key Steps Summary:

Define Open Datasets: Clearly identify and prepare the specific datasets in Dremio (preferably as VDS) that will be made public.

Secure Dremio:

Configure RBAC with a dedicated, least-privilege user/role for public access.[1]

Use API token authentication.[2][3]

Implement an API Gateway: This is crucial for security, control, and manageability.[4] Configure it for:

Authentication (e.g., API keys for public clients).

Rate limiting and throttling.

Mapping public API endpoints to specific Dremio queries/VDS.

Network Configuration:

Keep Dremio in a private network.

Use WAF and HTTPS.

Monitoring and Logging: Continuously monitor API usage, Dremio performance, and security logs.[5][13]

By following these best practices, you can expose your Dremio API for public access to open data in a more secure, controlled, and scalable manner.

---
