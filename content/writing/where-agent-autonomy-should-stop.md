---
title: When should an AI agent need human approval?
slug: where-agent-autonomy-should-stop
date: 2026-10-29
description: A practical way to decide which agent actions can proceed, which need approval and how to enforce the boundary.
diagram: where-agent-autonomy-should-stop
diagram_alt: Agent flow from proposal and preparation through authorization to execution and reconciliation.
diagram_caption: Freedom to propose does not imply permission to execute an external action.
tags:
  - Agentic Systems
  - AI Governance
  - Human-in-the-Loop
pillar: Agentic Systems
project: growthmesh
draft: true
featured: true
linkedin_text: |
  An agent can propose a publishing plan. That does not mean it should be able to publish it.

  I set autonomy boundaries by looking at the action, not at how confident the model sounds:
  Can it affect another person or an external system? Is it reversible? Does it spend money?
  Does it cross a tenant or permission boundary?

  For consequential actions, the application should enforce the rule: approved scope,
  authorization, budget, evidence and a persistent human decision when required.
  A prompt can guide the agent. It cannot be the final authorization layer.

  I wrote a longer note on how to turn these boundaries into an operating contract.
  [Add the article URL after publication.]
linkedin_url: ""
linkedin_published_at:
---

The question "How autonomous should this agent be?" is too broad to answer with a single setting. An agent can be free to explore options and still be unable to publish, spend money or change a customer's data. The boundary belongs to each action.

My starting point is to separate three kinds of work:

1. **Observe and propose.** Read permitted context, compare options, draft a plan or explain a finding.
2. **Prepare.** Create a reversible artifact that is visible to a reviewer, such as a draft post or a proposed change.
3. **Commit.** Trigger an external effect: publish content, alter access, deploy, purchase or send a message.

The third class needs the clearest contract. An agent's confidence is not authorization.

## Define the boundary before writing the prompt

For each tool or action, I ask:

- Who is the authorized actor and which tenant or account does the action affect?
- Can the effect be reversed? If so, how and by whom?
- What evidence must exist before execution?
- What is the maximum spend, volume or rate?
- Does a human need to approve this specific action?
- How will we know whether the external system actually accepted it?

These questions become application rules. A model may select an action, but the application checks the rules at the execution boundary. If required information is missing, the action stops in an explicit state rather than falling through to a best guess.

AWS Bedrock's agent documentation describes user confirmation before selected action-group functions and a return-control option that lets the application perform the action itself. Those are useful examples of the same principle: the application retains authority over side effects. The exact controls will differ by platform. [See the Bedrock confirmation documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-userconfirmation.html) and [return-control documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-returncontrol.html).

## Make human approval a system state

"Human in the loop" has little value if approval is only a sentence in a prompt or a visual badge. The approval decision must be persisted and checked by the backend when the action is attempted. A rejection or stop condition must remain effective after a retry, a new session or a different agent.

The record should identify the proposed action, the scope reviewed, the decision, the reviewer and the resulting execution. If the agent changes the proposal after approval, the approval no longer covers it.

## Treat ambiguous outcomes as ambiguous

External actions can time out after the provider has accepted them. Blindly retrying a publish or payment request can duplicate the effect. The workflow needs an idempotency key where supported, a way to reconcile the provider's actual state and an explicit "unknown" outcome until that check finishes.

In my personal project GrowthMesh, the design separates agentic marketing planning and content review from deterministic checks around tenant access, approval, budgets, publication and measurement. That separation matters more than the number of agents in the workflow.

The practical rule is simple: **give the agent freedom to reason within a bounded task; make consequential actions pass through enforceable, observable contracts.** Autonomy then becomes a property that can be reviewed and expanded deliberately, one action at a time.
