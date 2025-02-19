from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def text_to_text(text: str):
    """テキストを加工する（例: LLM に渡すなど）"""
    processed_text = text.upper()  # 仮の処理
    return {"processed_text": processed_text}
