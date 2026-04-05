---
title: "Standardizing Logging in dbt: How We Made Debugging Easier for Everyone"
source: https://medium.com/@reliabledataengineering/standardizing-logging-in-dbt-how-we-made-debugging-easier-for-everyone-f63e459f20d6
author:
  - "[[Reliable Data Engineering]]"
published: 2025-07-11
created: 2026-04-04
description: When something fails in production, you see cryptic lines that tell you nothing about where in your project it came from.
tags:
  - clippings
  - dbt
topic:
type: note
---
[Sitemap](https://medium.com/sitemap/sitemap.xml)

Read for free:### [If you’ve worked with dbt at any scale, you probably know this pain:](https://medium.com/@reliabledataengineering/standardizing-logging-in-dbt-how-we-made-debugging-easier-for-everyone-f63e459f20d6?source=post_page-----f63e459f20d6---------------------------------------)

[medium.com](https://medium.com/@reliabledataengineering/standardizing-logging-in-dbt-how-we-made-debugging-easier-for-everyone-f63e459f20d6?source=post_page-----f63e459f20d6---------------------------------------)

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*QFbGrt2wvPq5tbNyB7I7eQ.png)

If you’ve worked with dbt at any scale, you probably know this pain:

> *Logs are everywhere. But they’re* different *everywhere.*

Some people use `print`, others drop in `log` with different formats. When something fails in production, you see cryptic lines that tell you nothing about *where* in your project it came from.

As our dbt project grew, this got worse. Reviews took longer because people wrote logs in different styles. Debugging meant digging through random log lines with no timestamps or context.

We decided to fix this.

## The Problem 🏹

Our core challenges with logging in dbt:

- No standard format → hard to read in production logs.
- No caller context → you see a message but don’t know which macro wrote it.

We needed:

1. A consistent log format
2. Caller detection (macro, model, pre-hook, post-hook, materialization…)
3. Easy to adopt everywhere

## The Idea 💡

What if we wrote **one standard macro** that everyone used?

1. Easy to call in any model, hook, or macro
2. Automatically figures out which macro or hook wrote it
3. Labels pre-hooks, post-hooks, materializations

This would enforce consistency across the entire project without relying on developers to invent their own patterns.

## Overriding dbt’s log Macro 🤔

By design, we chose to **override the built-in dbt** `**log**` **macro**.

By replacing the built-in `log`, we ensure **every single call in the project** automatically gets our standardized format.

Of course, if you **don’t** want to override dbt’s `log`, you can rename it (for example, `standard_log`). But then you have to set a clear guideline and trust everyone to *remember* to use the new name in all macros.

We chose overriding because it enforces adoption automatically and prevents drift.

## The solution ✨

Here’s our macro:

```c
{% macro log(message, info=True) %}
    {# Macros we want to ignore in the stack #}
    {% set ignore_macros = ['run_hooks', 'log'] %}

    {# Get the call stack from the dbt context #}
    {% set raw_stack = context.get('context_macro_stack').call_stack %}

    {# Filter out known noisy system macros #}
    {% set filtered_stack = [] %}
    {% for item in raw_stack %}
        {% set name = item.split('.')[-1] %}
        {% if not (name.startswith('materialization_') and name not in ignore_macros %}
            {% do filtered_stack.append(name) %}
        {% endif %}
    {% endfor %}

    {# Determine which macro actually called log #}
    {% if filtered_stack | length > 0 %}
        {% set caller_macro = filtered_stack[-1] %}
    {% else %}
        {% set caller_macro = raw_stack[-1].split('.')[-1] %}
    {% endif %}

    {# Check if this macro appears in the configured pre_hooks/post_hooks #}
    {% set hook_info_ns = namespace() %}

    {% if 'macro.dbt.run_hooks' in raw_stack %}
        {% set pre_hooks = context.get('pre_hooks', []) %}
        {% set post_hooks = context.get('post_hooks', []) %}

        {% for hook in pre_hooks %}
            {% if caller_macro in hook['sql'] %}
                {% set hook_info_ns.value = "pre-hook" %}
            {% endif %}
        {% endfor %}

        {% for hook in post_hooks %}
            {% if caller_macro in hook['sql'] %}
                {% set hook_info_ns.value = "post-hook" %}
            {% endif %}
        {% endfor %}
    {% endif %}

    {# Print the final log line #}
    {% if info %}
        {% if model.resource_type == 'model' %}
            
            {% if hook_info_ns.value %}
                {{ print("[" ~ hook_info_ns.value ~ "][" ~ caller_macro  ~ "]:  " ~ message) }}
            {% elif caller_macro.startswith('materialization_') %}
                {{ print("[materialization][" ~ caller_macro.replace('materialization_', '')  ~ "]:  " ~ message) }}
            {% else %}
                {{ print("[" ~ caller_macro  ~ "]:  " ~ message) }}
            {% endif %}
                
        {% elif model.resource_type == 'macro'  %}
            {{ print("[" ~ model.name ~ hook_info_ns.value ~ "]:  " ~ message) }}
        
        {% else %}
        {% endif %}
    {% endif %}
{% endmacro %}
```

## How It Works 💪

- Digs into dbt’s macro call stack to find *who actually called* the log.
- Filters out dbt system noise like `run_hooks` and `log`.
- Detects if it’s running in a **pre-hook** or **post-hook**.
- Labels materializations cleanly.
- Outputs a structured log line like:
```c
10:28:42 [pre-hook][generate_schema_name]: Generating bronze schema
10:28:43 [materialization][snapshot]:  Dropping backup snapshot table if exists
```

## Final Thoughts 💭

This macro is a small but impactful change. It helped us clean up our logs, simplify reviews, and made production debugging way less painful.

If you’re running a growing dbt project, I highly recommend creating something similar. Standardization is one of the best gifts you can give your future self (and your team).

*Thanks for reading! Let me know if you have questions or ideas to improve it.*

[![Reliable Data Engineering](https://miro.medium.com/v2/resize:fill:96:96/1*ewisWhJkTid55OnnFA0EmA.png)](https://medium.com/@reliabledataengineering?source=post_page---post_author_info--f63e459f20d6---------------------------------------)

[![Reliable Data Engineering](https://miro.medium.com/v2/resize:fill:128:128/1*ewisWhJkTid55OnnFA0EmA.png)](https://medium.com/@reliabledataengineering?source=post_page---post_author_info--f63e459f20d6---------------------------------------)

[197 following](https://medium.com/@reliabledataengineering/following?source=post_page---post_author_info--f63e459f20d6---------------------------------------)

[https://reliable-data-engineering.netlify.app/](https://reliable-data-engineering.netlify.app/)

## Responses (2)

S Parodi

What are your thoughts?  

=={% if not (name.startswith('materialization\_') and name not in ignore\_macros %}==

```c
there is a missing parenthesis{% if not (name.startswith('materialization_') and name not in ignore_macros) %}
```

2

```c
i think dbt should standardize it by default! good article
```