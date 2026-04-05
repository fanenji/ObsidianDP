---
title: "Implementing CI/CD for dbt: First Steps"
source: https://medium.com/inthepipeline/implementing-ci-cd-for-dbt-first-steps-f595247bc25b
author:
  - "[[Jens Wilms]]"
published: 2023-11-14
created: 2026-04-04
description: "Implementing CI/CD for dbt: First Steps It’s Friday afternoon and you’re ready to enjoy your well-deserved weekend. Anxiety kicks in as you hear a new message from Slack. “Hey, can we hop on a …"
tags:
  - clippings
  - dbt
  - ci-cd
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)## [In the Pipeline](https://medium.com/inthepipeline?source=post_page---publication_nav-95447f9865fd-f595247bc25b---------------------------------------)

[![In the Pipeline](https://miro.medium.com/v2/resize:fill:76:76/1*uivUOAnjInp-pN1sRWaODg.jpeg)](https://medium.com/inthepipeline?source=post_page---post_publication_sidebar-95447f9865fd-f595247bc25b---------------------------------------)

Articles for data and analytics engineers

It’s Friday afternoon and you’re ready to enjoy your well-deserved weekend. Anxiety kicks in as you hear a new message from Slack. “Hey, can we hop on a call real quick? I promise it won’t be long”. An analyst asks you to revisit a pipeline as she notices some strange-looking data in her dashboard. And after some digging, you noticed that some newly pushed dbt code caused breakages downstream. Yikes, there goes your Friday night.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*DouBg2XG8C_DxLH0WNDQGA.png)

CI/CD for dbt — First Steps

## Why CI/CD matters

Implementing continuous integration and continuous delivery pipelines provides immense value for dbt projects and data teams. By automating testing and deployment processes, CI/CD helps with:

- Improving software reliability
- Enabling faster delivery of new features
- Reducing the risk of downstream impact on new code changes
- Increasing visibility into build health and test coverage
- Freeing up time spent on manual checking and fixing errors

All in all, CI/CD allows you to focus on building pipelines and enables analysts to focus on core data modeling tasks.

In this article, I’ll walk through the first steps to begin building a CI/CD foundation for your dbt pipeline. We’ll start by setting up a CI/CD platform, then we’ll set up environments to ensure errors are caught before pushing to production. After, we’ll install linting to ensure a uniform format to your code and create some initial tests for critical models to ensure they are as expected. Finally, I’ll show how external open-source tools can provide some out-of-the-box extensive testing that’ll help you prevent downstream breakages.## [dbt best practices in action at Cal-ITP’s data-infra project](https://medium.com/inthepipeline/dbt-best-practices-in-action-at-cal-itps-data-infra-project-0d11adf5513d?source=post_page-----f595247bc25b---------------------------------------)

### Cal-ITP uses a standardized PR template and automated report for comprehensive PR review. See their process in-action…

medium.com

[View original](https://medium.com/inthepipeline/dbt-best-practices-in-action-at-cal-itps-data-infra-project-0d11adf5513d?source=post_page-----f595247bc25b---------------------------------------)

## Setting up a CI/CD Platform

The first step to creating a CI/CD workflow is choosing the right platform. There are a few options available: GitHub Actions, GitLab CI/CD, CircleCI, and Jenkins, to name a few.

Of all the data engineers I’ve talked to, about 90% use GitHub Actions. It’s a natural fit for dbt users given its tight integration with GitHub for source control, and it’s quick to set up workflows right in your repos, so that’s what I’ll focus on for this article.

A workflow file allows you to define automation jobs for your GitHub repository using YAML syntax. Workflow files live under `.github/workflows` in your repo. You can set up a trigger (e.g. on pull\_request or a cron job) and define jobs. A job is a series of steps that should be run on the trigger, such as build, test, lint, release, and deploy. Jobs can be run in series or parallel. For more information, check out [the GitHub documentation](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)

To setup GitHub Actions in your dbt project, go to your repo and:

1. Create a `.github/workflows` folder
2. Create a workflow file to set up a scheduler: `run.yml`

Use the following template for your workflow file:

```c
name: My first worfklow
  
# Set up the trigger for this command
on:
  ...
      

# Define the jobs
jobs:
  run:
  ...
```

## Set Up Staging/Production Environments

Up next is setting up different environments. At a minimum, you’ll want to configure a staging and production environment for your dbt pipeline.

The **staging** environment acts as an integration layer to validate changes before pushing them to production. This “safety net” environment mirrors production but keeps risk away from impacting end users.

Staging allows complete testing and validation of changes in isolation:

- Run full dbt builds to catch breaking changes
- Integration testing with downstream dependencies
- Validate metrics and reporting are as expected
- Review performance impacts under load before releasing

Meanwhile, the **production** environment contains vetted changes ready for consumption. This provides stability for any applications relying on the dbt models. At a later stage, you can optimize for having multiple environments such as a development stage for engineers to play around or a UAT (User Acceptance Testing) to test for business users, but for now, we’ll stick to staging & production.

We’ll start by setting up a trigger in our workflow file, so our GitHub Actions jobs will run everything once we make a pull request on our staging branch.

```c
name: My first worfklow

# Set up the trigger for this command
on:
  pull_request:
    branches:
    - staging
```## [Next-Level Data Validation Toolkit for dbt Data Projects — Introducing Recce](https://medium.com/inthepipeline/data-modeling-validation-toolkit-better-pr-review-open-source-recce-b6e207b6c1f2?source=post_page-----f595247bc25b---------------------------------------)

### The ultimate data modeling validation toolkit for comprehensive PR review that doesn’t slow down merge times

medium.com

[View original](https://medium.com/inthepipeline/data-modeling-validation-toolkit-better-pr-review-open-source-recce-b6e207b6c1f2?source=post_page-----f595247bc25b---------------------------------------)

## Configure Linting

The first job we’ll set up is linting. SQL linting ensures your code is set to standardized styles and best practices. This improves overall code quality and maintainability within dbt projects.

A linter can check for issues like:

- Improper indentation or spacing
- Non-descriptive model and column names
- Overly complex SQL logic
- Unoptimized join patterns

For dbt, [SQLFluff](https://github.com/sqlfluff/sqlfluff) is a popular linting tool optimized for data workflows. It integrates with dbt and supports configuring custom rule sets.

To use SQLFluff for dbt, you first create a `.sqlfluff` file in your project’s root directory and add the following. This will ensure that it will use the dbt template and not the sqlfluff’s default jinja template. Add your local SQL dialect here too.

```c
[sqlfluff]
templater = dbt
dialect = snowflake (or whichever you are using)
```

Then we’ll add a `.sqlfluffignore` file to exclude a few folders

```c
analysis/
macros/
dbt_packages/
target/
```

And then we add the linting to our job in GitHub Actions

```c
[run.yml]
...

jobs:
  run:
  ...
  - name: Install SQLFluff
  run: pip install sqlfluff sqlfluff-templater-dbt
  - name: Run SQLFluff
  run: sqlfluff lint <dir with sql files: e.g. models OR models/marts>/
```

To customize your SQLFluff job, you can add custom rules to your `.sqlfluffignore` file.

```c
[sqlfluff:templater:dbt]
apply_dbt_builtins = true
profile = my_dbt_profile
project_dir = ./my_dbt_project
profiles_dir = ~/.dbt

[sqlfluff:indentation]
indented_joins = False
indented_using_on = True
template_blocks_indent = False

[sqlfluff:rules:capitalisation]
keywords = lower
```

For more information on customizing your SQLFluff, see [their documentation](https://docs.sqlfluff.com/en/stable/configuration.html)

## Add Testing

OK cool, my code is all indented correctly… But how do I prevent my code from breaking?

We’ll start by adding unit tests using dbt’s built-in test framework [(see their docs)](https://docs.getdbt.com/docs/build/tests). These allow validating logic within individual models in isolation and testing whether your data meets pre-defined expectations. You start by writing the test as SQL code, storing them in a `test` folder, and then, using the `dbt test` command to see the results. Some best practices for dbt tests:

- Add basic validation tests for your core models and metrics first. Get the foundations covered.
- Embed test cases directly in model files using dbt’s test nodes. Keep tests alongside the models they validate.
- Leverage dbt snapshots to cache and reuse representative test data sets.
- Enforce a minimum test coverage threshold (70–80%) for new models.
- Run tests on every PR build to get fast feedback on issues.

Here’s an example unit test validating a revenue calculation:

```c
{% test revenue_calculation(model) %}
 
select
  order_id,
  sum(quantity * unit_price) as revenue
from {{ ref('stg_orders') }}
group by 1
  
assert revenue = fct_revenue.revenue

{% endtest %}
```

The test above tests revenue logic in the stg\_orders model by comparing the calculated value to the final revenue model.

Once you’ve defined all your tests (or the tests for the most important models to start) you’d want to add a new job to our GitHub Actions workflow file and run the tests. If any test cases fail, the job will fail and the pull request checks will show the failure.

```c
jobs:
  test:
    runs-on: ubuntu-latest

  Steps:
    - uses: actions/checkout@v2
    - name: Run dbt tests
    run: dbt test
```

You could also add integration tests to confirm dependencies between models work correctly. These validate multi-model interfaces.

With a solid testing foundation, we can prevent tricky regressions from sneaking through down the line. Time to add some protection!

## Adding an extra layer of reliability

To improve the reliability of code reviews, we can incorporate tools such as PipeRider that automatically analyze the downstream data impact of proposed dbt model changes. For example, PipeRider leverages dbt’s lineage feature in their lineage diff and summarizes how a model change affects metrics, columns, dependencies, and other downstream models across the dbt project. You include a test like these to your GitHub Action jobs and review downstream impact. This can help to discover downstream changes, see how the change affects your important metrics, and prevent you from manually checking all models in the staging environment.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*KWHatetZ382aQWmC)

We can include a tool like PipeRider by adding a new job to our `run.yml` file:

```c
jobs:
  piperider-compare:
    runs-on: ubuntu-latest
    permissions:
    pull-requests: write

    steps:
    - uses: actions/checkout@v3
    - name: PipeRider Compare

    uses: InfuseAI/piperider-compare-action@v1
    with:
      cloud_api_token: ${{ secrets.PIPERIDER_CLOUD_TOKEN_ID }}
      cloud_project: ${{ secrets.PIPERIDER_API_PROJECT }}
      upload: true
      share: true
```

## Conclusion

You want to ensure that your data is correct and that the end-users don’t get angry when they realize after two weeks their model is broken, so you can enjoy your Friday afternoon. With all the tools out there, setting up CI/CD is actually not so difficult. The key is starting small — choose a platform like GitHub Actions, configure SQL linting, set up environments, implement testing, and consider impact analysis tools. After that, you can optimize by setting up Slim CI, different environments, and reversion & rollback workflows, but for a beginner — following the steps in the article will open the door to huge gains in productivity, reliability, and development velocity.

[![In the Pipeline](https://miro.medium.com/v2/resize:fill:96:96/1*uivUOAnjInp-pN1sRWaODg.jpeg)](https://medium.com/inthepipeline?source=post_page---post_publication_info--f595247bc25b---------------------------------------)

[![In the Pipeline](https://miro.medium.com/v2/resize:fill:128:128/1*uivUOAnjInp-pN1sRWaODg.jpeg)](https://medium.com/inthepipeline?source=post_page---post_publication_info--f595247bc25b---------------------------------------)

[Last published Aug 19, 2025](https://medium.com/inthepipeline/building-impact-radius-3-three-essential-workflows-for-data-teams-2965f1d207be?source=post_page---post_publication_info--f595247bc25b---------------------------------------)

Articles for data and analytics engineers

[![Jens Wilms](https://miro.medium.com/v2/resize:fill:96:96/1*AbNQi4ccAmIM8AFCuLUV_w.png)](https://medium.com/@pmjens?source=post_page---post_author_info--f595247bc25b---------------------------------------)

[![Jens Wilms](https://miro.medium.com/v2/resize:fill:128:128/1*AbNQi4ccAmIM8AFCuLUV_w.png)](https://medium.com/@pmjens?source=post_page---post_author_info--f595247bc25b---------------------------------------)

[3 following](https://medium.com/@pmjens/following?source=post_page---post_author_info--f595247bc25b---------------------------------------)

Product Manager in the Data & AI space

Notifications