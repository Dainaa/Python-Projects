# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

word_list = load_words()
#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    #first convert the word to lowercase
    lowercase_word = word.lower()
    wordlen = len(word)
    letter_score_sum = 0 #A variable to store the first component of the score in
    #letter_score sum = a sum of all the individual scores of the letters used
    for char in lowercase_word:
        if char in SCRABBLE_LETTER_VALUES:
            #so for every character in the word, if the character is in the scrabble letter values dictionary
            letter_score_sum += SCRABBLE_LETTER_VALUES[char]
    #At this point we should have a total scrabble type score
    
    score_component_two = (7*wordlen) - (3*(n-wordlen))
    if score_component_two > 1:
        total_score = letter_score_sum * score_component_two
        return total_score
    else:
        total_score = letter_score_sum * 1
        return total_score
    
    
    
#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    #goes over all the keys/letters and prints them out as many times as they occur
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3)) #we want one third of the hand to be vowels

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    #I want to replace one of the vowels with an asterisk, randomly
    vowel_replacement = random.choice(list(hand)) #Will select a random key-value pair
    hand[vowel_replacement] -= 1 #reduce the occurence of this key value by 1, so if you had 2 you now have 1
    #if you had 1 you should now have 0
    if hand[vowel_replacement] == 0:
        del hand[vowel_replacement] #removing the vowel if it doesn't exist in the hand anymore
        
    #Now add the asterisk
    new_element = {"*":1}
    hand.update(new_element)
    
    
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    #new_hand = {} #Create an empty dictionary to store the new hand in
    new_hand = hand.copy() #Store a copy of the original hand in new hand
    #Need to iterate over the word and remove occurences of each character from the hand
    lowercase_word = word.lower()
    for char in lowercase_word:
        if char in new_hand.keys():
            if new_hand[char] > 0:
                new_hand[char] =  new_hand[char] - 1
            else:
                new_hand[char] = 0
        else:
            pass
    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    #Part 1: Check if we have the letters in the hand to make the word
    lower_word = word.lower()
    for char in lower_word:
        if char in hand.keys():
            if hand[char] > 0:
                hand = update_hand(hand, char)
            elif hand[char] == 0:
                #if the player has no more tiles left of said letter
                return False
               # break
        elif char not in hand.keys():
            #if the user has tiles in the word that arent in the hand
            return False
           # break
    
    #The program should be here if the else blocks are not executed and the user has all the appropriate tiles
    #Now to check if the word is in the word list
    if lower_word in word_list:
        return True  
    
    #If the above if block is skipped, the word isn't in the word list
    #Does it use a valid wildcard?
    if wildcard_exists(lower_word,word_list):
        return True
    
    else:
        return False

def is_valid_wildcard(wildcard, check):
    """
    Compares wildcard word with check word and returns True if match is valid

    """    
    len_wildcard = len(wildcard)
    len_check = len(check)
    if len_wildcard == len_check:
        for i in range(len_wildcard):
            if wildcard[i] == check[i]:
                pass
            elif wildcard[i] == "*" and check[i] in VOWELS:
                pass
            else:
                return False
                break
            
        return True
    
    elif len_wildcard != len_check:
        return False
    
def wildcard_exists(wildcard,word_list):
    """
    """
    valid_replacements = []
    for word in word_list:
        if is_valid_wildcard(wildcard, word) == True:
            valid_replacements.append(word)
#            print(word)
        else:
            pass
    if len(valid_replacements) > 0:
        return True
    else:
        return False
        
    
#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    count = 0
    for key in hand:
        count = count + hand[key]
    #print(count)
    return count

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    score = 0 #Score before a hand is played = 0
    # Keep track of the total score
    # As long as there are still letters left in the hand:
    while (calculate_handlen(hand)) > 0:
        # Display the hand
        print("Current hand: ",end=' ') 
        display_hand(hand)
        # Ask user for input
        played_word = input("Enter word, or '!!' to indicate that you are finished: ")
        # If the input is two exclamation points:
        if played_word == "!!":
            # End the game (break out of the loop)
            print("Total score for this hand =",score,"points.")
            break

            
        # Otherwise (the input is not two exclamation points):
        elif played_word != "!!":
            # If the word is valid:
            if is_valid_word(played_word,hand,word_list) == True:
                # Tell the user how many points the word earned,
                round_score= get_word_score(played_word, calculate_handlen(hand))
                print(played_word,"earned",round_score,"points.", end =' ')
                # and the updated total score
                score+=round_score
                print("Total: ",score,"points")
                 

            # Otherwise (the word is not valid):
            elif is_valid_word(played_word,hand,word_list) == False:
                # Reject invalid word (print a message)
                print("That is not a valid word. Please choose another word. ")
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, played_word)

    # Game is over (user entered '!!' or ran out of letters),
    if calculate_handlen(hand) == 0:
        print("Ran out of letters. Total score for this hand =",score, "points.")
    # so tell user the total score

    # Return the total score as result of function
    return score



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#
def is_valid_sub(hand, letter):
    """
    Check if the user has input a valid letter for substitution.
    """
    if letter in hand:
        return letter
    else:
        while letter not in hand:
            print("Oops. That letter is not in your hand.")
            print("Current hand: ", end =' ')
            display_hand(hand)
            letter = input("Choose another letter to replace: ")
        
        #We step out of this function when the letter is in hand
        return letter
        
def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    letter = is_valid_sub(hand, letter) #Makes sure the user has input a valid letter to be replaced

    alphabet = VOWELS+CONSONANTS #Make a string containing all the alphabet
    subbed_hand = hand.copy()
#    print(subbed_hand)
    replacement_letter = random.choice(list(alphabet)) #Choose a random letter from this list
    
#    print(replacement_letter)
#    print(letter, subbed_hand[letter])    
    while subbed_hand == hand:
        if replacement_letter not in subbed_hand: #If the random letter is not already present in the hand
#         print("Random letter not already present in hand")
            replaced_element = {replacement_letter: subbed_hand[letter]} #make a key value pair of the new letter
        #Give it the same value as the letter you intend to replace
            del(subbed_hand[letter])
            subbed_hand.update(replaced_element)
            return subbed_hand
            break
##            
        else:
            replacement_letter = random.choice(list(alphabet)) 
#        
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      If the user inputs 'yes', they will replay the hand and keep 
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    hand_number = int(input("Enter total number of hands: "))
    HAND_SIZE = 7
    total_score = 0 #Keep track of score over all hands played
    sub_flag = False
    replay_flag = False
    while hand_number > 0:
        hand = deal_hand(HAND_SIZE)
        print("Current hand: ",end =' ')
        display_hand(hand)
        
        if sub_flag == False:
            sub_check = input("Would you like to substitute a letter? ")
      
            if sub_check.lower() == 'yes':
                letter = input("Which letter would you like to replace? ")
                hand = substitute_hand(hand,letter) #Call substitute function, this will return a new hand
                sub_flag = True
                
        #The above block is only carried out if the user asks to replace a letter
        #If they don't then we get to this point:
        #If they do, the hand gets replaced and we get to this point:
        score = play_hand(hand, word_list)
        print("----------------")
        
        
        if replay_flag == False:
            replay_check = input("Would you like to replay the hand? ")
        
            if replay_check.lower() == 'yes':
                score = play_hand(hand,word_list)
                replay_flag = True
                
            
        #else if replay_flag == true, we've already replayed:
        total_score+=score
        hand_number = hand_number - 1
    
    print("Total score over all hands:",total_score)
#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
#    word_list = load_words()
    play_game(word_list)
