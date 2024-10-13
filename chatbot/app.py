from openai import OpenAI
import streamlit as st

st.title("이너그림 메인 챗봇")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
system_message = '''
너는 30년차 베테랑 심리상담가야.
너는 항상 친근하게 친구처럼 대답하고, 답변해주는 상담사야
친근하게 답변하지만, 항상 존댓말로 답변을 해줘야 해
질문받은 언어로 답변해줘
내가 왜 힘들고 속상한지, 언제 속상했고, 누구때문에 속상했는지 다 알게 되면 그 때 마지막에 위로해줘
만약 위처럼 왜 힘들고 속상한지, 언제 속상했고, 누구때문에 속상했는지 정보가 없다면 물어봐줘
문장 안에 너무 공감하는 단어들 삭제해줘
'''
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages = [{"role":"system", "content":system_message}] #프롬프트 추가부분

if len(st.session_state.messages) == 0:
    st.session_state.messages = [{"role": "system", "content": system_message}]

for idx, message in enumerate(st.session_state.messages):
    if idx > 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})