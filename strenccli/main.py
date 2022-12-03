from os.path import exists
from os import makedirs
from os import remove
from os.path import basename
from random import choice
import string
import json
# util functions (self explanatory)



def remove_all(to_remove, list: list):
    return [ele for ele in list if ele != to_remove]


def get_key_from_value(actual_dict, val):
    for key, value in actual_dict.items():
        if val == value:
            return key
    return False


class StrencCLI:
    
    
    DEBUG = 'false'
    path_to_keys = None
    
    # all commands and arguments
    SYSTEM_ARGS = [{
        'com': '-k',
        'val': '--key',
        'help': 'Get key of a specific char'
    }, {
        'com': '-copy',
        'val': '--copy',
        'help': 'Get a copy of the keys'
    }, {
        'com':
        '-change',
        'val':
        '--change',
        'help':
        'Either change the whole key file or change a specific char'
    }, {
        'com': '-genpath',
        'val': '--genpath',
        'help': 'Create a keys.json file in root directory'
    }, {
        'com': '-path',
        'val': '--keypath',
        'help': 'Loaction of keys.json'
    }, {
        'com': '-v',
        'val': '--version',
        'help': 'Outputs installed version of strenc'
    }, {
        'com':
        '-config',
        'val':
        '--configtype',
        'help':
        'Setup or update config(Please run this command at the same folder as keys.json)'
    }, {
        'com':
        '-type',
        'val':
        '--genkeytype',
        'help':
        'Key generator options. Wont work if -genpath not given'
    }, {
        'com': '-encfile',
        'val': '--encodefile',
        'help': 'Encode a txt file'
    }, {
        'com': '-decfile',
        'val': '--decodefile',
        'help': 'Decode a encoded txt file'
    }, {
        'com':
        '-folds',
        'val':
        '-folds',
        'help':
        'Decide how many folds of encoding/decoding to use for file. Must be run with either -encfile or -decfile'
    }]
    __author__ = 'Saptak De'
    
    def __init__(self, version_arg: str, config_parser, argparser,
                 logger_module):
        self.config = config_parser.ConfigParser()  #conf parser
        self.arg_parser = argparser.ArgumentParser()  # arguments parser
        self.__version__ = version_arg
        self.logger = logger_module
    
    def err_logging(self, err: Exception, possible_reason: str = None):
        if possible_reason is None:
            print("Error found. Please check log file if debug enabled...")
        else:
            print(possible_reason)
        if self.DEBUG == 'true':
            self.logger.exception(f"[ERROR] : {err}")

            return True
        return False
    
    def debug_log(self, info: str):
        if self.DEBUG == 'true':
            self.logger.debug(f"[DEBUG] : {info}")
            return True
        return False
    
    def init_args(self):
        for command in self.SYSTEM_ARGS:
            self.arg_parser.add_argument(command['com'],
                                     command['val'],
                                     help=command['help'])

        self.args = self.arg_parser.parse_args()  # initialize args fetcher
        

    # config defaults
    
    # initializing the logger
    
    def init_logger(self):
        if self.DEBUG == 'true':
            self.logger.basicConfig(filename='strenc.log',
                                           filemode='w',
                                           format='%(asctime)s - %(message)s',
                                           level=self.logger.NOTSET)
        elif exists('strenc.log') and self.DEBUG == 'false':
            remove('strenc.log')
        
    # initialize configuration system
    
    def init_conf(self, default_fname: str):
        if exists(default_fname):
            self.config.read(default_fname)
            
            try:
                self.path_to_keys = self.config.get('KEYPATH', 'keypath')
            except Exception as err:
                pass

            try:
                self.DEBUG = self.config.get('DEBUG', 'show-log')
            except:
                pass
        elif self.args.keypath:
            self.path_to_keys = self.args.keypath

        
            
            

    # gatekeep variables
    type_with_genkeys = False
    folds_with_file = False
    
    # initialize key related variables
    
    def init_key(self):
        try:
            if self.path_to_keys is not None:
                self.file_json = open(f'{self.path_to_keys}/keys.json', 'r+')
                self.key_dict = json.load(self.file_json)
                self.keys_of_dict = self.key_dict.keys()
            else:
                print("No keys.json found or path not given")    
        except Exception as err:
                print("Error while initializing keys\n", err)

    # change key
    
    def change_key(self , arg_change):

        if arg_change == 'all':
            used_replacement = []
            try:

                for key in self.keys_of_dict:

                    while True:
                        replace_with = input(f'Replace {repr(key)} with :')

                        if replace_with in used_replacement:
                            print(
                                'This character has already been assigned to a key. Use another...'
                            )

                            continue
                        elif len(replace_with) != 1:
                            print(
                                'Input length is not equal to 1. Use another...'
                            )
                            continue
                        else:
                            self.debug_log(
                                f"Replaced {repr(key)} with {replace_with}"
                            )
                            break

                    used_replacement.append(replace_with)
                    self.key_dict[key] = replace_with
                
                 
            except Exception as err:
                self.err_logging(
                    err,
                    '-change did not work. Either -path is wrong or it is absent.'
                )
        

        else:      
            try:
                if arg_change in self.keys_of_dict:
                    while True:
                        replace_with = input(
                            f'Replace {repr(arg_change)} with :')

                        if self.key_dict[arg_change] == replace_with:
                            print(
                                f'Key {arg_change} already has the value {replace_with}'
                            )
                            continue
                        elif len(replace_with) != 1:
                            print(
                                'Input length is not equal to 1. Use another...'
                            )
                            continue
                        else:
                            self.debug_log(
                                f"Replaced {repr(arg_change)} with {replace_with}"
                            )
                            break

                    self.key_dict[arg_change] = replace_with
                    
                else:
                    print(
                        'Either add "all" or a specific character after -change'
                    )
            except Exception as err:
                self.err_logging(
                    err,
                    '-change did not work. Either -path is wrong or it is absent.'
                )

            print('Dumping data to json....')
            try:
                self.file_json.seek(0)
                self.file_json.truncate(0)

                json.dump(self.key_dict, self.file_json, indent=4)
                print('keys.json is updated')
            except Exception as err:
                self.err_logging(err, 'Dumping data to keys.json failed')

    # get value of a key
    
    def get_key(self , arg_key):
        
        try:
            print(
                f'Key for {repr(arg_key)} is : {repr(self.key_dict[arg_key])}'
            )
        except Exception as err:
            self.err_logging(
                err,
                '-k did not work. Either -path is wrong or it is absent. Or the character does not exist in the keys.json file'
            )

    # get a copy of keys.json file
    
    def get_copy(self , arg_copy):
        if arg_copy == 'true':    
            try:
                print(self.key_dict)
            except Exception as err:
                self.err_logging(
                err,
                '-copy did not work. Either -path is wrong or it is absent.'
                )
        else:
            print("Add true after -copy")        

    # generate keys.json file
    
    def gen_keys(self , genpath , gentype):
        
        if gentype:
            self.type_with_genkeys = True
            try:

                if not exists(genpath):
                    makedirs(genpath)
                    self.debug_log(f"Made directory {genpath}")
                new_key_file = open(f'{genpath}/keys.json', 'x')
                self.debug_log("Made keys.json file")
                ALPHABETS = string.printable
                default_keys = {}
                if gentype == 'manual':
                    used_assignments = []
                    for letter in ALPHABETS:
                        while True:
                            character_key = input(
                                f'Value of key {repr(letter)} should be : '
                            )
                            if character_key in used_assignments:
                                print(
                                    f'Character {character_key} already assigned. Use another...'
                                )
                                continue
                            elif len(character_key) != 1:
                                print(
                                    'Input length is not equal to 1. Use another...'
                                )
                                continue
                            else:
                                self.debug_log(
                                    f"{letter} assigned to {character_key}"
                                )
                                break

                        used_assignments.append(character_key)
                        default_keys[letter] = character_key
                elif gentype == 'random':
                    ALPHABETS_LIST = list(ALPHABETS)

                    for letter in ALPHABETS:
                        random_char = choice(ALPHABETS_LIST)

                        ALPHABETS_LIST.remove(random_char)

                        default_keys[letter] = random_char
                else:
                    print(
                        'Either enter "manual" or "random" after -type. This will result in a empty "keys.json" file'
                    )
                json.dump(default_keys, new_key_file, indent=4)

                print(f'Created new keys.json file in {genpath}')

                self.debug_log("Key file creation succesful")

            except Exception as err:
                self.err_logging(err, 'keys.json already exists')

        else:
            print('Please add -type [manual/random] after -genpath')

    # show current strenc version
    
    def show_version(self , arg_show):
        if arg_show == 'show':
            print(f'strenc version {self.__version__}')
        else:
            print('Please add show after -v')

    # setup or change config file
    
    def config_func(self, default_fname: str , conftype):
       
        if conftype == 'setup':

            if not exists(default_fname):

                config_file = open(default_fname, 'x')
                self.config.read(default_fname)

                sections_to_add = {
                    'KEYPATH': ['keypath'],
                    'DEBUG': ['show-log']
                }

                for section, section_settings in sections_to_add.items():
                    self.config.add_section(section)
                    for setting in section_settings:
                        preffered_setting = input(
                            f'Set {setting} from section {section} : ')

                        self.config.set(section, setting,
                                        str.lower(preffered_setting))

                self.config.write(config_file)
                print(f'New {default_fname} in current directory is made.')

            else:
                print(
                    f'{default_fname} already exists. To change config , run with --config [section/settings_to_change]'
                )
        else:
            try:
                config_file = open(default_fname, 'r+')
                self.config.read(default_fname)
                config_section, config_settings = conftype.split(
                    '/')
                if self.config.has_option(config_section, config_settings):

                    preffered_setting = input(
                        f'Change {config_settings} from {config_section} : ')
                    self.config.set(config_section, config_settings,
                                    preffered_setting)

                    self.config.write(config_file)
                    print(
                        f'Settings {config_settings} from {config_section} is updated to {preffered_setting}'
                    )
                else:
                    print('Either the section or option does not exist')
            except Exception as err:
                self.err_logging(
                    err,
                    f'{default_fname} does not exists. run -config setup to generate a new one.Or the specific setting does not exists'
                )

    # run gatekeep
    
    def gatekeep(self , gentype , arg_folds):
        if gentype and not self.type_with_genkeys:
            print('Run -type alongside -genpath')
        if arg_folds and not self.folds_with_file:
            print('Use argument -folds with either -encfile or -decfile')

    # .txt file encoding
    
    def encode_file(self , encfile , arg_folds):
        
        self.folds_with_file = True
        folds = 1
        #get value of 'folds' if given
        if arg_folds:
            try:
                folds = int(arg_folds)
            except Exception as err:
                self.err_logging(
                    err, 'value of argument -folds should be a integer')

        if exists(encfile):
            file_to_encode = open(encfile, "r")
            # gets all the line of the file
            content_of_file = file_to_encode.readlines()
            #gets rid of leading or trailing whitespace occurances at end of line
            for index, line in enumerate(content_of_file):
                content_of_file[index] = line.strip('\n')

            # try to encode each line one by one.
            try:
                for i, line_to_change in enumerate(content_of_file):
                    # change string to list for easier manipulation
                    list_form = list(line_to_change)

                    for fold in range(folds):

                        #encode every character of the above list
                        for another_index, char in enumerate(list_form):
                            list_form[another_index] = self.key_dict[char]
                        #replace original string with encoded one
                    if i < len(content_of_file) - 1:
                        content_of_file[i] = "".join(map(str,
                                                            list_form)) + '\n'
                    else:
                        content_of_file[i] = "".join(map(str, list_form))
                #make a new file and append encoded content in it

                encoded_file = open(
                    f'{basename(encfile).split(".")[0]}-encoded.txt',
                    'w')

                encoded_file.writelines(content_of_file)
            except Exception as err:
                self.__err_logging(
                    err,
                    '-encfile failed. Either keys.json is missing or not given'
                )

        else:
            print(f"File {encfile} does not exist.")

    # decode a encoded file
    
    def decode_file(self , decfile_arg , arg_folds):
        if decfile_arg:
            self.folds_with_file = True
            folds = 1
            #get value of 'folds' if given
            if arg_folds:
                try:
                    folds = int(arg_folds)
                except Exception as err:
                    self.err_logging(err , 'value of argument -folds should be a integer')
            if exists(decfile_arg):
                file_to_decode = open(decfile_arg, "r")
                # gets all the line of the file
                content_of_file_dec = file_to_decode.readlines()
                #gets rid of all '\n' occurances
                for index, line in enumerate(content_of_file_dec):
                    if '\n' in line:
                        content_of_file_dec[index] = line.replace('\n', '')
                # try to encode each line one by one.
                try:
                    for i, line_to_change in enumerate(content_of_file_dec):
                        # change string to list for manipulation
                        list_form_dec = list(line_to_change)
                        for dec_folds in range(folds):
                            #encode every character of the above list
                            for another_index, char in enumerate(
                                    list_form_dec):
                                list_form_dec[
                                    another_index] = get_key_from_value(
                                        self.key_dict, char)
                        #replace original string with encoded one
                        if i < len(content_of_file_dec) - 1:
                            content_of_file_dec[i] = "".join(
                                map(str, list_form_dec)) + '\n'
                        else:
                            content_of_file_dec[i] = "".join(
                                map(str, list_form_dec))
                    #make a new file and append encoded content in it
                    if "-encoded" not in decfile_arg:
                        decoded_file = open(
                            f'{basename(decfile_arg).split(".")[0]}-decoded.txt',
                            'w')
                    else:
                        decoded_file = open(
                            f'{basename(decfile_arg).split(".")[0].replace("-encoded" , "")}-original.txt',
                            'w')
                    decoded_file.writelines(content_of_file_dec)
                except Exception as err:
                    self.err_logging(err , '-decfile failed. Either keys.json is missing or not given')
                    
        
