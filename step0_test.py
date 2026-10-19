from pydantic_ai import Agent

from workshop.common import model

if __name__ == "__main__":
    result = Agent(model).run_sync("Reply with one word: OK")

    print(f"The model replied: {result.output}")
    print("The connection works.")
