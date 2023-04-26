import LanguageDetection as ld
from extras import *
from math import sqrt

from collections import defaultdict
from suffix_trees import STree
from itertools import combinations, combinations_with_replacement
from functools import reduce
import itertools

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

# Sample input string
# s = 'mississippi'

# Find all repeated substrings
# repeated_substrings = find_repeated_substirngs_and_indexes(s)

# Print out the repeated substrings and their indices
def print_repeated_substrings(repeated_substrings):
    for substr, indexes in repeated_substrings.items():
        print(f'{substr}: {indexes} - len({len(substr)})')

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

@show_execution_time
def dictionary_attack_Vigenere(crypted_text, alphabet=LETTERS_LOWER ):
    print(f"dictionary length: {len(ld.words)}")
    i=0
    for key in ld.words:
        if key =="AAAAAchompiklampibanana":
            print("found")
        if ld.is_text_english(decrypt_Vigenere(crypted_text, key, alphabet)):
            return key
    return None


    
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

@show_execution_time
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

def remove_non_alphabet_chars(text, alphabet):
    text = text.lower()
    return ''.join([char for char in text if char in alphabet])


def index_of_coincidence(text, alphabet=LETTERS_LOWER):
    index_coincidence = 0
    frequencies = get_chars_frequencies(text, alphabet)
    for char, freq in frequencies.items():
        index_coincidence += freq * (freq - 1)
    index_coincidence /= len(text) * (len(text) - 1)
    return index_coincidence

def get_average_index_of_coincidence(text, alphabet, key_length):
    average_index_of_coincidence = 0
    for i in range(key_length):
        average_index_of_coincidence += index_of_coincidence(text[i::key_length], alphabet)
    average_index_of_coincidence /= key_length
    return average_index_of_coincidence

def find_lenght_and_avarage_indexs_of_coincidence(text, max_key_length, alphabet = LETTERS_LOWER):
    avarage_indexes_of_coincidence = {}
    for key_lenght in range(1, max_key_length+1):
        avarage_indexes_of_coincidence[key_lenght] = get_average_index_of_coincidence(text, alphabet, key_lenght)
    avarage_indexes_of_coincidence = sorted(avarage_indexes_of_coincidence.items(), key=lambda x: x[1], reverse=True)
    return avarage_indexes_of_coincidence

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

def crack_Vigenere_with_key_length(crypted_text, key_length=45, alphabet= LETTERS_LOWER):
    cracked_text_without_non_alphabet_chars = remove_non_alphabet_chars(crypted_text, alphabet)
    key = {}
    crack_progress = 0 
    for i in range(key_length):
        key[i] = crack_substring(cracked_text_without_non_alphabet_chars[i::key_length], alphabet)
    # print(key)
    amount_of_possible_keys = 1
    for key_combination in key.values():
        amount_of_possible_keys *= len(key_combination)
    print(f"Amount of possible keys: {amount_of_possible_keys}, key length: {key_length}")
    if amount_of_possible_keys < 10_000:
        print(f"Trying all possible keys...")
        for key_combination in itertools.product(*key.values()):
            
            possible_key = ''.join(key_combination)
            # if crack_progress % 10000 == 0:
            #     print(f"Crack progress: {crack_progress}, key: {possible_key}")
            crack_progress += 1
            if ld.is_text_english(decrypt_Vigenere(crypted_text, possible_key, alphabet)):
                return possible_key
    return None

@show_execution_time
def crack_Vigenere_kesiski(crypted_text, alphabet= LETTERS_LOWER):
    crypted_text_without_non_alphabet_chars = remove_non_alphabet_chars(crypted_text, alphabet)
    possible_key_lengths = analyze_key_length_kesiski_method(crypted_text_without_non_alphabet_chars, alphabet)
    # print(f"Possible key lengths: {possible_key_lengths}")
    for key_length, _ in possible_key_lengths:
        key = crack_Vigenere_with_key_length(crypted_text, key_length, alphabet)
        if key != None:
            return key
    return None
        # for key_combination in itertools.product(*key.values()):
@show_execution_time
def crack_Vigenere_index_of_coincidence(crypted_text, max_key_lenght,alphabet= LETTERS_LOWER):#45 - longest english word
    crypted_text_without_non_alphabet_chars = remove_non_alphabet_chars(crypted_text, alphabet)
    possible_key_lengths = find_lenght_and_avarage_indexs_of_coincidence(crypted_text_without_non_alphabet_chars, max_key_lenght, alphabet) 
    # print(f"Possible key lengths: {possible_key_lengths}")
    for key_length, _ in possible_key_lengths:
        key = crack_Vigenere_with_key_length(crypted_text, key_length, alphabet)
        if key != None:
            return key
    return None

