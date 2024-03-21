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
from helper.settings import mode_dict, ext_mode

pf = pathfinder()
p = portal()
logging.basicConfig(level=logging.INFO , filename=pf.log_file, filemode='w', format='%(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

#doc def parse_args parsh the options
def parse_args():
    argy = argparse.ArgumentParser(description='Make API calls for bulk operation on Vectra Brain')
    argy.add_argument("--extension", "-e", type = str.lower, help="Extension of API example hosts, groups, rules", required=True, choices=mode_dict.keys())
    argy.add_argument("--mode", "-m",type = str.lower,  help="Mode of operaton example GET, POST, PATCH ", required=True, choices=['get','post', 'patch'])
    args = argy.parse_args()
    return args

#doc def main is the starting point of project
def main(args):
    #doc get class from settings 
    ext = mode_dict[args.extension]
    e= ext()
    #check if specific extension support called method
    if args.mode not in ext_mode[args.extension]:
        print('method not supported for extension')

    match args.mode:
        case 'get':
            e.get()
        case 'post':
            e.post()
        case 'patch':
            e.patch()


if __name__ == '__main__':
    main(parse_args())


