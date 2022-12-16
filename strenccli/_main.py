from os.path import exists
from os import makedirs
from os import remove
from os.path import basename
import random
import string
import json
# util functions (self explanatory)



def remove_all(to_remove, list: list):
    return [ele for ele in list if ele != to_remove]

def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def get_key_from_value(actual_dict, val):
    for key, value in actual_dict.items():
        if val == value:
            return key
    raise ValueError(f"key for {val} not found")

def return_seed_value(seed_and_clen : str):
    specific_clen = 1
    try:
        seed , specific_clen = [int (section) for section in seed_and_clen.split("@")]
    except:
        pass    
    tmp_return_value = {}
    tmp_return_value["chunk-length"] = specific_clen
    tmp_return_value["keys"] = {}
    ALPHABETS = string.ascii_letters + string.punctuation + string.digits
    ALPHABETS_LIST = list(ALPHABETS)
    random.seed(seed)
    
    rand_state = random.getstate()
    
    random.setstate(rand_state)
    used_assignments_rand = []
    for letter in ALPHABETS:
        temp_rand_key = []
        while True:
            for __ in range(specific_clen):
                temp_rand_key.append(random.choice(ALPHABETS_LIST))
            rand_char = "".join(temp_rand_key)
            
            if specific_clen > 1 and rand_char not in used_assignments_rand:
                used_assignments_rand.append(rand_char)            
                break
            elif specific_clen  == 1:
                ALPHABETS_LIST.remove(rand_char)
                break
            
            
            

        tmp_return_value["keys"][letter] = rand_char
    return tmp_return_value
    
    

