from fastapi import FastAPI

from api.routers import speech_to_text, test_to_speech, text_to_text

app = FastAPI()

app.include_router(speech_to_text.router, prefix="/api/stt")
app.include_router(test_to_speech.router, prefix="/api/tts")
app.include_router(text_to_text.router, prefix="/api/ttt")


@app.get("/")
def read_root():
    return {"message": "Welcome to nuigurumi machine!"}
