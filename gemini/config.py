from config.settings import GOOGLE_API_KEY
import google.generativeai as genai

class GeminiConfig:
    def __init__(self):
        self.api_key = GOOGLE_API_KEY

    def setModel(self):
        genai.configure(api_key=self.api_key)
            
        generation_config = {
            "temperature": 0,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 4000,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]

        return genai.GenerativeModel(model_name='gemini-pro',
                                    #   generation_config=generation_config, 
                                        safety_settings=safety_settings)