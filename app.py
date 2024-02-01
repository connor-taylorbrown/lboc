from api import configure_routing
from flask import Flask
import requests
from quotes import QuoteClient


class MockClient(QuoteClient):
    def __init__(self, port: int):
        self.address = f'http://localhost:{port}'

    def quotes(self) -> list[dict]:
        response = requests.get(f'{self.address}/quotes')
        return response.json()
    
    def source(self) -> dict:
        response = requests.get(f'{self.address}/source')
        return response.json()


def create_app():
    ''' Default factory method for Flask CLI runner '''
    app = Flask(__name__)
    return configure_routing(app, MockClient(3000))
