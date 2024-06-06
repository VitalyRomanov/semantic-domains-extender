from graphlib import TopologicalSorter
from itertools import chain
from typing import OrderedDict

from fastapi import dependencies


# class GrammarParser:
#     def __init__(self) -> None:
#         pass

#     def parse_production(self, production_rule):
#         parts = production_rule.split("->")
#         assert len(parts) == 2
#         head = parts[0].strip()
#         productions = []
#         for production_ in list(map(lambda x: x.strip(), parts[1].split("|"))):
#             productions.append([part.strip() for part in production_.split()])
#         return head, productions
    
#     def is_terminal(self, value):
#         return value.startswith("'") and value.endswith("'")
    
#     def determine_dependencies(self, head, productions):
            
#         seen_terminals = False
#         all_children_are_terminal = True
#         some_children_are_terminal = False
        
#         for child in chain(*productions):
#             child_is_terminal = self.is_terminal(child)
        
#             seen_terminals |= child_is_terminal
#             all_children_are_terminal &= child_is_terminal
#             some_children_are_terminal |= child_is_terminal

#         if some_children_are_terminal:
#             assert all_children_are_terminal

#         if all_children_are_terminal:
#             return head, list(map(lambda x: x.strip("'"), chain(*productions)))
#         return head, set(chain(*productions))

#     def parse(self, grammar):
#         graph = dict()
#         rules = {}
#         for rule in grammar.splitlines():
#             rule = rule.strip()
#             if not len(rule):
#                 continue

#             head, productions = self.parse_production(rule)
#             rules[head] = productions
            
#             head, dependencies = self.determine_dependencies(head, productions)
            
#             if isinstance(dependencies, list):
#                 rules[head] = dependencies

#             if isinstance(dependencies, set):
#                 graph[head] = dependencies

#         sorter = TopologicalSorter(graph)
#         ordered_rules = OrderedDict()
#         for head in sorter.static_order():
#             ordered_rules[head] = rules[head]

#         return ordered_rules
            

class GrammarParser:
    def __init__(self, grammar) -> None:
        self._terminal_nodes = {}
        self._non_terminal_nodes = {}

    @property
    def terminals(self):
        return self._terminal_nodes
    
    @property
    def non_terminals(self):
        return self._non_terminal_nodes

    def parse_production(self, production_rule):
        parts = production_rule.split("->")
        assert len(parts) == 2
        head = parts[0].strip()
        productions = []
        for production_ in list(map(lambda x: x.strip(), parts[1].split("|"))):
            productions.append([part.strip() for part in production_.split()])
        return head, productions
    
    def is_terminal(self, value):
        return value.startswith("'") and value.endswith("'")
    
    def incorporate(self, head, productions):
            
        seen_terminals = False
        all_children_are_terminal = True
        some_children_are_terminal = False
        
        for child in chain(*productions):
            child_is_terminal = self.is_terminal(child)
        
            seen_terminals |= child_is_terminal
            all_children_are_terminal &= child_is_terminal
            some_children_are_terminal |= child_is_terminal

        if some_children_are_terminal:
            assert all_children_are_terminal

        if all_children_are_terminal:
            self._terminal_nodes[head] = list(map(lambda x: x.strip("'"), chain(*productions)))
        else:
            self._non_terminal_nodes[head] = productions

    def parse(self, grammar):
        self._non_terminal_nodes.clear()
        self._terminal_nodes.clear()

        for rule in grammar.splitlines():
            rule = rule.strip()
            if not len(rule):
                continue

            head, productions = self.parse_production(rule)
            self.incorporate(head, productions)

        return self._non_terminal_nodes, self._terminal_nodes


