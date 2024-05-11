import os
import time
import json
from .logger import log

import google.generativeai as genai
from gemini.serializer import GoogleAIRequestSerializer, GoogleAIResponseSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_AI_TOKEN = os.getenv("GOOGLE_AI_TOKEN")


@api_view(["POST", "GET"])
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
        return Response({"message": "This is a GET request"}, status=status.HTTP_200_OK)

    # Confirm validation and deserialzing data by using serialized data model
    serializer = GoogleAIRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    content = ""
    contents = serializer.validated_data.get('contents', [])

    headers = {
        'Authorization': f'Token {GOOGLE_AI_TOKEN}',
        'Content-Type': 'application/json',
    }

    # parse user question in request form
    # contents: user's request
    # c: content of "contents" -> I use 'c' for parsing property that "contents/parts/text"
    for c in contents:
        parts = c.get('parts', [])
        for part in parts:
            text = part.get('text', None)
            if text:
                content = text

    try:
        start = time.time()
        response_text = model.generate_content(content)
        end = time.time()
        log.info(f"Time taken to generate content {end - start}")

        candidates = response_text.candidates if response_text else []
        parts = [{'text': candidate.content.parts[0].text} for candidate in candidates]

        text = [part['text'] for part in parts]

        # Deserialzing data by using serialized data model
        response_serializer = GoogleAIResponseSerializer({'response': text})
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
