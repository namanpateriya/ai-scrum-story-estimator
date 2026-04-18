import json
import logging
import os

from openai import OpenAI

from evaluation.evaluator import evaluate
from app.prompt import get_system_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ------------------ Failure Detection ------------------ #

def collect_failures(results):
    failures = []

    for r in results:
        if "error" in r:
            continue

        if not (r["structure_ok"] and r["points_ok"] and r["priority_ok"]):
            failures.append(r)

    return failures


# ------------------ Prompt Improvement ------------------ #

def improve_prompt(prompt, failures):
    try:
        prompt_text = f"""
You are an expert prompt engineer.

Improve this system prompt.

CURRENT PROMPT:
{prompt}

FAILURES:
{json.dumps(failures[:5], indent=2)}

GOALS:
- Fix incorrect story point estimation
- Fix priority classification
- Ensure correct structure

Return ONLY improved prompt.
"""

        res = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.3
        )

        return res.choices[0].message.content

    except Exception as e:
        logger.error(f"Prompt improvement failed: {str(e)}")
        return prompt


# ------------------ Optimization Loop ------------------ #

def optimize(iterations=3):
    prompt = get_system_prompt("standard")

    for i in range(iterations):
        print(f"\n=== ITERATION {i+1} ===")

        results = evaluate()
        failures = collect_failures(results)

        if not failures:
            print("No failures. Stable.")
            break

        new_prompt = improve_prompt(prompt, failures)

        if new_prompt.strip() == prompt.strip():
            print("No improvement detected.")
            break

        prompt = new_prompt

    return prompt


if __name__ == "__main__":
    final_prompt = optimize()
    print("\n=== FINAL PROMPT ===\n")
    print(final_prompt)
