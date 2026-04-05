---
title: State of testing in dbt - In-Depth Discussions
source: https://discourse.getdbt.com/t/state-of-testing-in-dbt/1778
author:
  - "[[dbt Community Forum]]"
published: 2020-11-04
created: 2026-04-04
description: Hello! My team and I have been thinking about testing lately and throughout this thinking I did a deep-dive into the current state of testing in dbt. In this post, I will try to motivate the importance of testing, prese…
tags:
  - clippings
  - dbt
topic:
type: note
---
boxysean dbt Labs

Hello!

My team and I have been thinking about testing lately and throughout this thinking I did a deep-dive into the current state of testing in dbt. In this post, I will try to motivate the importance of testing, present research I’ve collected about testing in dbt, make some conclusions from that research, and finally make some suggestions for advancement of testing in dbt.

I tagged a lot of folks on this post, would love to get more input, more research, and opinions here. Thanks!

## Motivation

Presently, dbt offers [two types of tests](https://docs.getdbt.com/docs/building-a-dbt-project/tests/), **schema tests** and **data tests**. For the purpose of this post, I will refer to these types of tests as dbt’s **primitive tests** in the sense they are implemented in the dbt core and can be used in more sophisticated ways. *Schema tests* are good for enforcing constraints that RDBMS systems typically offer but analytical databases don’t. Meanwhile, *data tests* can test anything with endless possibilities.

Zooming out a bit from dbt, I would like to motivate the value of [testing in software](https://en.wikipedia.org/wiki/Software_testing). The points here are applicable to all software projects including dbt projects.

### Why should I test software?

With software tests, an engineer can:

- reduce the likelihood of an unexpected outcome or side-effect from code or system under test,
- reduce the likelihood that a current or future code change will introduce a system error,
- inspire confidence in the test author and others that the code or system under test works as-intended, and
- document code and system behavior by illustrating edge-cases.

There are two parts to testing: writing tests and running tests. Both of these parts are necessary for a useful test suite to provide the above benefits.

### How should I test software?

A good test typically verifies *something:* that a piece of code behaves a certain way under certain conditions, or that a system functions in a certain way.

There are many established ways to test software, each with its own strengths and suitability. I would argue that the *best* way to test highly depends on what is trying to be accomplished, e.g., prevent code regressions, ensure a contract, introduce a new working feature. The level of effort for testing scales depending on the situation.

I would like to highlight two testing categories that I think are relevant to dbt:

- **[Smoke testing:](https://en.wikipedia.org/wiki/Smoke_testing_\(software\))** “Where there’s smoke, there’s fire.” A smoke test confirms that the system under test looks and/or behaves a certain way. Smoke tests are used in blue/green deployment pipelines as a last-step check before cutover; if the smoke test fails, then the deployment pipeline fails. Smoke tests are difficult to run at development-time because it requires the entire production system to be functioning for the developer. Smoke tests are particularly effective in continuous deployment pipelines to help catch issues difficult to detect at development-time. Smoke tests are a sign of a mature system.
- **[Unit testing:](https://www.martinfowler.com/bliki/UnitTest.html)** A unit test proves that a “unit” of code works as expected. A unit test commonly has three steps: setup, execute the code under test, and verification/teardown section. A unit can vary in size, from a single function, to an entire class. Unit tests are self-contained and typically do not test functionality of external systems (e.g., using HTTP calls or database connections). “Mocking” is a common technique used during unit tests and is often essential for unit testing. Unit tests are run at development-time and during continuous integration to detect breakages before code reaches production.

Testing can occur at a variety of points in the software development lifecycle. Unit tests are typically run at development-time (i.e., when the code is being developed) and during continuous integration (i.e., when the code is being merged into the main branch of the project). Smoke tests are typically run during continuous deployment (i.e., when the code/data is being deployed to production).

(For more on testing in software, I recommend to consult [Martin Fowler’s writing](https://www.martinfowler.com/testing/)!)

## Community research

I have conducted research about dbt by reading through blog posts, GitHub issues, and dbt Discourse. I’ve found there are a number of community members who described their attempts at and/or the challenges of building advanced tests to suit their needs:

- Petyo Pahunchev [pointed out](https://www.infinitelambda.com/post/dbt-testing-tools-gap) that primitive tests (schema tests and data tests) leave a gap in dbt development, saying “there is no tool to let us deterministically re-create a set of conditions, execute our code and validate the output.” In his post, he suggested a way to create tests using a Python library to allow for a **behavioural-driven development** methodology in dbt.
- [@michael-kaminsky](https://discourse.getdbt.com/u/michael-kaminsky) [outlined](https://kaminsky.rocks/2020/09/tdd-for-elt/) the challenges of adopting a **test driven development** approach in ELT. He made a number of good points, including “it takes a lot of work to generate realistic test-cases”, and “executing a pipeline and testing it can take upwards of 10 minutes — this is way too slow for doing real test-driven development”.
- MichelleArk [described](https://github.com/fishtown-analytics/dbt/issues/2354) their team’s attempt of hand-constructing static CSVs, building macros, and running primitive tests to assert model behavior generally and in edge cases. Ultimately, they wrap up the GitHub issue saying “a general issue with this approach is that writing assertions for **unit tests** feels quite unnatural in SQL - it’s tricky even to get the right semantics for an equality check.” Later in the post, I described my approach to **black box testing** pl/pgsql transformations using Python.
- [@fabrice.etanchaud](https://discourse.getdbt.com/u/fabrice.etanchaud) [noted](https://github.com/fishtown-analytics/dbt/issues/2740) that with the new --defer flag, there may be a way to automate **non-regression tests** ([see diagram](https://stackoverflow.com/a/60448514)). Later in the post, @jtcohen [described](https://github.com/fishtown-analytics/dbt/issues/2740#issuecomment-717670524) how to **mock** a dbt model using macros and run-time variables.

Despite these challenges, there are successful examples of building advanced tests using dbt’s primitive tests or by building scaffolding around dbt:

- [@claire](https://discourse.getdbt.com/u/claire) ’s [described](https://discourse.getdbt.com/t/testing-with-fixed-data-set/564/2) how to test with dbt using a fixed dataset. Her fixed dataset consists of “fake data consisting of all my known edge cases so that I can check that my SQL works.” She noted she only does this testing during development, and it’s not clear if engineers returning to her code are able to run these tests.
- [@claus](https://discourse.getdbt.com/u/claus) [presented](https://www.youtube.com/watch?v=jGwUonA3mDg&feature=youtu.be) how to run primitive dbt tests as a **smoke test** during a blue/green data deployment. If the smoke tests pass, then the dbt output is made available for use; otherwise the data deployment fails.
- [@gnilrets](https://discourse.getdbt.com/u/gnilrets) [built](https://discourse.getdbt.com/t/testing-data-transformations/733) a well-documented testing framework outside of dbt. A developer using the framework may write **testing specifications** for a data transformation, and the framework verifies the spec.
- The [dbt-utils](https://github.com/fishtown-analytics/dbt-utils) project has a series of **integration tests** that verify project functionality across the supported database. Meanwhile [dbt-audit-helper](https://github.com/fishtown-analytics/dbt-audit-helper) has macros that can supercharge dbt data tests.

## Conclusions

Based on this research, I conclude the following:

1. Strategies for smoke testing in dbt have been discovered and documented by the community.
2. Meanwhile, there is a high barrier-to-entry to advanced development-time dbt testing strategies. To achieve advanced dbt testing, one either needs expert-level knowledge of dbt, or a high investment of individual time.
3. There’s a general desire for advancing development-time testing capabilities inside or outside of dbt and community members are looking for capabilities known in the field of software testing.

## Suggestions

Here are some concrete suggestions that I think will advance testing in dbt:

- Product: Map out the current development-time testing workflow and map out an improved development-time testing workflow.
- Technical: Make “mocking” a dbt model and dbt source a well-designed and first-class construct in dbt. I think many of the community members I referenced above could benefit from a well-defined approach to mocking in dbt.
- Documentation: Motivate testing in the dbt docs and present the trade-offs of testing. Promote testing best-practices and advanced testing strategies in the dbt docs. (What does a well-tested model look like? When should tests be run? See [React Testing](https://reactjs.org/docs/testing.html) for an example.)

Looking forward to continuing the discussion!