import argparse
from collections import defaultdict
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


def main(args):

    levels = defaultdict(set)
    nlp = get_spacy_tokenizer()

    for level in ["A1", "A2", "B1", "B2", "C1"]:
        list_file = args.lists_dir / f"{level}.txt"
        for line in list_file.read_text().splitlines():
            doc = nlp(line)
            for token in doc:
                if token.text.strip() == "":
                    continue
                levels[level].add(token.text)
                # if token.is_alpha and token.is_stop == False and token.text.strip() != "":
                #     levels[level].add(token.text)
                #     levels[level].add(token.lemma_)

    for ind, level in ["A1", "A2", "B1", "B2", "C1"]:
        for ind_, level_ in ["A1", "A2", "B1", "B2", "C1"]:
            if ind >= ind_:
                continue
            levels[level_] = levels[level_] - levels[level_]

    

    levels = {
        level: sorted(map(lambda word: (word, None), levels[level])) for level in ["A1", "A2", "B1", "B2", "C1"]
    }

    dump_word_levels(levels, args.output_path, "https://www.esl-lounge.com/student/reference/a1-cefr-vocabulary-word-list.php")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lists_dir", type=Path, help="Path to the input file")
    parser.add_argument("output_path", type=Path, help="Path to the output file")

    args = parser.parse_args()
    main(args)