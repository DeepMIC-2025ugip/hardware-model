import json
import os
from datetime import datetime, timezone

from db.access_db import get_latest_character


def load_character():
    today = str(datetime.now(timezone.utc).date())

    if os.path.exists(f"data/character_{today}.json"):
        with open(f"data/character_{today}.json") as f:
            return json.load(f)
    else:
        character = get_latest_character()
        with open(f"data/character_{today}.json", "w") as f:
            json.dump(character, f)
        return character
