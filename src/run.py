#!/usr/bin/env python
"""
# Author: Nikhil
# Email: nikhil.eltrx@gmail.com
# Purpose: perform GET, post, PATCH data at bulk on Vectra brain using API and sve the output json file defined in conf file..
# Usage: 
##   - install Python 3
##   - configure config.json
##   - 
#Compatiblity_tested: Python3, VEctra Brain: 8.2 , API version : 2.5 :
"""
import argparse
import logging
from helper.utils import pathfinder  
from helper.settings import pnt, loglevel
from helper.extension_helper import get_exts
from helper.extension_main import extension_manager

exts : dict = get_exts()
pf = pathfinder()
#mapping of extension vrs class

format_val = '%(asctime)-15s %(levelname)s:%(filename)s:%(lineno)d: %(message)s'
logging.basicConfig(level=loglevel , filename=pf.log_file, filemode='w', format=format_val, datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger(__name__)



#doc def parse_args parsh the options
def parse_args() -> dict:
    log.info('===Start_parse_args===')
    argy = argparse.ArgumentParser(description='Make API calls for bulk operation on Vectra Brain')
    argy.add_argument("--extension", "-e", 
                      type = str.lower, 
                      help=f'Extension of API: \n\t {" ".join(exts.keys())}', 
                      required=True, 
                      #choices=cls_exts.all_exts(),
                      )
    argy.add_argument("--mode", "-m",
                      type = str.lower,
                      help=f'Mode of operaton. Most of extension support only get mode. The overall options are: \n\t get post patch put delete.',
                      required=True, 
                      choices=['get','post', 'patch', 'put', 'delete'],
                      )
    argy.add_argument("--query", "-q",
                      type = str.lower,
                      help=f'To use query with search extension',
                      required=False, 
                      )
    args = argy.parse_args()
    return args

#doc def main is the starting point of project
def main(args : dict) -> None:
    log.info('start_main')
    args_dict = vars(args)
    print(pnt.info(f'args are : {args_dict}'))
    em = extension_manager(**args_dict)
    em.start()
    log.info('stop_main')


if __name__ == '__main__':
    text = 'start_vapi_client'
    log.info(text)
    print(pnt.info(text))
    main(parse_args())
    text = 'stop_vapi_client'
    log.info(text)
    print(pnt.info(text))
    print(pnt.info(f'Script finished! The operation logs are {pf.log_file}'))
