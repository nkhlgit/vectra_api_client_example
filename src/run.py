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
from helper.extension_helper import get_exts

exts : dict = get_exts()
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
    args = argy.parse_args()
    return args

#doc def main is the starting point of project
def main(args : dict) -> None:
    log.info('start_main')
    #doc var ext is dictionary of specific extension
    ext : dict = exts.get(args.extension, None)
    if ext is None:
            text = f'The supported extensions are:\n\t <{" ".join(exts.keys())}>.\n You entered method <{args.extension}>'
            log.error(text)
            print(pnt.error(text))
            return

    #check if specific extension support called method
    if args.mode not in ext.get('modes', None):
        text = f'This API is configured and tested only with supported methods on extension <{args.extension}> are <{ext.get("modes")}>. \n \
            You entered method <{args.mode}>.\n \
            The program is not stoping however be ready for bumpy ride. \n'
        log.warning(text)
        print(pnt.warn(text))
        return
    e= ext.get('cls', None)(args.extension)
    match args.mode:
        case 'get':
            e.get()
        case 'post':
            e.post()
        case 'patch':
            e.patch()
        case 'delete':
            e.delete()
    e.log_stats()
    log.info('stop_main')


if __name__ == '__main__':
    text = 'start_vapi_client'
    log.info(text)
    print(pnt.info(text))
    main(parse_args())
    text = 'stop_vapi_client'
    log.info(text)
    print(pnt.info(text))
