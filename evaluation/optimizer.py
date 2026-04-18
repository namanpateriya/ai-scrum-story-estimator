import json
import logging
import os
from openai import OpenAI

from evaluation.evaluator import evaluate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def collect_failures(results):
    return [r for r in results if not r.get("structure_ok")]


def improve_prompt(failures):
    try:
        prompt = f"""
Improve system instructions to fix failures:

{json.dumps(failures[:5], indent=2)}
"""

        res = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return res.choices[0].message.content

    except Exception as e:
        logger.error(e)
        return None


def optimize():
    results = evaluate()
    failures = collect_failures(results)

    if not failures:
        print("No failures detected")
        return

    improved = improve_prompt(failures)

    print("\n=== IMPROVED PROMPT ===\n")
    print(improved)


if __name__ == "__main__":
    optimize()
