import os
from functools import cached_property
import google.generativeai as genai
from dotenv import load_dotenv
from retry import retry


class GeminiAIClient:

    SINGLETON_CLIENT = None

    @cached_property
    def is_gemini_enabled(self):
        print("Checking for OpenAI API key...")
        load_dotenv()
        if os.getenv("GEMINI_API_KEY") is None or os.getenv("GEMINI_API_KEY") == "":
            # Print warning message in red.
            print(
                "\033[91m"
                + "WARNING: GEMINI API key not found. GEMINI will not be used."
                + "\033[0m"
            )
            return False
        else:
            return True

    @retry(tries=3, delay=3.0)
    def get_completion(self, prompt: str):
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(f"{prompt}")

        return response


def gemini_client():
    if GeminiAIClient.SINGLETON_CLIENT is None:
        GeminiAIClient.SINGLETON_CLIENT = GeminiAIClient()
    return GeminiAIClient.SINGLETON_CLIENT
