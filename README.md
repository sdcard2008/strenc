# STRENC : A String Encode/Decoder

[![PyPI version](https://badge.fury.io/py/strenc.svg)](https://badge.fury.io/py/strenc) [![Downloads](https://pepy.tech/badge/strenc)](https://pepy.tech/project/strenc)


[**PyPi Link**](https://pypi.org/project/strenc/)



*v0.1.0 and v0.1.1 can be found at[TestPyPi](https://test.pypi.org/project/strenc/)*

***Please note that strenc is currently under devolpement***

## What is strenc?

Strenc , or String(str)Encoder(enc) , is a pip package that will encode and decode a piece of string into cryptic message and to normal text.

## Why is it 'customizable'?

We have a command line tool added with the package , that will help you create keys , check which character is replaced by which and change the keys.

## Why am i going to use this?
Honestly , I have no clue.

******

# Documentation
### How to install strenc
If you have python installed , run this from your command prompt:
```batch 
pip install strenc
```

**Errors**

1. 'pip' is not recognized as an internal or external command operable program or batch file.
*Solution* : Check if python is in your ```PATH``` variable.



### customizekeys (command line tool)

>### **From v0.2.4 , the command line tool is renamed from ```customizekeys``` to ```strenc```**

- To generate a keys.json file run this command:
    ```customizekeys -genpath [where_you_want_to_put_keys] -type [manual/random]```
    > ```-type [manual/random]``` is available from v0.1.4 . 
    for ```-type``` , put either manual or random as your option. If manual , then you get to manually choose the keys for every character , else if random is choosen , you get a random key. 


put your desired path instead of ```[where_you_want_to_put_keys]```
Also , if you want to generate the file in a relative path , add a *.* before the path.
For example , let's say we have this folder here:
```
sample-py
    -main.py
```

so if we want to make a keys.json file there , we have to do:
```customizekeys -genpath ./ -genpath[your_type]```




>*P.S : before v0.1.3 , it cannot make folders if not found. So make the folders , then run the command.*    
- To do any key file manipulation , besides to make a new keys.json file , you have to add the arguement ```-keypath [path_to_your_keys]```
where , ```[path_to_your_keys]``` is where your keys.json file is located.
for example , lets say path to the key is ```./path/to/key/keys.json```
then to fetch the keys , you run:
    ```customizekeys -keypath ./path/to/key```
- To change a specific key or rewrite all the keys , you have to do ```customizekeys -keypath [path_to_your_keys] -change{all/[specific_char]}```
if value is all , then it will prompt you for every single chararcter. Else , it will ask for the specific character you asked for.
>I will not be adding ```-keypath [path_to_your_keys]``` from now on. But you should while doing anything besides generating a new key.
- To get a copy of the current keys , simply add ```-copy true``` to your command.
- To get the char that will replace a specific character , just add ```-k [specific_char]``` to your command , where ```[specific_char]``` is the character you are searching for.
- From *v0.1.2* , you can make a config file using ```customizekeys -config [setup/specific_settings]```. You can set the key_path in the file so you don't have to put ```-keypath [path_to_your_keys]``` all the time. And to change a specific settings from specific section , just do ```-config [SECTION]/[settings]``` 

# v0.2.5

- Added command ```strenc -encfile [filepath]```. As the name suggests , it encodes any given .txt file. Path to keys.json should be given.
- Added command ```strenc -decfile [filepath]```. This command decodes a encoded file. Also needs path to keys.json file.

> From *v0.2.2* , there is a new config option called 'show-log' under DEBUG section. If 'show-log' is set to true , then it will log errors at the same directory as the command was ran in a file called 'customizekeys.log'. By default DEBUG  is set to false

- From *v0.1.3* , you can check current version of strenc by running ```customizekeys -version show```


### STRENC module documentation
> *From ```v0.1.4``` , the methods are stored in a class called ```Strenc```*

```def __init__(self , key_path=None)```

Constructor of the new ```Strenc``` class. ```key_path``` is an optional arguement which , if given , will load the key on initialization.

```strenc.load_keys(path : str)```

```python
    def load_keys(self ,path : str):
        #file name should be keys.json
        try:
            json_file = open(f'{path}/keys.json' , 'r+')
            self.Keys = json.load(json_file)
        except:
            return False 
 ```
 Used to load the keys.json file. ```path``` should be a string. Sets ```Keys``` variable from class Strenc to a dictionary.

 ```strenc.encode(self , msg : str , human_readable : bool , keys : dict) ```

 ```python
 def encode(self  , msg:str , human_readable : bool = False , keys : dict = None , folds=1):
    if keys is None:
        keys = self.Keys
    try:
        for fold in range(folds):
            msg_letters = list(msg)

            for letter_index ,letter in enumerate(msg_letters):
                msg_letters[letter_index] = keys[letter]
            msg = "".join(map(str,msg_letters))        
        if human_readable:
            return repr(msg)
        return msg    
    except Exception as e:
        print(e)
 ```
 Takes a dictionary with keys  , which can be either stored in a variable using ```strenc.return_keys(self , path : str)``` , or can be loaded using ```strenc.load_keys(self , path : str)```(preferably loaded with ```strenc.load_keys(path:str)```) , the message to encode , an optional arguement to output the encoded string with special characters (By default it's False) , and a ```folds``` arguement deciding how many times the message would be encoded (By default it is 1).
 Returns the encoded message using the keys.

 ```def decode(self  , msg:str , human_readable : bool = False ,  keys : dict = None , folds=1)```

 ```python
 def decode(self  , msg:str , human_readable : bool = False ,  keys : dict = None , folds=1) :
        
    if keys is None:
        keys = self.Keys
    try:    
        for dec_fold in range(folds):
                
            msg_letters = list(msg)

            for letter_index ,letter in enumerate(msg_letters):
                msg_letters[letter_index] = _get_key_from_value(keys , letter)
            msg = "".join(map(str ,msg_letters))    
        if human_readable:
            return repr(msg)
        return msg

    except Exception as e:
        print(e)
 ```
 Arguements same as ```strenc.encode(self , msg : str , human_readable : bool , keys : dict)```. Returns the decoded message from a encoded message. ```_get_key_from_value(keys : dict , char:str)``` is a function to get key from value.
 >The ```folds``` arguement should be the same as the ```folds``` arguement used during the encoding process

```strenc.return_keys(self , path : dict)```

```python
def return_keys(self , path : str):
    #file name should be keys.json
    try:
        json_file = open(f'{path}/keys.json' , 'r+')

        return _json.load(json_file)
    except:
        return False
```
Same as ```strenc.load_keys(self , path : str)``` , but returns the dictionary of keys rather than storing it in a class variable.

 ```strenc.__get_key_from_value(keys : dict , char : str)```

 ```python
 def _get_key_from_value(actual_dict : dict , val):
    for key,value in actual_dict.items():
        if val == value:
            return key
    return False                

 ``` 

 Return installed strenc version

 ```strenc.version()```

 ```python
 def version(self):
    return __version__
 ```   
Gets the value of a certain key.

 ```strenc.get_val_of_key(self ,key , keys : dict = None)```

```python 
 def get_val_of_key(self ,key , keys : dict = None):
        if keys is None:
            keys = self.Keys
        return keys[key]
 ```  

 Return the current keys.json file

 ```strenc.get_keys(self)```

 ```python
 def get_keys(self):
        if self.Keys is not None:
            return self.Keys
        else:
            raise Exception('keys are not initialized')
 ```

 Changes a certain key from the keys dictionary. You can make it either temporary or permanent using ```permanent``` argument.

 ```strenc.change_key(self , permanent : bool , key_to_change = None , val = None)```

 ```python
 def change_key(self , permanent : bool , key_to_change = None , val = None):
        if self.Keys is None:
            raise Exception('keys are not initialized')
        self.Keys[key_to_change] = val

        if permanent:
            self.KeyFile.seek(0)
            self.KeyFile.truncate(0)        
            _json.dump(self.Keys , self.KeyFile , indent=4)   
 ```



