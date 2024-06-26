from functools import lru_cache
import guidance
from guidance import one_or_more, select, one_or_more, capture, with_temperature

from extender.grammar.parser import GrammarParser
# stateless=True indicates this function does not depend on LLM generations

# @lru_cache
# def split_terms(terms_str):
#     return list(map(lambda x: x.strip().strip("'"), terms_str.split('|')))

# @guidance(stateless=True)
# def sep(lm, temperature=0.0):
#     return lm + with_temperature(select([' ']), temperature=temperature)

# @guidance(stateless=True)
# def noun(lm, temperature=0.0):
#     options = "'time' | '%' | 'years' | 'century' | 'number' | 'part' | 'system' | 'year' | 'people' | 'government' | 'state' | 'city' | 'world' | 'example' | 'use' | 'work' | 'name' | 'country' | 'language' | 'film' | 'life' | 'population' | 'group' | 'power' | 'area' | 'series' | 'period' | 'form' | 'term' | 'war' | 'end' | 'music' | 'day' | 'death' | 'members' | 'order' | 'water' | 'law' | 'countries' | 'family' | 'game' | 'way' | 'history' | 'development' | 'place' | 'theory' | 'team' | 'point' | 'case' | 'book' | 'production' | 'areas' | 'region' | 'role' | 'line' | 'groups' | 'systems' | 'control' | 'times' | 'process' | 'others' | 'home' | 'season' | 'field' | 'body' | 'word' | 'result' | 'level' | 'languages' | 'forces' | 'age' | 'species' | 'company' | 'land' | 'states' | 'data' | 'men' | 'addition' | 'energy' | 'support' | 'member' | 'service' | 'women' | 'party' | 'children' | 'works' | 'position' | 'terms' | 'version' | 'numbers' | 'school' | 'space' | 'force' | 'parts' | 'son' | 'information' | 'air' | 'side' | 'father' | 'album' | 'island' | 'function' | 'type' | 'days' | 'set' | 'style' | 'research' | 'games' | 'band' | 'design' | 'trade' | 'movement' | 'man' | 'elements' | 'character' | 'rate' | 'range' | 'words' | 'study' | 'evidence' | 'effect' | 'computer' | 'value' | 'structure' | 'culture' | 'person' | 'head' | 'influence' | 'source' | 'art' | 'rights' | 'program' | 'market' | 'industry' | 'class' | 'army' | 'films' | 'cases' | 'education' | 'science' | 'capital' | 'months' | 'hand' | 'forms' | 'size' | 'services' | 'model' | 'title' | 'majority' | 'economy' | 'community' | 'aircraft' | 'fact' | 'television' | 'food' | 'rule' | 'nature' | 'growth' | 'self' | 'story' | 'events' | 'record' | 'cities' | 'today' | 'court' | 'action' | 'election' | 'policy' | 'north' | 'types' | 'players' | 'town' | 'effects' | 'success' | 'business' | 'base' | 'church' | 'network' | 'interest' | 'player' | 'books' | 'king' | 'president' | 'problems' | 'mother' | 'problem' | 'schools' | 'material' | 'surface' | 'view' | 'practice' | 'students' | 'office' | 'percent' | 'conditions' | 'companies' | 'light' | 'names' | 'method' | 'changes' | 'performance' | 'concept' | 'lines' | 'idea' | 'change' | 'products' | 'variety' | 'half' | 'wife' | 'show' | 'society' | 'project' | 'basis' | 'construction' | 'relations' | 'right' | 'characters' | 'metal' | 'units' | 'house' | 'song' | 'era' | 'sources' | 'cell' | 'points' | 'software' | 'tradition' | 'relationship' | 'site' | 'territory' | 'list' | 'scale' | 'oil' | 'radio' | 'pressure' | 'sea' | 'centuries' | 'length' | 'health' | 'regions' | 'speed' | 'career' | 'product' | 'code' | 'media' | 'status' | 'technology' | 'event' | 'results' | 'methods' | 'gas' | 'laws' | 'letter' | 'levels' | 'islands' | 'studies' | 'mass' | 'troops' | 'response' | 'money' | 'functions' | 'rules' | 'ground' | 'operations' | 'cells' | 'building' | 'release' | 'leader' | 'rock' | 'degree' | 'independence' | 'stage' | 'text' | 'sense' | 'amount' | 'element' | 'attack' | 'knowledge' | 'center'"
#     return lm + sep(temperature=temperature) + with_temperature(select(split_terms(options)), temperature=temperature)

