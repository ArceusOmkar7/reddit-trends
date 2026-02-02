from __future__ import annotations

import logging
from functools import lru_cache
from typing import Iterable

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

logger = logging.getLogger("reddit_trends.nlp")

_REQUIRED_RESOURCES = ("punkt", "stopwords")


def ensure_nltk_resources() -> None:
    for resource in _REQUIRED_RESOURCES:
        try:
            nltk.data.find(f"tokenizers/{resource}")
        except LookupError:
            try:
                nltk.data.find(f"corpora/{resource}")
            except LookupError:
                logger.info("Downloading NLTK resource: %s", resource)
                nltk.download(resource, quiet=True)


@lru_cache(maxsize=1)
def get_stopwords() -> set[str]:
    ensure_nltk_resources()
    return set(stopwords.words("english"))


def tokenize(text: str) -> list[str]:
    ensure_nltk_resources()
    return [token.lower() for token in word_tokenize(text) if token.strip()]


def filter_stopwords(tokens: Iterable[str]) -> list[str]:
    stopword_set = get_stopwords()
    return [token for token in tokens if token not in stopword_set]
