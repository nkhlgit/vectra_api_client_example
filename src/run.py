#!/usr/bin/env python
"""
# Author: Nikhil Singh
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
from helper.gateway import portal
from helper.utils import pathfinder  
from helper.settings import conf, pnt, loglevel
from helper.extension_helper import ext_cls

pf = pathfinder()
p = portal()
#mapping of extension vrs class

format_val = '%(asctime)-15s %(levelname)s:%(filename)s:%(lineno)d: %(message)s'
logging.basicConfig(level=loglevel , filename=pf.log_file, filemode='w', format=format_val, datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger(__name__)



#doc def parse_args parsh the options
def parse_args() -> dict:
    log.info('===Start_parse_args===')
    argy = argparse.ArgumentParser(description='Make API calls for bulk operation on Vectra Brain')
    argy.add_argument("--extension", "-e", type = str.lower, help="Extension of API example hosts, groups, rules", required=True, choices=ext_cls.keys())
    argy.add_argument("--mode", "-m",type = str.lower,  help="Mode of operaton example GET, POST, PATCH ", required=True, choices=['get','post', 'patch'])
    args = argy.parse_args()
    return args

#doc def main is the starting point of project
def main(args : dict) -> None:
    log.info('start_main')
    #doc get class from settings 
    ext = ext_cls[args.extension]
    e= ext()
    #check if specific extension support called method
    if args.mode not in e.supported_mode:
        text = f'The supported methods on extension <{args.extension}> are <{e.supported_mode}>. You entered method <{args.mode}>'
        log.error(text)
        print(pnt.error(text))
        return

    match args.mode:
        case 'get':
            e.get()
        case 'post':
            e.post()
        case 'patch':
            e.patch()
    log.info('stop_main')


if __name__ == '__main__':
    text = 'start_vapi_client'
    log.info(text)
    print(pnt.info(text))
    main(parse_args())
    text = 'stop_vapi_client'
    log.info(text)
    print(pnt.info(text))
