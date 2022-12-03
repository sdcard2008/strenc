#PROGRAM TO RUN COMMAND "customizekeys"

#imports

import argparse 
import configparser 
import logging
from strenccli.main import StrencCLI


def __main():
    default_conf = "strenconf.ini"
    strenc_cli = StrencCLI ("0.2.8" , configparser , argparse , logging)
    
    # calling init functions
    
    strenc_cli.init_args()
    strenc_cli.init_conf(default_conf)
    strenc_cli.init_key()
    strenc_cli.init_logger()
    
    
    ARGUMENT_VARS = {
        "key" : strenc_cli.args.key,
        "copy" : strenc_cli.args.copy,
        "change" : strenc_cli.args.change,
        "genpath" : strenc_cli.args.genpath,
        "keypath" : strenc_cli.args.keypath,
        "version" : strenc_cli.args.version,
        "config" : strenc_cli.args.configtype,
        "genkeytype" : strenc_cli.args.genkeytype,
        "encfile" : strenc_cli.args.encodefile,
        "decfile" : strenc_cli.args.decodefile,
        "folds" : strenc_cli.args.folds
    }
    
    
    

    if (ARGUMENT_VARS["change"]):
        strenc_cli.change_key(ARGUMENT_VARS["change"])
    
    elif (ARGUMENT_VARS["key"]):
        strenc_cli.get_key(ARGUMENT_VARS["key"])
    elif (ARGUMENT_VARS["copy"]):
        strenc_cli.get_copy(ARGUMENT_VARS['copy'])
    elif (ARGUMENT_VARS["genpath"]):
        strenc_cli.gen_keys(ARGUMENT_VARS["genpath"] , ARGUMENT_VARS["genkeytype"])
    elif (ARGUMENT_VARS["version"]):
        strenc_cli.show_version(ARGUMENT_VARS["version"])
    elif (ARGUMENT_VARS["config"]):
        strenc_cli.config_func(default_conf , ARGUMENT_VARS["config"])
    elif (ARGUMENT_VARS["encfile"]):
        strenc_cli.encode_file(ARGUMENT_VARS["encfile"] ,ARGUMENT_VARS["folds"])
    elif (ARGUMENT_VARS["decfile"]):
        strenc_cli.decode_file(ARGUMENT_VARS["decfile"] , ARGUMENT_VARS["folds"])
    
    # gatekeep
    
    strenc_cli.gatekeep(ARGUMENT_VARS["genkeytype"] , ARGUMENT_VARS["folds"])
    