---
title: AI FinOps without false precision
slug: ai-finops-without-false-precision
date: 2026-10-29
description: Separate usage, estimates, forecasts and billed cost before making AI cost decisions.
description_es: Separar uso, estimaciones, proyecciones y coste facturado antes de tomar decisiones de FinOps de IA.
tags:
  - AI FinOps
  - AI Observability
  - Platform Engineering
pillar: Platform Engineering / SRE / FinOps
project: causio
draft: true
featured: false
linkedin_text: |
  "Cost per AI event: €0.04" looks precise. It may be an estimate from token counts,
  a provider quote, an incomplete trace or an allocated share of a daily bill.
  Those are different kinds of evidence.

  I use four labels in AI FinOps: ACTUAL, ESTIMATED, PROJECTED and UNAVAILABLE.
  Each number needs a scope, time window, model or provider, pricing basis and
  an explanation of what was excluded.

  That makes cost dashboards less impressive, but more useful for engineering
  decisions. I wrote a longer note on how to structure the measurement.
  [Add the article URL after publication.]
linkedin_url: ""
linkedin_published_at:
---

AI teams often know how many tokens a workflow used before they know what the provider will bill. That gap is normal. The problem starts when an estimate is displayed as though it were an invoice.

For AI FinOps, I separate four states:

- **ACTUAL:** cost reconciled against a provider billing source for the stated scope and period.
- **ESTIMATED:** cost calculated from observed usage and a stated price schedule.
- **PROJECTED:** a forecast based on expected future volume or behavior.
- **UNAVAILABLE:** insufficient data to produce a defensible number.

These labels are part of the data model, not a footnote on a dashboard.

## Record the basis of every number

For each cost figure, keep the time window, provider, model, usage unit, pricing version, attribution key and calculation method. Record missing inputs and any excluded charges. If a workflow uses several models or retries, attribute each invocation before aggregating.

The useful denominators are also explicit. "Cost per run" may include rejected runs. "Cost per published event" excludes them from the denominator but should still include the cost of attempts that did not publish if those attempts were necessary to produce the event. Otherwise the metric rewards hidden failure.

When the count is zero or attribution is incomplete, the result is **UNAVAILABLE**, not zero.

## Reconcile different views of the truth

Usage logs and billing data answer different questions. AWS Bedrock invocation logs can include model identifiers and input and output token counts for supported calls when logging is enabled. AWS's cost-management guidance distinguishes per-request token detail from aggregated billed dollars available through billing tools. A per-request estimate should not quietly inherit the authority of the invoice. [See Bedrock invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) and [cost tracking guidance](https://docs.aws.amazon.com/bedrock/latest/userguide/cost-management.html).

That distinction applies across providers. A platform can show operational estimates quickly, then reconcile them against actual charges at the granularity the provider makes available. If some provider or service charges cannot be attributed to a tenant or feature, show the unallocated amount separately.

## Put cost controls near execution

A monthly graph is useful for review. It is too late for a single runaway workflow. Before execution, a platform can check a budget ceiling, expected model route, maximum retries and allowed workload size. During execution, it can record actual usage and stop or degrade according to a documented policy.

Cost controls must be balanced with quality. A cheaper model route that increases unsupported claims, human review or retries may raise the cost of a reliable outcome. I would compare cost and quality together, with the same scope and evaluation set.

In CAUSIO, my personal project, the operating design tracks model usage and separates observed usage from estimated and projected cost. The purpose is to make source analysis and publication decisions explainable without claiming more precision than the evidence supports.

**A trustworthy AI cost dashboard does not always show a number. It shows what kind of number is available, how it was produced and which decision it can support.**