# @guidance(stateless=True)
# def verb(lm, temperature=0.0):
#     return lm + sep(temperature=temperature) + with_temperature(select(['used', 'known', 'called', 'made', 'including', 'became', 'based', 'found', 'include', 'began', 'using', 'led', 'considered', 'published', 'said', 'use', 'become', 'developed', 'given', 'took', 'following', 'make', 'held', 'included', 'wrote', 'established', 'According', 'written', 'released', 'produced', 'named', 'came', 'having', 'played', 'created', 'described', 'set', 'see', 'built', 'received', 'continued', 'take', 'won', 'left', 'died', 'seen', 'followed', 'formed', 'introduced', 'making', 'born', 'according', 'located', 'remained', 'referred', 'taken', 'lost', 'increased', 'went', 'provided', 'allowed', 'moved', 'provide', 'required', 'started', 'defined', 'gave', 'includes', 'believed', 'appeared', 'leading', 'form', 'associated', 'brought', 'announced', 'sent', 'returned', 'designed', 'served', 'founded', 'related', 'saw', 'stated', 'elected', 'caused', 'produce', 'replaced', 'reported', 'recorded', 'come', 'proposed', 'thought', 'added', 'working', 'involved', 'put', 'supported', 'create', 'reached', 'adopted', 'allow', 'claimed', 'performed', 'sold', 'worked', 'play', 'uses', 'discovered', 'killed', 'give', 'divided']), temperature=temperature)

# @guidance(stateless=True)
# def adp(lm, temperature=0.0):
#     return lm + sep(temperature=temperature) + with_temperature(select(['of', 'in', 'to', 'as', 'for', 'by', 'with', 'on', 'from',]), temperature=temperature)

# @guidance(stateless=True)
# def det(lm, temperature=0.0):
#     return lm + sep(temperature=temperature) + with_temperature(select(['the', "a", 'an']), temperature=temperature)

# @guidance(stateless=True)
# def propn(lm, temperature=0.0):
#     return lm + sep(temperature=temperature) + with_temperature(select(['United', 'New', 'States', 'World', 'War', 'John', 'University', 'National', 'Europe', 'U.S.', 'II', 'English', 'May', 'North', 'Germany', 'South', 'Church', 'January', 'France', 'Union', 'England', 'July', 'York', 'September', 'June', 'March', 'December', 'October', 'God', 'November', 'April', 'City', 'August', 'America', 'India', 'London', 'President', 'King', 'East', 'China', 'International', 'US', 'West', 'American', 'February', 'Empire', 'General', 'Council', 'Republic', 'British', 'Africa', 'River', 'Party', 'de', 'House', 'Kingdom', 'Army', 'State', 'Earth', 'Canada', 'William', 'Britain', 'League', 'James', 'French', 'Charles', 'Japan', 'Great', 'European', 'George', 'Australia', 'Henry', 'BC', 'David', 'Italy', 'UK', 'Court', 'Central', 'School', 'Island', 'Paul', 'al', 'Soviet', 'Ireland', 'Israel', 'Minister', 'Sea', 'Act', 'Robert', 'Air', 'Spain', 'Asia', 'Royal', 'Roman', 'Rome', 'Russia', 'College', 'St.', 'Jews', 'Park', 'Latin', 'Louis', 'Old', 'Paris', 'Thomas', 'California', 'Congress', 'Islands', 'Emperor', 'Parliament', 'Middle', 'Mexico', 'Egypt', 'Mary', 'Battle', 'Jesus', 'San', 'Washington', 'First', 'Red', 'Nations', 'Poland', 'Richard', 'Alexander', 'Saint', 'Force', 'Institute', 'Lord', 'Black', 'Society', 'I', 'Northern', 'Company', 'Christ', 'III', 'Eastern', 'Catholic', 'Award', 'Hall', 'Navy', 'German', 'Government', 'Peter', 'Americans', 'Greek', 'Lake', 'Pacific', 'Academy', 'Western', 'Association', 'Prime', 'County', 'Museum', 'Street', 'Day', 'Chicago', 'Book', 'Grand', 'Committee', 'Cup', 'Center', 'Smith', 'Holy', 'Bank', 'Netherlands', 'Revolution', 'Joseph', 'Greece', 'Zealand', 'Michael', 'Martin', 'Department', 'Age', 'White', 'Christianity', 'Scotland', 'Orthodox', 'High', 'Berlin', 'Second', 'Christian', 'La', 'Korea', 'Treaty', 'Civil', 'Assembly', 'Commission', 'Queen', 'Sun', 'Los', 'Al', 'Bay', 'Man', 'Pope', 'Edward', 'Iran', 'Group', 'Best', 'Prince', 'Christians', 'Bible', 'Brown', 'X', 'Spanish', 'Columbia', 'Christmas', 'Iraq', 'Sir', 'Afghanistan', 'Hitler', 'Supreme', 'Apple', 'Jerusalem', 'Southern', 'Airport', 'System', 'von', 'J.', 'Law', 'Finland', 'EU', 'Lincoln', 'Senate', 'Jean', 'Atlantic', 'Islam', 'BBC', 'Angeles', 'Duke', 'Secretary', 'Pakistan', 'Constitution', 'St', 'African', 'Jackson', 'Hungary', 'Service', 'Science', 'Windows', 'DNA', 'Kong', 'People', 'Festival', 'Microsoft', 'Ottoman', 'GDP', 'Jones', 'Office', 'Bill', 'Hebrew', 'De', 'Club', 'Federal', 'Muslims', 'El', 'Moon', 'Division', 'Forces', 'Dutch', 'Wales', 'Times', 'Valley', 'Brazil', 'Apollo', 'Prize', 'Governor', 'Sweden', 'Johnson', 'UN', 'Dr.', 'Lee', 'IBM', 'Ocean', 'Mark', 'C', 'Austria', 'Texas', 'Mediterranean', 'Film', 'Elizabeth', 'Arthur', 'Davis', 'Convention', 'Boston', 'Music', 'Chinese', 'Jersey', 'Series', 'Research', 'Albert', 'Hill', 'Time', 'Game', 'Indian', 'District', 'B', 'Young', 'Green', 'Corporation', 'Francisco', 'Bush', 'Hollywood', 'Turkey', 'Le', 'Hong', 'Norway', 'Conference', 'Coast', 'Indonesia', 'NFL', 'Denmark', 'Board', 'Democratic', 'Frank', 'Testament', 'Nobel', 'Big', 'Gulf', 'Commonwealth', 'Security', 'Library', 'Chief', 'Justice', 'Star', 'Muhammad', 'Rock', 'Germans']), temperature=temperature)

