# Evaluation & Prompt Optimization Module

This module adds **quality measurement + self-improvement** to your AI Scrum Estimator.

Instead of relying on subjective judgment, you now have a **repeatable evaluation pipeline** and a **closed-loop prompt optimization system**.

---

# What This Module Does

## 1. Evaluator (`evaluator.py`)

Runs your AI Scrum system against test cases and measures:

### Basic Metrics

* Structure validity (all required fields present)
* Story point validity (Fibonacci compliance)
* Priority accuracy (expected vs actual)

### Advanced Metrics

* Output completeness (via structure)
* Consistency of estimation
* Stability across runs

### LLM-as-Judge

Evaluates qualitative aspects:

* Clarity (0–10)
* Completeness (0–10)
* Usefulness for developers (0–10)

---

## 2. Optimizer (`optimizer.py`)

Creates a **self-improving loop**:

```text
Prompt → Run → Evaluate → Detect Failures → Improve Prompt → Repeat
```

This allows your system to:

* Fix estimation errors
* Improve prioritization
* Enforce output structure

---``

---

# Setup

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Set environment variables

Create `.env`:

```bash
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini
```

---

## 3. Ensure project structure

Evaluator expects access to:

```text
app/
  service.py   → run_scrum_team()
```

---

# Test Case Format

## `evaluation/test_cases.json`

```json
[
  {
    "input": "Fix login issue where users cannot sign in",
    "expected_priority": "High"
  },
  {
    "input": "Add search functionality for products",
    "expected_priority": "Medium"
  }
]
```

---

# How to Run Evaluator

```bash
python -m evaluation.evaluator
```

---

# Sample Output (Per Case)

```text
Fix login issue where users cannot sign in
Points: 5 | Priority: High
```

---

# Evaluation Summary

```text
=== SUMMARY ===

total_cases: 20
structure_accuracy: 0.95
points_accuracy: 0.85
priority_accuracy: 0.90
avg_clarity: 7.8
avg_usefulness: 7.5
```

---

# How to Interpret Metrics

## Structure Accuracy

> % of outputs that contain all required fields

Low → prompt not enforcing format properly

---

## Points Accuracy

> % of outputs using valid Fibonacci values

Low → estimation drift

---

## Priority Accuracy

> % match with expected priority

Low → weak prioritization logic

---

## LLM Scores

* **Clarity** → readability
* **Usefulness** → dev-ready quality

---

# How to Run Optimizer

```bash
python -m evaluation.optimizer
```

---

# Optimization Flow

Each iteration:

```text
1. Run evaluator
2. Collect failures
3. Ask LLM to improve prompt
4. Replace prompt
5. Repeat
```

---

# Sample Optimization Output

```text
=== ITERATION 1 ===
Failures detected: 6

=== ITERATION 2 ===
Failures detected: 2

=== ITERATION 3 ===
No failures. Stable.
```

---

# What Gets Improved Automatically

### Estimation accuracy

* Reduces incorrect story points

### Priority classification

* Fixes High vs Medium vs Low

### Output structure

* Ensures required fields

---

# Limitations

## Not true fine-tuning

* Model weights are NOT updated
* Only prompt evolves

---

## Risk of overfitting

* Optimizer may tune to dataset only

Mitigation:

* Use diverse test cases
* Periodically refresh dataset

---

# Best Practices

## 1. Keep iterations low

```text
2–3 iterations is optimal
```

---

## 2. Review final prompt manually

Never blindly trust automated changes

---

## 3. Track prompt versions

```text
prompts/
  v1.txt
  v2.txt
```

---

## 4. Expand dataset gradually

Use real-world Jira tickets

---
