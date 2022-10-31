
#PROGRAM TO RUN COMMAND "customizekeys"

#imports
import json as __json
import argparse as __argparse
import configparser as __configparser
from os.path import exists as __exists
from os import makedirs as __makedirs
from os import remove as __remove
from os.path import basename as __basename  
from random import choice as __choice 
import string as _string
import logging as __logging

__version__ = '0.2.4'
__author__ = 'Saptak De'

__config = __configparser.ConfigParser() # to parse strenc-config.ini
# err logging func
def __err_logging(debug : bool  , logger , err:Exception):
    if debug == 'true':
        logger.error(err)
        return True
    return False       

def __main():
    
        

    parser = __argparse.ArgumentParser() # argument parser

    # all the commands for 'strenc'
    SYSTEM_ARGS = [
        {'com' : '-k' , 'val' : '--Key' , 'help' : 'Get key of a specific char'} ,
        {'com' : '-copy' , 'val' : '--Copy' , 'help' : 'Get a copy of the keys'} ,
        {'com' : '-change' , 'val' : '--Type' , 'help' : 'Either change the whole key file or change a specific char'},
        {'com' : '-genpath' , 'val' : '--Path' , 'help' : 'Create a keys.json file in root directory'} ,
        {'com' : '-path' , 'val' : '--KeyPath' , 'help' : 'Loaction of keys.json' } ,
        {'com' : '-version' , 'val' : '--ShowOrNot' , 'help' : 'Outputs installed version of strenc'} ,
        {'com' : '-config' , 'val' : '--ConfigType' , 'help' : 'Setup or update config(Please run this command at the same folder as keys.json)' } ,
        {'com' : '-type' , 'val' : '--GenKeyType' , 'help' : 'Key generator options. Wont work if -genpath not given'} ,
        {'com' : '-encfile' , 'val' : '--EncodeFile' , 'help' : 'Encode a txt file'} ,
        {'com' : '-decfile' , 'val' : '--DecodeFile' , 'help' : 'Decode a encoded txt file'}

    ]
    # add all the commands to the parser
    for command in SYSTEM_ARGS:
        parser.add_argument(command['com'] , command['val'] , help =command['help'])

    args = parser.parse_args() # initialize args fetcher
 
    
    DEBUG = 'false' # to show logs
    
    
    # get config and do stuff accordingly
    if args.KeyPath:
        path_to_keys = args.KeyPath
    elif __exists('strenc-config.ini'):
        __config.read('strenc-config.ini')

        try:
            path_to_keys = __config.get('KEYPATH' , 'keypath')
        except:
            print('No keypath settings in KEYPATH section in key-config.ini. -k , -copy , -change will not work')
        try:
            DEBUG = __config.get('DEBUG' , 'show-log')
        except:
            pass
                        
    
    else:
        print('-path [key_path] is absent and strenc-config.ini is absent. -k , -copy , -change , -encfile will not work') 
              
    # initialize a logger if DEBUG is set to true
    if DEBUG == 'true':
        __logging.basicConfig(filename='strenc.log' , filemode='w' , format='%(asctime)s - %(message)s')
    elif __exists('strenc.log') and DEBUG == 'false':
        __remove('strenc.log')
    try:
        file_json = open(f'{path_to_keys}/keys.json' , 'r+')
        enc_keys = __json.load(file_json)
        letters_for_keys = enc_keys.keys()
    except:
        print('Cannot find keys.json from given path. -k , -copy , -change , -encfile will not work.')


    type_with_genkeys = False

     



    # replace a certain key
    if args.Type:
        if args.Type == 'all':    
            try:
                for enc_key_keys in letters_for_keys:
                    replace_with = input(f'Replace {repr(enc_key_keys)} with :')

                    enc_keys[enc_key_keys] = replace_with
            except Exception as err:
                __err_logging(DEBUG, __logging , err)
                print('-change did not work. Either -path is wrong or it is absent.')    
        else:
            
            try:
                if args.Type in letters_for_keys:    
                    replace_with = input(f'Replace {repr(args.Type)} with :')

                    enc_keys[args.Type] = replace_with
                else:
                    print('Either input "all" or a specific character after -change')    
            except Exception as err:
                __err_logging(DEBUG, __logging , err)
                print('-change did not work. Either -path is wrong or it is absent.')    
            
        print('Dumping data to json....')
        try:
            file_json.seek(0)
            file_json.truncate(0)

            __json.dump(enc_keys , file_json , indent=4)
            print('keys.json is updated')
        except Exception as err:
            __err_logging(DEBUG, __logging , err)
            print('Dumping data to keys.json failed')    
    # get value of a key
    if args.Key:
        try:
            print(f'Key for {repr(args.Key)} is : {repr(enc_keys[args.Key])}')
        except Exception as err:
            __err_logging(DEBUG, __logging , err)
            print('-k did not work. Either -path is wrong or it is absent. Or the character does not exist in the keys.json file')    
    # get a copy of current keys.json file
    if args.Copy:
        if args.Copy == 'true':
            try:
                print(enc_keys)
            except Exception as err:
                __err_logging(DEBUG, __logging , err)
                print('-copy did not work. Either -path is wrong or it is absent.')    
        else:
            print('Please type "true" after -copy')
         
    
    # type of key generation. Either random or manual
    if args.Path:
        if args.GenKeyType:
            type_with_genkeys = True
            try:
                
                if not __exists(args.Path):
                    __makedirs(args.Path)
                new_key_file = open(f'{args.Path}/keys.json' , 'x')
                ALPHABETS = _string.printable
                default_keys = {}
                if args.GenKeyType == 'manual':    
                    for letter in ALPHABETS:
                        character_key = input(f'Replace {repr(letter)} with : ')

                        default_keys[letter] = character_key
                elif args.GenKeyType == 'random':
                    ALPHABETS_LIST = list(ALPHABETS)

                    for letter in ALPHABETS:
                        random_char = __choice(ALPHABETS_LIST)

                        ALPHABETS_LIST.remove(random_char)

                        default_keys[letter] = random_char
                else:
                    print('Either enter "manual" or "random" after -type. This will result in a empty "keys.json" file')        
                __json.dump(default_keys , new_key_file , indent=4)
        
                print(f'Created new keys.json file in {args.Path}')
                

            except Exception as err:
                __err_logging(DEBUG, __logging , err)
                print('keys.json already exists')
        else:
            print('Please add -type [manual/random] after -genpath')    
    # show current version of strenc    
    if args.ShowOrNot:
        if args.ShowOrNot == 'show':
            print(f'strenc version {__version__}')
        else:
            print("Please add 'show' after '-version'")
    # make a config file
    if args.ConfigType:
        if args.ConfigType == 'setup':
            
            
            if not __exists('strenc-config.ini'):
                
                config_file = open('strenc-config.ini' , 'x')
                __config.read('strenc-config.ini')
                

                sections_to_add = {'KEYPATH':['keypath'] ,  'DEBUG' : ['show-log']}

                for section,section_settings in sections_to_add.items():
                    __config.add_section(section)
                    for setting in section_settings:
                        preffered_setting = input(f'Set {setting} from section {section} : ')

                        __config.set(section , setting , str.lower(preffered_setting))

                __config.write(config_file)
                print('New strenc-config.ini in root directory is made.')

            else:
                print('strenc-config.ini already exists. To change config , run with --config [section/settings_to_change]')
        else:
            try:
                config_file = open('strenc-config.ini' , 'r+')
                __config.read('strenc-config.ini')
                config_section , config_settings = args.ConfigType.split('/')
                if __config.has_option(config_section , config_settings):
                    

                    preffered_setting = input(f'Change {config_settings} from {config_section} : ')    
                    __config.set(config_section , config_settings , preffered_setting)

                    __config.write(config_file)
                    print(f'Settings {config_settings} from {config_section} is updated to {preffered_setting}')
                else:
                    print('Either the section or option does not exist')     
            except Exception as err:
                __err_logging(DEBUG, __logging , err)
                print('strenc-config.ini does not exists. run -config setup to generate a new one.Or the specific setting does not exists')    
    
    if args.GenKeyType and not type_with_genkeys:
        print('Run -type alongside -genpath')
    # file encoding
    if args.EncodeFile:
        if __exists(args.EncodeFile):
            file_to_encode = open(args.EncodeFile , "r")
            # gets all the line of the file
            content_of_file = file_to_encode.readlines()
            #gets rid of all '\n' occurances
            for index , line in enumerate(content_of_file):
                if '\n' in line:
                    content_of_file[index] = line.replace('\n' , '')
            # try to encode each line one by one.
            try:
                for i , line_to_change in enumerate(content_of_file):
                    # change string to list for manipulation
                    list_form = list(line_to_change)
                    #encode every character of the above list
                    for another_index , char in enumerate(list_form):
                        list_form[another_index] = enc_keys[char]
                    #replace original string with encoded one
                    if i < len(content_of_file)-1:
                        content_of_file[i] = "".join(list_form)+'\n'
                    else:
                        content_of_file[i] = "".join(list_form)
                #make a new file and append encoded content in it
                
                encoded_file = open(f'{__basename(args.EncodeFile).split(".")[0]}-encoded.txt' , 'w') 

                encoded_file.writelines(content_of_file)                   
            except Exception as err:
                __err_logging(DEBUG, __logging , err)
                print('-encfile failed. Either keys.json is missing or not given')            


        else:
            print(f"File {args.EncodeFile} does not exist.")    
    #file decoding
    #almost same as file encoding
    if args.DecodeFile:
        if __exists(args.DecodeFile):
            file_to_decode = open(args.DecodeFile , "r")
            # gets all the line of the file
            content_of_file_dec = file_to_decode.readlines()
            #gets rid of all '\n' occurances
            for index , line in enumerate(content_of_file_dec):
                if '\n' in line:
                    content_of_file_dec[index] = line.replace('\n' , '')
            # try to encode each line one by one.
            try:
                for i , line_to_change in enumerate(content_of_file_dec):
                    # change string to list for manipulation
                    list_form_dec = list(line_to_change)
                    #encode every character of the above list
                    for another_index , char in enumerate(list_form_dec):
                        list_form_dec[another_index] = _get_key_from_value(enc_keys , char)
                    #replace original string with encoded one
                    if i < len(content_of_file_dec)-1:
                        content_of_file_dec[i] = "".join(list_form_dec)+'\n'
                    else:
                        content_of_file_dec[i] = "".join(list_form_dec)
                #make a new file and append encoded content in it
                
                decoded_file = open(f'{__basename(args.DecodeFile).split(".")[0]}-decoded.txt' , 'w') 

                decoded_file.writelines(content_of_file_dec)                   
            except Exception as err:
                __err_logging(DEBUG, __logging , err)
                print('-decfile failed. Either keys.json is missing or not given')
def _get_key_from_value(actual_dict  , val):
    for key,value in actual_dict.items():
        if val == value:
            return key
    return False    
    


