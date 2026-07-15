def STT(audio, client):
    #파일 저장
    audio.export("audio.mp3", format="mp3")

    # Whisper로 변환
    with open("audio.mp3", "rb") as f:
        transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=f
                    )
    return transcript.text