import asyncio
import os
import aiohttp

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

IAM_TOKEN = os.getenv('IAM_TOKEN')
folder_id = os.getenv('FOLDER_ID')
target_language = 'ru'

async def translate(context):
    try:
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
    except Exception as e:
        print(f"Yandex translate exception: {e}")
