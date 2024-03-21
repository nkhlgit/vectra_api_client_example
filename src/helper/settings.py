from . import extension_helper as e

#doc: define the local values
get = 'get'
post = 'post'
patch = 'patch'
hosts = 'hosts'
groups = 'groups'
rules = 'rule'

#mapping of extension vrs class
mode_dict = {
    groups : e.groups,
    hosts: e.hosts,
    rules: e.rules,
}


ext_mode = {
    hosts: {get},
    groups:{get, post, patch},
    rules: {get},
}

