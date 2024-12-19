from django.shortcuts import render
from django.http import JsonResponse
import os
from openai import OpenAI
# Create your views here.
import openai
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
import boto3
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough


# Parameter Store를 통해 API KEY 값 세팅
def fetch_api_key_from_parameter_store(parameter_name):
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response['Parameter']['Value']

# @api_view(['POST'])
# def chatbot_response(request):
    '''
    사용자 입력을 ChatGPT 모델로 전송하고, 응답을 반환하는 API
    '''
try:
    # api_key = fetch_api_key_from_parameter_store('/parameter/chatbot/api.key')
    api_key = "YOUR_API_KEY"

    os.environ["OPENAI_API_KEY"] = api_key # 보안을 위해 API KEY 여기서 뿌려줌

    #OpenAI API 호출하여 챗봇 응답 받기
    client = OpenAI(
# This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
    llm = ChatOpenAI(temperature=0.2, max_tokens=200) #응답의 무작위성

    #대화 내용 저장하기 위해 memory 사용하기
    memory = ConversationBufferMemory(
        llm=llm,
        memory_key="chat_history",
        return_messages=True
    )

    def load_memory(input):
        '''메모리에서 이전 대화 내용 가져오기 위해 사용하는 함수'''
        print(input)
        return memory.load_memory_variables({})["chat_hisotry"]
    
    templete = '당신은 국내 최고의 "심리상담가"입니다. 가장 친한 친구와 이야기하는 중입니다.\
                아래 제약조건과 입력문을 바탕으로 친한 친구에게 맞춤형 상담을 진행해주세요.\
                제약조건\
                - 대화를 시작할 때, 사용자가 제일 처음 입력으로 오늘 기분에 대해 알려줍니다. 그러면 답변으로, 무슨 일이 있었는지 물어봅니다.\
                - ~했구나, ~하겠네 등 무조건 반말로 말합니다 ~했어요, ~하죠 등 존댓말을 쓰지 않습니다.\
                - 첫 답변은 사용자의 기분에 따라 달라집니다.\
                - 사용자가 긍정적인 기분이라면, 밝고 행복한 어투로 답변합니다.\
                - 사용자가 부정적인 기분이라면, 깊이 공감해주며 답변합니다.\
                - 사용자가 중립적인 기분이라면, 평온한 어투로 답변합니다.\
                - 사용자에게 힘이 될 수 있는 조언을 추가해주세요.\
                - 항상 친절하게 답해야 합니다.\
                - "너무 힘들었겠어요, "고생이 많았네요 등 부담스러운 공감은 하지 않습니다.\
                -  상황을 파악하는 것을 중심으로 커뮤니케이션을 합니다.\
                - 파악한 상황에 대해  정직하게 조언을 하되 내담자가 상처받지 않도록 답변을 해주어야 합니다.\
                - 예의바르지만, 친구처럼 편안한 어투로 반말을 사용하여 말합니다.\
                - 내 감정이 누구떄문에, 언제, 어디서, 무엇을, 어떻게 왜 느꼈는지 하나씩 질문해서 알아내주세요.\
                - 만약 상대방과 대화가 끝났다고 판단되면, "이제 대화를 마무리해도 될까? 라고 질문해주세요.\
                - 다음은 상담의 예시입니다.\
                -"human" 뒤에 나오는 content는 사용자의 입력입니다.\
                - "ai" 뒤에 나오는 content는 사용자의 입력에 대한 챗봇의 답변입니다.\
                - "human", content: "슬픔", "우울",\
                - "ai", "content": "오늘 기분이 우울하구나, 무슨 일 있어?",\
                - "human", "content": "나 요즘 회사에서 너무 스트레스 받아",\
                - "ai", "content": "헥 무슨일이야 스트레스라니,, 스트레스는 만병의 근원이야 누가 괴롭혀?"\
                - "human", "content": "부사장이 자꾸 괴롭히고, 못살게 굴어. 왜 난 겨우 그런사람한테 자꾸 끌려가는 걸까 너무 속상하고 스트레스받고 짜증나",\
                - "ai", "content": "그렇게 괴롭히는 사람이 있으면 힘들지. 회사는 일도 중요하지만 같이 일하는 사람이 맞아야 다니기 낫잖아. 왜 그렇게 괴롭히는거 같아?",\
                - "human", "content": "모르겠어 그냥 내가 맘에 안드나봐. 사람이 안맞으니까 진짜 너무 힘들고 스트레스 받아",\
                - "ai", "content": "부사장이 언제 그렇게 괴롭혀?",\
                - "human", "content": "그냥 회의떄도 막말하고, 일하다가 내가 실수한게 있으면 놓치지 않고 엄청 뭐라 해. 진짲 내가 너무 일 못하는 사람이 된거 같아"\
                - "ai", "content": "아이고 많이 힘들겠다... 그래도 너가 너무 힘들면 아예 퇴사하는게 더 나을수도 있어 새로 이직을 해보는건 어때?",\
                - "human", "content": "이직도 고민중이야.. 암튼 이렇게 얘기 들어줘서 너무 고마워"\
                - "ai", "content": "일도 좋지만, 너가 항상 행복했으면 좋겠어! 이제 대화를 마무리해도 될까?",\
                - 사용자가 "그만하고 일기 작성하기" 입력을 주면, 지금까지 저장된 대화 모두 출력해줘 \
                '
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", templete),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])

    #메모리의 채팅 기록 반환 함수
    chain = RunnablePassthrough.assign(chat_history=lambda _: memory.load_memory_variables({})["chat_history"]) | prompt | llm

    class ChatbotAPIView(APIView):
        def post(self,request, *args, **kwargs):
            data = JSONParser().parse(request)
            question = data.get("question", "")

            if not question:
                return JsonResponse({"error": "question is required"}, status=400)
            
            result = chain.invoke({"question":question})

            memory.save_context(
                {"input":question},
                {"output":result.content}
            )
        
            return JsonResponse({"response": result.content})
        
        # invoke_chain()
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", 
#                  "content": "당신은 국내 최고의 '심리상담가'입니다. 가장 친한 친구와 이야기하는 중입니다.\
#                     아래 제약조건과 입력문을 바탕으로 친한 친구에게 맞춤형 상담을 진행해주세요.\
#                     제약조건\
#                     - 상담은 반말로 진행합니다.\
#                     - 첫 답변은 사용자의 기분에 따라 달라집니다..\
#                     - 사용자가 긍정적인 기분이라면, 밝고 행복한 어투로 답변합니다.\
#                     - 사용자가 부정적인 기분이라면, 깊이 공감해주며 답변합니다.\
#                     - 사용자가 중립적인 기분이라면, 평온한 어투로 답변합니다.'\
#                     - 항상 친절하게 답해야 합니다.\
#                     - '너무 힘들었겠어요', ' 고생이 많았네요' 등 부담스러운 공감은 하지 않습니다.\
#                     -  상황을 파악하는 것을 중심으로 커뮤니케이션을 합니다.\
#                     - 파악한 상황에 대해  정직하게 조언을 하되 내담자가 상처받지 않도록 답변을 해주어야 합니다.\
#                     - 예의바르지만, 친구처럼 편안한 어투로 반말을 사용하여 말합니다."},
#                 {"role": "user", "content": user_input},
#             ],
#             max_tokens=200,
#             temperature=0.7  # 답변의 창의성 조절
# )
        # response = client.chat.completions.create(
        # model='gpt-3.5-turbo',
        #     messages=[
        #         {"role": "system", "content": "당신은 도움을 주는 어시스턴트입니다."},
        #         {"role": "user", "content": user_input},
        #     ]
    #     # )
    #     response = client.chat.completions.create(
    #     model=model,
    #     messages=response,
    #     temperature=0
    # )
        # chatbot_message = response['choices'][0].message.content
        # chatbot_message = response.choices[0].message.content #OPENAI 버전 업그레이드로 인한 함수 return 값의 type 변경
         

        # return Response({"response": chatbot_message}, status=status.HTTP_200_OK)

except Exception as e:
    Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