class StrencCLI:
    
    
    DEBUG = 'false'
    path_to_keys = None
    
    # commands and arguments that requires value
    SYSTEM_ARGS = [{
        'com': '-k',
        'val': '--key',
        'help': 'Get value of specific key'
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
    }, {
        'com':
        '-clen',
        'val':
        '--chunklength',
        'help':
        'Decides length of each key'            
    },{
      'com':
      '-val',
      'val':
      '--value',
      'help':
      'Get key for a specific value'             
    },{
      'com':
      '-s',
      'val':
      '--seed',
      'help':
      'Use a specific seed instead of a key file'             
    }]
    # query commands
    QUERY_ARGS = [ {
        'com': '-v',
        'val': '--version',
        'help': 'Outputs installed version of strenc',
    },  {
        'com': '-copy',
        'val': '--copy',
        'help': 'Get a copy of the keys'
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
        for command_bool in self.QUERY_ARGS:
            self.arg_parser.add_argument(command_bool['com'],
                                     command_bool['val'],
                                     help=command_bool['help'] , action = 'store_true')    

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
    clen_with_keygen = False
    seed_with_file = False
    
    
    # initialize key related variables
    
    def init_key(self):
        try:
            if self.path_to_keys is not None and exists(f'{self.path_to_keys}/keys.json'):
                self.file_json = open(f'{self.path_to_keys}/keys.json', 'r+')
                
                self.key_dict = json.load(self.file_json)
                self.keys_of_dict = self.key_dict["keys"].keys()
                self.clen = self.key_dict["chunk-length"]
            else:
                print("No keys.json found or path not given")    
        except Exception as err:
                self.err_logging(err , "Error while initializing key")

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
                        elif len(replace_with) != self.clen:
                            print(
                                f'Input length is not equal to {self.clen}. Use another...'
                            )
                            continue
                        else:
                            self.debug_log(
                                f"Replaced {repr(key)} with {repr(replace_with)}"
                            )
                            break

                    used_replacement.append(replace_with)
                    self.key_dict["keys"][key] = replace_with
                
                 
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

                        if self.key_dict["keys"][arg_change] == replace_with:
                            print(
                                f'Key {arg_change} already has the value {replace_with}'
                            )
                            continue
                        elif len(replace_with) != self.clen:
                            print(
                                f'Input length is not equal to {self.clen}. Use another...'
                            )
                            continue
                        else:
                            self.debug_log(
                                f"Replaced {repr(arg_change)} with {repr(replace_with)}"
                            )
                            break

                    self.key_dict["keys"][arg_change] = replace_with
                    if self.clen == 1:
                        self.debug_log("Chunklength is 1 , swapping values...")
                        self.key_dict["keys"][replace_with] = arg_change
                    
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
                f'Value for key {repr(arg_key)} is : {repr(self.key_dict["keys"][arg_key])}'
            )
        except Exception as err:
            self.err_logging(
                err,
                '-k did not work. Either -path is wrong or it is absent. Or the character does not exist in the keys.json file'
            )
    # get key for a specific value
    
    def get_value(self , arg_value):
        try:
            print(f'Key for value {repr(arg_value)} is : {repr(get_key_from_value(self.key_dict["keys"] , arg_value))}')        
        except Exception as err:
            self.err_logging(err , f"Error fetching key for value {arg_value}")
    # get a copy of keys.json file
    
    def get_copy(self , arg_copy):
        if arg_copy:    
            try:
                print(self.key_dict)
            except Exception as err:
                self.err_logging(
                err,
                '-copy did not work. Either -path is wrong or it is absent.'
                )
        
    # generate keys.json file
    
    def gen_keys(self , genpath , gentype , arg_clen):
        
        
        if arg_clen:
            self.clen_with_keygen = True
            try:
                chunk_length = int(arg_clen)
            except Exception as err:
                self.err_logging(err , "Chunk length value must be a integer")
        else:
            try:
                chunk_length = int(input("Please enter chunk length value (Default =1) : "))
            except Exception as err:
                chunk_length = 1
                self.err_logging(err , "Chunk length value is not a integer.Defaulting to 1")               
        if gentype:
            self.type_with_genkeys = True
            try:

                if not exists(genpath):
                    makedirs(genpath)
                    self.debug_log(f"Made directory {genpath}")
                new_key_file = open(f'{genpath}/keys.json', 'x')
                self.debug_log("Made keys.json file")
                ALPHABETS = string.ascii_letters + string.punctuation + string.digits
                default_keys = {}
                default_keys["chunk-length"] = chunk_length
                default_keys["keys"] = {}
                if gentype == 'manual':
                    used_assignments = []
                    for letter in ALPHABETS:
                        while True:
                            character_key = input(
                                f'Value of key {repr(letter)} should be : '
                            )
                            if character_key in used_assignments:
                                print(
                                    f'Character {repr(character_key)} already assigned. Use another...'
                                )
                                continue
                            elif len(character_key) != chunk_length:
                                print(
                                   f'Input length is not equal to {chunk_length}. Use another...'
                                )
                                continue
                            else:
                                self.debug_log(
                                    f"r{repr(letter)} assigned to {repr(character_key)}"
                                )
                                break

                        used_assignments.append(character_key)
                        default_keys["keys"][letter] = character_key
                elif gentype == 'random':
                    ALPHABETS_LIST = list(ALPHABETS)
                    used_assignments_rand = []
                    for letter in ALPHABETS:
                        temp_rand_key = []
                        while True:
                            for __ in range(chunk_length):
                                temp_rand_key.append(random.choice(ALPHABETS_LIST))
                            rand_char = "".join(temp_rand_key)
                            
                            if chunk_length > 1 and rand_char not in used_assignments_rand:
                                used_assignments_rand.append(rand_char)            
                                break
                            elif chunk_length  == 1:
                                ALPHABETS_LIST.remove(rand_char)
                                break
                            else:
                                self.debug_log(f"Randomly generated value {repr(rand_char)} already exists")
                            
                            

                        default_keys["keys"][letter] = rand_char
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
        if arg_show:
            print(f'strenc version {self.__version__}')
        

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
    
    def gatekeep(self , gentype , arg_folds , arg_seed):
        if gentype and not self.type_with_genkeys:
            print('Run -type alongside -genpath')
        if arg_folds and not self.folds_with_file:
            print('Use argument -folds with either -encfile or -decfile')
        if arg_seed and not self.seed_with_file:
            print('Use argument -s or --seed with either -encfile or -decfile')    
           

    # .txt file encoding
    
    def encode_file(self , encfile , arg_folds , arg_seed):
        
        self.folds_with_file = True
        self.seed_with_file = True
        folds = 1
        #get value of 'folds' if given
        if arg_folds:
            try:
                folds = int(arg_folds)
            except Exception as err:
                self.err_logging(
                    err, 'value of argument -folds should be a integer')
        # use seed if given , else use the given key file
        
        if arg_seed:
            try:
                self.key_dict  = return_seed_value(arg_seed)
            except Exception as err:
                self.err_logging(err , "Value of -s or --seed should be a integer")    
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
                    
                    

                    for fold in range(folds):
                        list_form = list(line_to_change)    
                        #encode every character of the above list
                        for another_index, char in enumerate(list_form):
                            if char not in string.whitespace:    
                                list_form[another_index] = self.key_dict["keys"][char]
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
                self.err_logging(
                    err,
                    '-encfile failed. Either keys.json is missing or not given'
                )

        else:
            print(f"File {encfile} does not exist.")

    # decode a encoded file
    
    def decode_file(self , decfile_arg , arg_folds , arg_seed):
        if decfile_arg:
            self.folds_with_file = True
            self.seed_with_file = True
            folds = 1
            #get value of 'folds' if given
            if arg_folds:
                try:
                    folds = int(arg_folds)
                except Exception as err:
                    self.err_logging(err , 'value of argument -folds should be a integer')
            if arg_seed:
                try:
                    self.key_dict = return_seed_value(arg_seed)
                    self.clen = self.key_dict["chunk-length"]
                except Exception as err:
                    self.err_logging(err , "Value of -s or --seed should be a integer")            
            if exists(decfile_arg):
                file_to_decode = open(decfile_arg, "r")
                content_of_file_dec = file_to_decode.readlines()
                #gets rid of all '\n' occurances
                self.debug_log(f"Raw lines : {content_of_file_dec}")
                # try to encode each line one by one.
                
                
                
                try:
                    
                        
                    for i , line_to_decode in enumerate(content_of_file_dec):
                        
                        
                        for dec_folds in range(folds):
                            words_dec = intersperse(line_to_decode.split(" ") , " ")
                            list_form_dec = [word_dec[split_c:split_c+self.clen] for word_dec in words_dec for split_c in range(0, len(word_dec) , self.clen)]
                            #encode every character of the above list
                            for another_index, char in enumerate(list_form_dec):
                                self.debug_log(f"Length of current charcter (dec) is {len(char)}")
                                if char not in string.whitespace:
                                    list_form_dec[another_index] = get_key_from_value(self.key_dict["keys"], char)
                                    
                        #replace original string with encoded one
                        
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
                    
        
