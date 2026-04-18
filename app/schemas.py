SCRUM_OUTPUT_SCHEMA = """
STRICT JSON OUTPUT ONLY:

{
  "user_story": "...",
  "acceptance_criteria": ["..."],
  "definition_of_done": ["..."],
  "technical_approach": "...",
  "test_cases": ["..."],
  "story_points": number,
  "priority": "Low | Medium | High",
  "confidence": "Low | Medium | High",
  "estimation_reasoning": "...",
  "risks": ["..."]
}

RULES:
- Return ONLY JSON
- No extra text
- story_points must be Fibonacci: 1,2,3,5,8,13
"""
