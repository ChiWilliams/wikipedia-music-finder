from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OpenAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OpenAI_API_KEY)

from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)