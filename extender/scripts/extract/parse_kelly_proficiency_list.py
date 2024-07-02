import argparse
from collections import defaultdict
import csv
import datetime
import json
from pathlib import Path

from extender.parsing.tokenizers import get_spacy_tokenizer


def dump_word_levels(word_levels, output_path, source):
    word_levels = {
        "source": source,
        "date": datetime.datetime.now().isoformat(),
        "levels": word_levels
    }

    with open(output_path, "w") as file:
        json.dump(word_levels, file, indent=4)


def read_word_levels(path):
    pos_map = {
        "Determiner": "DET",
        
        "Verb": "VERB",
        
        "Preposition": "PREP",
        "preposition": "PREP",
        
        "Conjunction": "CONJ",
        
        "Miscellaneous": "MISC",
        
        "Adjective": "ADJ",
        
        "Pronoun": "PRON",
        "pronoun": "PRON",
        
        "Modal verb": "VERB",
        "Modal Verb": "VERB",
        
        "Adverb": "ADV",
        "adverb": "ADV",
        
        "Number": "NUM",
        "number": "NUM",
        
        "Noun": "NOUN",
        "noun": "NOUN",
        
        "Exclamation": "",
        "exclamation": "",
        
        "Abbreviation": "",
        "": ""
        
    }

    # words = defaultdict(list)
    levels_ = defaultdict(set)

    with open(path, "r") as levels_csv:
        levels = csv.reader(levels_csv)
        for ind, row in enumerate(levels):
            if ind == 0:
                continue    
            word, pos, level = row[0].strip(), row[1].strip(), row[2].strip()
            real_pos = pos_map[pos]
            levels_[level].add((word, real_pos))
            # words[row[0]].append((real_pos, row[2]))

    for ind, level in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        for ind_, level_ in ["A1", "A2", "B1", "B2", "C1", "C2"]:
            if ind >= ind_:
                continue
            levels_[level_] = levels_[level_] - levels_[level_]

    return {level: sorted(levels_[level], key=lambda x: (x[0])) for level in ["A1", "A2", "B1", "B2", "C1", "C2"]}


def main(args):

    levels= read_word_levels(args.list_path)

    dump_word_levels(levels, args.output_path, "wordcyclopedia/Kelly")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("list_path", type=Path, help="Path to the input file")
    parser.add_argument("output_path", type=Path, help="Path to the output file")

    args = parser.parse_args()
    main(args)