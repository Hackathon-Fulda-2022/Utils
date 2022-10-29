import requests 
import time


def translate(text, lang = "DE"):
    for x in range (10):
        result = requests.get( 
       "https://api-free.deepl.com/v2/translate", 
       params={ 
         "auth_key": "6690e289-fb41-c5c0-5ed3-f0043cc6486a:fx", 
         "target_lang": lang, 
         "text": text, 
       },
       )
        translated_text = result.json()["translations"][0]["text"]
        if result.status_code == 200: return translated_text
        if result.status_code == 429: time.sleep(0.004)
        if result.status_code == 456: return "Quota exceeded! Change auth_key"
    
    return "Too many requests!"


print(translate("Hello"))