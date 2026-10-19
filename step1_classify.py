import argparse
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_ai import Agent

from workshop.common import Category, Confidence, model


class Classification(BaseModel):
    category: Category
    confidence: Confidence
    reason: str = Field(description="One sentence explaining the choice")


INSTRUCTIONS = """\
You classify messages received by the student office of the Computer Engineering school
at the University of Valladolid. Categories:
- enrollment: registration, adding or dropping courses, fees and payment.
- scholarships: grants and financial aid.
- credit_transfer: recognition or transfer of credits from other studies.
- grade_appeal: review or appeal of a grade.
- other: anything else.
"""

agent = Agent(model, output_type=Classification, instructions=INSTRUCTIONS)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify a single document.")
    parser.add_argument(
        "document", type=Path, help="path to the document, e.g. documents/doc_01.txt"
    )

    args = parser.parse_args()

    result = agent.run_sync(args.document.read_text(encoding="utf-8"))
    print(result.output.model_dump_json(indent=2))
