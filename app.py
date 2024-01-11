import uuid
import requests
from flask import Flask, request, jsonify
from requests_toolbelt.multipart.encoder import MultipartEncoder

app = Flask(__name__)

HEADERS = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "b1d7f01c5b5aaf56b5a978ef5e928d6a"
}

SUPABASE_URL = "https://praybook.supabase.co/storage/v1/object/public/kisses"
SUPABASE_HEADERS = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh3dHppZWpodGptbnp4ZHBmZ252Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDQ4OTg1NDAsImV4cCI6MjAyMDQ3NDU0MH0.oL89GuGChfbULff3k9g0KHp34ioiJd3-gnSDzL7jRxQ"}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/convert-text', methods=['POST'])
def convert_text():
    try:
        data = request.get_json()
        prayer_text = data.get('prayer')

        payload = {
          "text": prayer_text,
          "model_id": "eleven_monolingual_v1",
          "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
          }
        }

        response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/TRTmtbmKhZXKwNfQ6AsG', headers=HEADERS, json=payload)
        print(f"ElevenLabs API Response: {response.status_code}, {response.text}")

        filename = f'{uuid.uuid4()}.mp3'

        with open(filename, 'wb') as f:
            f.write(response.content)

        m = MultipartEncoder(
            fields={'file': (filename, open(filename, 'rb'), 'audio/mpeg')}
        )

        r = requests.post(SUPABASE_URL, headers={**SUPABASE_HEADERS, 'Content-Type': m.content_type}, data=m)
        print(f"Supabase Upload Response: {r.status_code}, {r.text}")

        return r.json()
    except Exception as e:
       return str(e)

if __name__ == '__main__':
    app.run(debug=True)