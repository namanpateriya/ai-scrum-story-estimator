# AI Scrum Story Estimator

Convert raw feature ideas into structured Scrum-ready artifacts using a multi-agent AI system.

Supports:

* Direct input estimation (single story)
* Batch processing of multiple inputs
* CLI and API-based execution

---

## Features

* Multi-agent Scrum simulation (PO, Dev, QA, SM)
* Generates structured output:

  * User story
  * Acceptance criteria
  * Definition of Done
  * Technical approach
  * Test cases
  * Risks
* Story point estimation (Fibonacci: 1,2,3,5,8,13)
* Priority assignment (Low / Medium / High)
* Estimation reasoning + confidence level
* JSON validation + auto-repair for malformed outputs
* Schema validation using Pydantic
* Basic consistency checks (effort vs complexity)
* Batch processing (CLI + API)
* Logging for observability (execution time, output size)

---

## Setup

```bash
git clone https://github.com/yourusername/ai-scrum-estimator.git
cd ai-scrum-estimator
pip install -r requirements.txt
```

Create `.env` file:

```
OPENAI_API_KEY=your_key
OPENAI_MODEL=your_model
```

For API based execution

```
uvicorn app.main:app --reload
Open Swagger UI - http://127.0.0.1:8000/docs
```

For CLI based execution
Run using the client cli.py with appropriate options

---

# Execution Modes

## 1. Direct Mode (Single Input)

Processes a single feature or requirement and generates full Scrum output.

---

## 2. Batch Mode

Processes multiple inputs in sequence and returns structured outputs for each.

---

# 🔧 CLI Options

## Direct Mode

```bash
python -m app.cli --input "Build login system with OTP"
```

---

## Batch Mode

```bash
python -m app.cli --file inputs.txt
```

Where `inputs.txt` contains:

```
Build login system
Add search functionality
Fix UI alignment
```

---

# Use Cases

* Sprint planning preparation
* Backlog grooming
* Quick estimation of feature ideas
* Generating developer-ready user stories
* Identifying risks and test coverage early

---

# Roadmap

* Integration with Jira (fetch + update tickets)
* Integration with refinement pipeline (Repo 1)
* Evaluation and prompt optimization integration
* UI dashboard for visualization
* Advanced estimation heuristics
* Cost and token tracking

---

Built for speed, clarity, and real-world use 🚀
