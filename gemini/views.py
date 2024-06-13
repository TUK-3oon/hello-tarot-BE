# from gemini.logger import log
import os
import time
from config.utils import validate_serializer, exception_handler, success_response
from gemini.serializer import GoogleAIRequestSerializer, GoogleAIResponseSerializer
import google.generativeai as genai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_AI_TOKEN = os.getenv("GOOGLE_AI_TOKEN")


@api_view(["POST", "GET"])
@exception_handler(view=True)
def google_ai(request):
    """
    Use Gemini Prompt View
     
    Request:\n
        {
            "contents":
                [
                    {"parts": [
                        {"text":"python에 대해 설명해줘"}
                    ]
                }
            ]
        }
    

    Response : \n
        candidates {
        index: 0
            content {
            parts {
                text: "Python은 가장 많이 쓰이는 프로그래밍 언어입니다."
            }
            role: "model"
            }
        ...
        }
    """
    if request.method == "GET":
        return success_response({"message": "This is a GET request"}, status=status.HTTP_200_OK)

    serializer = validate_serializer(GoogleAIRequestSerializer, request.data)
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    content = ""
    contents = serializer.get('contents', [])
    headers = {
        'Authorization': f'Token {GOOGLE_AI_TOKEN}',
        'Content-Type': 'application/json',
    }

    for c in contents:
        parts = c.get('parts', [])
        for part in parts:
            text = part.get('text', None)
            if text:
                content = text

    response_text = model.generate_content(content)
    candidates = response_text.candidates if response_text else []
    parts = [{'text': candidate.content.parts[0].text} for candidate in candidates]

    text = [part['text'] for part in parts]

    response_data = GoogleAIResponseSerializer({'response': text})
    return success_response(response_data.data, status=status.HTTP_200_OK)
