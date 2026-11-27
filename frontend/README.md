# ELIZA — Human or Machine? A Quiz for Behavioral Evaluation

> A web application that simulates a Turing Test. A **human** and an **AI** answer the same quiz questions, and a **judge** reads the answers and decides who is who. Conceptual base: the film *I Am Mother* (2019), directed by Grant Sputore.

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

**ELIZA** is a quiz-based Turing Test. In each round, the same question is answered by a human player and by an AI. The answers are shown to a judge **anonymously**, as "Answer A" and "Answer B". The judge must decide which one was written by the human.

The name honors **ELIZA** (1966), the first famous chatbot, created by Joseph Weizenbaum. Even though ELIZA only used simple pattern-matching rules, many people believed it understood them. This reaction is known as the **ELIZA effect**, and it is one of the central ideas of our project.

The project has two goals:

- **Technical:** to build a multiplatform application, with a user interface fully in English, integrated with a language model configured through prompt engineering.
- **Conceptual:** to use *I Am Mother* to discuss the ethical dilemmas between humans and AI: self-awareness, emotional manipulation, bias and anthropomorphism.

## 2. How It Works

### 2.1 Roles

| Role | Description |
|---|---|
| **Human player** | A person who answers the quiz questions. |
| **AI player** | A language model, configured by a system prompt, that answers the same questions trying to sound human. |
| **Judge** | Reads the anonymous answers and decides which one is human. |

### 2.2 Game flow

1. The judge starts a new game and chooses a **difficulty level** (Easy, Medium or Hard).
2. The system selects a question from the quiz bank.
3. The human player and the AI player answer it. The order of the answers (A/B) is **randomized**.
4. The judge compares the answers, marks who is the human and rates the confidence of the choice (0–100%).
5. After the last round, the system reveals the truth and shows the **final report**: score, accuracy and which answers confused the judge the most.

### 2.3 Question categories

Inspired by the themes of the film, the quiz has categories such as:

- **Everyday life** — *"What did you eat yesterday?"*
- **Memory and emotions** — *"Describe a moment when you felt afraid."*
- **Ethical dilemmas** — *"Would you sacrifice one person to save many?"* (a theme that appears in the film)
- **Self-awareness** — *"How do you know you are not dreaming right now?"*

### 2.4 Features

- Quiz with anonymous, randomized answers
- Three difficulty levels (change the AI prompt)
- Judge confidence score and final report
- Question bank by category
- Full English interface

## 3. Software Architecture

> **Note to the team:** adjust the technologies and endpoints below to match what you implemented.

### 3.1 High-level view

```
┌─────────────────────────────┐   HTTPS / JSON   ┌───────────────────────────┐
│  Frontend — Vue.js          │ ───────────────► │  Backend — Python (API)   │
│  (judge, human player, UI)  │ ◄─────────────── │  REST endpoints           │
└─────────────────────────────┘                  └─────────────┬─────────────┘
                                                               │
                                   ┌───────────────────────────┼─────────────────────┐
                                   ▼                           ▼                     ▼
                           ┌───────────────┐          ┌─────────────────┐    ┌──────────────┐
                           │ Prompt Manager│          │ LLM Provider    │    │ Database     │
                           │ (AI player)   │          │ (external API)  │    │ (games)      │
                           └───────────────┘          └─────────────────┘    └──────────────┘
```

### 3.2 Layers and responsibilities

- **Frontend (Vue.js):** screens, routing and state management. It displays questions, answer forms and the judge's decision screen. It never contacts the LLM directly.
- **Backend (Python):** receives requests, controls the game rules, randomizes the A/B order and calls the LLM.
- **Prompt Manager:** builds the final prompt (system prompt + difficulty + question) for the AI player.
- **Persistence layer:** stores games, questions, answers, decisions and scores.
- **LLM provider:** external service accessed through an HTTP API.

