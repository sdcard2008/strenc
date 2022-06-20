#DO NOT TOUCH
#PROGRAM TO RUN COMMAND "customizekeys"



import json as __json
import argparse as __argparse

def __main():
    parser = __argparse.ArgumentParser()

    parser.add_argument('-k' , '--Key' , help="Get key of a specific char")

    parser.add_argument('-copy' , '--Copy' , help="Get a copy of the keys")

    parser.add_argument('-change' , '--Type' , help="Either change the whole key file or change a specific char")
    parser.add_argument('-genkeys' , '--Path' , help="Create a keys.json file in root directory")
    parser.add_argument('-keypath' , '--KeyPath' , help="Loaction of keys.json")
    args = parser.parse_args()

    if args.KeyPath:
        path_to_keys = args.KeyPath


    try:
        file_json = open(f'{path_to_keys}/keys.json' , 'r+')
        enc_keys = __json.load(file_json)
        letters_for_keys = enc_keys.keys()
        file_loaded = True
    except:
        file_loaded = False
        pass






    if file_loaded:    
        if args.Type:
            if args.Type == 'all':    
                for enc_key_keys in letters_for_keys:
                    replace_with = input(f'Replace {enc_key_keys} with :')

                    enc_keys[enc_key_keys] = replace_with
                
            elif args.Type in letters_for_keys:
                replace_with = input(f'Replace {args.Type} with :')

                enc_keys[args.Type] = replace_with
            else:
                print('Wrong input : Enter either "all" or a specific char')    
            print('Dumping data to json....')
            file_json.seek(0)
            file_json.truncate(0)

            __json.dump(enc_keys , file_json , indent=4)
        elif args.Key:
            print(f'Key for {args.Key} is : {enc_keys[args.Key]}')
        elif args.Copy:
            if args.Copy == 'true':
                print(enc_keys)
            else:
                print('Please type "true" after -copy')
        elif args.Path:
            print('keys.json already exists')        
    else:
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
        else:
            print(
                """
                An error occured. Possible reasons:
                    -You forgot to add -keypath [path_to_keys] in the command
                    -keys.json does not exists. Try running with -genkeys [where_to_generate]
                    - -keypath [path_to_keys] path is wrong
                    
                """
            )
            

