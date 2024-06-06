import argparse
from copy import copy
from dataclasses import dataclass, field
from typing import List, Optional, Union

from semantic_domains.definitions import Question
from semantic_domains.hierarchy import assemble_hierarchy, read_domains_from_json
from guidance import models, gen

preamble = """
You are an expert in creating language resources. You help to provide examples of word usage to the domain in question. 
Responses that you give are short and concise. In those examples you show how to use the word, but do not overload the sentence with other 
words because this is important for creating a language resource. The words are organized in domains. Each domain includes
    a number for sorting purposes
    a domain label (consisting of a word or short phrase that captures the basic idea of the domain)
    a short description of the domain
    a series of questions designed to help people think of the words that belong to the domain
    a short list of English words under each question that belong to the domain, and their usage examples.

"""

EXT_VERSION = "EXTENDER_0.0.1"


@dataclass
class WordUsageExample:
    text: str
    source: str = ""


@dataclass
class Word:
    text: str
    source: str = ""
    usage_examples: List[WordUsageExample] = field(default_factory=list)


class PromptBuilder:
    def __init__(self):
        self.prompt = ""

    def __add__(self, extension: str):
        self.prompt += extension
        return self

    def estimate_tokens(self, string):
        return len(string.split()) * 2.5

    def truncate(self, max_length, split_on: str = "lines"):
        
        assert split_on == "lines"

        num_tokens = 0
        truncated_lines = []
        for line in reversed(self.prompt.split("\n")):
            line_tokens = self.estimate_tokens(line)
            if line_tokens + num_tokens > max_length:
                break

            truncated_lines.append(line)
            num_tokens += line_tokens

        truncated_prompt = "\n".join(reversed(truncated_lines))
        return self.__class__(truncated_prompt)
    
    def __repr__(self):
        return copy(self.prompt)
    
    def copy(self):
        return self.__class__() + self.prompt
    

class GeneratorWrapper:
    def __init__(self, llm, initial_prompt: Optional[Union[str, PromptBuilder]] = None):
        if initial_prompt is None:
            initial_prompt = ""
        self.llm = llm + self.prompt_as_string(initial_prompt)

    def prompt_as_string(self, prompt: Union[str, PromptBuilder]):
        if isinstance(prompt, str):
            return prompt
        elif isinstance(prompt, PromptBuilder):
            return repr(prompt)
        else:
            raise TypeError(f"Prompt must be a string or a PromptBuilder")

    def append(self, text: Union[str, PromptBuilder]):
        self.llm += self.prompt_as_string(text)

    def gen_append(self, **kwargs):
        existing = str(self.llm)
        self.llm += gen(**kwargs)
        generated = str(self.llm)[len(existing):]
        return generated
    

class DomainExtender:
    def __init__(self, llm):
        self.llm = llm

    @classmethod
    def domain_prompt(cls, domain):
        return (
            f"This is the language resource for the domain {domain.title}. "
            f"{domain.description} "
            f"The domain contains a list of questions, and a set of words and phrases, that answer those questions. "
            f"The questions are formulated in a way that they ask which words or phrases belong to this semantic domain. "
            f"The words and phrases are the answers to those questions. When there is an ambiguity about part of speech for a word, it is shown in the brackets after the word.\n"
        )
    
    @classmethod
    def questions_prompt(cls, domain):
        return (
            f"The questions that belong to this domain are:\n"
        )
    
    @classmethod
    def words_prompt(cls, question):
        return (
            f"The words or phrases that belong to this question are:\n"
        )
    
    @classmethod
    def examples_prompt(cls, word):
        return (
            f"Let's consider the word or phrase `{word}`. The usage examples that demonstrate how it should be used in a sentence are:\n"
        )
    
    @property
    def question_format(self):
        return "{q_num}. {question}\n"

    def extend_questions(self, domain, questions, prompt, extend_by: int = 10):
        prompt += self.questions_prompt(domain)
        
        for question in questions:
            prompt += self.question_format.format(q_num=question.num, question=question.text)

        next_question_num = len(domain.questions) + 1
        generator = GeneratorWrapper(self.llm, prompt)
        new_questions = []

        for i in range(extend_by):
            generator.append(f"{next_question_num}. ")
            new_question = generator.gen_append(stop=["\n", "?"], suffix="?\n", temperature=0.8)
            new_questions.append(Question(num=next_question_num, text=new_question.strip(), words=[]))
            next_question_num += 1

        return prompt.questions + new_questions
    
    def extend_words(self, domain, questions, prompt, extend_by: int = 10):
        prompt += self.questions_prompt(domain)

        updated_questions = []

        generator = GeneratorWrapper(self.llm, prompt)

        for question in questions:
            generator.append("\n")
            generator.append(self.question_format.format(q_num=question.num, question=question.text))
            generator.append(self.words_prompt(question))
            for word in question.words:
                generator.append(word + "; ")

            new_words = []

            for i in range(extend_by):
                generated = generator.gen_append(stop=[";", "\n"], suffix="; ", temperature=0.8)
                new_words.append(generated.strip("; "))

            updated_questions.append(
                Question(
                    num=question.num,
                    text=question.text,
                    words=question.words + new_words
                )
            )

        return updated_questions
    
    def extend_usage_examples(self, domain, questions, prompt, extend_by: int = 10):
        prompt += self.questions_prompt(domain)

        updated_questions = []

        generator = GeneratorWrapper(self.llm, prompt)

        for question in questions:
            generator.append("\n")
            generator.append(self.question_format.format(q_num=question.num, question=question.text))
            
            updated_words = []
            
            for word in question.words:
                generator.append(self.examples_prompt(word))

                if not isinstance(word, str):
                    for example in word.examples:
                        generator.append(f"- {example}\n")

                new_examples = []    

                for i in range(extend_by):
                    generator.append(f"- ")
                    generated = generator.gen_append(stop=[".", "\n"], suffix=".\n", temperature=0.8)
                    new_examples.append(WordUsageExample(generated.strip().replace("`", ""), source=EXT_VERSION))

                updated_words.append(Word(text=word, usage_examples=new_examples))

            updated_questions.append(
                Question(
                    num=question.num,
                    text=question.text,
                    words=updated_words
                )
            )

        return updated_questions

    def extend(
            self, domain, 
            extend_questions: bool = False, 
            extend_words: bool = False,
            extend_examples: bool = True
        ):
        prompt = PromptBuilder()
        prompt += self.domain_prompt(domain)
        questions = domain.questions
        if extend_questions:
            questions = self.extend_questions(domain, questions, prompt=prompt.copy())
        if extend_words:
            questions = self.extend_words(domain, questions, prompt=prompt.copy())
        if extend_examples:
            questions = self.extend_usage_examples(domain, questions, prompt=prompt.copy())
        domain.questions = questions
        

def main(args):
    domains = read_domains_from_json(args.domains)
    dh = assemble_hierarchy(domains)
    
    llm = models.LlamaCpp(args.model_path, n_ctx=4096) 
    
    extender = DomainExtender(llm)

    for domain in dh.traverse(max_depth=6):
        extender.extend(domain)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domains", help="Path to the domains json file")
    parser.add_argument("model_path", help="")
    
    args = parser.parse_args()
    main(args)
