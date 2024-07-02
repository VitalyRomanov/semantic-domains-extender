from collections import defaultdict
import json
from pathlib import Path

import spacy
from semantic_domains import read_domains_from_json
from nltk.corpus import wordnet as wn
from conllu import parse


def get_matching_wn_entries(word):
    # https://wordnet.princeton.edu/documentation/wndb5wn
    wordnet_pos_remap = {
        "n": "NOUN",
        "v": "VERB",
        "a": "ADJ",
        "s": "ADJ",
        "r": "ADV",
        "i": "PROPN",
    }
    synsets = wn.synsets(word)
    for synset in synsets:
        for lemma in synset.lemmas():
            if lemma.name().startswith(word):
                pos = str(lemma).split(".")[1]
                yield wordnet_pos_remap[pos]
    

def main(args):
    domains = read_domains_from_json("/Users/Vitalii.Romanov/dev/semantic-domains-extender/en.json", as_hierarchy=True)
    pos = defaultdict(set)
    nlp = spacy.load("en_core_web_md")

    sentences = parse(Path("/Users/Vitalii.Romanov/Downloads/en_gum-ud-train.conllu").read_text())
    for sentence in sentences:
        for token in sentence:
            pos[token["form"]].add(token["upos"])
            pos[token["lemma"]].add(token["upos"])

    sd_pos = defaultdict(set)
    unknown = list()

    for domain in domains.traverse(max_depth=6):
        for question in domain.questions:
            for word in question.words:
                for token in nlp(word):
                    word_ = token.text
                    if word_ in pos:
                        for pos_ in pos[word_]:
                            sd_pos[pos_].add(word_)
                            sd_pos[pos_].add(word_.capitalize())
                    else:
                        wn_match = False 
                        for pos_ in get_matching_wn_entries(word_):
                            wn_match = True
                            sd_pos[pos_].add(word_)
                            sd_pos[pos_].add(word_.capitalize())
                        
                        if wn_match is False:
                            sd_pos[token.pos_].add(word_)
                            sd_pos[token.pos_].add(word_.capitalize())
                                # doc = nlp(word)
                                # for word__ in doc:
                                #     if word__.text == word_:
                                #         sd_pos[word__.pos_].add(word_)
                                #     break
                                # else:
                                #     unknown.append(word_)

                    
    with open("pos.json", "w") as f:
        json.dump({k: list(v) for k, v in sd_pos.items()}, f, indent=4)
        
                

if __name__ == "__main__":
    main(None)