from crewai import Agent

def get_agents():
    po = Agent(
        role="Product Owner",
        goal="Write user stories, acceptance criteria, DoD and prioritize backlog",
        verbose=True
    )

    dev = Agent(
        role="Software Engineer",
        goal="Provide technical approach and estimate complexity",
        verbose=True
    )

    qa = Agent(
        role="QA Engineer",
        goal="Generate test cases and identify risks",
        verbose=True
    )

    sm = Agent(
        role="Scrum Master",
        goal="Facilitate estimation and finalize planning output",
        verbose=True
    )

    return po, dev, qa, sm
