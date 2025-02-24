from alg.llm_answer.answer import chat_answer
from db.access_db import save_conversation


def chat_roop():
    child_words = []
    ai_words = []

    visible = True
    while True:
        question = input("Q: ")

        # analysis, mental, character = load_analysis(), load_mental(), load_character()
        analysis, mental, character = "まだ不明です", "まだ不明です", "まだ不明です"

        response_text = chat_answer(
            question, analysis, mental, character, child_words, ai_words
        )

        child_words.append(question)
        ai_words.append(response_text)


def main():
    chat_roop()


if __name__ == "__main__":
    main()
