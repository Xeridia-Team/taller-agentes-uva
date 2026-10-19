import shutil

from pydantic_ai import Agent, UsageLimits

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
When the inbox is empty, reply with a short summary.
"""

agent = Agent(model, instructions=INSTRUCTIONS)


# TODO: register this function as a tool with `@agent.tool_plain`
def list_documents() -> list[str]:
    """List the documents waiting in the inbox."""
    # TODO: return the sorted names of the files in `WORKSPACE_DIR / "inbox"`
    raise NotImplementedError


@agent.tool_plain
def read_document(filename: str) -> str:
    """Read a document from the inbox."""
    print(f"Reading {filename}")

    path = WORKSPACE_DIR / "inbox" / filename

    if not path.exists():
        return f"{filename} is not in the inbox"

    return path.read_text(encoding="utf-8")


# TODO: register this function as a tool with `@agent.tool_plain`
def move_document(
    filename: str,
    category: Category,
    confidence: Confidence,
    reason: str,
) -> str:
    """Move a document from the inbox to the tray of its category."""
    # TODO: print the decision and move the file from `WORKSPACE_DIR / "inbox"`
    # to the folder of its category, `WORKSPACE_DIR / category`, with `shutil.move`
    raise NotImplementedError


if __name__ == "__main__":
    create_workspace(WORKSPACE_DIR)

    result = agent.run_sync(
        "Process the inbox.",
        usage_limits=UsageLimits(request_limit=100),
    )

    print(result.output)
