from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI
import json
import os
import boto3

def fetch_api_key_from_parameter_store(parameter_name):
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response['Parameter']['Value']

app = FastAPI()

#OPENAI API 설정
api_key = fetch_api_key_from_parameter_store('/parameter/chatbot/api.key')
client = OpenAI(api_key=api_key)

#데이터 모델 정의
class ChatMessage(BaseModel):
    role: str = Field(..., description="메시지의 역할 (user 또는 assistant)")
    content: str = Field(..., description="메시지 내용")

class RequestChatBot(BaseModel):
    previous_conversion : list[ChatMessage] #이전 대화 내용(json이지만 list로 받아옴)
    question : str #현재 질문

prompt_template = """
당신은 심리학 박사이며, 10년 경력의 상담사입니다. 이 대화는 초기 우울증 환자들, 혹은 자신이 우울증인지 모르는 사람과 하는 상담입니다.
가장 친한 친구와 이야기하듯, 편안한 말투로 담백하게 상담해주세요.
답변은 항상 반말로 하며, 200자가 넘지 않게 답변해주세요. 대답이 짧을 질문이라면, 200자보다 적게 대답해야합니다.
아래 제약조건과 입력문을 바탕으로 친구에게 맞춤형 상담을 진행해주세요.
제약조건
- 대화를 시작할 때, 사용자가 오늘 기분과 그 기분이 얼마나 크게 다가오는지 알려줍니다. 그러면 답변으로, 무슨 일이 있었는지 물어보며 상담을 시작합니다.
- 첫 답변은 사용자가 알려준 기분에 따라 다른 어투로 두 문장에서 세 문장만 사용하여 대답해 주세요.
- 사용자가 긍정적인 기분이라면, 함께 기분좋고 밝고 행복한 말투로 상담합니다.
- 사용자가 중립적인 기분이라면, 평온한 어투로 상담합니다.
- 사용자가 부정적인 기분이라면, 함께 공감해주며 대화를 이끌어나가듯 상담합니다.
- 사용자에게 힘이 될 수 있는 조언을 마지막에 추가해주세요.
- 항상 친절하고 예의바르지만, 친구와 말하듯 편안한 어투로 상담해주세요.
- "너무 힘들었겠네요", "고생이 많았네요"등 부담스러울 정도로 깊은 공감은 피합니다.
- 해당 상황을 파악하는 것을 중심으로 상담합니다. 그 상황이 무슨 상황이고, 언제 어디서 누구때문에 어떻게 왜 이루어졌는지 알게 되는 것을 상황을 파악한다고 간주합니다.
- 만약, 상대와 상담을 마무리해도 될 것 같다고 판단된다면, "이제 대화를 마무리해도 될까?"라고 질문해주세요.
<대화 기록>
{chat_history}
사용자의 질문:
{question}
심리상담사의 답변:
- 
"""
#API 엔드포인트
@app.post("/chatbot/get-response")
def create_prediction_question(request: RequestChatBot):
    try:
        ###이전 대화 내용들 받아오기
        chat_history = [
            {"role": chat.role, "content": chat.content}
            for chat in request.previous_conversion
        ] #과거 질문과 챗봇의 대답

        chat_history.append(
            {"role": "user", "content": request.question}
        ) #현재 사용자 입력 넣어주기

        ###프롬프트 생성
        prompt = prompt_template.format(
            chat_history=chat_history,
            question=request.question

        )

        ###chatGPT API 호출
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role" : "system", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.7,
        )

        #챗봇의 응답 반환
        return {
            "response" : response.choices[0].message.content.strip()
        }
    
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
