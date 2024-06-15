import json as _json
import string as _str
import random as _rand

"""
A very simple , customizable , string encoder and decoder.        
"""

__version__ = "0.3.2"
__author__ = "Saptak De"


class Strenc:
    @classmethod
    def __init__(self , key_path  = None , seed : int = None):
        if key_path is not None:
            self.KeyFile = open(f'{key_path}/keys.json' , 'r+')
            self.keys_dict = _json.load(self.KeyFile)
            self.clen = self.keys_dict["chunk-length"]
            self.Keys = self.keys_dict["keys"]
        
        elif seed is not None:
            self.keys_dict = _return_seed_value(seed)
            self.clen = self.keys_dict["chunk-length"]
            self.Keys = self.keys_dict["keys"]         
        else:
            self.Keys = None
            self.KeyFile = None   
    @classmethod        
    def return_keys(self , path : str):
    #file name should be keys.json
        try:
            self.KeyFile = open(f'{path}/keys.json' , 'r+')

            return _json.load(self.KeyFile)["keys"]
        except Exception as e:
            print(e)     
    @classmethod
    def load_keys(self , path : str):
        try:
            self.KeyFile = open(f'{path}/keys.json' , 'r+')

            self.Keys = _json.load(self.KeyFile)["keys"]
        except Exception as e:
            print(e)
               
    def load_keys_seed(self , seed:int):
        try:
            self.Keys = _return_seed_value(seed)["keys"]
        except Exception as e:
            print(e)
            
    @classmethod
    def encode(self  , msg:str , human_readable : bool = False , keys : dict = None , folds=1):
        if keys is None:
            keys = self.Keys
        try:
            for fold in range(folds):
                msg_letters = list(msg)

                for letter_index ,letter in enumerate(msg_letters):
                    if letter not in _str.whitespace:
                        msg_letters[letter_index] = keys[letter]
                msg = "".join(map(str,msg_letters))        
            if human_readable:
                return repr(msg)
            return msg    
        except Exception as e:
            print(e)
            
    @classmethod
    def decode(self  , msg:str , human_readable : bool = False ,  keys : dict = None , folds=1) :
        
        
        if keys is None:
            keys = self.Keys
        try:    
            for dec_fold in range(folds):
                    
                msg_words = _intersperse(msg.split(' ') , ' ')
                
                
                msg_letters = [word[split_c:split_c+self.clen] for word in msg_words for split_c in range(0, len(word) , self.clen)]
                
                for letter_index ,letter in enumerate(msg_letters):
                    if letter not in _str.whitespace:
                        msg_letters[letter_index] = _get_key_from_value(keys , letter)
                msg = "".join(map(str ,msg_letters))    
            if human_readable:
                return repr(msg)
            return msg

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
def  _intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result        
def _return_seed_value(seed_and_clen : str):
    tmp_return_value = {}
    specific_clen = 1
    try:
       seed , specific_clen = [int(i) for i in seed_and_clen.split("@")]
    except:
        pass    
    tmp_return_value["chunk-length"] = specific_clen
    tmp_return_value["keys"] = {}
    ALPHABETS = _str.ascii_letters + _str.punctuation + _str.digits
    ALPHABETS_LIST = list(ALPHABETS)
    _rand.seed(seed)
    
    rand_state = _rand.getstate()
    
    _rand.setstate(rand_state)
    used_assignments_rand = []
    for letter in ALPHABETS:
        temp_rand_key = []
        while True:
            for __ in range(specific_clen):
                temp_rand_key.append(_rand.choice(ALPHABETS_LIST))
            rand_char = "".join(temp_rand_key)
            
            if specific_clen > 1 and rand_char not in used_assignments_rand:
                used_assignments_rand.append(rand_char)            
                break
            elif specific_clen  == 1:
                ALPHABETS_LIST.remove(rand_char)
                break
            
            
            

        tmp_return_value["keys"][letter] = rand_char
    return tmp_return_value
    