if __name__ == '__main__':
    parser = GrammarParser()
    parser.parse("""
TOP -> S_1__ | S_2__
S_1__ -> VP_1__ | VP_2__ | NP_1__ VP_1__
VP_1__ -> VERB PP_1__ | VERB NP_1__ | VERB NP_2__ | VERB | VERB PP_2__
VERB -> 'used' | 'known' | 'called' | 'made' | 'including' | 'became' | 'based' | 'found' | 'include' | 'began' | 'using' | 'led' | 'considered' | 'published' | 'said' | 'use' | 'become' | 'developed' | 'given' | 'took' | 'following' | 'make' | 'held' | 'included' | 'wrote' | 'established' | 'According' | 'written' | 'released' | 'produced' | 'named' | 'came' | 'having' | 'played' | 'created' | 'described' | 'set' | 'see' | 'built' | 'received' | 'continued' | 'take' | 'won' | 'left' | 'died' | 'seen' | 'followed' | 'formed' | 'introduced' | 'making'
PP_1__ -> ADP NP_1__
ADP -> 'of' | 'in' | 'to' | 'as' | 'for' | 'by' | 'with' | 'on' | 'from' | 'In'
NP_1__ -> DET NOUN | NOUN | PROPN | DET ADJ NOUN
DET -> 'the'
NOUN -> 'time' | '%' | 'years' | 'century' | 'number' | 'part' | 'system' | 'year' | 'people' | 'government' | 'state' | 'city' | 'world' | 'example' | 'use' | 'work' | 'name' | 'country' | 'language' | 'film' | 'life' | 'population' | 'group' | 'power' | 'area' | 'series' | 'period' | 'form' | 'term' | 'war' | 'end' | 'music' | 'day' | '-' | 'death' | 'members' | 'order' | 'water' | 'law' | 'countries' | 'family' | 'game' | 'way' | 'history' | 'development' | 'place' | 'theory' | 'team' | 'point' | 'case' | 'book' | 'production' | 'areas' | 'region' | 'role' | 'line' | 'groups' | 'systems' | 'control' | 'times' | 'process' | 'others' | 'home' | 'season' | 'field' | 'body' | 'word' | 'result' | 'level' | 'languages' | 'forces' | 'age' | 'species' | 'company' | 'land' | 'states' | 'data' | 'men' | 'addition' | 'energy' | 'support' | 'member' | 'service' | 'women' | 'party' | 'children' | 'works' | 'position' | 'terms' | 'version' | 'numbers' | 'school' | 'space' | 'force' | 'parts' | 'son' | 'information' | 'air' | 'side' | 'father' | 'album' | 'island' | 'function' | 'type' | 'days' | 'set' | 'style' | 'research' | 'games' | 'band' | 'design' | 'trade' | 'movement' | 'man' | 'elements' | 'character' | 'rate' | 'range' | 'words' | 'study' | 'evidence' | 'effect' | 'computer' | 'value' | 'structure' | 'culture' | 'person' | 'head' | 'influence'
PROPN -> 'United' | 'New' | 'States' | 'World' | 'War' | 'John' | 'University' | 'National' | 'Europe' | 'U.S.' | 'II' | 'English' | 'May' | 'North' | 'Germany' | 'South' | 'Church' | 'January' | 'France' | 'Union' | 'England' | 'July' | 'York' | 'September' | 'June' | 'March' | 'December' | 'October' | 'God' | 'November' | 'April' | 'City' | 'August' | 'America' | 'India' | 'London' | 'President' | 'King' | 'East' | 'China' | 'International' | 'US' | 'West' | 'American' | 'February' | 'Empire' | 'General' | 'Council' | 'Republic' | 'British' | 'Africa' | 'River' | 'Party' | 'de' | 'House' | 'Kingdom' | 'Army' | 'State' | 'Earth' | 'Canada' | 'William' | 'Britain' | 'League' | 'James' | 'French' | 'Charles' | 'Japan' | 'Great' | 'European' | 'George' | 'Australia' | 'Henry' | 'BC' | 'David' | 'Italy' | 'UK' | 'Court' | 'Central' | 'School' | 'Island' | 'Paul' | 'al' | 'Soviet' | 'Ireland' | 'Israel' | 'Minister' | 'Sea' | 'Act' | 'Robert' | 'Air' | 'Spain' | 'Asia' | 'Royal' | 'Roman' | 'Rome' | 'Russia' | 'College' | 'St.' | 'Jews' | 'Park' | 'Latin' | 'Louis' | 'Old' | 'Paris' | '-' | 'Thomas' | 'California' | 'Congress' | 'Islands' | 'Emperor' | 'Parliament' | 'Middle' | 'Mexico' | 'Egypt' | 'Mary' | 'A' | 'Battle' | 'Jesus' | 'San' | 'Washington' | 'First' | 'Red' | 'Nations' | 'Poland' | 'Richard' | 'Alexander' | 'Saint' | 'Force' | 'Institute' | 'Lord' | 'Black' | 'Society' | 'I' | 'Northern'
ADJ -> 'other' | 'such' | 'first' | 'many' | '-' | 'new' | 'more' | 'same' | 'early' | 'several' | 'most' | 'large' | 'high' | 'different' | 'major' | 'own' | 'second' | 'common' | 'small' | 'American' | 'political' | 'modern' | 'important' | 'British' | 'non' | 'largest' | 'various' | 'German' | 'main' | 'military' | 'single' | 'public' | 'similar' | 'local' | 'late' | 'few' | 'popular' | 'general' | 'last' | 'human' | 'original' | 'national' | 'French' | 'long' | 'economic' | 'former' | 'European' | 'great' | 'international' | 'social' | 'free' | 'Many' | 'possible' | 'only' | 'old' | 'Other' | 'much' | 'natural' | 'low' | 'significant' | 'available' | 'religious' | 'particular' | 'full' | 'traditional' | 'certain' | 'short' | 'higher' | 'next' | 'final' | 'third' | 'present' | 'foreign' | 'central' | 'official' | 'strong' | 'English' | 'able' | 'Most' | 'Roman' | 'Jewish' | 'Greek' | 'total' | 'special' | 'little' | 'independent' | 'lower' | 'specific' | 'current' | 'black' | 'real' | 'ancient' | 'good' | 'white' | 'larger' | 'less' | 'private' | '19th' | 'legal' | 'recent' | 'Christian' | 'open' | 'northern' | 'young' | 'successful' | 'physical' | 'primary' | 'later' | 'Chinese'
NP_2__ -> NP_1__ PP_1__
PP_2__ -> ADP NP_2__
VP_2__ -> AUX VP_1__ | PART VP_1__
AUX -> 'is' | 'was' | 'are'
PART -> 'to'
S_2__ -> VP_3__ | NP_1__ VP_3__ | NP_1__ VP_3__ PUNCT | NP_1__ VP_2__ PUNCT | VP_2__ | VP_4__ | NP_1__ VP_2__ | NP_1__ VP_4__ PUNCT | NP_1__ VP_4__
VP_3__ -> AUX VP_2__ | VERB S_1__ | PART VP_2__ | VERB SBAR_1__
SBAR_1__ -> WHNP_1__ S_1__ | SCONJ S_1__
WHNP_1__ -> PRON
PRON -> 'his' | 'it' | 'he' | 'that' | 'their' | 'its' | 'who' | 'they' | 'It' | 'He' | 'her' | 'him' | 'there' | 'them'
SCONJ -> 'that' | 'when'
PUNCT -> ',' | '.'
VP_4__ -> AUX VP_3__ | PART VP_3__ | VERB S_1__ | VERB SBAR_1__
                 """)