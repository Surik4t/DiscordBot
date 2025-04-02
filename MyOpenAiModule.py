import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import asyncio

load_dotenv()
client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_TOKEN"),
    base_url="https://api.deepseek.com"
)
async def send_prompt(content):
    try:
        completion = await client.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {
                    'role': 'system',
                    'content': 'Говори на русском языке, общайся дружелюбно, по возможности используй эмодзи. НЕ ЗДОРОВАЙСЯ если с тобой не здоровались. НЕ нужно писать assistant'
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
        )

        response = completion.choices[0].message.content
        return(response)

    except Exception as e:
        print(f"GPT exception: {e}")


asyncio.run(send_prompt('test'))