# @guidance(stateless=True)
# def pron(lm, temperature=0.0):
#     return lm + sep(temperature=temperature) + with_temperature(select(['I', 'It', 'it', 'He', 'he', 'She', 'she', 'They', 'they', 'We', 'we']), temperature=temperature)

# @guidance(stateless=True)
# def aux(lm, temperature=0.0):
#     return lm + sep(temperature=temperature) + with_temperature(select(['is', 'are', ]), temperature=temperature)

# @guidance(stateless=True)
# def adj(lm, temperature=0.0):
#     return lm + sep(temperature=temperature) + with_temperature(select(['other', 'such', 'first', 'many', '-', 'new', 'more', 'same', 'early', 'several', 'most', 'large', 'high', 'different', 'major', 'own', 'second', 'common', 'small', 'American', 'political', 'modern', 'important', 'British', 'non', 'largest', 'various', 'German', 'main', 'military', 'single', 'public', 'similar', 'local', 'late', 'few', 'popular', 'general', 'last', 'human', 'original', 'national', 'French', 'long', 'economic', 'former', 'European', 'great', 'international', 'social', 'free', 'Many', 'possible', 'only', 'old', 'Other', 'much', 'natural', 'low', 'significant', 'available', 'religious', 'particular', 'full', 'traditional', 'certain', 'short', 'higher', 'next', 'final', 'third', 'present', 'foreign', 'central', 'official', 'strong', 'English', 'able', 'Most', 'Roman', 'Jewish', 'Greek', 'total', 'special', 'little', 'independent', 'lower', 'specific', 'current', 'black', 'real', 'ancient', 'good', 'white', 'larger', 'less', 'private', '19th', 'legal', 'recent', 'Christian', 'open', 'northern', 'young', 'successful', 'physical', 'primary', 'later', 'Chinese']), temperature=temperature)

# @guidance(stateless=True)
# def punct(lm, temperature=0.0):
#     return lm + with_temperature(select(["."]), temperature=temperature)
 

# @guidance(stateless=True)
# def top(lm, temperature=0.0):
#     return lm + capture(with_temperature(select([s_1__(temperature=temperature)]), temperature=temperature), "TOP")

