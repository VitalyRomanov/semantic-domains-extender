import argparse
from ast import literal_eval
from collections import defaultdict
from typing import List

import bm25s
from guidance import assistant, models, gen, user, system
from guidance.chat import Llama3ChatTemplate

from extender.data.model import Domain, PartOfSpeech, Word, read_domain_hierarchy
from semantic_domains.rwc_parser import dump_domains_to_json


EXT_VERSION = "EXTENDER_0.0.1"


class Prompter:
    def get_system_prompt(self) -> str:
        system_prompt = ""
        return system_prompt
    
    def get_user_prompt(self, **kwargs) -> str:
        return ""


class ResponseGenerator:
    def __init__(self, llm) -> None:
        self.llm = llm


class SemanticDomainsPosPrompter(Prompter):
    possible_pos_with_examples = {
        "noun": ["cake", "shoes", "bus", "car", "dog", "cat", "apple", "orange"],
        "pronoun": ["I", "you", "he", "she", "it"],
        "determiner": ["a", "the", "this", "that"],
        "adjective": ["red", "blue", "green", "yellow", "big", "small"],
        "verb": ["eat", "drink", "sleep", "run", "walk", "jump", "swim", "fly", "sing", "dance"],
        "adverb": ["quickly", "slowly", "well", "badly", "slowly", "slowly", "well", "badly"],
        "number": ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"],

        "adjective phrase": ["very happy", "incredibly difficult", "less interesting", "more excited than usual", "extremely intelligent", "absolutely wonderful", "somewhat tired", "highly controversial", "too expensive", "fairly common"],
        "adverb phrase": ["very quickly", "somewhat reluctantly", "surprisingly well", "more rapidly", "too slowly", "rather unfortunately", "almost always", "quite easily", "very rarely", "much better"],
        "conjunction phrase": ["as well as", "but also", "not only", "either...or", "both...and", "neither...nor", "rather than", "whether...or", "no sooner...than", "just as"],
        "interjection": ["oh", "wow", "ah", "uh", "um", "umm"],
        "noun phrase": ["the big brown dog", "a book on the table", "my younger brother", "an old friend of mine", "the CEO of the company", "a bright sunny day", "the President of the United States", "several interesting articles", "a glass of water", "the smell of fresh bread"],
        "prepositional phrase": ["on the table", "in the garden", "under the bed", "after the party", "before the meeting", "with my friends", "at the corner", "by the river", "about the incident", "for a long time"],
        "quantifier phrase": ["a lot of money", "many people", "three books", "several hours", "a few days", "less than half", "more than enough", "a couple of weeks", "all the time", "a dozen eggs"],
        "verb phrase": ["is running quickly", "has been studying hard", "will write a letter", "can speak three languages", "should have arrived by now", "might go to the party", "is cooking dinner", "has finished the project", "was reading a book", "would like to travel",]
    }

    def get_system_prompt(self):
        system_prompt = "Please help me create a language resource. It involves analyzing text and deciding parts of speech for words.\n"

        system_prompt += "Possible types of speech are:\n"
        for key, values in self.possible_pos_with_examples.items():
            system_prompt += f"{key} (for example {', '.join(values)}, etc.)\n"

        system_prompt += "When summarizing part of speech for a group of words, use only noun, pronoun, determiner, adjective, verb, adverb, and number.\n"
        return system_prompt

    def get_user_prompt(self, *, question, domain, **kwargs):
        assigner_prompt = (
            "The words below are associated by a common topic. "
            "The topic belongs to the domain that can be described by the title {domain_title}. "
            "The topic is described by the following question\n"
            "{question}\n"
            "The words (or phrases) that are described by answering the question are:\n"
            "{words}\n"
            "Which part of speech do these words or phrases belong to? If it is not a word but a phrase, e.g. a prepositional phrase, tell which role this phrase plays in the sentence (e.g. adjective or adverb, etc.).\n"
        )

        return assigner_prompt.format(
            domain_title=domain.title,
            question=question.text,
            words="; ".join([word.text for word in question.words])
        )
    
    def get_possible_answers(self):
        return list(self.possible_pos_with_examples.keys())


