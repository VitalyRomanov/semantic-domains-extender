import argparse
import json
from pathlib import Path
from typing import Dict, Optional, Union

from tqdm import tqdm
from semantic_domains.rwc_parser import dump_domains_to_json

from extender.data.model import WordFrequency, WordFrequency, read_domains_from_json


def read_frequencies(path: Path) -> Dict:
    with open(path, "r") as frequencies_json:
        json_data = json.load(frequencies_json)

    json_data["counts"] = dict(json_data["counts"])

    return json_data


def resolve_pos(word, source) -> Optional[str]:
    existing_pos = [pos.tag for pos in word.pos if pos.source == source]
    if len(existing_pos) == 0:
        return None
    return existing_pos[0]  # only one POS per word from one source


def resolve_frequency(word, frequencies, require_pos=False, pos_source=None) -> Optional[int]:
    if require_pos is True:
        word_ = [word.text, resolve_pos(word, pos_source)]
    else:
        word_ = word.text

    frequency = frequencies["counts"].get(word_, None)

    return frequency


def main(args):
    domains = read_domains_from_json(args.domains_path)
    
    frequencies = read_frequencies(args.frequencies_path)
    
    for domain in tqdm(domains):
        for question in domain.questions:
            for word in question.words:
                frequency = resolve_frequency(word, frequencies, require_pos=False)

                if frequency is not None:
                    word.add_frequency(WordFrequency(frequency, frequencies["source"]))

    dump_domains_to_json(domains, args.output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domains_path", type=Path, help="Path to the domains json file")
    parser.add_argument("frequencies_path", type=Path, help="")
    parser.add_argument("output_path", type=Path, help="")
    
    args = parser.parse_args()
    main(args)
