import argparse

from semantic_domains.rwc_parser import dump_domains_to_json

from extender.data.model import read_original_domains_from_json, read_domains_from_json


def main(args):
    converted_domains = read_original_domains_from_json(args.domains)
    dump_domains_to_json(converted_domains, args.output_path)
    imported_domains = read_domains_from_json(args.output_path)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domains", help="Path to the domains json file")
    parser.add_argument("output_path", help="")

    args = parser.parse_args()
    main(args)
    