import openai
import schedule
import time

# 서준이 이메일 주소
RECIPIENT_EMAIL = "dadmam0329@naver.com"  


# OpenAI API 키 설정
openai.api_key = "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"

# 서준이의 계획과 실행 상태 저장
plans = {"morning_plan": None, "evening_report": None}

# 아침 8시: 계획 질문 및 칭찬
def morning_message():
    print("메시지: '오늘의 계획은 무엇인가요?'")  # 아침 메시지 발송
    plans["morning_plan"] = input("서준이의 답변을 입력해주세요: ")  # 서준이의 답변 입력
    morning_response = f"좋은 생각이에요! '{plans['morning_plan']}' 같은 계획은 정말 멋진 선택이에요. 오늘 하루도 알차게 보내길 바랄게요! 😊"
    print(f"아침 답변: {morning_response}")

# 저녁 8시: 리마인드 메시지
def evening_message():
    print("메시지: '계획을 잘 지키고 있나요? 오늘 하루를 잘 보내고 있기를 바랄게요!'")  # 저녁 리마인드 메시지 발송

# 밤 10시: 계획 실행 여부 질문 및 칭찬
def night_message():
    print("메시지: '오늘의 계획을 얼마나 지켰는지 알려주세요!'")  # 밤 메시지 발송
    plans["evening_report"] = input("서준이의 답변을 입력해주세요: ")  # 서준이의 답변 입력
    
    # OpenAI를 사용해 긴 칭찬 메시지 생성
    prompt = f"서준이가 오늘 '{plans['morning_plan']}'이라는 계획을 세웠고, 그에 대한 실행 내용을 다음과 같이 답했습니다: {plans['evening_report']}. 이에 대해 진심 어린 칭찬을 5-6줄로 작성해주세요."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    compliment = response['choices'][0]['text'].strip()
    print(f"밤 답변: {compliment}")

# 스케줄 설정
schedule.every().day.at("08:00").do(morning_message)  # 아침 8시
schedule.every().day.at("20:00").do(evening_message)  # 저녁 8시
schedule.every().day.at("22:00").do(night_message)    # 밤 10시

# 스케줄 실행
while True:
    schedule.run_pending()
    time.sleep(1)
