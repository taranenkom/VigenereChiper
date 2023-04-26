import LanguageDetection as ld
from extras import *
from math import sqrt

from collections import defaultdict
from suffix_trees import STree
from itertools import combinations, combinations_with_replacement
from functools import reduce
import itertools

def remove_non_alphabet_chars(text, alphabet):
    text = text.lower()
    return ''.join([char for char in text if char in alphabet])
def prime_factors(n):
    for i in itertools.chain([2], itertools.count(3, 2)):
        if n <= 1:
            break
        while n % i == 0:
            n //= i
            yield i



def get_products(numbers):
    result = []
    for i in range(1, len(numbers)+1):
        comb = combinations(numbers, i)
        for c in comb:
            prod = reduce(lambda x, y: x*y, c)
            if prod not in result: # check if prod is not in the result list
                result.append(prod)
    return result


def find_repeated_substirngs_and_indexes(text):
    stree = STree.STree(text)
    repeated_substrings = defaultdict(list)
    for i in range(len(text)):
        for j in range(i+1, len(text)):
            if abs(i-j)>2 and len(stree.find_all(text[i:j])) > 1:
                repeated_substrings[text[i:j]].append(i)
    return repeated_substrings

def encrypt_Ceaser(plain_text,key, alphabet=LETTERS_LOWER):
    crypted_text = ''
    for char in plain_text:
        index = alphabet.find(char)
        if index != -1:
            crypted_text += alphabet[(index + key) % len(alphabet)]
        else:
            index = alphabet.find(char)
            if index != -1:
                crypted_text += alphabet[(index + key) % len(alphabet)]
            else:
                crypted_text += char
    return crypted_text

def decrypt_Ceaser(crypted_text,key, alphabet=LETTERS_LOWER):
    return encrypt_Ceaser(crypted_text, -key, alphabet)

def crack_substring(crypted_substring, alphabet = LETTERS_LOWER,alphabet_frequency = ENGLISH_WITH_FREQUENCY):
    possible_keys = []
    for key, _  in alphabet_frequency.items():
        char_frequency = get_chars_frequencies(decrypt_Ceaser(crypted_substring, alphabet.index(key), alphabet),alphabet)
        
        if is_frequency_of_letters_in_text_correct(char_frequency, alphabet_frequency):
            possible_keys.append(key)
    if possible_keys == []:
        for letter in alphabet:
            possible_keys.append(letter)
    return possible_keys

def encrypt_Vigenere(plain_text, key, alphabet=LETTERS_LOWER):
    crypted_text = ''
    key_index = 0
    for char in plain_text:
        index = alphabet.find(char)
        if index != -1:
            crypted_text += alphabet[(index + alphabet.find(key[key_index])) % len(alphabet)]
            key_index = (key_index + 1) % len(key)
        else:
            index = alphabet.find(char.lower())
            if index != -1:
                crypted_text += alphabet[(index + alphabet.find(key[key_index])) % len(alphabet)].upper()
                key_index = (key_index + 1) % len(key)
            else:
                crypted_text += char
    return crypted_text

def decrypt_Vigenere(crypted_text, key, alphabet=LETTERS_LOWER):
    alphabet = alphabet.lower()
    if not are_all_letters_in_alphabet_uniqe(alphabet):
        raise Exception("Alphabet should contain only unique letters")
    #Delete all duplicates and sort the alphabet
    plain_text = ''
    key_index = 0
    for char in crypted_text:
        index = alphabet.find(char)
        if index != -1:
            plain_text += alphabet[(index - alphabet.find(key[key_index])) % len(alphabet)]
            key_index = (key_index + 1) % len(key)
        else:
            index = alphabet.find(char.lower())
            if index != -1:
                plain_text += alphabet[(index - alphabet.find(key[key_index])) % len(alphabet)].upper()
                key_index = (key_index + 1) % len(key)
            else:
                plain_text += char
    return plain_text

def dictionary_and_lenght_attack_Vigenere(crypted_text, key_length, dictionary = "dictionary_sorted.txt",alphabet = LETTERS_LOWER):
    with open(dictionary) as file:
        for word in file:
            word = word.strip()
            if len(word) == key_length:
                if ld.is_text_english(decrypt_Vigenere(crypted_text, word, alphabet)):
                    return word
    return None

