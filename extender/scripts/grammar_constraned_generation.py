import argparse
from guidance import capture, models, gen, system, user, assistant
# from extender.grammar.factory import TermGrammarFactory
# from llama_cpp import Llama
# from extender.grammar.factory import Grammar
# from grammar import top
from extender.grammar.guidance_grammar import GuidanceGrammar


grammar = (
    "TOP -> S_1__\n"
    # "TOP -> S_1__ | S_2__\n"
    "S_1__ -> VP_1__ | VP_2__ | NP_1__ VP_1__\n"
    "VP_1__ -> VERB PP_1__ | VERB NP_1__ | VERB NP_2__ | VERB | VERB PP_2__\n"
    "PP_1__ -> ADP NP_1__\n"
    "NP_1__ -> DET NOUN | NOUN | PROPN | DET ADJ NOUN\n"
    "NP_2__ -> NP_1__ PP_1__\n"
    "PP_2__ -> ADP NP_2__\n"
    "VP_2__ -> AUX VP_1__ | PART VP_1__\n"
    # "S_2__ -> VP_3__ | NP_1__ VP_3__ | NP_1__ VP_3__ PUNCT | NP_1__ VP_2__ PUNCT | VP_2__ | VP_4__ | NP_1__ VP_2__ | NP_1__ VP_4__ PUNCT | NP_1__ VP_4__\n"
    # "VP_3__ -> AUX VP_2__ | VERB S_1__ | PART VP_2__ | VERB SBAR_1__\n"
    # "SBAR_1__ -> WHNP_1__ S_1__ | SCONJ S_1__\n"
    # "WHNP_1__ -> PRON\n"
    # "VP_4__ -> AUX VP_3__ | PART VP_3__ | VERB S_1__ | VERB SBAR_1__\n"
    "VERB -> 'used' | 'known' | 'called' | 'made' | 'including' | 'became' | 'based' | 'found' | 'include' | 'began' | 'using' | 'led' | 'considered' | 'published' | 'said' | 'use' | 'become' | 'developed' | 'given' | 'took' | 'following' | 'make' | 'held' | 'included' | 'wrote' | 'established' | 'According' | 'written' | 'released' | 'produced' | 'named' | 'came' | 'having' | 'played' | 'created' | 'described' | 'set' | 'see' | 'built' | 'received' | 'continued' | 'take' | 'won' | 'left' | 'died' | 'seen' | 'followed' | 'formed' | 'introduced' | 'making'\n"
    "ADP -> 'of' | 'in' | 'to' | 'as' | 'for' | 'by' | 'with' | 'on' | 'from' | 'In'\n"
    "DET -> 'the'\n"
    "NOUN -> 'time' | 'years' | 'century' | 'number' | 'part' | 'system' | 'year' | 'people' | 'government' | 'state' | 'city' | 'world' | 'example' | 'use' | 'work' | 'name' | 'country' | 'language' | 'film' | 'life' | 'population' | 'group' | 'power' | 'area' | 'series' | 'period' | 'form' | 'term' | 'war' | 'end' | 'music' | 'day' | 'death' | 'members' | 'order' | 'water' | 'law' | 'countries' | 'family' | 'game' | 'way' | 'history' | 'development' | 'place' | 'theory' | 'team' | 'point' | 'case' | 'book' | 'production' | 'areas' | 'region' | 'role' | 'line' | 'groups' | 'systems' | 'control' | 'times' | 'process' | 'others' | 'home' | 'season' | 'field' | 'body' | 'word' | 'result' | 'level' | 'languages' | 'forces' | 'age' | 'species' | 'company' | 'land' | 'states' | 'data' | 'men' | 'addition' | 'energy' | 'support' | 'member' | 'service' | 'women' | 'party' | 'children' | 'works' | 'position' | 'terms' | 'version' | 'numbers' | 'school' | 'space' | 'force' | 'parts' | 'son' | 'information' | 'air' | 'side' | 'father' | 'album' | 'island' | 'function' | 'type' | 'days' | 'set' | 'style' | 'research' | 'games' | 'band' | 'design' | 'trade' | 'movement' | 'man' | 'elements' | 'character' | 'rate' | 'range' | 'words' | 'study' | 'evidence' | 'effect' | 'computer' | 'value' | 'structure' | 'culture' | 'person' | 'head' | 'influence'\n"
    "PROPN -> 'United' | 'New' | 'States' | 'World' | 'War' | 'John' | 'University' | 'National' | 'Europe' | 'U.S.' | 'II' | 'English' | 'May' | 'North' | 'Germany' | 'South' | 'Church' | 'January' | 'France' | 'Union' | 'England' | 'July' | 'York' | 'September' | 'June' | 'March' | 'December' | 'October' | 'God' | 'November' | 'April' | 'City' | 'August' | 'America' | 'India' | 'London' | 'President' | 'King' | 'East' | 'China' | 'International' | 'US' | 'West' | 'American' | 'February' | 'Empire' | 'General' | 'Council' | 'Republic' | 'British' | 'Africa' | 'River' | 'Party' | 'de' | 'House' | 'Kingdom' | 'Army' | 'State' | 'Earth' | 'Canada' | 'William' | 'Britain' | 'League' | 'James' | 'French' | 'Charles' | 'Japan' | 'Great' | 'European' | 'George' | 'Australia' | 'Henry' | 'BC' | 'David' | 'Italy' | 'UK' | 'Court' | 'Central' | 'School' | 'Island' | 'Paul' | 'al' | 'Soviet' | 'Ireland' | 'Israel' | 'Minister' | 'Sea' | 'Act' | 'Robert' | 'Air' | 'Spain' | 'Asia' | 'Royal' | 'Roman' | 'Rome' | 'Russia' | 'College' | 'St.' | 'Jews' | 'Park' | 'Latin' | 'Louis' | 'Old' | 'Paris' | 'Thomas' | 'California' | 'Congress' | 'Islands' | 'Emperor' | 'Parliament' | 'Middle' | 'Mexico' | 'Egypt' | 'Mary' | 'A' | 'Battle' | 'Jesus' | 'San' | 'Washington' | 'First' | 'Red' | 'Nations' | 'Poland' | 'Richard' | 'Alexander' | 'Saint' | 'Force' | 'Institute' | 'Lord' | 'Black' | 'Society' | 'I' | 'Northern'\n"
    "ADJ -> 'other' | 'such' | 'first' | 'many' | 'new' | 'more' | 'same' | 'early' | 'several' | 'most' | 'large' | 'high' | 'different' | 'major' | 'own' | 'second' | 'common' | 'small' | 'American' | 'political' | 'modern' | 'important' | 'British' | 'non' | 'largest' | 'various' | 'German' | 'main' | 'military' | 'single' | 'public' | 'similar' | 'local' | 'late' | 'few' | 'popular' | 'general' | 'last' | 'human' | 'original' | 'national' | 'French' | 'long' | 'economic' | 'former' | 'European' | 'great' | 'international' | 'social' | 'free' | 'Many' | 'possible' | 'only' | 'old' | 'Other' | 'much' | 'natural' | 'low' | 'significant' | 'available' | 'religious' | 'particular' | 'full' | 'traditional' | 'certain' | 'short' | 'higher' | 'next' | 'final' | 'third' | 'present' | 'foreign' | 'central' | 'official' | 'strong' | 'English' | 'able' | 'Most' | 'Roman' | 'Jewish' | 'Greek' | 'total' | 'special' | 'little' | 'independent' | 'lower' | 'specific' | 'current' | 'black' | 'real' | 'ancient' | 'good' | 'white' | 'larger' | 'less' | 'private' | '19th' | 'legal' | 'recent' | 'Christian' | 'open' | 'northern' | 'young' | 'successful' | 'physical' | 'primary' | 'later' | 'Chinese'\n"
    "AUX -> 'is' | 'was' | 'are'\n"
    "PART -> 'to'\n"
    "PRON -> 'his' | 'it' | 'he' | 'that' | 'their' | 'its' | 'who' | 'they' | 'It' | 'He' | 'her' | 'him' | 'there' | 'them'\n"
    "SCONJ -> 'that' | 'when'\n"
    "PUNCT -> ',' | '.'\n"
)

