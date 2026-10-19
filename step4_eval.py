from pydantic_evals import Dataset, increment_eval_metric

from step1_classify import agent
from workshop.common import DOCUMENTS_DIR, ROOT, Category


async def classify(filename: str) -> Category:
    text = (DOCUMENTS_DIR / filename).read_text(encoding="utf-8")
    result = await agent.run(text)
    increment_eval_metric("tokens", result.usage.total_tokens)
    increment_eval_metric("cost_usd", float(result.response.cost().total_price))

    return result.output.category


if __name__ == "__main__":
    dataset = Dataset[str, Category, dict].from_file(ROOT / "dataset.yaml")

    report = dataset.evaluate_sync(classify, max_concurrency=5, repeat=3)

    report.print(
        include_input=True,
        include_output=True,
        include_metadata=True,
        include_durations=False,
    )
