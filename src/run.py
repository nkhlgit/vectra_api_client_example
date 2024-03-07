#!/usr/bin/env python
"""
# Author: Nikhil Singh
# Email: nikhil.eltrx@gmail.com
# Purpose: Pull hosts data from Vectra brain using API and sve the output json file defined in conf file..
# Usage: 
##   - install Python 3
##   - configure config.json
##   - 
#Compatiblity_tested: Python3, VEctra Brain: 8.2 , API version : 2.5 :
"""

import logging
from helper.gateway import portal, prepare
from helper.utils import pathfinder  

pf = pathfinder()
p = portal()
logging.basicConfig(level=logging.INFO , filename=pf.log_file, filemode='w', format='%(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')


def push_manager(ext):    
    data_list= pf.get_input('push', ext)
    prep = prepare(ext)
    for data in data_list:
        clean_data = {key: data[key] for key in prep.accepted_keys()}
        p.push_one(ext, clean_data)

def patch_manager(ext):
    data_list = pf.get_input('patch', ext)
    prep = prepare(ext)
    data_refs =  prep.get_data_refrs()  
    for data in data_list:
        if (data_id := data.get('id')) is None:
            query_1 = {}
            for key in data_refs:
                key_val = data.get(key, None)
                if key_val is not None:
                    query_1[key] = key_val
                    break
            if not query_1:
                print(f'Can find refrence id or name or description of ext to update')
                continue
            exts = p.get_many(ext, query = query_1)
            if isinstance(exts, list):
                print(f'Got {exts[0]=}')
                data_id  = exts[0].get('id')
            else:
                print(f'can not find the ext id in {exts[0]=}')
        clean_data = {key: data[key] for key in prep.accepted_keys()}
        p.patch_one(ext, data_id, clean_data)

def get_manager(ext):
    data_list = p.get_many(ext)
    pf.save_to_file(ext , data_list)


if __name__ == '__main__':
    ext = 'groups'
    #get_manager(ext)
    push_manager(ext)
    #patch_manager(ext)

