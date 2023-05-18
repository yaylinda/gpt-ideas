import configparser
import json
from typing import Dict, List

import requests

from exceptions import APIException


class OpenAPIModel:
    def __init__(self, initial_message: Dict = None):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.api_key: str = config.get('open.ai', 'apiKey')
        self.org_id: str = config.get('open.ai', 'orgId')

        self.messages: List[Dict[str, str]] = []
        if initial_message is not None:
            self.messages.append(initial_message)

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def chat(self, message: str, model: str = 'gpt-3.5-turbo', temperature: float = 0.7) -> Dict:
        """

        :param message:
        :param model:
        :param temperature:
        :return:
        """
        self.__add_message(role='user', content=message)

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=self.headers,
            data=json.dumps({
                "model": model,
                "temperature": temperature,
                "messages": self.messages,
            })
        )

        if response.status_code != 200:
            raise APIException(response.status_code, response.text)

        body = response.json()

        self.__add_message(role='assistant', content=body['choices'][0]['message']['content'])

        return body

    def prompt(self, message: str, model: str = 'gpt-3.5-turbo', temperature: float = 0.7) -> Dict:
        """

        :param message:
        :param model:
        :param temperature:
        :return:
        """
        self.__add_message(role='user', content=message)

        response = requests.post(
            "https://api.openai.com/v1/completions",
            headers=self.headers,
            data=json.dumps({
                "model": model,
                "temperature": temperature,
                "prompt": message,
            })
        )

        if response.status_code != 200:
            raise APIException(response.status_code, response.text)

        body = response.json()

        self.__add_message(role='assistant', content=body['choices'][0]['text'])

        return body

    def clear(self):
        self.messages = []

    def __add_message(self, role: str, content: str):
        self.messages.append({
            'role': role,
            'content': content,
        })
