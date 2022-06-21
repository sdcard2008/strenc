import json as __json

"""
A very simple , customizable , string encoder and decoder.        
"""

__version__ = "0.1.2"
__author__ = "Saptak De"


def load_keys(path : str):
    #file name should be keys.json
    try:
        json_file = open(f'{path}/keys.json' , 'r+')

        return __json.load(json_file)
    except:
        return False     


def encode(keys : dict , msg:str , will_be_decoded_later_by_human : bool = False):
    try:
        msg_words = str.lower(msg).split()

        for word_index , word in enumerate(msg_words):
            word_letter = list(word)

            for letter_index , letter in enumerate(word_letter):
                word_letter[letter_index] = keys[letter]
            msg_words[word_index] = "".join(word_letter)
        
        if will_be_decoded_later_by_human:
            return repr(" ".join(msg_words))
        return " ".join(msg_words)        
    except:
        return False
def decode(keys : dict , msg:str , will_be_encoded_later_by_humans : bool = False):
    try:
        msg_words = str.lower(msg).split()

        for word_index , word in enumerate(msg_words):
            word_letter = list(word)

            for letter_index , letter in enumerate(word_letter):
                
                word_letter[letter_index] = __get_key_from_value(keys , letter)
            msg_words[word_index] = "".join(word_letter)
        if will_be_encoded_later_by_humans:
            return repr(" ".join(msg_words))
        return " ".join(msg_words)


    except:
        return False 

def __get_key_from_value(actual_dict : dict , val):
    for key,value in actual_dict.items():
        if val == value:
            return key
    return False                
