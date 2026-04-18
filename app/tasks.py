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
Create:
- User Story
- Acceptance Criteria (list)
- Definition of Done (list)
- Priority (Low/Medium/High)

{PRIORITY_RULES}

Input:
{input_text}
""",
        agent=po
    )

    dev_task = Task(
        description="""
Based ONLY on PO output:

Provide:
- Technical approach
- Components
- Complexity drivers
- Initial story point estimate (Fibonacci: 1,2,3,5,8,13)
""",
        agent=dev,
        context=[po_task]
    )

    qa_task = Task(
        description="""
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
Based on ALL outputs:

Finalize:
- Story points (must be Fibonacci: 1,2,3,5,8,13)
- Confidence (Low/Medium/High)
- Estimation reasoning

Return STRICT JSON ONLY.
""",
        agent=sm,
        context=[po_task, dev_task, qa_task]
    )

    return [po_task, dev_task, qa_task, sm_task]
