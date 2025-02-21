import json

import requests

from settings import settings

headers = {"Content-Type": "application/json"}


def check_response(response: requests.Response):
    if response.status_code == 200:
        response_data = response.json()
        print("Success:", response_data)
        return response_data
    else:
        print("Error:", response.status_code, response.text)
        return None


def save_conversation(child_content, ai_content, visible: bool = True):
    """会話データをDBに保存"""
    for from_system, content in zip([False, True], [child_content, ai_content]):
        data = {"from_system": from_system, "content": content, "visible": visible}

        response = requests.post(
            f"{settings.backend_url}/conversations/",
            data=json.dumps(data),
            headers=headers,
        )
        check_response(response)


def analyze_day():
    """1日の会話データを解析"""
    response = requests.post(f"{settings.backend_url}/analyses/analyze_day/")
    return check_response(response)


def get_latest_character():
    """最新の子どもの性格を取得"""
    response = requests.get(f"{settings.backend_url}/characters/latest/")
    return check_response(response)


def analyze_character():
    """子どもの性格を解析"""
    response = requests.post(f"{settings.backend_url}/characters/analyze/")
    return check_response(response)


if __name__ == "__main__":
    save_conversation(from_system=False, content="もう一回テストするよー！！！！")

    analyze_day()

    get_latest_character()

    analyze_character()
