from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cache
from logging import Logger
import random


@dataclass
class Quote:
    label: int
    text: str


class QuoteClient(ABC):
    @abstractmethod
    def quotes(self) -> list[dict]:
        pass

    @abstractmethod
    def source(self) -> dict:
        pass


class FallbackQuoteClient(QuoteClient):
    def __init__(self, client: QuoteClient, logger: Logger):
        self.client = client
        self.logger = logger

    @cache
    def quotes(self) -> list[dict]:
        try:
            return self.client.quotes()
        except Exception:
            self.logger.exception("Error reading from database")
            return [
                {"label": "Wisdom #1", "text": "I said maybe..."},
                {"label": "Wisdom #2", "text": "You're gonna be the one that saves me..."}
            ]
        
    def source(self) -> dict:
        try:
            return self.client.source()
        except Exception:
            self.logger.exception("Error reading from database")
            return {
                "link": "https://en.wikipedia.org/wiki/Oasis_(band)"
            }
    

class QuoteGenerator:
    def __init__(self, client: QuoteClient):
        quotes = client.quotes()
        self.quotes = random.sample(quotes, len(quotes))

    def get(self, id: str) -> tuple[Quote, int]:
        id = int(id)
        quote = Quote(**self.quotes[id])
        return quote, (id + 1) % len(self.quotes)