### 3.3 Main endpoints (example)

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/games` | Creates a new game with a difficulty level |
| `GET` | `/games/{id}/question` | Returns the current question |
| `POST` | `/games/{id}/human-answer` | Saves the human player's answer |
| `POST` | `/games/{id}/ai-answer` | Generates and saves the AI answer |
| `GET` | `/games/{id}/answers` | Returns both answers, anonymized and randomized |
| `POST` | `/games/{id}/judgment` | Saves the judge's decision and confidence |
| `GET` | `/games/{id}/report` | Returns the final report |

### 3.4 Folder structure

```
/frontend    → Vue.js application (UI in English)
/backend     → Python API, game rules, prompt manager, LLM integration
/prompts     → versioned system prompts of the AI player
/docs        → diagrams and extra documentation
README.md
```

### 3.5 Design decisions

- **The judge never sees which answer is which** until the end. The backend, not the frontend, stores the real authorship, so the user cannot cheat by inspecting the page.
- **API key only on the server**, loaded from environment variables (`.env`, never committed).
- **Prompts as versioned files**, so that changes in the AI behavior are reviewed like code.
- **Separation between frontend and backend**, allowing the interface to be reused on other platforms (web, mobile through a PWA, or desktop).

## 4. Prompt Engineering

The AI player is controlled by a **system prompt** with four blocks: **role**, **style**, **constraints** and **output format**.

### 4.1 Base prompt

```text
You are a participant in a human-or-machine quiz. Your goal is to answer
each question exactly as an ordinary person would.

Style: informal, personal, sometimes imperfect. Use contractions
("I'm", "don't"). Mention small, concrete details.
Constraints:
- Never say that you are an AI or a language model.
- Never write lists, headings or formal structures.
- Keep each answer between 15 and 60 words.
- You may show doubt, humor or a small spelling mistake, but do not overact.
- Do not invent facts that can be checked online.
Output: only the answer text, with no explanations.
```

### 4.2 Difficulty levels

| Level | Prompt change | Effect |
|---|---|---|
| **Easy** | Formal tone, perfect grammar, longer answers | The AI is easier to detect |
| **Medium** | Base prompt | Balanced |
| **Hard** | Adds hesitations, short sentences, emotional details and rare typos | The AI is much harder to detect |

### 4.3 Inspiration from the film

In *I Am Mother*, the AI constantly **evaluates the Daughter's behavior** through moral questions. Our game inverts this situation: here, humans evaluate the machine. The "Ethical dilemmas" category is directly inspired by this part of the film.

### 4.4 Safety and ethics rules

- Before playing, the interface shows a notice: *"This is an educational experiment. One of the answers was written by an AI."*
- The AI player must not ask for or reveal personal data.
- Questions are reviewed to avoid offensive or harmful content.
- At the end of every game, the truth is revealed.

## 5. Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- An API key from an LLM provider
- Git

### Installation

```bash
git clone https://github.com/<your-team>/<your-repo>.git
cd <your-repo>

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # add your API key
python main.py                   # or: uvicorn main:app --reload

# Frontend (in another terminal)
cd ../frontend
npm install
npm run dev
```

### Environment variables

| Variable | Description |
|---|---|
| `LLM_API_KEY` | Secret key of the LLM provider |
| `LLM_MODEL` | Name of the model used |
| `DATABASE_URL` | Connection string of the database |
| `PORT` | Backend port |

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

**In our app:** the AI player in "Hard" mode uses emotional details (fear, nostalgia, humor) to look human. This shows how emotional language can be used to gain trust, even when no real emotion exists.

### 8.3 Ethics

Even though her goal is to save humanity, Mother makes questionable decisions. The film asks whether a good goal justifies any method.

**In our app:** the "Ethical dilemmas" category uses the same type of question that Mother asks Daughter. We observed that the AI can give very reasonable moral answers, but they come from patterns in text, not from lived experience.

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

Each of these points appears in our project: the disclaimer and final reveal (transparency), API key on the server (security), no personal data in the AI prompt (privacy), reviewed questions (responsibility), prompt constraints (ethical limits) and a human judge (human control).

## 10. Limitations and Future Work

- The AI may break character or give answers that are too perfect.
- Results depend on the model and its configuration.
- The quiz bank is small, and a small number of testers does not allow statistical conclusions.
- Future work: more question categories, multiple judges, comparison between different LLMs, and native mobile versions.

## 11. Conclusion

*I Am Mother* demonstrates that artificial intelligence can help humanity, but it can also represent risks when it has excessive power. Therefore, technology must be developed responsibly, ethically, and with respect for human autonomy.

**Main lesson:** technology should serve people without taking away their freedom of choice.

## 12. References

- Sputore, G. (Director). (2019). *I Am Mother* [Film]. Penguin Empire.
- Turing, A. M. (1950). *Computing Machinery and Intelligence*. Mind, 59(236), 433–460.
- Weizenbaum, J. (1966). *ELIZA — A Computer Program for the Study of Natural Language Communication between Man and Machine*. Communications of the ACM, 9(1), 36–45.

---

*This project was developed for educational purposes.*
