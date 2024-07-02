# python extender/scripts/extend/assign_word_pos.py res/data/en.json None res/data/en_with_pos.json --pos_file_path res/pos/domain_question_pos.txt && \
python extender/scripts/extend/assign_word_frequencies.py res/data/en_with_pos.json res/frequencies/open_subtitle_word_count.json res/data/en_with_freq.json && \
python extender/scripts/extend/assign_word_proficiency_levels.py res/data/en_with_freq.json res/levels/kelly/levels.json EXTENDER_0.0.1 res/data/en_with_lvl.json && \
python extender/scripts/extend/rank_semantic_domains.py res/data/en_with_lvl.json opensubtitles.org wordcyclopedia/Kelly res/levels/ranking.json
