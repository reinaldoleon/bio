---
title: Can AI help evaluate technical candidates without deciding for us?
slug: ai-assisted-technical-interviews-without-outsourcing-judgment
date: 2026-10-29
description: What an AI-assisted technical exercise review can reveal, where bias can enter and why the hiring decision must remain human.
illustration_en: ai-assisted-technical-interviews-en.jpg
illustration_es: ai-assisted-technical-interviews-es.svg
illustration_alt: A conceptual comparison between an AI score that drives a hiring decision and an evidence-led review that informs a human interview.
illustration_caption: "A conceptual illustration of the boundary: AI can organize evidence and suggest questions; people retain the hiring decision."
tags:
  - AI Governance
  - Human-in-the-Loop
  - AI Evaluation
pillar: AI Governance
draft: false
featured: false
linkedin_text: ""
linkedin_url: ""
linkedin_published_at:
---

Recently, during a hiring process for Platform Engineers, we built an AI-assisted technical exercise review. The aim was straightforward: reduce manual preparation without making AI the hiring decision-maker.

The exercise had two parts: a technical solution design and architecture decision records (ADRs) explaining the choices behind it. Agents and reusable skills reviewed the submission against several criteria and prepared questions for the interview.

## From a submission to useful signals

The review could highlight decisions with thin justification, trade-offs left unexplored, and risks around reliability, security, cost or operability. It could also point out inconsistencies between the proposed architecture and its ADRs.

The intended flow was:

**Submission → evidence → observations → areas to explore → interview questions.**

The output was a starting point for a technical conversation. It was not a verdict on whether a candidate was “good” or “bad.”

## A score is an inference, not a decision

This work sharpened a concern I have about LLM bias. A model does not assess a design from a neutral position. Its learned patterns can favor familiar technologies, conventional architecture and particular ways of explaining a choice. Removing explicit personal attributes does not eliminate the possibility of indirect bias.

A candidate may reason well in a style the model does not expect. An unusual architecture may still be valid. A justified trade-off may differ from the solution most frequently represented in training data.

So the important question is not only whether an LLM *can* score an exercise. It is **what authority we give that score**. A percentage can compress uncertainty and disagreement into a number that appears more objective than it is.

## Three boundaries for AI-assisted evaluation

1. **Rubric before model.** Define what the exercise is meant to assess before asking a model to review it. Criteria should be visible and open to challenge.
2. **Evidence before score.** An observation should point to a specific part of the submission and explain why it matters. Unsupported ratings are poor interview material.
3. **Questions before conclusions.** A model's inference should lead to a question the interviewer can test with the candidate, including the chance to hear the rationale behind an unconventional choice.

These boundaries do not make bias disappear. They keep uncertain model judgments inspectable and prevent them from silently becoming decisions.

## Keep the authority with the interviewer

The useful outcome was less time spent preparing interviews and more time for deeper technical conversations. AI helped turn a complex submission into evidence and targeted questions. The interviewer still had to listen, challenge the analysis, understand context and make the final decision.

Bias becomes especially dangerous when an inference is automatically promoted into action. In hiring, the system should help people exercise better judgment, not outsource judgment to a model.
