# Document classification with AI agents

Hands-on workshop: build an AI agent in Python with [Pydantic AI](https://ai.pydantic.dev/).
The agent processes the inbox of a university student office, classifies each document
into a fixed set of categories, moves it to the right tray, and asks a human for approval
when the case is doubtful. Finally, we measure how good it is with an eval.

## Setup

Requirements: Python basics and [uv](https://docs.astral.sh/uv/).

```
uv sync
```

Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY` with the key given in the workshop.

Check the connection to the model:

```
uv run step0_test.py
```

## Lint and type check

```
uv run ruff check
uv run ruff format
uv run ty check
```

## Steps

| Step | Script | Concept |
|---|---|---|
| 0 | `uv run step0_test.py` | Setup: check the connection to the model |
| 1 | `uv run step1_classify.py documents/doc_01.txt` | Typed output: the agent returns a validated `Classification` |
| 2 | `uv run step2_move.py` | Tools: the agent lists, reads and moves every document in the inbox |
| 3 | `uv run step3_approval.py` | Human in the loop: doubtful moves stop and wait for approval |
| 4 | `uv run step4_eval.py` | Eval: run the agent over a labelled dataset and score it |
| 5 | | Discussion: improve the score and lower the cost |

On `main`, steps 1 to 3 have `TODO` comments for you to complete.
The `solucion` branch has the complete code.

Steps 2 and 3 copy `documents/` into `workspace/inbox/` on every run, so you can repeat
them as many times as you want. After a run, look inside `workspace/` to see where each
document ended up.

## Categories

| Category | Content |
|---|---|
| `enrollment` | Registration, adding or dropping courses, fees and payment |
| `scholarships` | Grants and financial aid |
| `credit_transfer` | Recognition or transfer of credits from other studies |
| `grade_appeal` | Review or appeal of a grade |
| `other` | Anything else |

The agent also reports a confidence (`high`, `medium` or `low`). In step 3, a move needs
human approval when the confidence is `low` or the category is `other`
(see `needs_review` in `step3_approval.py`).

## Dataset

`documents/` contains 21 emails sent to the student office. `dataset.yaml` holds the
expected category of each one.
In a real project these labels would come from manual labelling, AI-assisted labelling
or historical data.

The documents are of four kinds:

- `clear`: one obvious category.
- `ambiguous`: could fit more than one category.
- `insufficient`: not enough information to decide.
- `out_of_scope`: spam, phishing or requests the office does not handle.

## Eval

`step4_eval.py` runs the step 1 agent on each document and scores:

- `EqualsExpected`: the agent chose the expected category.
- `tokens`: tokens used per document (model cost).

## Ideas for step 5

- Improve the instructions: define each category better or add examples.
- Add fields to `Classification`, for example a flag for missing information.
- Try a cheaper or a more capable model by changing `MODEL` in `.env`.
