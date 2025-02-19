from typing import Any, Generator, Literal

from openai import OpenAI

from alg.settings import settings

client = OpenAI(api_key=settings.openai_api_key)


def create_messages(system_prompt: str, user_prompt: str) -> list[dict[str, Any]]:
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]
    return messages


def openai_call(
    messages: list[dict[str, Any]],
    modelname: str = "gpt-4o-mini",
) -> Generator[str, None, None]:
    response = client.chat.completions.create(
        model=modelname,
        messages=messages,  # type: ignore
        temperature=0.7,
        max_tokens=2000,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stream=True,
        timeout=100,
    )

    for chunk in response:
        content = chunk.choices[0].delta.content  # type: ignore
        if type(content) == str:
            yield content


if __name__ == "__main__":
    system_prompt = "You are the most intelligent person in the world."
    user_prompt = input("Q: ")
    messages = create_messages(system_prompt, user_prompt)
    for response in openai_call(messages):
        print(response, end="", flush=True)
