import shutil

from pydantic_ai import Agent, UsageLimits

from step2_move import list_documents, read_document
from workshop.common import WORKSPACE_DIR, Category, Confidence, create_workspace, model

INSTRUCTIONS = """\
You process the inbox of the student office of the Computer Engineering school
at the University of Valladolid. Categories:
- enrollment: registration, adding or dropping courses, fees and payment.
- scholarships: grants and financial aid.
- credit_transfer: recognition or transfer of credits from other studies.
- grade_appeal: review or appeal of a grade.
- other: anything else.

List the documents, then read each one, classify it and move it with `move_document`.
Work on one document at a time: never read or move more than one document at once.
If a human reviewer denies a move, follow the reviewer's comment: it has the final word.
When the inbox is empty, reply with a short summary.
"""

agent = Agent(model, instructions=INSTRUCTIONS)
agent.tool_plain(list_documents)
agent.tool_plain(read_document)


def needs_review(category: Category, confidence: Confidence) -> bool:
    # TODO: a move needs review when the confidence is "low" or the category is "other"
    raise NotImplementedError


@agent.tool_plain
def move_document(
    filename: str,
    category: Category,
    confidence: Confidence,
    reason: str,
) -> str:
    """Move a document from the inbox to the tray of its category."""
    print(f"{filename} -> {category} ({confidence}): {reason}")

    # TODO: when the move needs review, ask the human with `input("Approve? [y/n] ")`.
    # If the answer is not "y", ask for a comment with `input()` and return it
    # to the agent instead of moving the file.

    source = WORKSPACE_DIR / "inbox" / filename
    destination = WORKSPACE_DIR / category

    if not source.exists():
        return f"{filename} is not in the inbox"

    destination.mkdir(exist_ok=True)
    shutil.move(source, destination)

    return f"{filename} moved to {category}/"


if __name__ == "__main__":
    create_workspace(WORKSPACE_DIR)

    result = agent.run_sync(
        "Process the inbox.",
        usage_limits=UsageLimits(request_limit=100),
    )

    print(result.output)
