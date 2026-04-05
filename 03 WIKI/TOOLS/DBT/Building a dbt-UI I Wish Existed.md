---
title: Building a dbt-UI I Wish Existed
source: https://medium.com/@remisharoon/building-a-dbt-ui-i-wish-existed-6eb44e0b3834
author:
  - "[[Remis Haroon]]"
published: 2025-12-15
created: 2026-04-04
description: Building a dbt-UI I Wish Existed 🔗dbt-Workbench🔗 A few months ago, I found myself doing the same thing over and over again. Open dbt Cloud.  Click through models.  Check lineage.  Open docs.  …
tags:
  - clippings
  - dbt
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*X553Lz060RvnYJfyUEyq-Q.png)

[**https://github.com/rezer-bleede/dbt-Workbench**](https://github.com/rezer-bleede/dbt-Workbench)

> 🔗 [dbt-Workbench](https://github.com/rezer-bleede/dbt-Workbench) 🔗

A few months ago, I found myself doing the same thing over and over again.

> Open dbt Cloud.  
> Click through models.  
> Check lineage.  
> Open docs.  
> Switch projects.  
> Repeat.

None of this was *bad*. dbt Cloud does its job well. But the more I worked across different environments — local setups, on-prem systems, restricted networks — the more friction I felt. Not enough to complain loudly, but enough that it stayed in the back of my mind.

Why does this workflow feel heavier than it needs to be?

## The gap I kept running into

Most dbt workflows eventually revolve around the same questions:

- What models exist here?
- How does this model depend on others?
- What changed recently?
- Can I quickly inspect the SQL behind this?
- What happened in the last run?

You don’t need a lot of bells and whistles to answer those questions. You need visibility, clarity, and speed.

But when you’re not fully cloud-native — or when you care about running things locally, on-prem, or inside constrained environments — options thin out quickly. You either stitch together scripts, or you accept that some things will always live behind a hosted service.

That’s fine for many teams. It just wasn’t fine for *all* of my use cases.

## So I started experimenting

At first, it was just curiosity.

What if dbt artifacts themselves — `manifest.json`, `run_results.json`, `catalog.json` —were enough to power a clean UI?  
What if you didn’t need a remote service to explore your project?  
What if switching between dbt projects felt as lightweight as switching folders?

I started hacking together a small UI that simply *read what dbt already produces*. No magic. No extra metadata. Just visibility.

That experiment slowly grew into something more intentional.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*H2KmRV45BExoYzPuXSS7-A.png)

## Enter dbt-Workbench

I ended up building **dbt-Workbench**: a self-hosted, open-source UI for dbt projects.

Not as a replacement for dbt Cloud, but as an alternative for situations where you want:

- ***Local or on-prem setups***
- ***No vendor lock-in***
- Multiple dbt projects in one place
- Direct access to compiled SQL and artifacts
- A UI that stays close to how dbt actually works

The idea was simple:  
*Let dbt be dbt. Just make it easier to see what’s going on.*

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*ol16VBTpMUsaC_weqCBdvg.png)

## What it focuses on (and what it doesn’t)

dbt-Workbench isn’t trying to reinvent dbt. It leans on what dbt already does well.

It gives you:

- Model browsing and documentation
- Lineage visualization
- A SQL workspace that shows **compiled SQL side by side with model code**
- Run history and logs
- Multi-project support with proper isolation
- A plugin-friendly architecture for extensions

What it doesn’t try to do:

- Abstract dbt away
- Hide how dbt works
- Replace your existing workflows overnight

You can run it locally with Docker, point it at your dbt artifacts, and see value almost immediately.

## Why open source mattered here

This kind of tool only makes sense if it’s transparent.

Teams have different constraints:

- **Air-gapped environments**
- Strict security policies
- Custom dbt setups
- Unusual warehouse configurations

Open source makes it possible to adapt the UI to those realities instead of forcing everything into one mold.

It also keeps the project honest. If something feels wrong or unnecessary, it shows up quickly when other engineers look at it.

## Still early, intentionally

dbt-Workbench is very much a work in progress. Some parts are solid, others are actively evolving. That’s intentional.

I’d rather build it in the open, shaped by real feedback, than polish something in isolation and hope it fits.

If you’re curious, the project lives here:  
[**https://github.com/rezer-bleede/dbt-Workbench**](https://github.com/rezer-bleede/dbt-Workbench)

No signup. No sales pitch. Just code.

## Final thought

Most of us don’t need *more* tools.  
We need tools that quietly reduce friction.

dbt-Workbench is my attempt at one of those. If it resonates, great. If it sparks ideas or critiques, even better.

That’s usually how the best tools start anyway.

[![Remis Haroon](https://miro.medium.com/v2/resize:fill:96:96/1*4CeS6xo3XBqa5J65I7mNkw.jpeg)](https://medium.com/@remisharoon?source=post_page---post_author_info--6eb44e0b3834---------------------------------------)

[![Remis Haroon](https://miro.medium.com/v2/resize:fill:128:128/1*4CeS6xo3XBqa5J65I7mNkw.jpeg)](https://medium.com/@remisharoon?source=post_page---post_author_info--6eb44e0b3834---------------------------------------)

[368 following](https://medium.com/@remisharoon/following?source=post_page---post_author_info--6eb44e0b3834---------------------------------------)

[https://www.linkedin.com/in/remisharoon/](https://www.linkedin.com/in/remisharoon/)

## Responses (3)

S Parodi

What are your thoughts?  

```c
Impressive work! You nailed the real-world dbt challenges with a really solid design. Wishing this project huge success!
```

52

```c
Wow, just checked out the GitHub repo and it looks seriously impressive 🙌🙂 The project Readme alone is absolute gold. Will give this a go when I get back to work next week ⚙️
```

50

```c
This is awesome! Great work.. would you consider bundling this with your orchestrator?
```