class SemanticDomainsPosResponseGenerator(ResponseGenerator):
    pos_canonical_names = {
        "noun": "NOUN",
        "pronoun": "PRON",
        "determiner": "DET",
        "adjective": "ADJ",
        "verb": "VERB",
        "adverb": "ADV",
        "number": "NUM",

        "adjective phrase": "ADJP",
        "adverb phrase": "ADVP",
        "conjunction phrase": "CONJP",
        "interjection": "INTJ",
        "noun phrase": "NP",
        "prepositional phrase": "PP",
        "quantifier phrase": "QP",
        "verb phrase": "VP"
    }

    def __init__(self, llm, prompter) -> None:
        super().__init__(llm)
        self.prompter = prompter
        self.pos_matcher = POSMatcher(prompter.get_possible_answers())

    def decode_pos(self, pos):
        return self.pos_canonical_names[self.pos_matcher.get(pos)]
    
    def remove_brackets(self, text):
        try:
            opening = text.index("(")
            closing = text.index(")")
            text = text[:opening] + text[closing + 1:]
        except ValueError:
            ...
        return text
        
    def get_response(self, *, question, domain, **kwargs):
        with system():
            llm = self.llm + self.prompter.get_system_prompt()

        with user():
            llm += self.prompter.get_user_prompt(question=question, domain=domain)

        with assistant():
            llm += "Let's assign the part of speech to each word or phrase. Each word can belong to one or several parts of speech. However, we can narrow it down given the current topic.\n"
            for word in question.words:
                llm += f"The word or phrase `{self.remove_brackets(word.text)}` is a" + gen(stop=["\n", "."], suffix=". ", name="pos", list_append=True)  # type: ignore
            llm += "Overall, we can say that this group of words or phrases belongs to the part of speech" + \
                gen(stop=["\n", ".", ","], suffix=". ", name="group_pos")  # type: ignore
            
            wwpos = list(
                zip(
                    question.words,
                    [self.decode_pos(pos) for pos in llm["pos"]]
                )
            )
            group_pos = self.decode_pos(llm["group_pos"])

        return {
            "group_pos": group_pos,
            "word_pos": wwpos
        }
    

class SemanticDomainsPosResponseReader(ResponseGenerator):
    def __init__(self, file_path) -> None:
        self.parse_file(file_path)

    def parse_file(self, file_path):
        storage = defaultdict(lambda: defaultdict(list))
        
        with open(file_path, "r") as f:
            for line in f:
                code, qnum, group_pos, *rest = line.split()
                storage[code][int(qnum)].extend(literal_eval(" ".join(rest)))

        self.storage = storage

    def get_response(self, *, question, domain, **kwargs):
        wwpos = self.storage[domain.code][question.num]    

        assert len(wwpos) == len(question.words)
        output = []
        for word, (pos, w_text) in zip(question.words, wwpos):
            assert word.text == w_text, f"Word `{word.text}` does not match the expected word `{w_text}`"
            output.append((Word(text=word.text, source="semantic-domains"), pos))

        return {
            "group_pos": None,
            "word_pos": output
        }


class POSMatcher:
    def __init__(self, possible_pos) -> None:
        corpus_tokens: List[List[str]] = bm25s.tokenize(possible_pos)  # type: ignore
        self.retriever = bm25s.BM25(corpus=possible_pos)
        self.retriever.index(corpus_tokens)

    def get(self, query: str):
        query_tokens: List[List[str]] = bm25s.tokenize([query])  # type: ignore
        docs, scores = self.retriever.retrieve(query_tokens, k=1)
        return docs[0, 0]


class PosAssigner:
    def __init__(self, response_generator) -> None:
        self.response_generator = response_generator

    def assign_pos(self, question, domain):
        if len(question.words) == 0:
            return None

        response = self.response_generator.get_response(question=question, domain=domain)
        for word, (w_, pos) in zip(question.words, response["word_pos"]):
            assert word.text == w_.text, f"Word {word} does not match the expected word {w_}"
            word.add_pos(PartOfSpeech(pos, source=EXT_VERSION))
        return response
        

def main(args):
    dh = read_domain_hierarchy(args.domains)

    if args.pos_file_path is None:
        llm = models.LlamaCpp(args.model_path, n_ctx=8192, echo=False, n_gpu_layers=-1, chat_template=Llama3ChatTemplate)  # type: ignore
        response_generator = SemanticDomainsPosResponseGenerator(llm, SemanticDomainsPosPrompter())
    else:
        response_generator = SemanticDomainsPosResponseReader(args.pos_file_path)

    assigner = PosAssigner(response_generator)

    updated_domains: List[Domain] = []
    for domain in dh.traverse():
        for question in domain.questions:
            assigner.assign_pos(question, domain=domain.content)
        
        if isinstance(domain.content, Domain):
            updated_domains.append(domain.content)
        else:
            raise ValueError(f"Expected Domain, got {type(domain.content).__name__}")

    dump_domains_to_json(updated_domains, args.output_path)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domains", help="Path to the domains json file")
    parser.add_argument("model_path", help="")
    parser.add_argument("output_path", help="")
    parser.add_argument("--pos_file_path", help="")
    
    
    args = parser.parse_args()
    main(args)
