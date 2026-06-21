# Introduction

Intense climate-related disasters have been on the rise worldwide, causing widespread devastation, loss of life and livelihoods as well as property damage and critical infrastructure failures. Now more than ever, we need to help the most vulnerable people cope with the effects of our rapidly changing climate. But building resilience is hard: disaster risk reduction involves many actors making complex decisions across different stages of crisis management. Information is often fragmented and siloed — scattered across agencies, in different systems and formats — making it difficult to make joined-up, data-informed decisions that accurately prioritize the most urgent needs.

This is why the [Open Contracting Partnership (OCP)](https://www.open-contracting.org) and [CivicDataLab (CDL)](https://civicdatalab.in/) worked together on a transformational approach to break down silos, power up data-driven decision-making and implement innovative reforms that better serve those at greatest risk. The Intelligent Data Solution for Disaster Risk Reduction (IDS-DRR) joins up government spending data with complex datasets spanning hazard, exposure, vulnerability, and coping capacity. It is an integrated digital platform for collecting, analyzing, and disseminating disaster-related data to improve coordination and decision-making so that government spending can be targeted toward those who need it the most.

This will help governments and communities better:

- **Prepare** through more robust planning and management activities that can help minimize the worst effects of disasters on vulnerable communities
- **Repair and restore** essential infrastructure and infrastructure services in the aftermath of a disaster event

The risk-scoring methodology is hazard-agnostic: the same SENDAI-aligned framework supports floods, cyclones, droughts, earthquakes, and other natural hazards, with different input indicators per hazard.

## Platform

IDS-DRR turns the risk-scoring outputs into an analytical interface for disaster management authorities. On an interactive map, decision-makers can switch between the composite risk score and individual factor scores (hazard, exposure, vulnerability, coping capacity) to see not just *which* regions are most at risk but *why*; scrub through monthly time periods to track how conditions evolve; and drill from district to sub-district to focus on specific communities. Cross-referenced against historical government spending, the platform surfaces gaps or mismatches between need and investment — flagging where the most urgent interventions are required and where past response has fallen short.

## Reference deployment

```{admonition} Assam flood pilot
:class: note

The [first IDS-DRR deployment](https://drr.open-contracting.in) was a 4-year pilot in the state of Assam, India, focused on **floods**. Floods are the most frequent of natural disasters, and Assam is among the most flood-affected states in India. Of the 1.47 billion people worldwide directly exposed to the risk of intense flooding, over a third are poor and 132 million live in extreme poverty. In India, natural disasters claimed more than 2,000 lives in 2022 alone, with over 2.2 million people affected. In the last decade, [87% of deaths by natural disasters in India were due to floods](https://ourworldindata.org/explorers/natural-disasters?time=2010..latest&facet=none&Disaster+Type=All+disasters+%28by+type%29&Impact=Deaths&Timespan=Annual&Per+capita=false&country=~IND).

The Assam pilot has since been replicated with state disaster management authorities in Odisha, Uttar Pradesh, Bihar, and Himachal Pradesh. Most of the worked examples and reference data sources in this documentation reflect that flood-pilot context.
```

## Sustainable Development Goals

IDS-DRR directly supports:

- **SDG 13 — Climate Action**, in particular target 13.1 (strengthen resilience and adaptive capacity to climate-related hazards) and indicator 13.1.1 (number of people affected by disasters).
- **SDG 11 — Sustainable Cities and Communities**, in particular target 11.5 (reduce deaths and economic losses caused by disasters) and target 11.b (integrated policies for resilience to disasters).

By producing transparent, reproducible risk scores at granular administrative levels, the platform enables agencies to plan mitigation, target relief, and audit historical response patterns against measured exposure and vulnerability.

## Partners

IDS-DRR is led by [CivicDataLab](https://civicdatalab.in/) and the [Open Contracting Partnership](https://www.open-contracting.org/), with support from The Rockefeller Foundation and the Patrick J. McGovern Foundation. Risk-score methodology and indicator validation were developed in collaboration with the Assam and Himachal Pradesh State Disaster Management Authorities.

## About this documentation

This documentation covers the platform's risk-scoring methodology, end-to-end architecture, and per-component technical guides — for teams using or adopting IDS-DRR.

- **[Data lifecycle](architecture/overview.md)**: End-to-end flow from sourcing to publishing.
- **[Risk model](datasources/data-model.md)**: Risk-scoring methodology.
- **[Data sources](datasources/data-ingestion.md)**: Illustrative data sources (from the Assam reference deployment).
- **[Platform overview](platform/index.md)**: Component documentation, quick-start, and deployment guide.