grammar = (
    "NP_1__ -> DET NOUN | NOUN | PROPN | DET ADJ NOUN\n"
    "DET -> 'the'\n"
    "NOUN -> 'time' | 'years' | 'century' | 'number' | 'part' | 'system' | 'year' | 'people' | 'government' | 'state' | 'city' | 'world' | 'example' | 'use' | 'work' | 'name' | 'country' | 'language' | 'film' | 'life' | 'population' | 'group' | 'power' | 'area' | 'series' | 'period' | 'form' | 'term' | 'war' | 'end' | 'music' | 'day' | 'death' | 'members' | 'order' | 'water' | 'law' | 'countries' | 'family' | 'game' | 'way' | 'history' | 'development' | 'place' | 'theory' | 'team' | 'point' | 'case' | 'book' | 'production' | 'areas' | 'region' | 'role' | 'line' | 'groups' | 'systems' | 'control' | 'times' | 'process' | 'others' | 'home' | 'season' | 'field' | 'body' | 'word' | 'result' | 'level' | 'languages' | 'forces' | 'age' | 'species' | 'company' | 'land' | 'states' | 'data' | 'men' | 'addition' | 'energy' | 'support' | 'member' | 'service' | 'women' | 'party' | 'children' | 'works' | 'position' | 'terms' | 'version' | 'numbers' | 'school' | 'space' | 'force' | 'parts' | 'son' | 'information' | 'air' | 'side' | 'father' | 'album' | 'island' | 'function' | 'type' | 'days' | 'set' | 'style' | 'research' | 'games' | 'band' | 'design' | 'trade' | 'movement' | 'man' | 'elements' | 'character' | 'rate' | 'range' | 'words' | 'study' | 'evidence' | 'effect' | 'computer' | 'value' | 'structure' | 'culture' | 'person' | 'head' | 'influence'\n"
    "PROPN -> 'United' | 'New' | 'States' | 'World' | 'War' | 'John' | 'University' | 'National' | 'Europe' | 'U.S.' | 'II' | 'English' | 'May' | 'North' | 'Germany' | 'South' | 'Church' | 'January' | 'France' | 'Union' | 'England' | 'July' | 'York' | 'September' | 'June' | 'March' | 'December' | 'October' | 'God' | 'November' | 'April' | 'City' | 'August' | 'America' | 'India' | 'London' | 'President' | 'King' | 'East' | 'China' | 'International' | 'US' | 'West' | 'American' | 'February' | 'Empire' | 'General' | 'Council' | 'Republic' | 'British' | 'Africa' | 'River' | 'Party' | 'de' | 'House' | 'Kingdom' | 'Army' | 'State' | 'Earth' | 'Canada' | 'William' | 'Britain' | 'League' | 'James' | 'French' | 'Charles' | 'Japan' | 'Great' | 'European' | 'George' | 'Australia' | 'Henry' | 'BC' | 'David' | 'Italy' | 'UK' | 'Court' | 'Central' | 'School' | 'Island' | 'Paul' | 'al' | 'Soviet' | 'Ireland' | 'Israel' | 'Minister' | 'Sea' | 'Act' | 'Robert' | 'Air' | 'Spain' | 'Asia' | 'Royal' | 'Roman' | 'Rome' | 'Russia' | 'College' | 'St.' | 'Jews' | 'Park' | 'Latin' | 'Louis' | 'Old' | 'Paris' | 'Thomas' | 'California' | 'Congress' | 'Islands' | 'Emperor' | 'Parliament' | 'Middle' | 'Mexico' | 'Egypt' | 'Mary' | 'A' | 'Battle' | 'Jesus' | 'San' | 'Washington' | 'First' | 'Red' | 'Nations' | 'Poland' | 'Richard' | 'Alexander' | 'Saint' | 'Force' | 'Institute' | 'Lord' | 'Black' | 'Society' | 'I' | 'Northern'\n"
    "ADJ -> 'other' | 'such' | 'first' | 'many' | 'new' | 'more' | 'same' | 'early' | 'several' | 'most' | 'large' | 'high' | 'different' | 'major' | 'own' | 'second' | 'common' | 'small' | 'American' | 'political' | 'modern' | 'important' | 'British' | 'non' | 'largest' | 'various' | 'German' | 'main' | 'military' | 'single' | 'public' | 'similar' | 'local' | 'late' | 'few' | 'popular' | 'general' | 'last' | 'human' | 'original' | 'national' | 'French' | 'long' | 'economic' | 'former' | 'European' | 'great' | 'international' | 'social' | 'free' | 'Many' | 'possible' | 'only' | 'old' | 'Other' | 'much' | 'natural' | 'low' | 'significant' | 'available' | 'religious' | 'particular' | 'full' | 'traditional' | 'certain' | 'short' | 'higher' | 'next' | 'final' | 'third' | 'present' | 'foreign' | 'central' | 'official' | 'strong' | 'English' | 'able' | 'Most' | 'Roman' | 'Jewish' | 'Greek' | 'total' | 'special' | 'little' | 'independent' | 'lower' | 'specific' | 'current' | 'black' | 'real' | 'ancient' | 'good' | 'white' | 'larger' | 'less' | 'private' | '19th' | 'legal' | 'recent' | 'Christian' | 'open' | 'northern' | 'young' | 'successful' | 'physical' | 'primary' | 'later' | 'Chinese'\n"
)

