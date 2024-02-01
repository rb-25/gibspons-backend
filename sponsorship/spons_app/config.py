import google.generativeai as genai
from IPython.display import display, Markdown
import textwrap
import pathlib

genai.configure(api_key="AIzaSyCsZB7PvKp5gO0JhtvD5pWfbgYmofU2DNc")

model = genai.GenerativeModel('gemini-pro')