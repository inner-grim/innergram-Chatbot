from pydantic import BaseModel

class RequestChatBot(BaseModel):
    previous_conversion : list[dict] #이전 대화 내용(json이지만 list로 받아옴)
    question : str #현재 질문
