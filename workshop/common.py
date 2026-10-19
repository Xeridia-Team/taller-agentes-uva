import os
import shutil
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()

ROOT = Path(__file__).parent.parent
DOCUMENTS_DIR = ROOT / "documents"
WORKSPACE_DIR = ROOT / "workspace"

Category = Literal[
    "enrollment", "scholarships", "credit_transfer", "grade_appeal", "other"
]
Confidence = Literal["high", "medium", "low"]

model = OpenAIResponsesModel(
    os.environ["MODEL"],
    provider=OpenAIProvider(
        base_url=os.environ["OPENAI_BASE_URL"], api_key=os.environ["OPENAI_API_KEY"]
    ),
)


def create_workspace(path: Path) -> None:
    """Copy the original documents into `path/inbox`, discarding any previous run."""
    shutil.rmtree(path, ignore_errors=True)
    shutil.copytree(DOCUMENTS_DIR, path / "inbox")
