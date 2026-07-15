from gtts import gTTS
import base64

def TTS(answer):
    tts = gTTS(text=answer, lang="ko")
    tts.save("answer.mp3")

    with open("answer.mp3", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        
    return b64