# @guidance(stateless=True)
# def s_1__(lm, temperature=0.0):
#     return lm + capture(with_temperature(select([np_1__(temperature=temperature) + vp_1__(temperature=temperature), vp_1__(temperature=temperature), vp_2__(temperature=temperature)]) + punct(temperature=temperature), temperature=temperature), "S1")

# @guidance(stateless=True)
# def np_1__(lm, temperature=0.0):
#     return lm + capture(with_temperature(select([det(temperature=temperature) + noun(temperature=temperature), noun(temperature=temperature), one_or_more(propn(temperature=temperature)), det(temperature=temperature) + adj(temperature=temperature) + noun(temperature=temperature)]), temperature=temperature), "NP1")

# @guidance(stateless=True)
# def np_2__(lm, temperature=0.0):
#     return lm + capture(with_temperature(select([np_1__(temperature=temperature) + pp_1__(temperature=temperature)]), temperature=temperature), "NP2")

# @guidance(stateless=True)
# def vp_1__(lm, temperature=0.0):
#     return lm + capture(with_temperature(select([verb(temperature=temperature) + pp_1__(temperature=temperature), verb(temperature=temperature) + np_1__(temperature=temperature), verb(temperature=temperature) + np_2__(temperature=temperature)]), temperature=temperature), "VP1")

# @guidance(stateless=True)
# def vp_2__(lm, temperature=0.0):
#     return lm + capture(with_temperature(select([aux(temperature=temperature) + vp_1__(temperature=temperature)]), temperature=temperature), "VP2")

# @guidance(stateless=True)
# def pp_1__(lm, temperature=0.0):
#     return lm + capture(with_temperature(select([adp(temperature=temperature) + np_1__(temperature=temperature)]), temperature=temperature), "PP1")

@guidance(stateless=True)  # type: ignore
def select_with_temperature(lm, options, temperature=0.0):
    return lm + with_temperature(select(options), temperature=temperature)


