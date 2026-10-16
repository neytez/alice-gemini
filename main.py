import os
import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Читаем ключ из системных переменных
API_KEY = os.environ.get("GEMINI_API_KEY", "")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/', methods=['POST'])
def webhook():
    data = request.json or {}
    req = data.get('request', {})
    user_text = req.get('original_utterance', '').strip()

    # Реакция на запуск навыка (когда пользователь еще ничего не спросил)
    if not user_text:
        return jsonify({
            "response": {
                "text": "Чем могу помочь?",
                "end_session": False
            },
            "version": "1.0"
        })

    # Отправка запроса пользователя в Gemini
    try:
        res = model.generate_content(user_text)
        reply = res.text
    except Exception as e:
        print(f"ОШИБКА GEMINI: {e}")
        reply = "Произошла ошибка при обращении к нейросети."

    return jsonify({
        "response": {
            "text": reply,
            "end_session": False
        },
        "version": "1.0"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
