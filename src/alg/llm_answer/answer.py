import requests
from pydantic import BaseModel, Field

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


def chat_answer(question: str, analysis: str, mental: str, character: str) -> str:
    rag_decision = determine_use_rag(question)

    # TODO: analyze, mental, characterを入れてプロンプトを作る

    system_prompt = """"""
    if rag_decision.use_rag:
        related_docs = hybrid_search()
        user_prompt = f"""
        hogehoge
        
        Question:
        {question}
        
        Related Documents:
        {related_docs}
        
        Output:
        """
    else:
        user_prompt = f"""
        fugafuga
        
        Question:
        {question}
        
        Output:
        """

    answer = gpt_call(system_prompt, user_prompt.format(question))
    return answer