grammar = (
    "TOP -> S_1__\n"
    "S_1__ -> VP_1__ | VP_2__ | NP_1__ VP_1__\n"
    "VP_1__ -> VERB PP_1__ | VERB NP_1__ | VERB NP_2__\n"
    "PP_1__ -> ADP NP_1__\n"
    "NP_1__ -> DET NOUN | NOUN | PROPN\n"
    "NP_2__ -> NP_1__ PP_1__\n"
    "VP_2__ -> AUX VP_1__\n"
    "VERB -> 'used' | 'known' | 'called' | 'made' | 'including' | 'became' | 'based' | 'found' | 'include' | 'began' | 'using' | 'led' | 'considered' | 'published' | 'said' | 'use' | 'become' | 'developed' | 'given' | 'took' | 'following' | 'make' | 'held' | 'included' | 'wrote' | 'established' | 'According' | 'written' | 'released' | 'produced' | 'named' | 'came' | 'having' | 'played' | 'created' | 'described' | 'set' | 'see' | 'built' | 'received' | 'continued' | 'take' | 'won' | 'left' | 'died' | 'seen' | 'followed' | 'formed' | 'introduced' | 'making' | 'born' | 'according' | 'located' | 'remained' | 'referred' | 'taken' | 'lost' | 'increased' | 'went' | 'provided' | 'allowed' | 'moved' | 'provide' | 'required' | 'started' | 'defined' | 'gave' | 'includes' | 'believed' | 'appeared' | 'leading' | 'form' | 'associated' | 'brought' | 'announced' | 'sent' | 'returned' | 'designed' | 'served' | 'founded' | 'related' | 'saw' | 'stated' | 'elected' | 'caused' | 'produce' | 'replaced' | 'reported' | 'recorded' | 'come' | 'proposed' | 'thought' | 'added' | 'working' | 'involved' | 'put' | 'supported' | 'create' | 'reached' | 'adopted' | 'allow' | 'claimed' | 'performed' | 'sold' | 'worked' | 'play' | 'uses' | 'discovered' | 'killed' | 'give' | 'divided'\n"
    "ADP -> 'of' | 'in'\n"
    "DET -> 'the'\n"
    "NOUN -> 'time' | 'years' | 'century' | 'number' | 'part' | 'system' | 'year' | 'people' | 'government' | 'state' | 'city' | 'world' | 'example' | 'use' | 'work' | 'name' | 'country' | 'language' | 'film' | 'life' | 'population' | 'group' | 'power' | 'area' | 'series' | 'period' | 'form' | 'term' | 'war' | 'end' | 'music' | 'day' | 'death' | 'members' | 'order' | 'water' | 'law' | 'countries' | 'family' | 'game' | 'way' | 'history' | 'development' | 'place' | 'theory' | 'team' | 'point' | 'case' | 'book' | 'production' | 'areas' | 'region' | 'role' | 'line' | 'groups' | 'systems' | 'control' | 'times' | 'process' | 'others' | 'home' | 'season' | 'field' | 'body' | 'word' | 'result' | 'level' | 'languages' | 'forces' | 'age' | 'species' | 'company' | 'land' | 'states' | 'data' | 'men' | 'addition' | 'energy' | 'support' | 'member' | 'service' | 'women' | 'party' | 'children' | 'works' | 'position' | 'terms' | 'version' | 'numbers' | 'school' | 'space' | 'force' | 'parts' | 'son' | 'information' | 'air' | 'side' | 'father' | 'album' | 'island' | 'function' | 'type' | 'days' | 'set' | 'style' | 'research' | 'games' | 'band' | 'design' | 'trade' | 'movement' | 'man' | 'elements' | 'character' | 'rate' | 'range' | 'words' | 'study' | 'evidence' | 'effect' | 'computer' | 'value' | 'structure' | 'culture' | 'person' | 'head' | 'influence' | 'source' | 'art' | 'rights' | 'program' | 'market' | 'industry' | 'class' | 'army' | 'films' | 'cases' | 'education' | 'science' | 'capital' | 'months' | 'hand' | 'forms' | 'size' | 'services' | 'model' | 'title' | 'majority' | 'economy' | 'community' | 'aircraft' | 'fact' | 'television' | 'food' | 'rule' | 'nature' | 'growth' | 'self' | 'story' | 'events' | 'record' | 'cities' | 'today' | 'court' | 'action' | 'election' | 'policy' | 'north' | 'types' | 'players' | 'town' | 'effects' | 'success' | 'business' | 'base' | 'church' | 'network' | 'interest' | 'player' | 'books' | 'king' | 'president' | 'problems' | 'mother' | 'problem' | 'schools' | 'material' | 'surface' | 'view' | 'practice' | 'students' | 'office' | 'percent' | 'conditions' | 'companies' | 'light' | 'names' | 'method' | 'changes' | 'performance' | 'concept' | 'lines' | 'idea' | 'change' | 'products' | 'variety' | 'half' | 'wife' | 'show' | 'society' | 'project' | 'basis' | 'construction' | 'relations' | 'right' | 'characters' | 'metal' | 'units' | 'house' | 'song' | 'era' | 'sources' | 'cell' | 'points' | 'software' | 'tradition' | 'relationship' | 'site' | 'territory' | 'list' | 'scale' | 'oil' | 'radio' | 'pressure' | 'sea' | 'centuries' | 'length' | 'health' | 'regions' | 'speed' | 'career' | 'product' | 'code' | 'media' | 'status' | 'technology' | 'event' | 'results' | 'methods' | 'gas' | 'laws' | 'letter' | 'levels' | 'islands' | 'studies' | 'mass' | 'troops' | 'response' | 'money' | 'functions' | 'rules' | 'ground' | 'operations' | 'cells' | 'building' | 'release' | 'leader' | 'rock' | 'degree' | 'independence' | 'stage' | 'text' | 'sense' | 'amount' | 'element' | 'attack' | 'knowledge' | 'center'\n"
    "PROPN -> 'United' | 'New' | 'States' | 'World' | 'War' | 'John' | 'University' | 'National' | 'Europe' | 'U.S.' | 'II' | 'English' | 'May' | 'North' | 'Germany' | 'South' | 'Church' | 'January' | 'France' | 'Union' | 'England' | 'July' | 'York' | 'September' | 'June' | 'March' | 'December' | 'October' | 'God' | 'November' | 'April' | 'City' | 'August' | 'America' | 'India' | 'London' | 'President' | 'King' | 'East' | 'China' | 'International' | 'US' | 'West' | 'American' | 'February' | 'Empire' | 'General' | 'Council' | 'Republic' | 'British' | 'Africa' | 'River' | 'Party' | 'de' | 'House' | 'Kingdom' | 'Army' | 'State' | 'Earth' | 'Canada' | 'William' | 'Britain' | 'League' | 'James' | 'French' | 'Charles' | 'Japan' | 'Great' | 'European' | 'George' | 'Australia' | 'Henry' | 'BC' | 'David' | 'Italy' | 'UK' | 'Court' | 'Central' | 'School' | 'Island' | 'Paul' | 'al' | 'Soviet' | 'Ireland' | 'Israel' | 'Minister' | 'Sea' | 'Act' | 'Robert' | 'Air' | 'Spain' | 'Asia' | 'Royal' | 'Roman' | 'Rome' | 'Russia' | 'College' | 'St.' | 'Jews' | 'Park' | 'Latin' | 'Louis' | 'Old' | 'Paris' | 'Thomas' | 'California' | 'Congress' | 'Islands' | 'Emperor' | 'Parliament' | 'Middle' | 'Mexico' | 'Egypt' | 'Mary' | 'A' | 'Battle' | 'Jesus' | 'San' | 'Washington' | 'First' | 'Red' | 'Nations' | 'Poland' | 'Richard' | 'Alexander' | 'Saint' | 'Force' | 'Institute' | 'Lord' | 'Black' | 'Society' | 'I' | 'Northern' | 'Company' | 'Christ' | 'III' | 'Eastern' | 'Catholic' | 'Award' | 'Hall' | 'Navy' | 'German' | 'Government' | 'Peter' | 'Americans' | 'Greek' | 'Lake' | 'Pacific' | 'Academy' | 'Western' | 'Association' | 'Prime' | 'County' | 'Museum' | 'Street' | 'Day' | 'Chicago' | 'Book' | 'Grand' | 'Committee' | 'Cup' | 'Center' | 'Smith' | 'Holy' | 'Bank' | 'Netherlands' | 'Revolution' | 'Joseph' | 'Greece' | 'Zealand' | 'Michael' | 'Martin' | 'Department' | 'Age' | 'White' | 'Christianity' | 'Scotland' | 'Orthodox' | 'High' | 'Berlin' | 'Second' | 'Christian' | 'La' | 'Korea' | 'Treaty' | 'Civil' | 'Assembly' | 'Commission' | 'Queen' | 'Sun' | 'Los' | 'Al' | 'Bay' | 'Man' | 'Pope' | 'Edward' | 'Iran' | 'Group' | 'Best' | 'Prince' | 'Christians' | 'Bible' | 'Brown' | 'X' | 'Spanish' | 'Columbia' | 'Christmas' | 'Iraq' | 'Sir' | 'Afghanistan' | 'Hitler' | 'Supreme' | 'Apple' | 'Jerusalem' | 'Southern' | 'Airport' | 'System' | 'von' | 'J.' | 'Law' | 'Finland' | 'EU' | 'Lincoln' | 'Senate' | 'Jean' | 'Atlantic' | 'Islam' | 'BBC' | 'Angeles' | 'Duke' | 'Secretary' | 'Pakistan' | 'Constitution' | 'St' | 'African' | 'Jackson' | 'Hungary' | 'Service' | 'Science' | 'Windows' | 'DNA' | 'Kong' | 'People' | 'Festival' | 'Microsoft' | 'Ottoman' | 'GDP' | 'Jones' | 'Office' | 'Bill' | 'Hebrew' | 'De' | 'Club' | 'Federal' | 'Muslims' | 'El' | 'Moon' | 'Division' | 'Forces' | 'Dutch' | 'Wales' | 'Times' | 'Valley' | 'Brazil' | 'Apollo' | 'Prize' | 'Governor' | 'Sweden' | 'Johnson' | 'UN' | 'Dr.' | 'Lee' | 'IBM' | 'Ocean' | 'Mark' | 'C' | 'Austria' | 'Texas' | 'Mediterranean' | 'Film' | 'Elizabeth' | 'Arthur' | 'Davis' | 'Convention' | 'Boston' | 'Music' | 'Chinese' | 'Jersey' | 'Series' | 'Research' | 'Albert' | 'Hill' | 'Time' | 'Game' | 'Indian' | 'District' | 'B' | 'Young' | 'Green' | 'Corporation' | 'Francisco' | 'Bush' | 'Hollywood' | 'Turkey' | 'Le' | 'Hong' | 'Norway' | 'Conference' | 'Coast' | 'Indonesia' | 'NFL' | 'Denmark' | 'Board' | 'Democratic' | 'Frank' | 'Testament' | 'Nobel' | 'Big' | 'Gulf' | 'Commonwealth' | 'Security' | 'Library' | 'Chief' | 'Justice' | 'Star' | 'Muhammad' | 'Rock' | 'Germans'\n"
    "AUX -> 'is' | 'was'\n"
)