@show_execution_time
def encrypt_a_file(input_file, output_file, key, alphabet):
    with open(input_file, 'r') as file:
        text = file.read()
    text = encrypt_Vigenere(text, key, alphabet)
    with open(output_file, 'w') as file:
        file.write(text)
        
@show_execution_time
def decrypt_a_file(input_file, output_file, key, alphabet, block_size=100):
    with open(input_file, 'r') as read_file, open(output_file, 'w') as write_file:
        while True:
            text = read_file.read()
            if not text:
                break
            write_file.write(decrypt_Vigenere(text, key, alphabet))

#decrypt_a_file('output.txt', 'decryptedVigenere.txt', 'papaikozak', Alphabet)


def crack_a_file(input_file, output_file, max_key_lenght = 25,head_lines = 30,alphabet= LETTERS_LOWER, method = 'not kesiski'):
    with open(input_file) as file:
        head = [next(file) for _ in range(head_lines)]
    head = ''.join(head)
    if method == 'kesiski':
        key = crack_Vigenere_kesiski(head, alphabet)
    elif method == 'dictionary':
        key = dictionary_attack_Vigenere(head, alphabet)
    elif method == "all":
        key = ultimate_crack_Vigenere(head, max_key_lenght, alphabet)
    else:
        key = crack_Vigenere_index_of_coincidence(head, max_key_lenght,alphabet)
    print(f"The key is: {key}")
    if key != None:
        decrypt_a_file(input_file, output_file, key, alphabet)
    return key


def dictionary_and_lenght_attack_Vigenere(crypted_text, key_length, dictionary = "dictionary_sorted.txt",alphabet = LETTERS_LOWER):
    for word in ld.words:
        if len(word) == key_length:
            if ld.is_text_english(decrypt_Vigenere(crypted_text, word, alphabet)):
                return word
    # with open(dictionary) as file:
    #     for word in file:
    #         word = word.strip()
    #         if len(word) == key_length:
    #             if ld.is_text_english(decrypt_Vigenere(crypted_text, word, alphabet)):
    #                 return word
    return None

@show_execution_time
def ultimate_crack_Vigenere(crypted_text, max_key_lenght=48,alphabet = LETTERS_LOWER):
    # max_key_lenght = 48
    crypted_text_without_non_alphabet_chars = remove_non_alphabet_chars(crypted_text, alphabet)
    possible_key_lengths = find_lenght_and_avarage_indexs_of_coincidence(crypted_text_without_non_alphabet_chars,max_key_lenght, alphabet)
    # print(f"Possible key lengths: {possible_key_lengths}")
    cracked_key = None
    for key_length, _ in possible_key_lengths:
        cracked_text_without_non_alphabet_chars = remove_non_alphabet_chars(crypted_text, alphabet)
        key = {}
        crack_progress = 0 
        for i in range(key_length):
            key[i] = crack_substring(cracked_text_without_non_alphabet_chars[i::key_length], alphabet)
        # print(key)
        amount_of_possible_keys = 1
        for key_combination in key.values():
            amount_of_possible_keys *= len(key_combination)
        print(f"Amount of possible keys: {amount_of_possible_keys}, key length: {key_length}")
        if amount_of_possible_keys < 3:
            print(f"Trying all possible keys...")
            for key_combination in itertools.product(*key.values()):
                
                cracked_key = ''.join(key_combination)
                # if crack_progress % 10000 == 0:
                #     print(f"Crack progress: {crack_progress}, key: {possible_key}")
                crack_progress += 1
                if ld.is_text_english(decrypt_Vigenere(crypted_text, cracked_key, alphabet)):
                        return cracked_key
    # for key_length, _ in possible_key_lengths:
        else:
            print(f"Trying dictionary...whith key length: {key_length}")
            dictionary_name = 'dictionary_sorted.txt'
            if key_length > 12:
                dictionary_name = 'dictionary_sorted_reversed.txt'
            cracked_key = dictionary_and_lenght_attack_Vigenere(crypted_text,key_length,dictionary_name,alphabet)
            if cracked_key != None:
                return cracked_key
    return None


