from dataclasses import dataclass, field
from typing import Callable, Dict, List, Union


from semantic_domains.definitions import Question as OriginalQuestion, Domain as OriginalDomain, SemanticDomainObject
from semantic_domains import read_domains_from_json as original_read_domains_from_json
from semantic_domains.hierarchy import assemble_hierarchy, DomainNode


original_source = "semantic-domains"


@dataclass
class WordUsageExample(SemanticDomainObject):
    text: str
    source: str


@dataclass
class PartOfSpeech(SemanticDomainObject):
    tag: str
    source: str


@dataclass
class WordFrequency(SemanticDomainObject):
    freq: int
    source: str

@dataclass
class Synset(SemanticDomainObject):
    synset: str
    source: str


@dataclass
class ProficiencyLevel(SemanticDomainObject):
    level: str
    source: str


@dataclass
class Word(SemanticDomainObject):
    text: str
    source: str
    frequencies: List[WordFrequency] = field(default_factory=list)
    pos: List[PartOfSpeech] = field(default_factory=list)
    syncets: List[Synset] = field(default_factory=list)
    proficiency_levels: List[ProficiencyLevel] = field(default_factory=list)
    usage_examples: List[WordUsageExample] = field(default_factory=list)

    def add_frequency(self, freq: WordFrequency):
        for f in self.frequencies:
            assert f.source != freq.source, f"Frequency from {freq.source} already exists"
        self.frequencies.append(freq)
            
    def add_pos(self, pos: PartOfSpeech):
        for p in self.pos:
            assert p.source != pos.source, f"POS from {pos.source} already exists"
        self.pos.append(pos)

    def add_synset(self, synset: Synset):
        for s in self.syncets:
            assert s.source != synset.source, f"Synset from {synset.source} already exists"
        self.syncets.append(synset)

    def add_proficiency_levels(self, level: ProficiencyLevel):
        for l in self.proficiency_levels:
            assert l.source != level.source, f"Level from {level.source} already exists"
        self.proficiency_levels.append(level)

    @classmethod
    def get_field_parsing_exceptions(cls) -> Dict[str, Callable]:
        return {
            "frequencies": lambda frequencies: [WordFrequency.from_dict(f) for f in frequencies],
            "pos": lambda pos: [WordFrequency.from_dict(p) for p in pos],
            "syncets": lambda syncets: [WordFrequency.from_dict(s) for s in syncets],
            "proficiency_levels": lambda proficiency_levels: [WordFrequency.from_dict(l) for l in proficiency_levels]
        }
    
    @classmethod
    def from_original(cls, original_word: str):
        return cls(
            text=original_word,
            source=original_source
        )


@dataclass
class Question(OriginalQuestion):
    words: List[Word] = field(default_factory=list)  # type: ignore
    source: str = ""

    @classmethod
    def get_field_parsing_exceptions(cls) -> Dict[str, Callable]:
        return {
            "words": lambda words: [Word.from_dict(w) for w in words]
        }
    
    @classmethod
    def from_original(cls, original_question: OriginalQuestion):
        return cls(
            num=original_question.num,
            text=original_question.text,
            words=[Word.from_original(w) for w in original_question.words],
            source=original_source
        )
    

@dataclass
class Domain(OriginalDomain):
    questions: List[Question] = field(default_factory=list)  # type: ignore
    source: str = ""

    @classmethod
    def get_field_parsing_exceptions(cls) -> Dict[str, Callable]:
        return {
            "questions": lambda questions: [Question.from_dict({"source": original_source, **q}) for q in questions]
        }
    
    @classmethod
    def from_original(cls, original_domain: OriginalDomain):
        return cls(
            code=original_domain.code,
            title=original_domain.title,
            description=original_domain.description,
            questions=[Question.from_original(q) for q in original_domain.questions],
            source=original_source,
        )


def read_original_domains_from_json(path, as_hierarchy=False) -> Union[List[Domain], DomainNode]:
    domains = original_read_domains_from_json(path, as_hierarchy=False)
    converted_domains = [Domain.from_original(d) for d in domains]  # type: ignore

    if as_hierarchy:
        converted_domains = assemble_hierarchy(converted_domains)  # type: ignore

    return converted_domains


def read_domains_from_json(path, as_hierarchy=False):
    return original_read_domains_from_json(path, as_hierarchy=as_hierarchy, alternative_domain_class=Domain)
    