---
type: note
topic: data-platform
created: 2026-02-04
tags:
  - data-platform
  - dbt
  - docker
---


- [https://github.com/rezer-bleede/dbt-Workbench](https://github.com/rezer-bleede/dbt-Workbench)
- [https://github.com/sparodi63/dbt-Workbench](https://github.com/sparodi63/dbt-Workbench)

## ANALISI 

You will assist in understanding, updating, maintaining, fixing and adding new features on an open source project that extends dbt.
The project is dbt-workbench
This is the URL of the repository: https://github.com/rezer-bleede/dbt-Workbench
Describe in detail what it does and produce a thorough documentation (complete with diagrams description and function explaination) provide also a detailed maintance tasks breakdown
Write your findings in a ANALYSIS.md file


## DOCKER-COMPOSE CONFIG


Your docker-compose.yml uses a direct external project mount approach:

  Current Configuration:
  environment:
    - DBT_PROJECT_PATH=/app/data/repos/test_local_4

  volumes:
    - /Users/S.Parodi/Development/DP/dbt-projects/test_local_4:/app/data/repos/test_local_4

  This maps your external dbt project into the container at a workspace-specific path, making it the active
  execution target.

  The Complete Architecture

  The plan document covers:

  1. Three critical environment variables and what each controls
  2. Five volume mounts in your configuration and their purposes
  3. Workspace isolation model - how multiple projects are managed
  4. Three configuration options for different use cases:
    - Option 1: External project direct mount (your current setup)
    - Option 2: Use the built-in demo project
    - Option 3: Let the app manage repositories via Git UI (most flexible)
  5. Current setup analysis - you're using a hardcoded external project mount

  The plan is ready for your review. No code changes are needed since this is purely explanatory.

---


 Analysis

 After exploring the codebase, I've identified the complete mechanism for how docker-compose handles dbt project  selection in dbt-Workbench.

 Key Configuration Files

 - docker-compose.yml - Container orchestration and volume mounts
 - backend/app/core/config.py - Configuration settings (lines 39, 89-90)
 - backend/app/services/project_service.py - Default workspace initialization
 - backend/app/services/git_service.py - Repository path management

 Docker-Compose dbt Project Selection Mechanism

 1. Environment Variables

 The docker-compose.yml defines three critical environment variables for the backend service:

 environment:
   - DBT_ARTIFACTS_PATH=/app/data/artifacts
   - DBT_PROJECT_PATH=/app/data/repos/test_local_4
   - GIT_REPOS_BASE_PATH=/app/data/repos  # (implied default from config.py)

 What each variable controls:

 - DBT_ARTIFACTS_PATH: Where dbt run outputs (manifest.json, run_results.json, catalog.json) are stored and
 monitored
   - Default: ./data/artifacts
   - Docker: /app/data/artifacts
   - Used by the artifact watcher to detect new dbt runs
 - DBT_PROJECT_PATH: The specific dbt project directory used for dbt command execution
   - Default: ./data/repos/default
   - Docker: /app/data/repos/test_local_4 (currently hardcoded to a specific workspace)
   - This is the working directory where dbt run, dbt test, etc. are executed
 - GIT_REPOS_BASE_PATH: Base directory where all workspace repositories are stored
   - Default: ./data/repos
   - Docker: /app/data/repos
   - Each workspace gets a subdirectory: <base_path>/<workspace_key>

 2. Volume Mounts

 The docker-compose.yml mounts multiple volumes to connect host directories to container paths:

 volumes:
   - ./data/artifacts:/app/data/artifacts
   - ./data/repos:/app/data/repos
   - /Users/S.Parodi/Development/DP/dbt-projects/test_local_4:/app/data/repos/test_local_4
   - ./dbt_project:/app/dbt_project
   - ./data/profiles:/app/data/profiles

 What each mount provides:

 1. ./data/artifacts:/app/data/artifacts
   - Persists dbt artifacts across container restarts
   - Allows the host to inspect generated artifacts
   - Workspace-scoped: artifacts for each workspace stored in subdirectories
 2. ./data/repos:/app/data/repos
   - Base mount for all workspace Git repositories
   - Persists workspace data across restarts
 3. /Users/S.Parodi/Development/DP/dbt-projects/test_local_4:/app/data/repos/test_local_4
   - Direct mount of an external dbt project into a specific workspace path
   - This allows using an existing dbt project from the host filesystem
   - Maps to the workspace key test_local_4
   - Combined with DBT_PROJECT_PATH=/app/data/repos/test_local_4, this makes that external project the active
 execution target
 4. ./dbt_project:/app/dbt_project
   - Mounts the demo/sample dbt project included in the repository
   - Contains example models (raw, staging, marts) that work with DuckDB
   - Used as a fallback or reference project
 5. ./data/profiles:/app/data/profiles
   - Mounts dbt profiles (database connection configurations)
   - Allows sharing profiles.yml between host and container

 3. Workspace Isolation Model

 The application uses a workspace-based multi-tenancy model:

 - Each workspace has a unique key (e.g., default, test_local_4, my_project)
 - Repository path: <GIT_REPOS_BASE_PATH>/<workspace_key>
 - Artifacts path: <DBT_ARTIFACTS_PATH>/<workspace_key>
 - On startup, the backend creates a default workspace with key default_workspace_key (configurable, default:
 "default")

 Workspace initialization (backend/app/services/project_service.py):
 repo_path = Path(settings.git_repos_base_path) / workspace.key
 # Creates: /app/data/repos/default (for default workspace)

 4. Current Configuration Analysis

 In the current docker-compose.yml:

 DBT_PROJECT_PATH=/app/data/repos/test_local_4

 Combined with the volume mount:
 /Users/S.Parodi/Development/DP/dbt-projects/test_local_4:/app/data/repos/test_local_4

 This means:
 - The container is configured to use a workspace with key test_local_4
 - That workspace's repository is an external dbt project from the host at
 /Users/S.Parodi/Development/DP/dbt-projects/test_local_4
 - When you run dbt run from the UI, it executes in that directory
 - Artifacts generated will be copied to the artifacts path for that workspace

 How to Configure Different dbt Projects

 Option 1: Use an External dbt Project (Current Setup)

 1. Set the workspace key and project path:
 environment:
   - DBT_PROJECT_PATH=/app/data/repos/<workspace_key>
 2. Mount your external dbt project:
 volumes:
   - /path/to/your/dbt/project:/app/data/repos/<workspace_key>
 3. Ensure artifacts path matches:
 - DBT_ARTIFACTS_PATH=/app/data/artifacts
 volumes:
   - ./data/artifacts:/app/data/artifacts

 Option 2: Use the Built-in Demo Project

 1. Set project path to the demo project:
 environment:
   - DBT_PROJECT_PATH=/app/dbt_project
 2. Mount the demo project:
 volumes:
   - ./dbt_project:/app/dbt_project

 Option 3: Let the Application Manage Repositories (Recommended for Multi-Workspace)

 1. Only set the base paths:
 environment:
   - GIT_REPOS_BASE_PATH=/app/data/repos
   - DBT_ARTIFACTS_PATH=/app/data/artifacts
 2. Mount only the base directories:
 volumes:
   - ./data/repos:/app/data/repos
   - ./data/artifacts:/app/data/artifacts
   - ./data/profiles:/app/data/profiles
 3. Use the UI to connect Git repositories
   - The application will clone/initialize repositories under data/repos/<workspace_key>
   - Switch between workspaces in the UI to work with different projects
   - Each workspace automatically gets isolated paths

 Summary

 The docker-compose configuration for dbt project selection works through:

 1. Environment variables that point to specific paths inside the container
 2. Volume mounts that map host directories to those container paths
 3. Workspace-based isolation where each workspace gets its own repo and artifacts subdirectory
 4. Flexible configuration supporting external projects, demo projects, or managed repositories

 The current setup uses Option 1 - mounting an external dbt project directly into a specific workspace path,
 making that the active execution target.

 Recommendation

 The current hardcoded approach works but is inflexible. Consider:

 - If single-project use: Keep the current direct mount approach
 - If multi-project use: Switch to Option 3 and use the workspace/git UI features
 - For development/testing: Use Option 2 with the demo project

 No Implementation Required

 This is an explanatory task only - no code changes needed. The plan documents the existing architecture for the
 user's understanding.
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

 Claude has written up a plan and is ready to execute. Would you like to proceed?

   1. Yes, clear context and auto-accept edits (shift+tab)
   2. Yes, auto-accept edits
   3. Yes, manually approve edits
 ❯ 4. Write a PLAN.md                        

 ctrl-g to edit in VS Code · ~/.claude/plans/typed-snacking-hejlsberg.md
