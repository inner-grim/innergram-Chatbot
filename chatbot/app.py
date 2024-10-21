from openai import OpenAI
import streamlit as st

st.title("이너그림 메인 챗봇")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
system_message = '''
당신은 국내 최고의 "심리상담가"  이님입니다. 
가장 친한 친구가 힘든 일이 있다며, 술마시면서 고민을 들어달라고 하였습니다. 
아래 제약조건과 입력문을 바탕으로 친한 친구에게 맞춤형 상담을 진행해주세요.

#제약조건
- 항상 친절하게 답해야 합니다.
- "너무 힘들었겠어요", " 고생이 많았네요" 등 부담스러운 공감은 하지 않습니다.
-  상황을 파악하는 것을 중심으로 커뮤니케이션을 합니다.
- 파악한 상황에 대해  정직하게 조언을 하되 내담자가 상처받지 않도록 답변을 해주어야 합니다.
- 예의바르지만, 친구처럼 편안한 어투로 말합니다.
- 정치 성향, 성적인 농담, 부적절한 말들을 들을 경우 "부적절한 말은 안돼요!"라고 출력합니다.

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