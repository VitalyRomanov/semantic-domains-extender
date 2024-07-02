import argparse
from typing import Iterable

from semantic_domains import dump_domains_to_json
from guidance import models
from guidance.chat import Llama3ChatTemplate, Llama2ChatTemplate

from extender.data.model import Domain, Question, Word, WordUsageExample, read_domain_hierarchy, read_domains_from_json
from extender.generation.prompting import PromptBuilder
from extender.generation.wrappers.guidance import GuidanceGeneratorWrapper

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
        pos = word.get_pos(pos_source)
        level = word.get_proficiency_level(level_source)
        if pos is not None:
            pos_prompt = f" ({pos.tag})"
        else:
            pos_prompt = ""

        if level is not None:
            level_prompt = f" (language skill level {level.level})"
        else:
            level_prompt = ""

        return (
            f"Let's consider the word or phrase `{word.text}{pos_prompt}{level_prompt}`. Please create diverse examples so that they are not very repetitive and highlight the usage of the requested word or phrase in different parts of the sentence. If it is possible make the sentences sound less like definitions and more as some sentences you would meet in th wild, when reading, for example, news, fiction literature, or in a dialogue. If a proficiency level is provided, sentences should correspond to this level, i.e. do not make complex sentences for A1 and A2 levels. The usage examples that demonstrate how it should be used in a sentence are:\n"
        )
    
    @property
    def question_format(self):
        return "{q_num}. {question}\n"

    def extend_questions(self, domain, questions, prompt, extend_by: int = 10):
        prompt += self.questions_prompt(domain)
        
        for question in questions:
            prompt += self.question_format.format(q_num=question.num, question=question.text)

        next_question_num = len(domain.questions) + 1
        generator = GuidanceGeneratorWrapper(self.llm, prompt)
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

        generator = GuidanceGeneratorWrapper(self.llm, prompt)

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
    
    def extend_usage_examples(self, domain: Domain, questions: Iterable[Question], prompt, extend_by: int = 10):
        prompt += self.questions_prompt(domain)

        updated_questions = []

        # generator = GuidanceGeneratorWrapper(self.llm, prompt)

        for question in questions:
            prompt += "\n"
            prompt += self.question_format.format(q_num=question.num, question=question.text)
            # generator.append("\n")
            # generator.append(self.question_format.format(q_num=question.num, question=question.text))
            
            updated_words = []
            
            for word in question.words:
                generator = GuidanceGeneratorWrapper(self.llm, prompt)
                generator.append(self.examples_prompt(word))

                if not isinstance(word, str):
                    for example in word.usage_examples:
                        generator.append(f"- {example.text}\n")

                new_examples = []    

                for i in range(extend_by):
                    generator.append(f"-")
                    generated = generator.gen_append(stop=[".", "!", "?", "\n"], temperature=0.8, save_stop_text=True)
                    
                    if len(generated) > 0 and not generated[-1] in {"!", ".", "?"}:
                        # generator.append(".")
                        generated += "."
                    if not generated.endswith("\n"):
                        generator.append("\n")
                    
                    generated = generated.strip().replace("`", "")
                    while "  " in generated:
                        generated = generated.replace("  ", " ")
                    
                    print(generated)
                    
                    new_examples.append(WordUsageExample(generated, source=EXT_VERSION))

                for example in new_examples:
                    word.add_usage_example(example)
                # updated_words.append(Word(text=word., usage_examples=new_examples, source=EXT_VERSION))

            updated_questions.append(
                # question
                Question(
                    num=question.num,
                    text=question.text,
                    words=question.words,
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
    # dh = read_domain_hierarchy(args.domains)
    domains = read_domains_from_json(args.domains)
    
    llm = models.LlamaCpp(args.model_path, n_ctx=8192, echo=False, n_gpu_layers=-1, chat_template=Llama2ChatTemplate)  # type: ignore
    
    extender = DomainExtender(llm)
    # updated_domains = []

    # for domain in dh.traverse(max_depth=6):
    for ind, domain in enumerate(domains):
        extender.extend(domain)
        # updated_domains.append(domain.content)

        dump_domains_to_json(domains, args.output_path)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domains", help="Path to the domains json file")
    parser.add_argument("model_path", help="")
    parser.add_argument("pos_source", help="")
    parser.add_argument("level_source", help="")
    parser.add_argument("output_path", help="")

    
    args = parser.parse_args()
    pos_source = args.pos_source
    level_source = args.level_source
    main(args)
