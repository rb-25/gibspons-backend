import google.generativeai as genai
from decouple import config

genai.configure(api_key=config('GEMINI_KEY'))

model = genai.GenerativeModel('gemini-pro')