def home_menu(alphabet = LETTERS_LOWER):
    choose = input("\tMENU:\n1. Encrypt a file\n2. Decrypt a file\n3. Crack a file\n4. Exit\nChoose: ")
    if choose == '1':
        print("____Encrypt a file_____")
        key = input("Enter the key: ")
        input_file = input("Enter the input file name: ")
        output_file = input("Enter the output file name: ")
        if key != '' and input_file != '' and output_file != '':
            encrypt_a_file(input_file, output_file, key, alphabet)
        else:
            print("Wrong input")
    elif choose == '2':
        print("____Decrypt a file_____")
        key = input("Enter the key: ")
        input_file = input("Enter the input file name: ")
        output_file = input("Enter the output file name: ")
        if key != '' and input_file != '' and output_file != '':
            decrypt_a_file(input_file, output_file, key, alphabet)
        else:
            print("Wrong input")
            return
    elif choose == '3':
        print("____Crack a file_____")
        input_file = input("Enter the input file name: ")
        output_file = input("Enter the output file name: ")
        print("Choose method:\n1. Index of coincidence\n2. Kesiski\n3. Dictionary\n4. All of them")
        method = input()
        max_key_lenght = 0
        head_lines = 0
        
        if method == '1':
            max_key_lenght = int(input("Enter the max key lenght: "))
            head_lines = int(input("Enter the number of lines to check: "))
            method = 'index of coincidence'
        elif method == '2':
            head_lines = int(input("Enter the number of lines to check: "))
            method = 'kesiski'
        elif method == '3':
            head_lines = int(input("Enter the number of lines to check: "))
            method = 'dictionary'
        elif method == '4':
            max_key_lenght = int(input("Enter the max key lenght: "))
            head_lines = int(input("Enter the number of lines to check: "))
            method = 'all'
        else:
            print("Wrong input")
            return
        crack_a_file(input_file, output_file, max_key_lenght, head_lines, alphabet, method)
    elif choose == '4':
        return

# key  = "AAAAAchompiklampibanana"

# encrypt_a_file('1.txt', '1_out.txt',key, LETTERS_LOWER)
# decrypt_a_file('1_out.txt', '1_decrypted.txt',key, LETTERS_LOWER)
# with open('1_out.txt', 'r') as f:
#     head = [next(f) for x in range(10)]
# head = ''.join(head)
# print(head)
# print(decrypt_Vigenere(head, key, LETTERS_LOWER))
# ld.change_dictionary('english_words.txt_sorted.txt')
# print(dictionary_attack_Vigenere(head))
        


#https://pages.mtu.edu/~shene/NSF-4/Tutorial/VIG/Vig-Kasiski.html
# alphabet = "abcdefghijklmnopqrstuvwxyz"
# key = 'babe'
# to_encrypt = 'big_text.txt'
# encrypted = '1_out.txt'
# decrypted = 'decryptedVigenere.txt'
# cracked = 'crackedVigenere.txt'
# head_lines = 50
# max_key_lenght = 10

# encrypt_a_file(to_encrypt, encrypted, key, alphabet)

# with open(encrypted) as file:
#     head = [next(file) for _ in range(head_lines)]
# head = ''.join(head)
# print(crack_Vigenere_kesiski(head, alphabet))

# encrypt_a_file(to_encrypt, encrypted, key, alphabet)
# with open(encrypted) as file:
#         head = [next(file) for _ in range(head_lines)]
# head = ''.join(head)

# cracked_key = crack_a_file(encrypted,cracked,max_key_lenght,head_lines,alphabet, 'index of coincidence')
# cracked_key = crack_a_file(encrypted,cracked,max_key_lenght,head_lines,alphabet, 'kasinski')

# decrypt_a_file(encrypted, decrypted, key, alphabet)
# if cracked_key != None:
#     print(f"\nThe cracked key is: {cracked_key}\n")
#     # decrypt_a_file(encrypted, cracked, cracked_key, alphabet)
# else:
#     print("The key was not cracked")
# crack_Vigenere_kesiski(head, alphabet)
# 30724527451069218816000000000 - pneumonoultramicroscopicsilicovolcanoconiosis
# 326135832690844237824000000 - astrospherecentrosomic



if __name__ == "__main__":
    alphabet = input("Enter the path to the alphabet file: ")
    if alphabet == '':
        alphabet = LETTERS_LOWER
    else:
        with open(alphabet) as file:
            alphabet = file.read()
        alphabet = remove_extra_chars_from_alphabet(alphabet)
    dictionary_for_crack = input("Enter the path to the dictionary file: ")
    if dictionary_for_crack != '':
        sort_dictionary(dictionary_for_crack, dictionary_for_crack+'_sorted.txt')
        dictionary_for_crack = dictionary_for_crack+'_sorted.txt'
        ld.change_dictionary(dictionary_for_crack)
    while True:
        home_menu(alphabet)
    
    
    

    
    