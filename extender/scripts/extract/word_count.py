import argparse
import datetime
import json
from multiprocessing import Pool
from pathlib import Path
import sys

from extender.parsing.tokenizers import get_spacy_tokenizer


def compute_word_counts(text):
    counts = dict()

    nlp = get_spacy_tokenizer()
    nlp.max_length = len(text) + 1
    doc = nlp(text)
    for token in doc:
        if token.text in counts:
            counts[token.text] += 1
        else:
            counts[token.text] = 1
        
    return counts


def dump_word_count(counts, output_path, count_source, min_count=1):
    dump = {
        "source": count_source,
        "date": datetime.datetime.now().isoformat(),
        "counts": list(filter(
            lambda item: item[1] >= min_count,
            sorted(counts.items(), key=lambda item: item[1], reverse=True),
        )),
    }
    with open(output_path, "w") as file:
        json.dump(dump, file, indent=4)


def main(args):
    word_counts = dict()

    with Pool() as pool:
        for counts in pool.imap(compute_word_counts, sys.stdin):
            for word, count in counts.items():
                if word in word_counts:
                    word_counts[word] += count
                else:
                    word_counts[word] = count

    dump_word_count(
        word_counts, 
        args.counts_output_path, 
        args.counts_source,
        min_count=args.min_counts,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("counts_output_path", type=Path)
    parser.add_argument("counts_source", type=str)
    parser.add_argument("--min_counts", default=1, type=int)
    args = parser.parse_args()

    main(args)
