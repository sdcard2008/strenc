#DO NOT TOUCH
#PROGRAM TO RUN COMMAND "customizekeys"


import json as __json
import argparse as __argparse
import configparser as __configparser
from os.path import exists as __exists
__version__ = '0.1.2'
__author__ = 'Saptak De'

config = __configparser.ConfigParser()


def __main():
    parser = __argparse.ArgumentParser()

    parser.add_argument('-k' , '--Key' , help="Get key of a specific char")

    parser.add_argument('-copy' , '--Copy' , help="Get a copy of the keys")

    parser.add_argument('-change' , '--Type' , help="Either change the whole key file or change a specific char")
    parser.add_argument('-genkeys' , '--Path' , help="Create a keys.json file in root directory")
    parser.add_argument('-keypath' , '--KeyPath' , help="Loaction of keys.json")
    parser.add_argument('-version' , '--ShowOrNot' , help="Outputs installed version of strenc")
    parser.add_argument('-config' , '--ConfigType' , help="Setup or update config")
    args = parser.parse_args()

    if args.KeyPath:
        path_to_keys = args.KeyPath
    elif __exists('key-config.ini'):
        config.read('key-config.ini')

        try:
            path_to_keys = config.get('KEYPATH' , 'keypath')
        except:
            print('No keypath settings in KEYPATH section in key-config.ini. -k , -copy , -change will not work')    
    else:
        print('-keypath [key_path] is absent and key-config.ini is absent. -k , -copy , -change will not work')        


    try:
        file_json = open(f'{path_to_keys}/keys.json' , 'r+')
        enc_keys = __json.load(file_json)
        letters_for_keys = enc_keys.keys()
    except:
        print('Cannot find keys.json from given path. -k , -copy , -change will not work.')






    
    if args.Type:
        if args.Type == 'all':    
            try:
                for enc_key_keys in letters_for_keys:
                    replace_with = input(f'Replace {enc_key_keys} with :')

                    enc_keys[enc_key_keys] = replace_with
            except:
                print('-change did not work. Either -keypath is wrong or it is absent.')    
        elif args.Type in letters_for_keys:
            try:
                replace_with = input(f'Replace {args.Type} with :')

                enc_keys[args.Type] = replace_with
            except:
                print('-change did not work. Either -keypath is wrong or it is absent.')    
        else:
            print('Wrong input : Enter either "all" or a specific char')    
        print('Dumping data to json....')
        try:
            file_json.seek(0)
            file_json.truncate(0)

            __json.dump(enc_keys , file_json , indent=4)
            print('keys.json is updated')
        except:
            print('Dumping data to keys.json failed')    
    if args.Key:
        try:
            print(f'Key for {args.Key} is : {enc_keys[args.Key]}')
        except:
            print('-k did not work. Either -keypath is wrong or it is absent. Or the alphabet does not exist in the keys.json file')    
    if args.Copy:
        if args.Copy == 'true':
            try:
                print(enc_keys)
            except:
                print('-copy did not work. Either -keypath is wrong or it is absent.')    
        else:
            print('Please type "true" after -copy')
         
    
    
    if args.Path:
        try:
            new_key_file = open(f'{args.Path}/keys.json' , 'x')
            ALPHABETS = 'abcdefghijklmnopqrstuvwxyz1234567890`~!@#$%^&*()-_=+[{]}\\|;:\'\",<.>/?'
            default_keys = {}
            for letter in ALPHABETS:
                character_key = str.lower(input(f'Replace {letter} with : '))

                default_keys[letter] = character_key
            __json.dump(default_keys , new_key_file , indent=4)

            print(f'Created new keys.json file in {args.Path}')
        except:
            print('keys.json already exists')
        
    if args.ShowOrNot:
        if args.ShowOrNot == 'show':
            print(f'strenc version {__version__}')
        else:
            print("Please add 'show' after '-version'")

    if args.ConfigType:
        if args.ConfigType == 'setup':
            
            
            if not __exists('key-config.ini'):
                
                config_file = open('key-config.ini' , 'x')
                config.read('keys-config.ini')
                

                sections_to_add = {'KEYPATH':['keypath'] ,  'DEFAULTKEYVALUES' : []}

                for section,section_settings in sections_to_add.items():
                    config.add_section(section)
                    for setting in section_settings:
                        preffered_setting = input(f'Set {setting} from section {section} : ')

                        config.set(section , setting , str.lower(preffered_setting))

                config.write(config_file)
                print('New key-config.ini in root directory is made.')

            else:
                print('key-config.ini already exists. To change config , run with --config [section/settings_to_change]')
        else:
            try:
                config_file = open('key-config.ini' , 'r+')
                config.read('key-config.ini')
                config_section , config_settings = args.ConfigType.split('/')

                preffered_setting = input(f'Change {config_settings} from {config_section} : ')

                config.set(config_section , config_settings , preffered_setting)

                config.write(config_file)
                print(f'Settings {config_settings} from {config_section} is updated to {preffered_setting}') 
            except:
                print('key-config.ini does not exists. run -config setup to generate a new one.Or the specific setting does not exists')    

            


