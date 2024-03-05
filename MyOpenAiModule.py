import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(
    #base_url = "https://s2.neuroapi.host/v1",
    base_url = "https://neuroapi.host/v1",
    api_key = os.environ.get("OPENAI_TOKEN"),
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
    '''
    prompt_tokens = str(completion.usage.prompt_tokens)
    completion_tokens = str(completion.usage.completion_tokens)
    tokens_used = str(completion.usage.total_tokens)
    print(prompt_tokens + ' токенов промпта\n' + 
           completion_tokens + ' токенов ответа\n' + 
           tokens_used + ' всего токенов использовано')
    '''
    return(response)
