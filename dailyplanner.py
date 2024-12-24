from flask import Flask, request, render_template
import openai

# OpenAI API 키 설정
openai.api_key = "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"

# Flask 앱 생성
app = Flask(__name__)

# 기본 경로 (홈페이지)
@app.route("/")
def home():
    return render_template("index.html")

# 칭찬 생성 경로
@app.route("/generate", methods=["POST"])
def generate_compliment():
    user_input = request.form["daily_input"]  # 사용자가 입력한 텍스트 가져오기

    # OpenAI API로 칭찬 생성
    prompt = f"오늘 사용자가 한 일을 다음과 같이 적었습니다: '{user_input}'. 이를 바탕으로 사용자를 따뜻하게 칭찬하는 문구를 5-6줄로 작성해주세요."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    compliment = response['choices'][0]['text'].strip()

    return render_template("result.html", compliment=compliment)

# Flask 실행
if __name__ == "__main__":
    app.run(debug=True)
