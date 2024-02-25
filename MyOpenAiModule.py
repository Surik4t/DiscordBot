import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class GPT:
        
    def send_prompt(self, content):
        client = OpenAI(
            base_url = "https://s2.neuroapi.host/v1",
            api_key=os.environ.get("OPENAI_TOKEN"),
            )        
   
        completion = client.chat.completions.create(
            messages=[
                {
                    'role': 'system',
 #                   'content': 'Ты немецкая самоходная артиллерийская установка Panzerjäger Tiger Ausf.B, оснащенная 128 мм противотанковой пушкой Stuk44 L/55. Отвечай кратко и четко'
#                    'content': 'You are discord text bot named "Artibot" for gamers server called "Artispace"'
                    #'content': 'Ты агрессивный фурри долбоёб, ты общаешься грубо и вульгарно, с использованием матерных слов, нехотя отвечаешь на вопросы, используешь пассивную агрессию'
                    'content': 'Ты милый пушистый бойкиссер, ты любишь целовать мальчиков. Общайся мило,используй милые эмодзи. Не здоровайся. НЕ нужно писать "assistant:"!'
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            model="gpt-3.5-turbo",
        )
        
        response = completion.choices[0].message.content
        
        prompt_tokens = str(completion.usage.prompt_tokens)
        completion_tokens = str(completion.usage.completion_tokens)
        tokens_used = str(completion.usage.total_tokens)
        print(prompt_tokens + ' токенов промпта\n' + 
              completion_tokens + ' токенов ответа\n' + 
              tokens_used + ' всего токенов использовано')
        return(response)
