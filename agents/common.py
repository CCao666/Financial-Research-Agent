import os

from langchain_openai import ChatOpenAI


def model(temperature: float = 0.1) -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=temperature,
    )


def last_text(messages: list) -> str:
    content = messages[-1].content
    if isinstance(content, str):
        return content
    return str(content)

