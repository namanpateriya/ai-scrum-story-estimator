from crewai import Task

PRIORITY_RULES = """
Priority rules:
- High → blockers, revenue impact, critical systems
- Medium → feature improvements
- Low → UI / minor enhancements
"""

def get_tasks(input_text, po, dev, qa, sm):

    po_task = Task(
        description=f"""
[PO OUTPUT REQUIRED]

Create:
- User Story
- Acceptance Criteria
- Definition of Done
- Priority

{PRIORITY_RULES}

Input:
{input_text}
""",
        agent=po
    )

    dev_task = Task(
        description="""
[DEV OUTPUT REQUIRED]

Based ONLY on PO output:

Provide:
- Technical approach
- Components
- Complexity drivers
- Initial story point estimate (Fibonacci only)
""",
        agent=dev,
        context=[po_task]
    )

    qa_task = Task(
        description="""
[QA OUTPUT REQUIRED]

Based ONLY on PO + Dev outputs:

Provide:
- Test cases
- Edge cases
- Risks
""",
        agent=qa,
        context=[po_task, dev_task]
    )

    sm_task = Task(
        description="""
[SM FINAL OUTPUT]

Based on ALL outputs:

Return STRICT JSON:
- Story points (Fibonacci)
- Confidence
- Estimation reasoning
""",
        agent=sm,
        context=[po_task, dev_task, qa_task]
    )

    return [po_task, dev_task, qa_task, sm_task]
