# Development

This page collects design notes for developers maintaining or extending the platform, including how settings is organized, and how to decide where a new setting belongs.

## Settings philosophy

Each component (backend and frontend) reads two kinds of settings:

- **Configuration** describes **what this deployment is**: its name, its states, which GeoJSON files to load, which CSV schemas to expect, which indicator slugs to whitelist, whether the PDF report is enabled, which partners and resources to display.
- **Environment variables** describe **where this deployment is running right now**: database credentials, Redis URL, secret key, allowed hosts, hostnames of downstream services, Sentry DSN, analytics IDs.

The configuration takes a different form per component:

- The **backend** loads it from a TOML file (`config.toml`). See [Data Management API](data-management.md#configuration).
- The **frontend** receives it as a `config` object exported by its branding package. See [Frontend](frontend.md#configuration).

The same configuration should be usable unchanged across production, staging, and local development for a given deployment. Only the environment differs between those.

Mixing the two makes it harder to reason about what changed between deployments, and to spin up new environments or promote builds across environments without re-editing files.

### Deciding where a new setting belongs

Ask, in order:

1. **Does the value change between staging and production of the same deployment?** If yes,  
   → Environment variable
2. **Is it a secret or credential?**  
   → Environment variable
3. **Is it tied to the infrastructure the code is running on** (database, hostname, etc.)?  
   → Environment variable
4. **Does it describe the deployment itself** — its data model, its states, its content, its feature flags?  
   → Configuration

For concrete examples, see the existing settings already in place:

- Configuration: [Frontend](frontend.md#configuration), [Data Management API](data-management.md#configuration).
- Environment variables: [Frontend](frontend.md#environment-variables), [Data Management API](data-management.md#environment-variables).
