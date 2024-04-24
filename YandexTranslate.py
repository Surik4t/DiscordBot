import asyncio
import os
import aiohttp

def get_IAM_token():
    file = open('IAM_token.txt', 'r')
    token = file.read().strip()
    file.close()
    return(token)


def parse_response(text):
    text = dict(text['translations'][0])

    answer = text['text']
    lang_code = text['detectedLanguageCode']

    if lang[lang_code] != None:
        language = lang[lang_code]
    else:
        language = lang_code

    return(answer, language)


lang = {'ar': 'арабский',
        'zh': 'китайский',
        'hr': 'хорватский',
        'cs': 'чешский',
        'da': 'датский',
        'nl': 'нидерландский',
        'en': 'английский',
        'fr': 'французский',
        'de': 'немецкий',
        'hi': 'индийский',
        'hu': 'венгерский',
        'it': 'итальянский',
        'kk': 'казахский',
        'id': 'индонезийский',
        'ja': 'японский',
        'ko': 'корейский',
        'ms': 'малазийский',
        'mn': 'монгольский',
        'no': 'норвежский',
        'pl': 'польский',
        'pt': 'португальский',
        'ro': 'румынский',
        'ru': 'русский',
        'sr': 'сербский',
        'es': 'испанский',
        'sv': 'шведский',
        'tt': 'татарский',
        'th': 'тайский',
        'tr': 'турецкий',
        'uk': 'украинский',
        'vi': 'вьетнамский'
        }

IAM_TOKEN = get_IAM_token()
folder_id = os.getenv('FOLDER_ID')
target_language = 'ru'

async def translate(context):
    async with aiohttp.ClientSession() as session:
        body = {
            "targetLanguageCode": target_language,
            "texts": context,
            "folderId": folder_id,
            }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {IAM_TOKEN}"
            }

        response = await session.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                 json = body,
                                 headers = headers
                                 )

        json = await response.json()
        response, lang_code = parse_response(json)
        await session.close()
        return(response, lang_code)

#asyncio.run(translate('what is your name'))
