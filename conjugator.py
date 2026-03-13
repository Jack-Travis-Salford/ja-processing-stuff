import json
import pykatsuyou
import pykakasi



def conjugate_and_kanarize(verb):
    try:
        all_form = json.loads(pykatsuyou.getInflections(verb)["json"])
        kanji_form = "Dict: {}\n---Present Forms---\nAffirm: {}\nNegative: {}\n\n---Te-Form---\nAffirm: {}\nNegative: {}".format(
            all_form["Affirmative"]["Dict-Form"],
            all_form["Affirmative"]["Non-Past Polite"],
            all_form["Negative"]["Non-Past Polite"],
            all_form["Affirmative"]["Te-Form"],
            all_form["Negative"]["Te-Form"]

        )
        kana_form = "Dict: {}\n---Present Forms---\nAffirm: {}\nNegative: {}\n\n---Te-Form---\nAffirm: {}\nNegative: {}".format(
            kanarizor(all_form["Affirmative"]["Dict-Form"]),
            kanarizor(all_form["Affirmative"]["Non-Past Polite"]),
            kanarizor(all_form["Negative"]["Non-Past Polite"]),
            kanarizor(all_form["Affirmative"]["Te-Form"]),
            kanarizor(all_form["Negative"]["Te-Form"])

        )
        return kanji_form, kana_form

    except:
        return False, False

def kanarizor(string_thing):
    kks = pykakasi.kakasi()
    result = kks.convert(string_thing)
    out = ""
    for res in result:
        #print(res)
        out += res["hira"]
    return out if out.strip() != "" else False


#print(kanarizor("私には、五つ上の兄がいる。"))


# import fugashi
#
# # Initialize the tokenizer
# tagger = fugashi.Tagger()
#
#
# def get_kana(text):
#     """
#     Convert Japanese text to kana readings using Fugashi.
#     Returns both hiragana and katakana readings.
#     """
#     words = tagger(text)
#
#     # Get hiragana reading (using .pron attribute)
#     hiragana = ''.join(word.feature.pron if word.feature.pron else word.surface for word in words)
#
#     # Get katakana reading (using .kana attribute)
#     katakana = ''.join(word.feature.kana if word.feature.kana else word.surface for word in words)
#
#     return {
#         'hiragana': hiragana,
#         'katakana': katakana
#     }
#
#
# # Example usage
# text = "私には、五つ上の兄がいる。"
# result = get_kana(text)
# print(f"Original: {text}")
# print(f"Hiragana: {result['hiragana']}")
# print(f"Katakana: {result['katakana']}")


# import fugashi
#
# # Initialize the tokenizer
# tagger = fugashi.Tagger()
#
#
# def get_kana(text):
#     """
#     Convert Japanese text to kana readings using Fugashi.
#     Returns both hiragana and katakana readings.
#     """
#     words = tagger(text)
#
#     # Get hiragana reading
#     hiragana = ''
#     for word in words:
#         # If there's no pronunciation or it contains *, use the original text
#         pron = word.feature.pron
#         if not pron or '*' in pron:
#             hiragana += word.surface
#         else:
#             hiragana += pron
#
#     # Get katakana reading
#     katakana = ''
#     for word in words:
#         # If there's no reading or it contains *, use the original text
#         kana = word.feature.kana
#         if not kana or '*' in kana:
#             katakana += word.surface
#         else:
#             katakana += kana
#
#     return {
#         'hiragana': hiragana,
#         'katakana': katakana
#     }
#
#
# # Example usage
# text = "私には、5つ上の兄がいる。"
# result = get_kana(text)
# print(f"Original: {text}")
# print(f"Hiragana: {result['hiragana']}")
# print(f"Katakana: {result['katakana']}")


# import fugashi
# from jaconv import kata2hira
#
# # Initialize the tokenizer
# tagger = fugashi.Tagger()
#
#
# def get_kana(text):
#     """
#     Convert Japanese text to kana readings using Fugashi.
#     Returns both hiragana and katakana readings.
#     """
#     words = tagger(text)
#
#     # Get hiragana reading (convert from katakana)
#     hiragana = ''
#     for word in words:
#         # If there's no pronunciation or it contains *, use the original text
#         pron = word.feature.pron
#         if not pron or '*' in pron:
#             hiragana += word.surface
#         else:
#             hiragana += kata2hira(pron)
#
#     # Get katakana reading
#     katakana = ''
#     for word in words:
#         # If there's no reading or it contains *, use the original text
#         kana = word.feature.kana
#         if not kana or '*' in kana:
#             katakana += word.surface
#         else:
#             katakana += kana
#
#     return {
#         'hiragana': hiragana,
#         'katakana': katakana
#     }
#
#
# # Example usage
# text = "私には、5つ上の兄がいる。"
# result = get_kana(text)
# print(f"Original: {text}")
# print(f"Hiragana: {result['hiragana']}")
# print(f"Katakana: {result['katakana']}")

# from sudachipy import dictionary, Dictionary
# import pykakasi
#
#
# def kanji_to_hiragana(sentence):
#     tokenizer = dictionary.Dictionary(dict="full").create()
#     print(dictionary.Dictionary(dict="full").lookup("私"))
#     kakasi = pykakasi.kakasi()
#     kakasi.setMode("J", "H")  # Kanji to Hiragana
#     kakasi.setMode("K", "H")  # Katakana to Hiragana
#     converter = kakasi.getConverter()
#     # result = converter.do(sentence)
#     # return result
#
#     tokens = tokenizer.tokenize(sentence)
#     result = ""
#     for token in tokens:
#         # Use pronunciation if available
#         reading = token.reading_form()
#         if reading:
#             result += converter.do(reading)
#         else:
#             result += converter.do(token.surface())
#
#     return result
#
#
# # Example usage
# sentence = "私には、5つ上の兄がいる"
#
# print("The output was {}".format(kanji_to_hiragana(sentence)))

