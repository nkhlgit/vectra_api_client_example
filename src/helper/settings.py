import json
import os
import logging
log = logging.getLogger(__name__)

#constants
constants = {
    'max_vec_api_version' : 'v2.5'
}

#doc ger configuration
def get_conf():
    script_dir = os.path.realpath(os.path.dirname(__file__))
    conf_file_name = 'config.json'
    conf_file = f'{script_dir}/../conf/{conf_file_name}'
    f = open(conf_file)
    conf = json.load(f)
    f.close()
    return conf
conf = get_conf()



loglevel_dict = { 
    'debug' : logging.DEBUG,
    'info' : logging.INFO,
     'WARN' : logging.WARN,
     'error': logging.ERROR,
     'critical': logging.CRITICAL,
     'fetal' : logging.FATAL
}    
loglevel = loglevel_dict.get(conf.get('loglevel', 'info'), logging.INFO)

#doc get_query for future get static query
def get_query():
    script_dir = os.path.realpath(os.path.dirname(__file__))
    query_file_name = 'config.json'
    query_file = f'{script_dir}/{query_file_name}'
    f = open(query_file)
    query = json.load(f)
    f.close()
    return query



class pnt():
    def error(text : str) -> str:
        return '\033[31m' + text + '\033[0m'

    def warn(text : str) -> str:
        return '\033[33m' + text + '\033[0m'

    def info(text : str) -> str:
        return '\033[32m' + text + '\033[0m'
