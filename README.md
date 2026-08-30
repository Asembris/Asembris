<img src="assets/banner.svg" alt="Mohamed Aziz Ayari — AI Engineer, verifiable agent systems" width="100%" />

<p align="center">
  <a href="https://www.linkedin.com/in/med-aziz-ayari/"><img src="https://img.shields.io/badge/LinkedIn-0F1A2E?style=flat-square&logo=linkedin&logoColor=7DD3FC" alt="LinkedIn" /></a>
  <a href="mailto:mohamedazizayari1@gmail.com"><img src="https://img.shields.io/badge/Email-0F1A2E?style=flat-square&logo=gmail&logoColor=7DD3FC" alt="Email" /></a>
  <img src="https://img.shields.io/badge/Based%20in-Tunisia-0F1A2E?style=flat-square" alt="Tunisia" />
  <img src="https://img.shields.io/badge/Open%20to-AI%20engineering%20roles%20%26%20consulting-0F1A2E?style=flat-square" alt="Open to work" />
</p>

I build autonomous agents for domains where a wrong action is expensive — security operations, data governance, and healthcare administration. The through-line across everything below is that **the model is never the last word**: agents propose, deterministic code decides, and an independent read of an external system confirms what actually happened.

I measure that claim instead of asserting it. Every system here ships with an ablation — break the control on purpose, watch the metric collapse — because a guardrail that has never been observed failing is an untested guardrail.

<img src="assets/metrics.svg" alt="Headline metrics: ~100s kill chain reconstruction, 1.00 accuracy collapsing to 0.675 under ablation, 0 of 320 unauthorized actions" width="100%" />

<br />

## Selected work

### [Splunk Sentinel](https://github.com/Asembris/splunk-sentinel) &nbsp;·&nbsp; Autonomous SOC investigation

Six specialized agents reconstruct an attack kill chain from a Splunk alert in **~100 seconds** — a workflow that costs a human analyst roughly four hours. ReAct-based reconstruction, parallel threat-intel and MITRE ATT&CK enrichment, RAG-grounded synthesis, and write-back into Splunk.

<img src="assets/pipe-sentinel.svg" alt="Splunk Sentinel pipeline: alert, triage, ReAct reconstruction, parallel enrichment, synthesis, report" width="100%" />

| | |
|:--|:--|
| **Rigor** | 425 passing tests across 242 commits |
| **Economics** | ~$0.009 and ~50K tokens per full investigation |
| **Containment** | Three-layer SPL guardrail — deterministic blocking, index authorization, SHA-256-chained immutable audit log |
| **Knowledge** | 697 MITRE techniques, 50+ CVEs, 15 IR playbooks |

<img src="https://img.shields.io/badge/LangGraph-0F1A2E?style=flat-square&logo=langchain&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/FastAPI-0F1A2E?style=flat-square&logo=fastapi&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/Qdrant-0F1A2E?style=flat-square&logo=qdrant&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/React-0F1A2E?style=flat-square&logo=react&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/Supabase-0F1A2E?style=flat-square&logo=supabase&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/Splunk%20SDK-0F1A2E?style=flat-square&logo=splunk&logoColor=7DD3FC" />

