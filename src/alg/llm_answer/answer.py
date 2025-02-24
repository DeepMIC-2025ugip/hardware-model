import requests
from pydantic import BaseModel, Field

from alg.llm_answer.prompt.chat_answer_prompt import (
    ANSWER_SYSTEM_PROMPT,
    CHAT_ANSWER_USER_PROMPT,
    RAG_ANSWER_USER_PROMPT,
)
from alg.llm_answer.prompt.use_rag_prompt import (
    DETERMINE_RAG_SYSTEM_PROMPT,
    DETERMINE_RAG_USER_PROMPT,
)
from model.gpt_call import gpt_call, gpt_call_schema
from settings import settings


def hybrid_search(question: str, top: int = 4) -> list[str]:
    url = f"{settings.backend_url}/search/hybrid_search/"
    payload = {"question": question, "top": top}
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"Failed to get related documents: {response.text}")
    else:
        return response.json()


class RagDecision(BaseModel):
    use_rag: bool = Field(..., description="Whether to use RAG")
    search_sentence: str = Field(..., description="The sentence to search for")


def determine_use_rag(question) -> RagDecision:
    response = gpt_call_schema(
        DETERMINE_RAG_SYSTEM_PROMPT,
        DETERMINE_RAG_USER_PROMPT.format(question=question),
        RagDecision,
    )
    return response


def format_conversation(user: list[str], ai: list[str]) -> str:
    return "\n".join(
        [f"Child: {user[i]}\nYou: {ai[i]}" for i in range(min(len(user), len(ai)))]
    )


def chat_answer(
    question: str,
    analysis: str,
    mental: str,
    character: str,
    child_words: list[str],
    ai_words: list[str],
) -> str:
    rag_decision = determine_use_rag(question)
    conversation = format_conversation(child_words, ai_words)

    if rag_decision.use_rag:
        related_docs = hybrid_search()
        user_prompt = CHAT_ANSWER_USER_PROMPT.format(
            question=question,
            character=character,
            analysis=analysis,
            mental=mental,
            conversation=conversation,
        )
    else:
        user_prompt = RAG_ANSWER_USER_PROMPT.format(
            question=question,
            character=character,
            analysis=analysis,
            mental=mental,
            conversation=conversation,
            related_docs=related_docs,
        )

    answer = gpt_call(ANSWER_SYSTEM_PROMPT, user_prompt)
    return answer
