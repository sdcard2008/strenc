import json as _json


"""
A very simple , customizable , string encoder and decoder.        
"""

__version__ = "0.1.4"
__author__ = "Saptak De"


class Strenc:
    @classmethod
    def __init__(self , key_path  = None):
        if key_path is not None:
            self.Keys = _json.load(open(f'{key_path}/keys.json' , 'r+')) 
        else:
            self.Keys = None   
    @classmethod        
    def return_keys(self , path : str):
    #file name should be keys.json
        try:
            json_file = open(f'{path}/keys.json' , 'r+')

            return _json.load(json_file)
        except:
            return False     
    @classmethod
    def load_keys(self , path : str):
        try:
            json_file = open(f'{path}/keys.json' , 'r+')

            self.Keys = _json.load(json_file)
        except:
            return False    

    @classmethod
    def encode(self  , msg:str , will_be_decoded_later_by_human : bool = False , keys : dict = None):
        if keys is None:
            keys = self.Keys
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
    @classmethod
    def decode(self  , msg:str , will_be_encoded_later_by_humans : bool = False ,  keys : dict = None):
        if keys is None:
            keys = self.Keys
        try:
            msg_words = str.lower(msg).split()

            for word_index , word in enumerate(msg_words):
                word_letter = list(word)

                for letter_index , letter in enumerate(word_letter):
                    
                    word_letter[letter_index] = _get_key_from_value(keys , letter)
                msg_words[word_index] = "".join(word_letter)
            if will_be_encoded_later_by_humans:
                return repr(" ".join(msg_words))
            return " ".join(msg_words)


        except:
            return False 

def _get_key_from_value(actual_dict : dict , val):
    for key,value in actual_dict.items():
        if val == value:
            return key
    return False                
        