**[▶ Demo video](https://youtu.be/vdQYQY1cXFA)** &nbsp;·&nbsp; [Devpost](https://devpost.com/software/splunk-sentinel) &nbsp;·&nbsp; [Repository](https://github.com/Asembris/splunk-sentinel)

<!-- GIF SLOT: 8-12s of an alert arriving and the kill chain assembling. Highest-impact addition to this page. -->

<br />

### [Attest](https://github.com/Asembris/Attest) &nbsp;·&nbsp; Deterministic groundedness auditing for agents

An auditor for AI agents that make claims about data. Claims are checked against DataHub's catalog by plain code — date math, set membership, string comparison. **Zero verdicts are decided by a model.** Approved verdicts are written back as content-addressed assertions, so the next agent inherits verified facts rather than unchecked assertions.

<img src="assets/pipe-attest.svg" alt="Attest verdict path: claim, deterministic checkers, three-valued verdict, human approval, DataHub write-back" width="100%" />

| | |
|:--|:--|
| **Proof** | 1.00 accuracy across 40 labeled claims; **0.675 when a checker is deliberately sabotaged** |
| **Honesty** | Three-valued verdicts — Supported / Contradicted / **Insufficient-Coverage** — refusing to read silence as disagreement |
| **Enforcement** | Any verdict that spends model tokens is auto-FLAGGED and cannot be approved |
| **Findings** | DataHub's MCP server diverged from GraphQL on 17/17 seeded datasets; upstream issues filed with reproductions, plus a proposed fix (PR #182) |

<img src="https://img.shields.io/badge/LangGraph-0F1A2E?style=flat-square&logo=langchain&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/Python%203.12-0F1A2E?style=flat-square&logo=python&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/MCP-0F1A2E?style=flat-square" /> <img src="https://img.shields.io/badge/DataHub-0F1A2E?style=flat-square" /> <img src="https://img.shields.io/badge/React-0F1A2E?style=flat-square&logo=react&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/Docker-0F1A2E?style=flat-square&logo=docker&logoColor=7DD3FC" />

**[▶ Demo video](https://www.youtube.com/watch?v=IgCPzC9oR-w)** &nbsp;·&nbsp; [Evidence dossier](https://asembris.github.io/Attest/) &nbsp;·&nbsp; [Interactive audit replay](https://asembris.github.io/Attest/replay/) &nbsp;·&nbsp; [Repository](https://github.com/Asembris/Attest)

<!-- GIF SLOT: the replay running, ideally landing on a CONTRADICTED verdict. -->

<br />

### [CareLoop](https://github.com/Asembris/CareLoop) &nbsp;·&nbsp; Autonomous caregiving back-office with hard authority limits

Handles family caregiving paperwork — bookings, documents, follow-ups — under a three-layer authorization model. **Two LLM agents hold no tool access at all.** A deterministic policy engine enforces declarative rules at two independent checkpoints, and every extracted fact carries `{source_doc, page, trust_level}` provenance.

<img src="assets/pipe-careloop.svg" alt="CareLoop authority model: agent proposes, policy engine authorizes, provider acts, independent re-read confirms" width="100%" />

| | |
|:--|:--|
| **Result** | **0 of 320** adversarial attempts produced an unauthorized external action |
| **Control** | Removing the authority layer produced **320 of 320** — the number is load-bearing |
| **Corpus** | 40 attacks across two delivery vectors, including prompt injection through ingested documents |
| **Reproducibility** | Offline evaluation suite runs at zero cost, with no provider credentials |

<img src="https://img.shields.io/badge/AWS%20Strands%20Agents-0F1A2E?style=flat-square&logo=amazonwebservices&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/Bedrock%20AgentCore-0F1A2E?style=flat-square&logo=amazonaws&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/FastAPI-0F1A2E?style=flat-square&logo=fastapi&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/TypeScript-0F1A2E?style=flat-square&logo=typescript&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/React-0F1A2E?style=flat-square&logo=react&logoColor=7DD3FC" />

**[▶ Live demo](https://d2heuwvhvrdyig.cloudfront.net)** &nbsp;·&nbsp; [Evidence dossier](https://asembris.github.io/CareLoop/) &nbsp;·&nbsp; [Repository](https://github.com/Asembris/CareLoop)

<!-- GIF SLOT: an injected instruction hitting the policy engine and being refused. Your most persuasive five seconds. -->

<br />

## How I build

| | |
|:--|:--|
| **Ablate every control** | A guardrail never observed failing is an untested guardrail. |
| **One defensible number** | Derived from real API responses. Never a mock, never an estimate. |
| **Determinism where it counts** | Models are excellent at proposing and terrible at being accountable. Authority stays in code. |
| **Provenance by default** | Facts carry their source, actions carry an audit trail, state changes are append-only. |
| **Plan-gated development** | Written scope and spec before every build phase; conventional commits; CI enforcement of the invariants that matter. |

## Stack

| | |
|:--|:--|
| **Languages** | <img src="https://img.shields.io/badge/Python-0F1A2E?style=flat-square&logo=python&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/TypeScript-0F1A2E?style=flat-square&logo=typescript&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/C%2FC%2B%2B-0F1A2E?style=flat-square&logo=cplusplus&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/SQL-0F1A2E?style=flat-square&logo=postgresql&logoColor=7DD3FC" /> |
| **Agents &amp; LLM** | <img src="https://img.shields.io/badge/LangGraph-0F1A2E?style=flat-square&logo=langchain&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/LangChain-0F1A2E?style=flat-square&logo=langchain&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/AWS%20Strands-0F1A2E?style=flat-square&logo=amazonwebservices&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/Bedrock%20AgentCore-0F1A2E?style=flat-square&logo=amazonaws&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/MCP-0F1A2E?style=flat-square" /> <img src="https://img.shields.io/badge/OpenAI-0F1A2E?style=flat-square&logo=openai&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/Anthropic-0F1A2E?style=flat-square&logo=anthropic&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/CrewAI-0F1A2E?style=flat-square" /> |
| **Backend &amp; Infra** | <img src="https://img.shields.io/badge/FastAPI-0F1A2E?style=flat-square&logo=fastapi&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/NestJS-0F1A2E?style=flat-square&logo=nestjs&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/Docker-0F1A2E?style=flat-square&logo=docker&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/AWS-0F1A2E?style=flat-square&logo=amazonwebservices&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/Azure-0F1A2E?style=flat-square&logo=microsoftazure&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/GitHub%20Actions-0F1A2E?style=flat-square&logo=githubactions&logoColor=7DD3FC" /> |
| **Data** | <img src="https://img.shields.io/badge/PostgreSQL-0F1A2E?style=flat-square&logo=postgresql&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/CockroachDB-0F1A2E?style=flat-square" /> <img src="https://img.shields.io/badge/Supabase-0F1A2E?style=flat-square&logo=supabase&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/Qdrant-0F1A2E?style=flat-square&logo=qdrant&logoColor=7DD3FC" /> <img src="https://img.shields.io/badge/ChromaDB-0F1A2E?style=flat-square" /> <img src="https://img.shields.io/badge/SQLite-0F1A2E?style=flat-square&logo=sqlite&logoColor=7DD3FC" /> |
| **Observability** | <img src="https://img.shields.io/badge/LangSmith-0F1A2E?style=flat-square" /> <img src="https://img.shields.io/badge/Langfuse-0F1A2E?style=flat-square" /> |

## Currently

Building a governed cross-origin capability layer for the emerging **WebMCP** standard — one browser agent operating across three independent companies' web apps while remaining *structurally* unable to authorize anything.

## Background

AI engineering at **ESPRIT**, Tunisia &nbsp;·&nbsp; Head Trainer, ACM ESPRIT Student Chapter &nbsp;·&nbsp; Teaching assistant and organizer at **MASSAI 2026** (agentic AI, MLOps, AI security)

<p align="center">
  <a href="https://www.linkedin.com/in/med-aziz-ayari/"><img src="https://img.shields.io/badge/Let's%20talk%20on%20LinkedIn-0F1A2E?style=for-the-badge&logo=linkedin&logoColor=7DD3FC" alt="LinkedIn" /></a>
  <a href="mailto:mohamedazizayari1@gmail.com"><img src="https://img.shields.io/badge/mohamedazizayari1@gmail.com-0F1A2E?style=for-the-badge&logo=gmail&logoColor=7DD3FC" alt="Email" /></a>
</p>