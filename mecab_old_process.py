# def process_sent(text):
#     tagger = Tagger('-Owakati')
#     #text = "日本経済回復への内外の期待は年々高まっている。"
#     tagger.parse(text)
#
#
#     stop = False
#
#     word_parts = []
#     for word in tagger(text):
#         #char_type', 'feature', 'feature_raw', 'is_unk', 'length', 'pos', 'posid', 'rlength', 'stat', 'surface', 'white_space'
#         # print(word, word.feature.lemma, word.pos, sep='\t')
#         pos1 = word.feature.pos1
#         if pos1 in pos1_translation:
#             pos1 = pos1_translation[pos1]
#         elif pos1 != "*":
#             print(f"New pos 1: {pos1}")
#             stop = True
#         pos2 = word.feature.pos2
#         if pos2 in pos2_translation:
#             pos2 = pos2_translation[pos2]
#         elif pos2 != "*":
#             print(f"New pos 2: {pos2}")
#             stop = True
#         pos3 = word.feature.pos3
#         if pos3 in pos3_translation:
#             pos3 = pos3_translation[pos3]
#         elif pos3 != "*":
#             print(f"New pos 3: {pos3}")
#             stop = True
#         pos4 = word.feature.pos4
#         if pos4 in pos4_translation:
#             pos4 = pos4_translation[pos4]
#         elif pos4 != "*":
#             print(f"New pos 4: {pos4}")
#             stop = True
#         #print(word.feature)
#         word_part= [word.feature.orth, word.feature.lemma, word.feature.kana, pos1, pos2, pos3, pos4]
#         word_parts.append(word_part)
#         print(*word_part , sep=', ')


    # Extract all the words from sentence, excluding things like particles, as dict form, to lock behind access  reqs.
    # no 3. 控える こと verb - noun

    # key_words = []
    # comp_key_words = []
    #
    # for x in range(len(word_parts)):
    #     word_part = word_parts[x]
    #     str_word, dict_word, kana, p1, p2, p3, p4 = word_part
    #
    #     if p1 in {"Noun", "Verb", "Adjective"}:
    #         excluded_verbs = {'し', 'い'}
    #         if str_word in excluded_verbs:
    #             continue
    #         key_words.append((str_word, word_part))
    #
    #         combined_word = str_word
    #         combined_word_elements = [word_part]
    #         for y in range(x+1, len(word_parts)):
    #             word_next_parts = word_parts[y]
    #             str_next_word, dict_next_word, kana_next_word, nw_p1, nw_p2, nw_p3, nw_p4 = word_next_parts
    #             if nw_p1 in {"Noun", "Verb", "Adjective", "Suffix"} and str_next_word not in {'し', 'い'}:
    #                 combined_word += str_next_word
    #                 combined_word_elements.append(word_next_parts)
    #                 comp_key_words.append((combined_word, combined_word_elements))
    #                 continue
    #             break
    #     if p1 == "Suffix":
    #         if p2 != "Noun":
    #             print("!!! New suffix case encountered !!!")
    #             continue
    #         key_words.append((str_word, word_part))
    #
    #     if p1 == "Suffix":
    #         key_words.append((str_word, word_part))
    #
    #     if p1 == "Adverb":
    #         if x+1 >= len(word_parts):
    #             print("!!! Adverb at the end !!!")
    #             continue
    #
    #         combined_word = str_word
    #         combined_word_elements = [word_part]
    #         # check if next is verb
    #         str_next_word, dict_next_word, kana_next_word, nw_p1, nw_p2, nw_p3, nw_p4 = word_next_parts =  word_parts[x+1]
    #         if nw_p1 != "Verb":
    #             print("!!! Verb not encountered after adverb !!!")
    #             continue
    #         combined_word += str_next_word
    #         combined_word_elements.append(word_next_parts)
    #
    #         if x + 2 < len(word_parts):
    #             str_next_word, dict_next_word, kana_next_word, nw_p1, nw_p2, nw_p3, nw_p4 = word_next_parts = \
    #             word_parts[x + 2]
    #             if nw_p1 == "Aux verb":
    #                 combined_word += str_next_word
    #                 combined_word_elements.append(word_next_parts)
    #
    #         comp_key_words.append((combined_word, combined_word_elements))

    # print("Words")
    # print([word[0] for word in key_words])
    # print("Potential combined results")
    # print([word[0] for word in comp_key_words])

    # return stop