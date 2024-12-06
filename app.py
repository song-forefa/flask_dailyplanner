from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Bitly Access Token
ACCESS_TOKEN = "aadce181c724f76d691b4a7d6be067bf1c814728"

# HTML 템플릿
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
    <head>
        <title>UTM URL Shortener</title>
    </head>
    <body>
        <h1>UTM URL Shortener</h1>
        <form method="POST" action="/shorten">
            <label for="base_url">Base URL (상세 페이지 URL):</label><br>
            <input type="text" id="base_url" name="base_url" required style="width: 400px;"><br><br>
            
            <label for="utm_source">UTM Source:</label><br>
            <select id="utm_source" name="utm_source" required>
                <option value="facebook">Facebook</option>
                <option value="google">Google</option>
                <option value="instagram">Instagram</option>
                <option value="message">Message</option>
                <option value="kakaotalk">KakaoTalk</option>
                <option value="everytime">Everytime</option>
                <option value="ssgsac">SSGSAC</option>
                <option value="email">Email</option>
                <option value="coop">Coop</option>
                <option value="slack">Slack</option>
                <option value="landing">Landing</option>
                <option value="other">Other</option>
            </select><br><br>
            
            <label for="utm_medium">UTM Medium:</label><br>
            <input type="text" id="utm_medium" name="utm_medium" required><br><br>
            
            <label for="utm_campaign">UTM Campaign:</label><br>
            <input type="text" id="utm_campaign" name="utm_campaign" required><br><br>
            
            <label for="utm_content">UTM Content (선택):</label><br>
            <input type="text" id="utm_content" name="utm_content"><br><br>
            
            <button type="submit">Generate and Shorten URL</button>
        </form>
        
        {% if short_url %}
        <p>Generated URL with UTM: <a href="{{ long_url }}" target="_blank">{{ long_url }}</a></p>
        <p>Shortened URL: <a href="{{ short_url }}" target="_blank">{{ short_url }}</a></p>
        {% endif %}
    </body>
</html>
'''

# 메인 페이지
@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

# UTM 생성 및 Bitly로 축약
@app.route('/shorten', methods=['POST'])
def shorten_url():
    # 폼 입력값 가져오기
    base_url = request.form.get('base_url')
    utm_source = request.form.get('utm_source')  # 선택된 값 가져오기
    utm_medium = request.form.get('utm_medium')
    utm_campaign = request.form.get('utm_campaign')
    utm_content = request.form.get('utm_content', '')  # 선택 항목

    # UTM 파라미터 추가
    utm_params = f"utm_source={utm_source}&utm_medium={utm_medium}&utm_campaign={utm_campaign}"
    if utm_content:
        utm_params += f"&utm_content={utm_content}"
    long_url = f"{base_url}?{utm_params}"

    # Bitly API 요청
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {"long_url": long_url}
    response = requests.post("https://api-ssl.bitly.com/v4/shorten", json=data, headers=headers)

    if response.status_code in [200, 201]:
        short_url = response.json().get("link")
        return render_template_string(HTML_TEMPLATE, long_url=long_url, short_url=short_url)
    else:
        return f"Error: Unable to shorten URL. Status Code: {response.status_code}", 400

if __name__ == '__main__':
    app.run(debug=True)
