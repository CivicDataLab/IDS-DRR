# QA & Automation

This component provides end-to-end browser tests for a deployed instance of the [Frontend](frontend.md).

**Repository**: [IDS-DRR-QA-Automation](https://github.com/CivicDataLab/IDS-DRR-QA-Automation)

## Features

A pytest + Selenium framework with a Page Object Model, self-healing locators, and parallel execution. Tests exercise the public-facing UI (analytics maps, the components/widgets, and the datasets pages), implicitly covering frontend-to-backend communication along the way.

## What's covered

- **Analytics workflows**: map rendering, indicator switching, time-period filtering, drill-down between geography levels.
- **Component behaviour**: shared UI primitives used across pages.
- **Datasets pages** when the DataSpace backend is configured.

The suite supports the `smoke` pytest marker for a fast subset suitable for CI gates.

## Running tests

See the [repository](https://github.com/CivicDataLab/IDS-DRR-QA-Automation) for setup instructions, environment configuration, and the parallel-execution helper scripts.
