from flask import Flask, render_template
from quotes import FallbackQuoteClient, QuoteClient, QuoteGenerator


def configure_routing(app: Flask, client: QuoteClient):
    logger = app.logger
    client = FallbackQuoteClient(client, logger)
    quotes = QuoteGenerator(client)
    source = client.source()

    @app.get('/')
    def home():
        quote, next = quotes.get(0)
        return render_template('index.html', label=quote.label, text=quote.text, next=next, source=source)

    @app.get('/quotes/<id>')
    def get_quote(id):
        quote, next = quotes.get(id)
        return render_template('partials/hello.html', label=quote.label, text=quote.text, next=next, source=source)
    
    @app.after_request
    def set_max_age(response):
        response.cache_control.max_age = 300
        return response
    
    return app
