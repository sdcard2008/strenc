import json as _json


"""
A very simple , customizable , string encoder and decoder.        
"""

__version__ = "0.2.4"
__author__ = "Saptak De"


class Strenc:
    @classmethod
    def __init__(self , key_path  = None):
        if key_path is not None:
            self.KeyFile = open(f'{key_path}/keys.json' , 'r+')
            self.Keys = _json.load(self.KeyFile) 
        else:
            self.Keys = None
            self.KeyFile = None   
    @classmethod        
    def return_keys(self , path : str):
    #file name should be keys.json
        try:
            self.KeyFile = open(f'{path}/keys.json' , 'r+')

            return _json.load(self.KeyFile)
        except Exception as e:
            print(e)     
    @classmethod
    def load_keys(self , path : str):
        try:
            self.KeyFile = open(f'{path}/keys.json' , 'r+')

            self.Keys = _json.load(self.KeyFile)
        except Exception as e:
            print(e)
               

    @classmethod
    def encode(self  , msg:str , will_be_decoded_later_by_human : bool = False , keys : dict = None):
        if keys is None:
            keys = self.Keys
        try:
            msg_letters = list(msg)

            for letter_index ,letter in enumerate(msg_letters):
                msg_letters[letter_index] = keys[letter]
            if will_be_decoded_later_by_human:
                return repr("".join(msg_letters))
            return "".join(msg_letters)    
        except Exception as e:
            print(e)
            
    @classmethod
    def decode(self  , msg:str , will_be_encoded_later_by_humans : bool = False ,  keys : dict = None):
        if keys is None:
            keys = self.Keys
        try:
            msg_letters = list(msg)

            for letter_index ,letter in enumerate(msg_letters):
                msg_letters[letter_index] = _get_key_from_value(keys , letter)
            if will_be_encoded_later_by_humans:
                return repr("".join(msg_letters))
            return "".join(msg_letters)

        except Exception as e:
            print(e)
    @classmethod
    def version(self):
        return __version__
    @classmethod
    def get_val_of_key(self ,key , keys : dict = None):
        if keys is None:
            keys = self.Keys
        return keys[key]
    @classmethod
    def get_keys(self):
        if self.Keys is not None:
            return self.Keys
        else:
            raise Exception('keys are not initialized')
    @classmethod
    def change_key(self , permanent : bool , key_to_change = None , val = None):
        if self.Keys is None:
            raise Exception('keys are not initialized')
        self.Keys[key_to_change] = val

        if permanent:
            self.KeyFile.seek(0)
            self.KeyFile.truncate(0)        
            _json.dump(self.Keys , self.KeyFile , indent=4)




def _get_key_from_value(actual_dict  , val):
    for key,value in actual_dict.items():
        if val == value:
            return key
    return False                
        