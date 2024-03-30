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
from helper.extension_helper import cls_ext_map

cls_exts = cls_ext_map()
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
                      help="Extension of API example hosts, groups, rules", 
                      required=True, 
                      #choices=cls_exts.all_exts(),
                      )
    argy.add_argument("--mode", "-m",
                      type = str.lower,
                      help="Mode of operaton example GET, POST, PATCH ",
                      required=True, 
                      choices=['get','post', 'patch', 'put', 'delete'],
                      )
    args = argy.parse_args()
    return args

#doc def main is the starting point of project
def main(args : dict) -> None:
    log.info('start_main')
    #doc get class from settings 
    #ext = ext_cls.get(args.extension, None)
    all_exts = []
    ext = cls_exts.get_cls(args.extension)
    if ext is None:
            text = f'The supported extensions are:\n\t <{" ".join(cls_exts.all_exts())}>.\n You entered method <{args.extension}>'
            log.error(text)
            print(pnt.error(text))
            return
    e= ext(args.extension)
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
        case 'delete':
            e.delete()
    log.info('stop_main')


if __name__ == '__main__':
    text = 'start_vapi_client'
    log.info(text)
    print(pnt.info(text))
    main(parse_args())
    text = 'stop_vapi_client'
    log.info(text)
    print(pnt.info(text))
