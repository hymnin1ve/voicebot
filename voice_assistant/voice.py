import streamlit as st
from audiorecorder import audiorecorder
import openai
from datetime import datetime

from stt import STT
from gpt import ask_gpt
from tts import TTS

def main():
    st.set_page_config(
        page_title="음성 비서 프로그램",
        layout="wide"
    )
    st.header("음성 비서 프로그램")
    st.markdown("---")

    with st.expander("음성비서 프로그램에 관하여", expanded=True):
        st.write("""
        - UI는 스트림릿 활용
        - STT는 Whisper AI 활용
        - 답변은 GPT 모델 활용
        - TTS는 Google TTS 활용
        """
        )

    st.markdown("")

    #프로그램 처음 실행시 session_state 초기화
    if "chat" not in st.session_state:
        st.session_state["chat"] = []
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role":"system", "content":"You are a thoughtful assistant. Remember the conversation history and respond based on context. Always answer in Korean."}]
    
    if "check_reset" not in st.session_state:
        st.session_state["check_reset"] = False

    if "client" not in st.session_state:
        st.session_state["client"] = None

    #사이드바
    with st.sidebar:

        openai.api_key = st.text_input(
            label="OPENAI API 키",
            placeholder="Enter Your API Key",
            value="",
            type="password"
        )

        if openai.api_key:
            st.session_state["client"] = openai.OpenAI(api_key=openai.api_key)

        st.markdown("---")

        model = st.radio(
            label="GPT 모델",
            options=["gpt-4", "gpt-3.5-turbo"]
        )

        st.markdown("---")
        
        #실행 중 리셋(다시 처음으로)버튼
        if st.button(label="초기화"):
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role":"system", "content":"You are a thoughtful assistant. Remember the conversation history and respond based on context. Always answer in Korean."}]
            st.session_state["check_reset"] = True

    #열 분리        
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("음성 입력")

        audio = audiorecorder("녹음하기", "녹음중...")

        if (len(audio) > 0) and (st.session_state["check_reset"]==False):
            st.audio(audio.export().read()) #메모리에 저장. 파일 생성 없이 바로 데이터로 읽음.
            #audio.export("audio.mp3", format="mp3") - 파일로 저장. 실제 파일이 생성됨
            
            #STT 변환
            question = STT(audio, st.session_state["client"])

            #채팅 저장(화면 표시용)
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"].append(("user", now, question))

            #gpt(에게 보낼) 프롬프트 저장
            st.session_state["messages"].append({"role":"user", "content":question})

            #gpt 답변 받기
            answer = ask_gpt(st.session_state["messages"], model, st.session_state["client"])

            #TTS 변환 및 자동 재생
            b64 = TTS(answer)

            st.session_state["chat"].append(("assistant", now, answer, b64)) 
            #"chat"은 우리가 화면에 보기 위한 용도

            st.session_state["messages"].append({"role":"assistant", "content":answer}) 
            #"messages"는 GPT에게 보내기 위한 용도

    
    with col2:
        st.subheader("채팅 내용")

        if st.session_state["check_reset"]:
            st.session_state["check_reset"] = False 
            
            #check_reset = 초기화 알림 버튼 

            #True  =  울리는 중 (초기화 됐어!)
            #False =  꺼진 상태 (아무것도 안함)

            #한번 울리고 나면 다시 꺼야하니까
            #True 확인 후 → False로 바꾸는 것!
        
        for i, item in enumerate(st.session_state["chat"]):
            sender = item[0]
            time = item[1]
            message = item[2]

            if sender == "user":
                st.write(f"나({time}): {message}")
            else:
                st.write(f"GPT({time}):{message}")     
                
                if i == len(st.session_state["chat"]) -1:
                    b64 = item[3]
                    md = f"""
                        <audio autoplay="True">
                        <source src = "data:audio/mp3;base64,{b64}" type="audio/mp3">
                        </audio>
                        """
                    st.markdown(md,unsafe_allow_html=True)
    

if __name__ == "__main__":
    main()












