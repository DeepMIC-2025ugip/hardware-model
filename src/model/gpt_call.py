from typing import Any, Generator, Type

from openai import OpenAI
from pydantic import BaseModel

from settings import settings

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


def gpt_call(
    system_prompt: str,
    user_prompt: str,
    modelname: str = "gpt-4o-mini",
) -> Generator[str, None, None]:
    messages = create_messages(system_prompt, user_prompt)

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

    response_text = ""
    for chunk in response:
        content = chunk.choices[0].delta.content  # type: ignore
        if type(content) == str:
            response_text += content
            # print(content, end="", flush=True)
            # yield content
    return response_text


def gpt_call_schema(
    system_prompt: str,
    user_prompt: str,
    response_format: Type[BaseModel],
    model: str = "gpt-4o-mini",
) -> BaseModel:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=messages,
        response_format=response_format,
        timeout=100,
    )

    event = completion.choices[0].message.parsed
    return event


if __name__ == "__main__":
    system_prompt = "You are the most intelligent person in the world."
    user_prompt = input("Q: ")
    messages = create_messages(system_prompt, user_prompt)
    for response in gpt_call(messages):
        print(response, end="", flush=True)