@show_execution_time
def encrypt_a_file(input_file, output_file, key, alphabet):
    with open(input_file, 'r') as file:
        text = file.read()
    text = encrypt_Vigenere(text, key, alphabet)
    with open(output_file, 'w') as file:
        file.write(text)
        
@show_execution_time
def decrypt_a_file(input_file, output_file, key, alphabet):
    with open(input_file, 'r') as file:
        text = file.read()
    text = decrypt_Vigenere(text, key, alphabet)
    with open(output_file, 'w') as file:
        file.write(text)

def analyze_key_length_kesiski_method(crypted_text, alphabet=LETTERS_LOWER): #https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-Kasiski.html
    #Delete all of the non-alphabet characters
    # crypted_text = ''.join([char for char in crypted_text if char in alphabet])
    # print(crypted_text)
    
    repeated_substrings = find_repeated_substirngs_and_indexes(crypted_text)
    substring_distances = {}
    for substr, indexes in repeated_substrings.items():
        for i in range(len(indexes)-1):
            distance = indexes[i+1] - indexes[i]
            if(distance in substring_distances):
                substring_distances[distance] += 1
            else:
                substring_distances[distance] = 1 
    factors = {}
    for distance, count in substring_distances.items():
        for factor in (get_products(list(prime_factors(distance)))):
            if int(factor) in factors:
                factors[factor] += 1
            else:
                factors[factor] = 1
    
    factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)
    return factors

@show_execution_time
def crack_Vigenere(crypted_text, max_key_lenght=48,alphabet = LETTERS_LOWER):
    # max_key_lenght = 48
    crypted_text_without_non_alphabet_chars = remove_non_alphabet_chars(crypted_text, alphabet)
    possible_key_lengths = analyze_key_length_kesiski_method(crypted_text_without_non_alphabet_chars, alphabet)
    # print(f"Possible key lengths: {possible_key_lengths}")
    cracked_key = None
    for key_length, _ in possible_key_lengths:
        key = {}
        crack_progress = 0 
        for i in range(key_length):
            key[i] = crack_substring(crypted_text_without_non_alphabet_chars[i::key_length], alphabet)
        # print(key)
        amount_of_possible_keys = 1
        for key_combination in key.values():
            amount_of_possible_keys *= len(key_combination)
        print(f"Amount of possible keys: {amount_of_possible_keys}, key length: {key_length}")
        if amount_of_possible_keys < 5_000:
            print(f"Trying all possible keys...")
            for key_combination in itertools.product(*key.values()):
                
                cracked_key = ''.join(key_combination)
                # if crack_progress % 10000 == 0:
                #     print(f"Crack progress: {crack_progress}, key: {possible_key}")
                crack_progress += 1
                if ld.is_text_english(decrypt_Vigenere(crypted_text, cracked_key, alphabet)):
                        return cracked_key
    # for key_length, _ in possible_key_lengths:
        # else:
        #     print(f"Trying dictionary...whith key length: {key_length}")
        #     dictionary_name = 'dictionary_sorted.txt'
        #     if key_length > 12:
        #         dictionary_name = 'dictionary_sorted_reversed.txt'
        #     cracked_key = dictionary_and_lenght_attack_Vigenere(crypted_text,key_length,dictionary_name,alphabet)
        #     if cracked_key != None:
        #         return cracked_key
    return None

alphabet = "abcdefghijklmnopqrstuvwxyz"
key = 'couldbeanything'
to_encrypt = 'big_text.txt'
encrypted = 'encryptedVigenere.txt'
decrypted = 'decryptedVigenere.txt'
cracked = 'crackedVigenere.txt'
head_lines = 35
max_key_lenght = 48

encrypt_a_file(to_encrypt, encrypted, key, alphabet)
with open(encrypted) as file:
        head = [next(file) for _ in range(head_lines)]
head = ''.join(head)

cracked_key = crack_Vigenere(head,max_key_lenght,alphabet)

if cracked_key != None:
    print(f"\nThe cracked key is: {cracked_key}\n")
    decrypt_a_file(encrypted, cracked, cracked_key, alphabet)
else:
    print("The key was not cracked")
