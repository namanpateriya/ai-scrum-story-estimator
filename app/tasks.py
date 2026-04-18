from crewai import Task
from app.schemas import SCRUM_OUTPUT_SCHEMA

def get_tasks(input_text, po, dev, qa, sm):

    po_task = Task(
        description=f"""
Create:
- User Story
- Acceptance Criteria (list)
- Definition of Done (list)
- Priority (Low/Medium/High)

Input:
{input_text}
""",
        agent=po
    )

    dev_task = Task(
        description="""
Based on PO output:
- Technical approach
- Components
- Complexity drivers
- Initial story point estimate (Fibonacci scale)
""",
        agent=dev
    )

    qa_task = Task(
        description="""
Based on PO + Dev output:
- Test cases
- Edge cases
- Risks
""",
        agent=qa
    )

    sm_task = Task(
        description=f"""
Based on all outputs:

Finalize:
- Story points
- Confidence
- Estimation reasoning

Return final output in this format:

{SCRUM_OUTPUT_SCHEMA}
""",
        agent=sm
    )

    return [po_task, dev_task, qa_task, sm_task]
