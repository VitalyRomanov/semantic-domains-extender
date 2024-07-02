import argparse
import json
from pathlib import Path

from tqdm import tqdm
from semantic_domains.rwc_parser import dump_domains_to_json

from extender.data.model import ProficiencyLevel, Word, read_domains_from_json


def read_word_levels(path: Path):
    data = json.load(path.open("r"))
    for level in data["levels"]:
        data["levels"][level] = set(map(tuple, data["levels"][level]))
    return data


def resolve_pos(word, source):
    existing_pos = [pos.tag for pos in word.pos if pos.source == source]
    if len(existing_pos) == 0:
        return None
    return existing_pos[0]  # only one POS per word from one source


def resolve_level(word, levels, require_pos=False, pos_source=None):
    if require_pos is True:
        word_ = (word.text, resolve_pos(word, pos_source))
    else:
        word_ = (word.text, None)

    levels_ = [level for level, level_words in levels["levels"].items() if word_ in level_words]

    if len(levels_) == 0:
        level = None
    else:
        level = levels_[0]

    return level


def main(args):
    domains = read_domains_from_json(args.domains_path)
    
    levels = read_word_levels(args.levels_path)
    
    for domain in tqdm(domains):
        for question in domain.questions:
            word: Word
            for word in question.words:
                level = resolve_level(word, levels, require_pos=True, pos_source=args.pos_source)
                
                if level is not None:
                    word.add_proficiency_level(ProficiencyLevel(level, levels["source"]))

    dump_domains_to_json(domains, args.output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domains_path", type=Path, help="Path to the domains json file")
    parser.add_argument("levels_path", type=Path, help="")
    parser.add_argument("pos_source", type=str, help="")
    parser.add_argument("output_path", type=Path, help="")
    
    args = parser.parse_args()
    main(args)
