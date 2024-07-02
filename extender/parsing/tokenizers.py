from functools import lru_cache

import spacy


@lru_cache
def get_spacy_tokenizer():
    return spacy.load("en_core_web_md", enable=["tokenizer"])
