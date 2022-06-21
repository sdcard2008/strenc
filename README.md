# STRENC : A String Encode/Decoder

*v0.1.1*

[**TestPyPi Link**](https://test.pypi.org/project/strenc/)

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
pip install -i https://test.pypi.org/simple/ strenc
```

**Errors**

1. 'pip' is not recognized as an internal or external command operable program or batch file.
*Solution* : Check if python is in your ```PATH``` variable.



### customizekeys.exe (command line tool)

- To generate a keys.json file run this command:
    ```customizekeys -genkeys [where_you_want_to_put_keys]```
put your desired path instead of ```[where_you_want_to_put_keys]```



>*P.S : Currently , it cannot make folders if not found. So make the folders , then run the command.*    
- To do anything besides make a new keys.json file , you have to add the arguement ```-keypath [path_to_your_keys]```
where , ```[path_to_your_keys]``` is where your keys.json file is located.
for example , lets say path to the key is ```./path/to/key/keys.json```
then to fetch the keys , you run:
    ```customizekeys -keypath ./path/to/key```
- To change a specific key or rewrite all the keys , you have to do ```customizekeys -keypath [path_to_your_keys] -change{all/[specific_char]}```
if value is all , then it will prompt you for every single chararcter. Else , it will ask for the specific character you asked for.
>I will not be adding ```-keypath [path_to_your_keys]``` from now on. But you should while doing anything besides generating a new key.
- To get a copy of the current keys , simply add ```-copy true``` to your command.
- To get the char that will replace a specific character , just add ```-k [specific_char]``` to your command , where ```[specific_char]``` is the character you are searching for.

### STRENC module documentation

```strenc.load_keys(path : str)```

```python
    def load_keys(path : str):
        #file name should be keys.json
        try:
            json_file = open(f'{path}/keys.json' , 'r+')

            return json.load(json_file)
        except:
            return False 
 ```
 Used to load the keys.json file. ```path``` should be a string. Returns either a dictionary or a boolean(False)

 ```strenc.encode(keys : dict , msg : str , would_be_decoded_by_human : bool) ```

 ```python
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
 ```
 Takes a dictionary with keys (preferably loaded with ```strenc.load_keys(path:str)```) , the message to encode , and an optional arguement if it would be manually put in a function (By default it's False).
 Returns the encoded message using the keys.

 ```strenc.decode(keys : dict , msg : str , would_be_encoded_by_human : bool)```

 ```python
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

 ```
 Arguements same as ```strenc.encode(keys : dict , msg : str , would_be_decoded_by_human : bool)```. Returns the decoded message from a encoded message. ```__get_key_from_value(keys : dict , char:str)``` is a function to get key from value.


 ```strenc.__get_key_from_value(keys : dict , char : str)```

 ```python
 def __get_key_from_value(actual_dict : dict , val):
    for key,value in actual_dict.items():
        if val == value:
            return key
    return False                

 ```        
