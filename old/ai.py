import apiai
import json
import tokens


def smallTalk(msg):
    request = apiai.ApiAI(tokens.dialogflow).text_request()
    request.lang = 'ru'
    request.session_id = 'telegram-bot'
    request.query = msg
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    if response:
        return response
    else:
        return 'Я Вас не совсем понял!'
