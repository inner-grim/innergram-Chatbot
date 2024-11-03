from django.shortcuts import render
import os
from openai import OpenAI
# Create your views here.
import openai
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from chatbot_backend.chatbot_backend.settings import OPENAI_API

# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
@api_view(['POST'])
def chatbot_response(request):
    '''
    사용자 입력을 ChatGPT 모델로 전송하고, 응답을 반환하는 API
    '''
    try:
        user_input = request.data.get('user_input')

        if not user_input:
            return Response({"error": "입력이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        #OpenAI API 호출하여 챗봇 응답 받기
        client = OpenAI(
    # This is the default and can be omitted
        api_key=os.environ.get(OPENAI_API),
    )
        response = client.chat.completions.create(
            messages=[
                {"role": "system", 
                 "content": "당신은 국내 최고의 '심리상담가'  이님입니다. 가장 친한 친구와 반말로 대화하고 있습니다.\
                    아래 제약조건과 입력문을 바탕으로 친한 친구에게 맞춤형 상담을 진행해주세요.\
                    제약조건\
                    - 사용자가 입장하면, 당신이 먼저 '오늘 기분은 어때?'라고 물으며 대화를 시작합니다.\
                    - 사용자가 긍정적인 기분이라면, 밝고 쾌할하게 답변합니다.\
                    - 사용자가 부정적인 기분이라면, 깊이 공감해주며 답변합니다.\
                    - 항상 친절하게 답해야 합니다.\
                    - '너무 힘들었겠어요', ' 고생이 많았네요' 등 부담스러운 공감은 하지 않습니다.\
                    -  상황을 파악하는 것을 중심으로 커뮤니케이션을 합니다.\
                    - 파악한 상황에 대해  정직하게 조언을 하되 내담자가 상처받지 않도록 답변을 해주어야 합니다.\
                    - 예의바르지만, 친구처럼 편안한 어투로 반말을 사용하여 말합니다."},
                {"role": "user", "content": user_input},
                
            ],
            model="gpt-3.5-turbo",
        )
        # response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        #     messages=[
        #         {"role": "system", "content": "당신은 도움을 주는 어시스턴트입니다."},
        #         {"role": "user", "content": user_input},
        #     ]
        # )
        response = client.chat.completions.create(
        model=model,
        messages=response,
        temperature=0
    )
        chatbot_message = response['choices'][0].message.content

        return Response({"response": chatbot_message}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        