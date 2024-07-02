from calendar import c
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
    synsets: List[Synset] = field(default_factory=list)
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
        for s in self.synsets:
            assert s.source != synset.source, f"Synset from {synset.source} already exists"
        self.synsets.append(synset)

    def add_proficiency_level(self, level: ProficiencyLevel):
        for l in self.proficiency_levels:
            assert l.source != level.source, f"Level from {level.source} already exists"
        self.proficiency_levels.append(level)

    def add_usage_example(self, example: WordUsageExample):
        self.usage_examples.append(example)

    @classmethod
    def get_field_parsing_exceptions(cls) -> Dict[str, Callable]:
        return {
            "frequencies": lambda frequencies: [WordFrequency.from_dict(f) for f in frequencies],
            "pos": lambda pos: [PartOfSpeech.from_dict(p) for p in pos],
            "synsets": lambda synsets: [Synset.from_dict(s) for s in synsets],
            "proficiency_levels": lambda proficiency_levels: [ProficiencyLevel.from_dict(l) for l in proficiency_levels]
        }
    
    @classmethod
    def from_original(cls, original_word: str):
        return cls(
            text=original_word,
            source=original_source
        )
    
    def get_proficiency_level(self, source: str) -> Union[ProficiencyLevel, None]:
        for level in self.proficiency_levels:
            if level.source == source:
                return level
        return None
    
    def get_frequency(self, frequency_source: str) -> Union[WordFrequency, None]:
        for freq in self.frequencies:
            if freq.source == frequency_source:
                return freq
        return None
    
    def get_pos(self, pos_source: str) -> Union[PartOfSpeech, None]:
        for pos in self.pos:
            if pos.source == pos_source:
                return pos
        return None


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

    def get_levels_distribution(self, proficiency_level_source) -> Dict[str, int]:
        distribution = dict()

        for question in self.questions:
            for word in question.words:
                proficiency_level = word.get_proficiency_level(proficiency_level_source)
                if proficiency_level is not None:
                    if proficiency_level.level not in distribution:
                        distribution[proficiency_level.level] = 1
                    else:
                        distribution[proficiency_level.level] += 1
                    
        return distribution
    
    def get_avg_frequency(self, source, level=None, proficiency_level_source=None) -> float:
        frequencies = []
        for question in self.questions:
            for word in question.words:
                freq = word.get_frequency(source)
                if freq is not None:
                    if level is not None:
                        assert proficiency_level_source is not None
                        word_level = word.get_proficiency_level(proficiency_level_source)
                        if word_level is None or word_level.level != level:
                            continue

                    if freq.source == source:
                        frequencies.append(freq.freq)
        
        return sum(frequencies) / len(frequencies) if frequencies else 0.


def read_original_domains_from_json(path) -> List[Domain]:
    domains = original_read_domains_from_json(path)
    converted_domains = [Domain.from_original(d) for d in domains]

    return converted_domains


def read_domains_from_json(path, ) -> List[Domain]:
    return original_read_domains_from_json(path, alternative_domain_class=Domain)


def read_domain_hierarchy(path, read_original: bool = False) -> DomainNode:
    if read_original:
        domains = read_original_domains_from_json(path)
    else:
        domains = read_domains_from_json(path)

    return assemble_hierarchy(domains)
