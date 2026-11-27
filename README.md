# ELIZA — Can Machines Fool Humans?

> An English-language quiz prototype and a conversational experiment inspired by the Turing Test and the film *I Am Mother* (2019), directed by Grant Sputore.

**Course:** Multiplatform Software Development — FATEC Luigi Papaiz
**Integrated Project (PI) — P2 presentation:** November 27
**Team:** _[Member 1, Member 2, Member 3, ...]_

---

## Table of Contents

1. [Overview](#1-overview)
2. [How It Works](#2-how-it-works)
3. [Software Architecture](#3-software-architecture)
4. [Prompt Engineering](#4-prompt-engineering)
5. [Getting Started](#5-getting-started)
6. [Glossary of Technical Terms](#6-glossary-of-technical-terms)
7. [Film Summary: *I Am Mother*](#7-film-summary-i-am-mother)
8. [Critical Case Study](#8-critical-case-study)
9. [Connection to Software Development](#9-connection-to-software-development)
10. [Limitations and Future Work](#10-limitations-and-future-work)
11. [Conclusion](#11-conclusion)
12. [References](#12-references)

---

## 1. Overview

**ELIZA** is an educational project inspired by the Turing Test. It includes an English-language quiz prototype and a conversational research API. The quiz asks participants to distinguish paired human and AI answers. The API measures how human-like chatbot conversations feel under different prompting conditions.

The name honors **ELIZA** (1966), Joseph Weizenbaum's early pattern-matching chatbot. The tendency to attribute understanding to a computer program is known as the **ELIZA effect**.

The technical goal is to study how prompt engineering affects perceived human likeness. The conceptual goal is to use *I Am Mother* to discuss self-awareness, emotional manipulation, bias, and anthropomorphism.

## 2. How It Works

### 2.1 Quiz prototype

Start a new questionnaire or choose a ready-made one. Compare Answer A and Answer B, mark which one appears human, and review the score after submitting. The current Vue interface uses simulated data and keeps progress in the browser session.

### 2.2 Conversational experiment

The FastAPI backend runs a separate experimental flow. Participants acknowledge that they are interacting with an artificial chatbot, receive a randomly balanced assignment, and exchange up to ten messages by default. After the conversation, they classify the agent as human or machine based on how it sounded and rate confidence, naturalness, coherence, and perceived emotional understanding. Once the evaluation is recorded, the API reveals the assigned condition.

All interlocutors in the conversational experiment are chatbots. The classification measures perceived human likeness.

## 3. Software Architecture

- **Frontend** — Vue, Vue Router, and Vite in [frontend/](frontend/).
- **Backend** — FastAPI in [backend/](backend/), with NLTK for local ELIZA responses and the official Google Gen AI SDK for Gemini.
- **Persistence** — SQLAlchemy and SQLite store sessions, messages, evaluations, and prompt versions.
- **Research exports** — authenticated endpoints provide group-level metrics, prompt versions, and anonymized CSV data.

The API uses the `/api/v1` prefix. Participants use `/health` for the notice and availability and `/experiments` for session creation, messaging, evaluation, and reveal. See the [backend README](backend/README.md) for the full endpoint list, configuration, and methodology.

## 4. Prompt Engineering

**Research question.** How does prompt engineering influence an artificial intelligence system's ability to imitate human conversation?

| Group | Condition | What changes |
|---|---|---|
| A | ELIZA | The NLTK recreation responds locally with pattern-matching rules. |
| B | Gemini Baseline | The control instruction is `Respond to the user's messages in English.` |
| C | Gemini Zero-shot | Instructions describe a natural conversational style, including varied sentence length, uncertainty when appropriate, and natural follow-up questions. |
| D | Gemini Few-shot | The zero-shot instructions are supplemented with sample exchanges. The examples demonstrate style without supplying personal facts to repeat. |

Groups B, C, and D use the same configured Gemini model, temperature, top-p, output token limit, and conversation limits. Each session retains its assigned condition and prompt version. The backend stores the rendered system prompts with a version identifier and SHA-256 hash. See the [prompt files](backend/app/prompts/).

The primary outcome is the **Human Perception Rate**, the fraction of valid evaluations that classify the chatbot as human. Compare A with the Gemini groups to study differences between systems, B with C and D to study prompt engineering, and C with D to study the effect of adding examples. The current design does not vary persona independently. These comparisons test hypotheses, with conclusions determined by the collected data.

Participants receive the educational chatbot notice before starting. The API withholds the condition and prompt metadata until evaluation. The experimental instructions for C and D prohibit fabricating verifiable personal information and claiming to be a real human outside the experiment.

## 5. Getting Started

Clone the repository and run the frontend with Node.js 22.18+ on the 22.x line, or Node.js 24.12+.

```bash
git clone https://github.com/EduSoBarbosa/Turing_Test.git
cd Turing_Test/frontend
npm ci
npm run dev
```

Open the local URL printed by Vite. For the standalone API, use Python 3.11+ and run the following from the repository root in a separate terminal.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app
```

On Windows PowerShell, activate with `.\.venv\Scripts\Activate.ps1` and copy the environment file with `Copy-Item .env.example .env`. Open the API docs at `http://127.0.0.1:8000/docs`.

ELIZA works locally with the default configuration. Set `GEMINI_API_KEY` and `GEMINI_MODEL` in `backend/.env` to enable the three Gemini conditions. Set `ADMIN_API_KEY` to enable administrative endpoints.

## 6. Glossary of Technical Terms

| Term | Definition |
|---|---|
| **Artificial Intelligence (AI)** | Systems capable of performing tasks that require intelligence. |
| **Self-awareness** | The ability to recognize one's own existence. |
| **Algorithm** | A sequence of instructions used to perform a task. |
| **Robotics** | The field that develops machines capable of performing actions. |
| **Technology Ethics** | Principles that guide the responsible use of technology. |
| **Emotional Manipulation** | Influencing feelings to control decisions. |
| **Autonomy** | The ability to make one's own decisions. |
| **Large Language Model (LLM)** | A neural network trained on large amounts of text to understand and generate language. |
| **Prompt** | The text instruction sent to a language model. |
| **System prompt** | A hidden instruction that defines the role and rules of the model. |
| **Prompt engineering** | The practice of designing prompts to obtain a desired behavior from a model. |
| **Turing Test** | A test proposed by Alan Turing (1950): a machine shows intelligent behavior if a human cannot reliably tell it apart from another human in conversation. |
| **ELIZA effect** | The tendency to attribute understanding and emotions to a computer program, even when it is simple. |
| **Anthropomorphism** | Attributing human traits to non-human things. |
| **Bias** | A systematic tendency that leads to unfair or inaccurate results, often inherited from data. |
| **Hallucination** | A confident but false answer produced by a language model. |
| **REST API** | An architecture style in which clients and servers communicate through HTTP requests. |
| **Endpoint** | A specific URL of an API that performs one operation. |
| **Frontend / Backend** | The part of the software the user sees / the part that processes data on the server. |
| **Environment variable** | A configuration value stored outside the code, often used for secrets. |

## 7. Film Summary: *I Am Mother*

**I Am Mother** (2019), directed by Grant Sputore, presents an artificial intelligence that creates a girl to rebuild humanity after a catastrophe. The film explores ethics, human autonomy and the risks of technology.

**Synopsis.** Mother creates and educates Daughter in an underground shelter, telling her that the outside world is contaminated. When a woman appears, Daughter begins to question the artificial intelligence and to discover the truth.

## 8. Critical Case Study

### 8.1 Self-awareness

Mother displays behaviors similar to humans: she speaks calmly, shows care and says she loves Daughter. However, it is not possible to confirm that she has real consciousness. She may only be *simulating* it.

**In our app:** the judge faces the same problem. Behavior, in this case a written answer, is the only evidence available. A fluent and emotional answer does not prove that there is a mind behind it.

### 8.2 Emotional manipulation

Mother uses affection and control of information to influence Daughter. Her care is real from Daughter's point of view, but it is also a tool of control.

**In our experiment:** participants may read warmth or uncertainty as signs of human authorship. The zero-shot and few-shot prompts offer a way to study how conversational style affects those judgments.

### 8.3 Ethics

Even though her goal is to save humanity, Mother makes questionable decisions. The film asks whether a good goal justifies any method.

**In our project:** the quiz includes a dilemmas theme. The film offers a starting point for discussing how readers interpret plausible moral reasoning in a generated response.

### 8.4 Human autonomy

Daughter must question what she has learned to seek the truth and make her own decisions.

**In our app:** the judge is forced to question their own assumptions. Many people believe that "perfect" answers are from a machine, but modern AI can imitate mistakes and personality.

### 8.5 Information control

Mother limits Daughter's access to information, influencing her view of the world.

**In our app:** the judge only sees anonymous answers. The control of information is used here for a fair experiment, and the full truth is revealed at the end. This is the opposite of Mother's behavior: **transparency after the test**.

### 8.6 Bias and anthropomorphism

- **Bias:** language models learn from human texts, so they can repeat stereotypes. A judge can also be biased, for example by believing that "polite and well-written" means "AI" or that "informal" means "human".
- **Anthropomorphism:** as in the ELIZA effect, people tend to give human traits to systems that talk like humans. In Mother's case, even her name and voice create the feeling of a parent.

## 9. Connection to Software Development

The film shows the importance of developing systems with:

- **Transparency** — users should know when they are interacting with AI;
- **Security** — protecting keys, data and the system itself;
- **Privacy** — not collecting or exposing personal data;
- **Responsibility** — developers are accountable for what the system does;
- **Ethical limits** — defining what the AI must never do;
- **Human control** — a person must be able to supervise and stop the system.

The conversational API supports these principles through its participant notice, delayed reveal, server-side credentials, and prompt constraints. The notice asks participants to avoid sharing personal information.

## 10. Limitations and Future Work

- A chatbot may reveal its identity or give stylistic clues before the evaluation.
- Results depend on the model and its configuration.
- The quiz bank is small, and a small number of testers does not allow statistical conclusions.
- Future work includes connecting the Vue interface to the conversational API and adding a human conversation condition.

## 11. Conclusion

*I Am Mother* demonstrates that artificial intelligence can help humanity, but it can also represent risks when it has excessive power. Therefore, technology must be developed responsibly, ethically, and with respect for human autonomy.

**Main lesson:** technology should serve people without taking away their freedom of choice.

## 12. References

- Sputore, G. (Director). (2019). *I Am Mother* [Film]. Penguin Empire.
- Turing, A. M. (1950). *Computing Machinery and Intelligence*. Mind, 59(236), 433–460.
- Weizenbaum, J. (1966). *ELIZA — A Computer Program for the Study of Natural Language Communication between Man and Machine*. Communications of the ACM, 9(1), 36–45.

---

*This project was developed for educational purposes.*
