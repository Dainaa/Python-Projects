# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations
import random

### HELPER CODE ###
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


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text
    
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        copy = self.valid_words.copy()
        return copy
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        # vowels_permutation = get_permutations(VOWELS_LOWER)
        # vowels_permutation.pop(0) #remove the original aeiou
        # cipher = random.choice(vowels_permutation)     
        vowels_perm_upper = vowels_permutation.upper()
        alphabet = string.ascii_letters
        transpose_dict = {}
        for letter in alphabet:
            if letter in VOWELS_LOWER:
                ind = VOWELS_LOWER.index(letter)
                transpose_dict.update({letter: vowels_permutation[ind] })
            elif letter in VOWELS_UPPER:
                ind = VOWELS_UPPER.index(letter)
                transpose_dict.update({letter: vowels_perm_upper[ind]})
            elif letter in CONSONANTS_LOWER:
                ind = CONSONANTS_LOWER.index(letter)
                transpose_dict.update({letter: CONSONANTS_LOWER[ind]})
            elif letter in CONSONANTS_UPPER:
                ind = CONSONANTS_UPPER.index(letter)
                transpose_dict.update({letter: CONSONANTS_UPPER[ind]})
        # print(transpose_dict)
        return transpose_dict
        
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        message = self.get_message_text()
        encryption = []
        for letter in message:
            if letter in transpose_dict.keys():
                encryption.append(transpose_dict[letter])
            else:
                encryption.append(letter)
        
        return ''.join(encryption)
                
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        msg = self.message_text
        # print("message:",msg)
        perms = get_permutations(VOWELS_LOWER)
        # print(perms)
        decryptions = []
        correct_dec = {}
        for permutation in perms:
            dec = []
            compare_dict = {permutation[0]:'a',permutation[1]:'e',permutation[2]:'i',permutation[3]:'o',permutation[4]:'u'}
            compare_dict.update({permutation.upper()[0]:'A',permutation.upper()[1]:'','I':permutation.upper()[2],'O':permutation.upper()[3],'U':permutation.upper()[4]})
            for letter in msg:
                if letter in compare_dict.keys():
                    dec.append(compare_dict[letter])
                else:
                    dec.append(letter)
            decryptions.append(''.join(dec))
            # print(''.join(dec))
        for word in decryptions:
            x = word.split()
            valid = 0
            for item in x:
                if is_word(self.valid_words,item):
                    valid+=1
                correct_dec.update({word:valid})
        maxval = max(correct_dec.values())
        for k,v in correct_dec.items():
            if v == maxval:
                return k
                
        
            
            
            
if __name__ == '__main__':

    # Example test case
    # message = SubMessage("Hello World!")
    # permutation = "eaiuo"
    # enc_dict = message.build_transpose_dict(permutation)
    # print("Original message:", message.get_message_text(), "Permutation:", permutation)
    # print("Expected encryption:", "Hallu Wurld!")
    # print("Actual encryption:", message.apply_transpose(enc_dict))
    # enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    # print("Decrypted message:", enc_message.decrypt_message())
     
    #TODO: WRITE YOUR TEST CASES HERE
    message = SubMessage("I make robots for a living!")
    permutation = "euoai"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "U miko rabats far i luvung!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
