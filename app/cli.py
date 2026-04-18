import argparse
import logging
import sys

from app.service import run_scrum_team

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_cli(input_text):
    try:
        result = run_scrum_team(input_text)

        print("\n=== SCRUM OUTPUT ===\n")
        print(result)

    except Exception as e:
        logger.error(f"CLI failed: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


parser = argparse.ArgumentParser(description="AI Scrum Estimator CLI")

parser.add_argument("--input", required=True)

args = parser.parse_args()

run_cli(args.input)
