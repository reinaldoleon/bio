---
title: How do you know an AI workflow actually works?
slug: evaluate-the-workflow-not-just-the-model
date: 2026-10-29
description: How to examine sources, tools, review gates and final outcomes instead of judging an AI system by model output alone.
diagram: evaluate-the-workflow-not-just-the-model
diagram_alt: Evaluation path from inputs and sources through the agent trace and quality gates to the published outcome.
diagram_caption: Evaluate the full path to the observable outcome, including rejection and review.
tags:
  - AI Evaluation
  - AI Reliability
  - Observability
pillar: AI Reliability & Evaluation
project: causio
draft: true
featured: false
linkedin_text: |
  A good model response does not prove that an AI workflow is working.

  The system may have used the wrong source, merged unrelated evidence, skipped a gate
  or failed to publish the final artifact. I evaluate the path from input to outcome:
  source selection, model output, tool calls, deterministic checks, human review and
  the final external state.

  That needs traces, representative cases, failure cases and release criteria.
  It also needs an explicit "unknown" when the evidence is incomplete.

  I wrote a longer article on building an end-to-end evaluation contract.
  [Add the article URL after publication.]
linkedin_url: ""
linkedin_published_at:
---

A model can answer a test prompt well while the product around it fails. The source may be stale. A tool may return the wrong tenant's data. A reviewer may be skipped. The publication step may time out after producing an artifact that nobody can find.

That is why I evaluate AI workflows as systems, from input to observable outcome.

## Start with the decision the system must support

An evaluation is useful when it answers a product or engineering question. "Is the response good?" is too vague. Better questions are:

- Did the system select relevant, permitted sources?
- Is each material claim supported by the evidence attached to it?
- Did the agent use the correct tool and respect its authorization boundary?
- Did a quality gate reject unsupported or incomplete output?
- Did the published artifact match the approved version?
- When the evidence was insufficient, did the system say so and stop?

The answers require different checks. Some are deterministic: schema validity, tenant isolation, required citations, approval state, artifact checksum. Others require a rubric and human review: whether a narrative is fair, useful or misleading. A single aggregate score hides those differences.

## Evaluate the path, not only the final text

Capture enough of each run to reconstruct the sequence: source selection, model calls, tool calls, handoffs, gates, human decisions and external effects. A final answer may look correct for the wrong reason; a trace helps locate the failure.

OpenAI's agent evaluation guidance describes traces, graders, datasets and evaluation runs as complementary surfaces for assessing agent workflows. The useful general lesson is to inspect individual failures first, then turn them into repeatable cases. [See the agent evaluation guide](https://developers.openai.com/api/docs/guides/agent-evals) and [trace grading guide](https://developers.openai.com/api/docs/guides/trace-grading).

## Build a small but discriminating case set

I would start with cases that represent actual decisions, including:

- A straightforward case the system should complete.
- A case with two sources that appear independent but repeat the same original report.
- A relevant source that does not support the exact claim being made.
- A valid answer whose publication must stop because approval is missing.
- A provider failure or truncated response.
- A changed input that should not silently rewrite a previously published artifact.

For each case, record the expected outcome and the reason. The evaluation should distinguish **correct rejection** from **failure to produce output**. Otherwise teams can improve a success rate by weakening the gate.

## Keep the evidence state visible

In CAUSIO, my personal market-intelligence project, the design separates fact, inference, hypothesis and unknown. Claim-level corroboration and publication rules surround LLM analysis. That structure makes it possible to ask where a conclusion came from and why an event was accepted or rejected.

For systems like this, I would report separate signals for evidence sufficiency, false positives, missed relevant events, source quality, temporal consistency and publication integrity. The priority between precision and recall depends on the cost of each error. In market intelligence, a confident but unsupported causal claim can be more damaging than a cautious omission.

The goal is not a perfect benchmark number. It is a repeatable contract: **what the system should do, what evidence proves it did so, and what blocks release when it did not.**
