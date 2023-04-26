LETTERS_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_LOWER = 'abcdefghijklmnopqrstuvwxyz'
LONG_TEXT = """This header should be the first thing seen when viewing this Project Gutenberg file.  Please do not remove it.  Do not change or edit the header without written permission. Please read the "legal small print," and other information about theeBook and Project Gutenberg at the bottom of this file.  Included isimportant information about your specific rights and restrictions inhow the file may be used.  You can also find out about how to make adonation to Project Gutenberg, and how to get involved."""
ENGLISH_ALPABET_WITH_INDEXES= {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25,'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
ENGLISH_WITH_FREQUENCY = {'a':0.082, 'b':0.015, 'c':0.028, 'd':0.043, 'e':0.127, 'f':0.022, 'g':0.02, 'h':0.061, 'i':0.07, 'j':0.0015, 'k':0.0077, 'l':0.04, 'm':0.024, 'n':0.067, 'o':0.075, 'p':0.019, 'q':0.00095, 'r':0.060, 's':0.063, 't':0.091, 'u':0.028, 'v':0.0098, 'w':0.024, 'x':0.0015, 'y':0.019, 'z':0.00074}
ENGLISH_WITH_FREQUENCY = {k: v * 100 for k, v in ENGLISH_WITH_FREQUENCY.items()}

# INDEX_OF_COINCIDENCE_ENGLISH = 0.0686

def show_execution_time(func):
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function: {func.__name__}\nExecution time: {end_time - start_time}")
        return result
    return wrapper

def get_chars_frequencies(text, alphabet = LETTERS_LOWER):
    char_frequency = {}
    for char in alphabet:
        char_frequency[char] = text.count(char)
    return char_frequency

def are_all_letters_in_alphabet_uniqe(alphabet):
    return len(alphabet) == len(set(alphabet))

def remove_extra_chars_from_alphabet(alphabet):
    return_alpabet = ''
    for char in alphabet:
        if char.isalpha():
            if char.lower() not in return_alpabet:
                return_alpabet += char
        elif char not in return_alpabet:
            return_alpabet += char
    return return_alpabet


def is_frequency_of_letters_in_text_correct(text_char_frequency: dict, true_char_frequency = ENGLISH_WITH_FREQUENCY,difference = 12.5):
    for char, frequency in true_char_frequency.items():
        if abs(text_char_frequency[char] - frequency)/frequency > difference:
            return False
    return True

def sort_dictionary(dictionary_path, output_path):
    with open(dictionary_path, 'r') as f:
        # lines = f.read().splitlines()
        lines = [line.lower() for line in f.read().splitlines()]
    lines.sort()
    with open(output_path, 'w') as f:
        for line in lines:
            f.write(line+'\n')
# def reverse_text_in_file(file_name, output_file_name):#just the lines not words
#     with open(file_name, 'r') as f:
#         lines = f.read().splitlines()
#     with open(output_file_name, 'w') as f:
#         for line in reversed(lines):
#             f.write(line+'\n')

# reverse_text_in_file('dictionary_sorted.txt', 'dictionary_sorted_reversed.txt')
