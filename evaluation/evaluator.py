import json
import logging
import os
from statistics import mean

from openai import OpenAI

from app.service import run_scrum_team

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TEST_FILE = "evaluation/test_cases.json"


# ------------------ Validators ------------------ #

REQUIRED_KEYS = [
    "user_story",
    "acceptance_criteria",
    "definition_of_done",
    "technical_approach",
    "test_cases",
    "story_points",
    "priority",
    "confidence",
    "estimation_reasoning",
    "risks"
]


def check_structure(output: dict):
    return all(k in output for k in REQUIRED_KEYS)


def check_story_points(output):
    return output.get("story_points") in [1, 2, 3, 5, 8, 13]


# ------------------ LLM Judge ------------------ #

def judge_output(output: dict):
    try:
        prompt = f"""
Evaluate this Scrum output:

Return STRICT JSON:
{{
  "clarity": 0-10,
  "completeness": 0-10,
  "usefulness": 0-10
}}

OUTPUT:
{json.dumps(output)}
"""

        res = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return json.loads(res.choices[0].message.content)

    except Exception as e:
        logger.warning(f"Judge failed: {str(e)}")
        return {"clarity": None, "completeness": None, "usefulness": None}


# ------------------ Evaluation ------------------ #

def evaluate():
    with open(TEST_FILE) as f:
        test_cases = json.load(f)

    results = []

    for case in test_cases:
        try:
            output = run_scrum_team(case["input"], use_refinement=False)

            if "error" in output:
                results.append({"input": case["input"], "error": output["error"]})
                continue

            structure_ok = check_structure(output)
            points_ok = check_story_points(output)
            priority_ok = output["priority"] == case["expected_priority"]

            judge = judge_output(output)

            result = {
                "input": case["input"],
                "structure_ok": structure_ok,
                "points_ok": points_ok,
                "priority_ok": priority_ok,
                "story_points": output["story_points"],
                "priority": output["priority"],
                "judge_clarity": judge["clarity"],
                "judge_usefulness": judge["usefulness"]
            }

            results.append(result)

            print(f"\n{case['input']}")
            print(f"Points: {output['story_points']} | Priority: {output['priority']}")

        except Exception as e:
            results.append({"input": case["input"], "error": str(e)})

    return results


# ------------------ Summary ------------------ #

def summarize(results):
    valid = [r for r in results if "error" not in r]

    total = len(valid)

    summary = {
        "total_cases": total,
        "structure_accuracy": sum(r["structure_ok"] for r in valid) / total,
        "points_accuracy": sum(r["points_ok"] for r in valid) / total,
        "priority_accuracy": sum(r["priority_ok"] for r in valid) / total,
        "avg_clarity": mean([r["judge_clarity"] for r in valid if r["judge_clarity"]]),
        "avg_usefulness": mean([r["judge_usefulness"] for r in valid if r["judge_usefulness"]])
    }

    print("\n=== SUMMARY ===")
    for k, v in summary.items():
        print(f"{k}: {round(v,2) if isinstance(v,float) else v}")

    return summary


if __name__ == "__main__":
    res = evaluate()
    summarize(res)
