import requests

from tools.settings import Settings

class Telegram:
    __SEND_MESSAGE_URL = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s'

    __idChannel = None
    __idChat    = None
    __token     = None

    def __init__(self):
        config = Settings().getTelegramConfig()

        self.__token     = config['bot_token']
        self.__idChannel = config['channel_id']
        self.__idChat    = config['chat_id']

    def sendToBot(self, message: str) -> bool:
        return self.__send(self.__idChat, message)

    def sendToChannel(self, message: str):
        return self.__send(self.__idChannel, message)

    def __send(self, idChat: str, message: str):
        url = self.__SEND_MESSAGE_URL % (self.__token, idChat, message)

        response = requests.get(url)

        return response.status_code == 200
