import argparse
import json
import logging
import sys

from app.service import run_scrum_team

logger = logging.getLogger(__name__)


def run_single(input_text, refine):
    result = run_scrum_team(input_text, use_refinement=refine)
    print(json.dumps(result, indent=2))


def run_batch(file_path, refine):
    try:
        with open(file_path) as f:
            inputs = [line.strip() for line in f if line.strip()]

        results = []

        for i, inp in enumerate(inputs):
            print(f"\nProcessing {i+1}/{len(inputs)}")
            res = run_scrum_team(inp, use_refinement=refine)
            results.append(res)

        print("\n=== BATCH OUTPUT ===\n")
        print(json.dumps(results, indent=2))

    except Exception as e:
        logger.error(str(e))
        sys.exit(1)


parser = argparse.ArgumentParser()

parser.add_argument("--input")
parser.add_argument("--file")
parser.add_argument("--refine", action="store_true")

args = parser.parse_args()

if args.input and args.file:
    print("Use either --input or --file, not both")
    sys.exit(1)
    
if args.input:
    run_single(args.input, args.refine)
elif args.file:
    run_batch(args.file, args.refine)
else:
    print("Provide --input or --file")
