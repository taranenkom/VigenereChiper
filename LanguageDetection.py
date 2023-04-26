import bisect
import wordninja
with open('dictionary.txt', 'r') as f:
    words = f.read().splitlines()

def change_dictionary(new_dict_path):
    global words
    with open(new_dict_path, 'r') as f:
        words = f.read().splitlines()
        

def is_a_word(word):
    index = bisect.bisect_left(words, word.lower())
    return index < len(words) and words[index] == word.lower()

def pretify_text(text):
    for i in [',', '.', '"', "'", '?', '!', ';', ':', '(', ')', '[', ']', '{', '}', '\n', '\r', '\t']:
        text = text.replace(i, '')
    return text

def count_words(text):
    words = text.lower().split()
    matches = 0
    for word in words:
        if is_a_word(word):
            matches += 1
    return matches

def is_text_english(text):
    matches = count_words(text)
    # print(f"Matches: {matches}, Words: {len(text.split())}, Precentage: {matches / len(text.split())*100}")
    perccentage = matches / len(text.split())
    return perccentage > 0.6

# def is_text_english_ninja(text):
#     text = pretify_text(text)
#     text = wordninja.split(text)
#     text = ' '.join(text)
#     print(text)
#     return is_text_english(text)

# print(is_text_english_ninja("Hello,mynameisJohn.Iam20yearsold.IliveinLondon."))
# print(is_text_english_ninja("Hallo,meinnameistJohn.Ichbin20Jahrealt.IchlebeinLondon."))
# print(is_text_english_ninja("FTFFTYHI@**#*aksdfjlasdfjlqwertyuiopasdfghjklzxcvbnm,df"))