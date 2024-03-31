# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 14:43:46 2020

@author: Daina Noor
"""
import string
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


WORDLIST_FILENAME = 'words.txt'

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


possible_messages= {}
message_text = "Lipps, Asvph!"
valid_words = load_words(WORDLIST_FILENAME)
valid_messages = {}
cap_letters = string.ascii_uppercase
low_letters = string.ascii_lowercase
for i in range (26):
    decrypted_list = []
    for char in message_text:
        if char in cap_letters:
            new_index = cap_letters.index(char) - i
            if new_index < 0:
                new_index+=26
            decrypted_list.append(cap_letters[new_index])
        elif char in low_letters:
            new_index = low_letters.index(char) - i
            if new_index <0:
                new_index+=26
            decrypted_list.append(low_letters[new_index])
        else:
            decrypted_list.append(char)
            #after the loop has run for one shift value
    # print(''.join(decrypted_list))
    possible_messages.update({''.join(decrypted_list): i})

# print(possible_messages)    
for word in possible_messages.keys():
    x = word.split(" ")
    valid_occurence = 0       
    for item in x:
        if is_word(valid_words, item):
            valid_occurence+=1
    valid_messages.update({word: valid_occurence})
maxval = max(valid_messages.values())

for k,v in valid_messages.items():
    if v == maxval:
        print(v,k)
        
        
                
                    
            