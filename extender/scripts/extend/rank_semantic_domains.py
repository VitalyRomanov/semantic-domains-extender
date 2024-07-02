import argparse
from pathlib import Path


from extender.data.model import read_domains_from_json


def main(args):
    domains = read_domains_from_json(args.domains_path)
    
    domains_data = []
    for domain in domains:
        level_dist = domain.get_levels_distribution(args.levels_source)
        for level in level_dist:
            level_freq = level_dist[level]
            top_freq = domain.get_avg_frequency(args.frequencies_source, level=level, proficiency_level_source=args.levels_source)
            domain_data = (domain.code, domain.title, level, level_freq, top_freq)
            domains_data.append(domain_data)

    domains_data.sort(key=lambda x: x[-1], reverse=True)  # by top frequency
    domains_data.sort(key=lambda x: x[-2], reverse=True)  # by frequencies
    domains_data.sort(key=lambda x: x[-3])  # by top level
    
    with open(args.output_path, "w", encoding="utf-8") as f:
        for domain_data in domains_data:
            record = "\t".join(map(str, domain_data))
            f.write(f"{record}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domains_path", type=Path, help="Path to the domains json file")
    parser.add_argument("frequencies_source", type=str, help="")
    parser.add_argument("levels_source", type=str, help="")
    parser.add_argument("output_path", type=Path, help="")
    
    args = parser.parse_args()
    main(args)