def main(args):
    model = models.LlamaCpp(args.model_path, n_ctx=0, seed=-1, echo=False, n_threads=8)

    # top = TermGrammarFactory.from_string(grammar)
    top = GuidanceGrammar(grammar)

    system_prompt = (
        "You are an expert on language learning and are very attentive to the needs of your user. "
        # "You understand that for practicing language one should take one small step at a time."
    )
    
    prompt = (
        "I'm learning a new language and need to practice a lot. For practice, I take sentences in english and translate them in the language I learn. "
        "I aws doing this for a long time and am out of ideas for practice sentences. Could you please help me to come up with new sentences? "
        "I am still on a beginner level so the sentences should be simple and concise. Should not contain comas and subordinate conjunctions. "
        "Also, the examples need to be quite diverse so that I can maximite the effectiveness of the practice hours. "
        "\n"
    )

    with system():
        model += system_prompt

    with user():
        model += prompt

    with assistant():
        model += "Sure, here is a list of sentences you can use for practice: \n"

        seen = set()
        for i in range(100):
            temperature = 0.8
            trial = model + f"{i + 1}." + capture(top(temperature=temperature), "sentence") + "\n"
            while trial["sentence"] in seen:
                temperature *= 1.1
                trial = model + f"{i + 1}." + capture(top(temperature=temperature), "sentence") + "\n"

            seen.add(trial["sentence"])
            model += f"{i + 1}." + trial["sentence"] + "\n"

    print(model)
    print()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path")
    args = parser.parse_args()

    main(args)