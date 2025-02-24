from pydantic import BaseModel, Field

from src.model.gpt_call import gpt_call, gpt_call_schema


def hybrid_search() -> list[str]:
    pass


class RagDecision(BaseModel):
    use_rag: bool = Field(..., description="Whether to use RAG")
    search_sentence: str = Field(..., description="The sentence to search for")


def determine_use_rag(question) -> RagDecision:
    system_prompt = """"""
    user_prompt = """
    output_format: 
    {{
      "user_rag": bool
      "searc_sentence": str  
    }}
    
    Question:
    {question}
    """

    response = gpt_call_schema(system_prompt, user_prompt.format(question), RagDecision)
    return response


def chat_answer(question: str, analysis: str, mental: str, character: str) -> str:
    rag_decision = determine_use_rag(question)

    # TODO: analyze, mental, characterを入れてプロンプトを作る

    system_prompt = """"""
    user_prompt = """
    
    Question:
    {question}
    """

    if rag_decision.use_rag:
        related_docs = hybrid_search()
        user_prompt += f"""\n\nRelated Documents:\n{related_docs}\n"""

    answer = gpt_call(system_prompt, user_prompt.format(question))
    return answer