class GuidanceGrammar:
    def __init__(self, grammar: str) -> None:
        parser = GrammarParser(grammar)
        self._non_terminals, self._terminals = parser.parse(grammar)
        self._terminals["sep"] = [' ']
        self._terminals["eos"] = ['.', '?', '!']
        # self._terminals = {
        #     "sep": [' '],
        #     "noun": ['time', '%', 'years', 'century', 'number', 'part', 'system', 'year', 'people', 'government', 'state', 'city', 'world', 'example', 'use', 'work', 'name', 'country', 'language', 'film', 'life', 'population', 'group', 'power', 'area', 'series', 'period', 'form', 'term', 'war', 'end', 'music', 'day', 'death', 'members', 'order', 'water', 'law', 'countries', 'family', 'game', 'way', 'history', 'development', 'place', 'theory', 'team', 'point', 'case', 'book', 'production', 'areas', 'region', 'role', 'line', 'groups', 'systems', 'control', 'times', 'process', 'others', 'home', 'season', 'field', 'body', 'word', 'result', 'level', 'languages', 'forces', 'age', 'species', 'company', 'land', 'states', 'data', 'men', 'addition', 'energy', 'support', 'member', 'service', 'women', 'party', 'children', 'works', 'position', 'terms', 'version', 'numbers', 'school', 'space', 'force', 'parts', 'son', 'information', 'air', 'side', 'father', 'album', 'island', 'function', 'type', 'days', 'set', 'style', 'research', 'games', 'band', 'design', 'trade', 'movement', 'man', 'elements', 'character', 'rate', 'range', 'words', 'study', 'evidence', 'effect', 'computer', 'value', 'structure', 'culture', 'person', 'head', 'influence', 'source', 'art', 'rights', 'program', 'market', 'industry', 'class', 'army', 'films', 'cases', 'education', 'science', 'capital', 'months', 'hand', 'forms', 'size', 'services', 'model', 'title', 'majority', 'economy', 'community', 'aircraft', 'fact', 'television', 'food', 'rule', 'nature', 'growth', 'self', 'story', 'events', 'record', 'cities', 'today', 'court', 'action', 'election', 'policy', 'north', 'types', 'players', 'town', 'effects', 'success', 'business', 'base', 'church', 'network', 'interest', 'player', 'books', 'king', 'president', 'problems', 'mother', 'problem', 'schools', 'material', 'surface', 'view', 'practice', 'students', 'office', 'percent', 'conditions', 'companies', 'light', 'names', 'method', 'changes', 'performance', 'concept', 'lines', 'idea', 'change', 'products', 'variety', 'half', 'wife', 'show', 'society', 'project', 'basis', 'construction', 'relations', 'right', 'characters', 'metal', 'units', 'house', 'song', 'era', 'sources', 'cell', 'points', 'software', 'tradition', 'relationship', 'site', 'territory', 'list', 'scale', 'oil', 'radio', 'pressure', 'sea', 'centuries', 'length', 'health', 'regions', 'speed', 'career', 'product', 'code', 'media', 'status', 'technology', 'event', 'results', 'methods', 'gas', 'laws', 'letter', 'levels', 'islands', 'studies', 'mass', 'troops', 'response', 'money', 'functions', 'rules', 'ground', 'operations', 'cells', 'building', 'release', 'leader', 'rock', 'degree', 'independence', 'stage', 'text', 'sense', 'amount', 'element', 'attack', 'knowledge', 'center'],
        #     "verb": ['used', 'known', 'called', 'made', 'including', 'became', 'based', 'found', 'include', 'began', 'using', 'led', 'considered', 'published', 'said', 'use', 'become', 'developed', 'given', 'took', 'following', 'make', 'held', 'included', 'wrote', 'established', 'According', 'written', 'released', 'produced', 'named', 'came', 'having', 'played', 'created', 'described', 'set', 'see', 'built', 'received', 'continued', 'take', 'won', 'left', 'died', 'seen', 'followed', 'formed', 'introduced', 'making', 'born', 'according', 'located', 'remained', 'referred', 'taken', 'lost', 'increased', 'went', 'provided', 'allowed', 'moved', 'provide', 'required', 'started', 'defined', 'gave', 'includes', 'believed', 'appeared', 'leading', 'form', 'associated', 'brought', 'announced', 'sent', 'returned', 'designed', 'served', 'founded', 'related', 'saw', 'stated', 'elected', 'caused', 'produce', 'replaced', 'reported', 'recorded', 'come', 'proposed', 'thought', 'added', 'working', 'involved', 'put', 'supported', 'create', 'reached', 'adopted', 'allow', 'claimed', 'performed', 'sold', 'worked', 'play', 'uses', 'discovered', 'killed', 'give', 'divided'],
        #     "adp": ['of', 'in', 'to', 'as', 'for', 'by', 'with', 'on', 'from',],
        #     "det": ['the', "a", 'an'],
        #     "propn": ['United', 'New', 'States', 'World', 'War', 'John', 'University', 'National', 'Europe', 'U.S.', 'II', 'English', 'May', 'North', 'Germany', 'South', 'Church', 'January', 'France', 'Union', 'England', 'July', 'York', 'September', 'June', 'March', 'December', 'October', 'God', 'November', 'April', 'City', 'August', 'America', 'India', 'London', 'President', 'King', 'East', 'China', 'International', 'US', 'West', 'American', 'February', 'Empire', 'General', 'Council', 'Republic', 'British', 'Africa', 'River', 'Party', 'de', 'House', 'Kingdom', 'Army', 'State', 'Earth', 'Canada', 'William', 'Britain', 'League', 'James', 'French', 'Charles', 'Japan', 'Great', 'European', 'George', 'Australia', 'Henry', 'BC', 'David', 'Italy', 'UK', 'Court', 'Central', 'School', 'Island', 'Paul', 'al', 'Soviet', 'Ireland', 'Israel', 'Minister', 'Sea', 'Act', 'Robert', 'Air', 'Spain', 'Asia', 'Royal', 'Roman', 'Rome', 'Russia', 'College', 'St.', 'Jews', 'Park', 'Latin', 'Louis', 'Old', 'Paris', 'Thomas', 'California', 'Congress', 'Islands', 'Emperor', 'Parliament', 'Middle', 'Mexico', 'Egypt', 'Mary', 'Battle', 'Jesus', 'San', 'Washington', 'First', 'Red', 'Nations', 'Poland', 'Richard', 'Alexander', 'Saint', 'Force', 'Institute', 'Lord', 'Black', 'Society', 'I', 'Northern', 'Company', 'Christ', 'III', 'Eastern', 'Catholic', 'Award', 'Hall', 'Navy', 'German', 'Government', 'Peter', 'Americans', 'Greek', 'Lake', 'Pacific', 'Academy', 'Western', 'Association', 'Prime', 'County', 'Museum', 'Street', 'Day', 'Chicago', 'Book', 'Grand', 'Committee', 'Cup', 'Center', 'Smith', 'Holy', 'Bank', 'Netherlands', 'Revolution', 'Joseph', 'Greece', 'Zealand', 'Michael', 'Martin', 'Department', 'Age', 'White', 'Christianity', 'Scotland', 'Orthodox', 'High', 'Berlin', 'Second', 'Christian', 'La', 'Korea', 'Treaty', 'Civil', 'Assembly', 'Commission', 'Queen', 'Sun', 'Los', 'Al', 'Bay', 'Man', 'Pope', 'Edward', 'Iran', 'Group', 'Best', 'Prince', 'Christians', 'Bible', 'Brown', 'X', 'Spanish', 'Columbia', 'Christmas', 'Iraq', 'Sir', 'Afghanistan', 'Hitler', 'Supreme', 'Apple', 'Jerusalem', 'Southern', 'Airport', 'System', 'von', 'J.', 'Law', 'Finland', 'EU', 'Lincoln', 'Senate', 'Jean', 'Atlantic', 'Islam', 'BBC', 'Angeles', 'Duke', 'Secretary', 'Pakistan', 'Constitution', 'St', 'African', 'Jackson', 'Hungary', 'Service', 'Science', 'Windows', 'DNA', 'Kong', 'People', 'Festival', 'Microsoft', 'Ottoman', 'GDP', 'Jones', 'Office', 'Bill', 'Hebrew', 'De', 'Club', 'Federal', 'Muslims', 'El', 'Moon', 'Division', 'Forces', 'Dutch', 'Wales', 'Times', 'Valley', 'Brazil', 'Apollo', 'Prize', 'Governor', 'Sweden', 'Johnson', 'UN', 'Dr.', 'Lee', 'IBM', 'Ocean', 'Mark', 'C', 'Austria', 'Texas', 'Mediterranean', 'Film', 'Elizabeth', 'Arthur', 'Davis', 'Convention', 'Boston', 'Music', 'Chinese', 'Jersey', 'Series', 'Research', 'Albert', 'Hill', 'Time', 'Game', 'Indian', 'District', 'B', 'Young', 'Green', 'Corporation', 'Francisco', 'Bush', 'Hollywood', 'Turkey', 'Le', 'Hong', 'Norway', 'Conference', 'Coast', 'Indonesia', 'NFL', 'Denmark', 'Board', 'Democratic', 'Frank', 'Testament', 'Nobel', 'Big', 'Gulf', 'Commonwealth', 'Security', 'Library', 'Chief', 'Justice', 'Star', 'Muhammad', 'Rock', 'Germans'],
        #     "pron": ['I', 'It', 'it', 'He', 'he', 'She', 'she', 'They', 'they', 'We', 'we'],
        #     "aux": ['is', 'are', ],
        #     "adj": ['other', 'such', 'first', 'many', '-', 'new', 'more', 'same', 'early', 'several', 'most', 'large', 'high', 'different', 'major', 'own', 'second', 'common', 'small', 'American', 'political', 'modern', 'important', 'British', 'non', 'largest', 'various', 'German', 'main', 'military', 'single', 'public', 'similar', 'local', 'late', 'few', 'popular', 'general', 'last', 'human', 'original', 'national', 'French', 'long', 'economic', 'former', 'European', 'great', 'international', 'social', 'free', 'Many', 'possible', 'only', 'old', 'Other', 'much', 'natural', 'low', 'significant', 'available', 'religious', 'particular', 'full', 'traditional', 'certain', 'short', 'higher', 'next', 'final', 'third', 'present', 'foreign', 'central', 'official', 'strong', 'English', 'able', 'Most', 'Roman', 'Jewish', 'Greek', 'total', 'special', 'little', 'independent', 'lower', 'specific', 'current', 'black', 'real', 'ancient', 'good', 'white', 'larger', 'less', 'private', '19th', 'legal', 'recent', 'Christian', 'open', 'northern', 'young', 'successful', 'physical', 'primary', 'later', 'Chinese'],
        #     "punct": ["."],
        #     "eos": [".", "!", "?"],
        # }
        # self._non_terminals = {
        #     "top": [
        #         ["s_1__"]
        #     ],
        #     "s_1__": [
        #         ["np_1__", "vp_1__"],
        #         ["vp_1__"],
        #         ["vp_2__"]
        #     ],
        #     "np_1__": [
        #         ["pron"],
        #         ["det", "noun"],
        #         ["noun"],
        #         ["det", "adj", "noun"]
        #     ],
        #     "np_2__": [
        #         ["np_1__", "pp_1__"]
        #     ],
        #     "vp_1__": [
        #         ["verb", "pp_1__"],
        #         ["verb", "np_1__"],
        #         ["verb", "np_2__"]
        #     ],
        #     "vp_2__": [
        #         ["aux", "vp_1__"]
        #     ],
        #     "pp_1__": [
        #         ["adp", "np_1__"]
        #     ],
        # }
    # @guidance(stateless=True)
    # def sep(lm, self, temperature=0.0):
    #     return lm + select_with_temperature(self._productions["sep"], temperature=temperature)

    # @guidance(stateless=True)
    # def noun(lm, self, temperature=0.0):
    #     return lm + self.sep(temperature=temperature) + select_with_temperature(self._productions["noun"], temperature=temperature)

    # @guidance(stateless=True)
    # def verb(lm, self, temperature=0.0):
    #     return lm + self.sep(temperature=temperature) + select_with_temperature(self._productions["verb"], temperature=temperature)

    # @guidance(stateless=True)
    # def adp(lm, self, temperature=0.0):
    #     return lm + self.sep(temperature=temperature) + select_with_temperature(self._productions["adp"], temperature=temperature)

    # @guidance(stateless=True)
    # def det(lm, self, temperature=0.0):
    #     return lm + self.sep(temperature=temperature) + select_with_temperature(self._productions["det"], temperature=temperature)

    # @guidance(stateless=True)
    # def propn(lm, self, temperature=0.0):
    #     return lm + self.sep(temperature=temperature) + select_with_temperature(self._productions["propn"], temperature=temperature)

    # @guidance(stateless=True)
    # def pron(lm, self, temperature=0.0):
    #     return lm + self.sep(temperature=temperature) + select_with_temperature(self._productions["pron"], temperature=temperature)

    # @guidance(stateless=True)
    # def aux(lm, self, temperature=0.0):
    #     return lm + self.sep(temperature=temperature) + select_with_temperature(self._productions["aux"], temperature=temperature)

    # @guidance(stateless=True)
    # def adj(lm, self, temperature=0.0):
    #     return lm + self.sep(temperature=temperature) + select_with_temperature(self._productions["adj"], temperature=temperature)

    # @guidance(stateless=True)
    # def punct(lm, self, temperature=0.0):
    #     return lm + select_with_temperature(self._productions["punct"], temperature=temperature)
    
    @guidance(stateless=True)  # type: ignore
    def select_terminal(lm, self, rule, temperature=0.0, add_leading_sep=True):
        return (  # TODO select seems to be broken
            lm +   # type: ignore
            (self.select_terminal("sep", temperature=temperature, add_leading_sep=False) if add_leading_sep else "") + 
            select_with_temperature(self._terminals[rule], temperature=temperature)  # type: ignore  
        )
    
    @guidance(stateless=True)  # type: ignore
    def combine(lm, self, grammars, temperature=0.0):
        for grammar in grammars:
            # if isinstance(grammar, str):
            #     lm += self.select_terminal(grammar, temperature=temperature)
            # else:
            #     lm += grammar(temperature=temperature)
            lm += self.construct_recursively(grammar, temperature=temperature)
        return lm
    
    @guidance(stateless=True)  # type: ignore
    def construct_recursively(lm, self, rule, temperature=0.0):
        if rule in self._terminals:
            lm += self.select_terminal(rule, temperature=temperature)
        elif rule in self._non_terminals:
            options = self._non_terminals[rule]
            lm += select_with_temperature(  # type: ignore
                [self.combine(option, temperature=temperature) for option in options], 
                temperature=temperature
            )
        else:
            raise ValueError(f"Unrecognized grammar: {rule}")
        return lm
    

    # @guidance(stateless=True)
    # def top(lm, self, temperature=0.0):
    #     options = [
    #         self.s_1__(temperature=temperature) + self.select_terminal("punct", temperature=temperature, add_leading_space=False)
    #     ]
    #     return lm + with_temperature(select(options), temperature=temperature)

    # @guidance(stateless=True)
    # def s_1__(lm, self, temperature=0.0):
    #     options = [
    #         [self.np_1__, self.vp_1__],
    #         [self.vp_1__],
    #         [self.vp_2__]
    #     ]
    #     # options = [
    #     #     self.np_1__(temperature=temperature) + self.vp_1__(temperature=temperature), 
    #     #     self.vp_1__(temperature=temperature), 
    #     #     self.vp_2__(temperature=temperature)
    #     # ]
        
    #     return lm + select_with_temperature(
    #         [self.combine(option, temperature=temperature) for option in options], 
    #         temperature=temperature
    #     )

    # @guidance(stateless=True)
    # def np_1__(lm, self, temperature=0.0):
    #     options = [
    #         ["pron"],
    #         ["det", "noun"],
    #         ["noun"],
    #         ["det", "adj", "noun"]
    #     ]
    #     # options = [
    #     #     self.select_terminal("pron", temperature=temperature),
    #     #     self.select_terminal("det", temperature=temperature) + self.select_terminal("noun", temperature=temperature),
    #     #     # self.det(temperature=temperature) + self.noun(temperature=temperature), 
    #     #     self.select_terminal("noun", temperature=temperature), 
    #     #     # self.noun(temperature=temperature), 
    #     #     one_or_more(self.select_terminal("propn", temperature=temperature)), 
    #     #     # one_or_more(self.propn(temperature=temperature)), 
    #     #     self.select_terminal("det", temperature=temperature) + self.select_terminal("adj", temperature=temperature) + self.select_terminal("noun", temperature=temperature)
    #     #     # self.det(temperature=temperature) + self.adj(temperature=temperature) + self.noun(temperature=temperature)
    #     # ]

    #     return lm + select_with_temperature(
    #         [self.combine(option, temperature=temperature) for option in options], 
    #         temperature=temperature
    #     )

    # @guidance(stateless=True)
    # def np_2__(lm, self, temperature=0.0):
    #     options = [
    #         [self.np_1__, self.pp_1__]
    #     ]
    #     # options = [
    #     #     self.np_1__(temperature=temperature) + self.pp_1__(temperature=temperature)
    #     # ]
    #     return lm + select_with_temperature(
    #         [self.combine(option, temperature=temperature) for option in options], 
    #         temperature=temperature
    #     )

    # @guidance(stateless=True)
    # def vp_1__(lm, self, temperature=0.0):
    #     options = [
    #         ["verb", self.pp_1__],
    #         ["verb", self.np_1__],
    #         ["verb", self.np_2__]
    #     ]
    #     # options = [
    #     #     self.select_terminal("verb", temperature=temperature) + self.pp_1__(temperature=temperature), 
    #     #     # self.verb(temperature=temperature) + self.pp_1__(temperature=temperature), 
    #     #     self.select_terminal("verb", temperature=temperature) + self.np_1__(temperature=temperature), 
    #     #     # self.verb(temperature=temperature) + self.np_1__(temperature=temperature), 
    #     #     self.select_terminal("verb", temperature=temperature) + self.np_2__(temperature=temperature)
    #     #     # self.verb(temperature=temperature) + self.np_2__(temperature=temperature)
    #     # ]
    #     return lm + select_with_temperature(
    #         [self.combine(option, temperature=temperature) for option in options], 
    #         temperature=temperature
    #     )

    # @guidance(stateless=True)
    # def vp_2__(lm, self, temperature=0.0):
    #     options = [
    #         ["aux", self.vp_1__]
    #     ]
    #     # options = [
    #     #     self.select_terminal("aux", temperature=temperature) + self.vp_1__(temperature=temperature)
    #     #     # self.aux(temperature=temperature) + self.vp_1__(temperature=temperature)
    #     # ]
    #     return lm + select_with_temperature(
    #         [self.combine(option, temperature=temperature) for option in options], 
    #         temperature=temperature
    #     )

    # @guidance(stateless=True)
    # def pp_1__(lm, self, temperature=0.0):
    #     options = [
    #         ["adp", self.np_1__]
    #     ]
    #     # options = [
    #     #     self.select_terminal("adp", temperature=temperature) + self.np_1__(temperature=temperature)
    #     #     # self.adp(temperature=temperature) + self.np_1__(temperature=temperature)
    #     # ]
    #     return lm + select_with_temperature(
    #         [self.combine(option, temperature=temperature) for option in options], 
    #         temperature=temperature
    #     )
    
    @guidance(stateless=True)  # type: ignore
    def __call__(lm, self, temperature=0.0):
        # return lm + self.top(temperature=temperature)
        assert "TOP" in self._non_terminals
        return (
            lm + self.construct_recursively("TOP", temperature=temperature) + 
            self.select_terminal("eos", temperature=temperature, add_leading_sep=False)
        )
