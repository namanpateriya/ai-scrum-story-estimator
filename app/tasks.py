from crewai import Task

FULL_OUTPUT_SCHEMA = """
Return STRICT JSON ONLY:

{
  "user_story": "...",
  "acceptance_criteria": ["..."],
  "definition_of_done": ["..."],
  "technical_approach": "...",
  "test_cases": ["..."],
  "story_points": 1|2|3|5|8|13,
  "priority": "Low | Medium | High",
  "confidence": "Low | Medium | High",
  "estimation_reasoning": "...",
  "risks": ["..."]
}

RULES:
- DO NOT omit any field
- DO NOT add extra text
- Ensure valid JSON
"""

PRIORITY_RULES = """
Priority rules:
- High → blockers, revenue impact, critical systems
- Medium → feature improvements
- Low → UI / minor enhancements
"""

def get_tasks(input_text, po, dev, qa, sm):

    po_task = Task(
        description=f"""
Generate:
- user_story
- acceptance_criteria
- definition_of_done
- priority

{PRIORITY_RULES}

Input:
{input_text}
""",
        agent=po
    )

    dev_task = Task(
        description="""
Based ONLY on PO output:
- technical_approach
- components
- complexity drivers
- story_points (Fibonacci only)
""",
        agent=dev,
        context=[po_task]
    )

    qa_task = Task(
        description="""
Based ONLY on PO + Dev:
- test_cases
- risks
""",
        agent=qa,
        context=[po_task, dev_task]
    )

    sm_task = Task(
        description=f"""
Combine ALL outputs and return FINAL structured JSON.

{FULL_OUTPUT_SCHEMA}
""",
        agent=sm,
        context=[po_task, dev_task, qa_task]
    )

    return [po_task, dev_task, qa_task, sm_task]
