import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
import asyncio

load_dotenv()
client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_TOKEN"),
    base_url="https://eu.neuroapi.host/v1"
)
async def send_prompt(content):
    completion = await client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': 'Ты милый пушистый бойкиссер, ты любишь целовать мальчиков. Говори на русском языке, общайся мило, используй милые эмодзи. Не здоровайся. НЕ нужно писать assistant'
            },
            {
                 "role": "user",
                "content": content
            }
        ],
        model="gpt-3.5-turbo",
    )
     
    response = completion.choices[0].message.content

    return(response)


asyncio.run(send_prompt('test'))