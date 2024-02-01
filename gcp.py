import json
import logging
from api import configure_routing
from flask import Flask
from google.cloud import storage
from quotes import QuoteClient


class CloudStorageQuoteClient(QuoteClient):
    def __init__(self, bucket_name: str, object_name: str):
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        self.content = blob.download_as_string()

    def quotes(self) -> list[dict]:
        return json.loads(self.content)['quotes']
    
    def source(self) -> dict:
        return json.loads(self.content)['source']


gunicorn_logger = logging.getLogger('gunicorn.error')
config = {
    'bucket_name': 'lboc-quotes',
    'object_name': 'quotes.json'
}
app = Flask(__name__)
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

configure_routing(app, CloudStorageQuoteClient(**config))
