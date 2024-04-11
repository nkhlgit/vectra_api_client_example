import logging
from helper.gateway import portal
from helper.utils import pathfinder, mydb
from helper.settings import pnt
import json
log = logging.getLogger(__name__)
pf = pathfinder()
p = portal()  


class base_extension():
    def __init__(self, **kargs) -> None:
        self.kargs = kargs
        self.ext = self.kargs.get('extension', None)
        self.clmns_list = 'members members_name'.split()
        self.payload_plus=  {} if self.kargs.get('payload', None) is None else json.loads(self.kargs.get('payload'))
        if self.kargs.get('query', None) is not None:
            self.payload_plus =  self.payload_plus.update({'query_string': self.kargs.get('query')})
        self.clmns_bool = None
        self.clmns_dict = None


    def get_api(self, save : bool= True) :
        data_list = p.get_many(self.ext, self.payload_plus)
        if save:
            pf.save_to_file(self.ext , data_list)

    def post_api(self):    
        data_list= pf.get_input('post', self.ext)
        for data in data_list:
            clean_data = self.tosend_clean_data(data, 'post')
            p.post_one(self.ext, clean_data)
    
    def delete_api(self):    
        data_list= pf.get_input('delete', self.ext)
        for data in data_list:
            #cmnt: If id in not present in data then look for other key for search.
            #This will be used toget id to post data
            if (data_id := data.get('id')) is None:
                query_1 = {}
                        #cmnt: get lsit if feilds that can be used  as key to post data. 
                for key in self.data_prim_keys:
                    key_val = data.get(key, None)
                    if key_val is not None:
                        query_1[key] = key_val
                        break
                if not query_1:
                    log.error(f'Can find refrence id or name or description of ext to update')
                    continue
                #cmnt: get as many data for extension this will be used toget id to post data
                exts = p.get_many(self.ext, query = query_1)
                log.debug(f'log: {exts=}')
                if isinstance(exts, list) and len(exts) > 0:
                    log.debug(f'Got {exts[0]=}')
                    data_id  = exts[0].get('id')
                else:
                    log.error(f'can not find the {self.ext=} id in {query_1=}')
                    continue
            p.delete_one(self.ext, data_id)

    def patch_api(self):
        data_list = pf.get_input('patch', self.ext)
        for data in data_list:
            #cmnt: If id in not present in data then look for other key for search.
            #This will be used toget id to post data
            if (data_id := data.get('id')) is None:
                query_1 = {}
                        #cmnt: get lsit if feilds that can be used  as key to post data. 
                for key in self.data_prim_keys:
                    key_val = data.get(key, None)
                    if key_val is not None:
                        query_1[key] = key_val
                        break
                if not query_1:
                    log.error(f'Can find refrence id or name or description of ext to update')
                    continue
                #cmnt: get as many data for extension this will be used toget id to post data
                exts = p.get_many(self.ext, query = query_1)
                log.debug(f'log: {exts=}')
                if isinstance(exts, list) and len(exts) > 0:
                    log.debug(f'Got {exts[0]=}')
                    data_id  = exts[0].get('id')
                else:
                    log.error(f'can not find the {self.ext=} id in {query_1=}')
                    continue
            clean_data = self.tosend_clean_data(data, 'patch')
            p.patch_one(self.ext, data_id, clean_data)

    def search_manager(self, query_string ):
        if self.ext.startswith('search'):
            ext = self.ext
        else: 
            ext = f'search/{self.ext}'
        query_1 = {'query_string': query_string} 
        search_results = p.get_many(ext, query = query_1) 
        log.debug(search_results)
        return search_results
    
    def bool_typing(self, b) -> dict:
        if isinstance( b , str):
            b = b.strip().lower()
            if b == 'true':
                return True
            else:
                return False
        elif isinstance( b , bool):
            return b
        else:
            return b

    def dict_typing(self, ac) -> dict:
        if isinstance(ac , str):
            return json.loads(ac.replace("'","\""))
        elif isinstance(ac , dict):
            return ac
        else:
            return {}

    def list_typing(self, members) -> dict:
        if isinstance(members, str):
            members = members.strip()
            if members.startswith('[') and members.endswith(']') :
                members = members.lstrip('[')
                members = members.rstrip(']')
            members = members.split(',')
            print(members)
        elif not isinstance(members, list):
            members = [members]
        return list(filter(None, members))


    def data_typing(self, data : dict) -> dict:
        """set proper data type for reay to send"""
        #col_name and typing_fun
        colss = (self.clmns_bool, self.clmns_dict, self.clmns_list )
        funs = (self.bool_typing, self.dict_typing, self.list_typing )
        for cols, fun in zip(colss,funs):
            if not cols:
                continue
            for col in cols:
                if col not in data:
                    continue
                data[col] = fun(data.get(col))
        return data

    
    def tosend_clean_data(self, data : dict, mode : str) -> dict:
        """tosend_clean_data make ata clean for post or put or patch"""
        data = self.data_typing(data)
        if mode == 'patch':
            for k,v in data:
                if v or v is None:
                    del data[k]
        drop_key = 'id url created_timestamp last_timestamp'.split()
        for k in drop_key:
            if k in data:
                del data[k]
        return data
    
    def log_stats(self) -> None:
        tub = mydb.get_tub()
        if not tub or tub is None or len(tub) < 1:
            msg = f'FYI only: No member_name queried'
        else:
            f= f'{self.ext}_member_name_searched'
            pf.save_to_file( f , tub)
            msg = f'{len(tub)} memeber names searched. result are saved in :{f}'
        log.info(msg)
        print(pnt.info(msg))

                
class groups(base_extension):
    def __init__(self, **kargs ):
        super().__init__(**kargs)
        #for Post and patch
        self.valid_columns = 'name description type members'.split()
        self.data_prim_keys = 'name description'.split()   

    #doc def tosend_clean_data(self,data): prepare data to send for upload
    def tosend_clean_data(self, data : dict, mode : str) -> dict:
        data = self.data_typing(data)
        if data['type'] == 'host' and (memebers_names := data.get('members_name', None)) is not None:
            memeber_ids = []
            for memeber_name in memebers_names:
                name_ids = []
                memeber_name = memeber_name.strip()
                if memeber_name in mydb.get_tub():
                    name_ids = mydb.get_tub_member(memeber_name)
                    continue
                else:
                    if '*' in memeber_name:
                        query_string = f'host.name:{memeber_name}'
                    else:
                        query_string = f'host.name:"{memeber_name}"'
                    log.info(query_string)
                    {'extension' : 'hosts'}
                    hst = getter(**{'extension' : 'hosts'})
                    name_members = hst.search_manager(query_string )
                    if name_members is None or len(name_members) < 1:
                        mydb.add_name( memeber_name, name_ids)
                        log.error(f'member result no sutable:{name_members}')
                        continue
                    for name_member in name_members:
                        name_ids.append(name_member['id'])
                    mydb.add_name( memeber_name, name_ids)
                memeber_ids.extend(name_ids)
            memeber_ids = list(set(memeber_ids))
            data['members'].extend(memeber_ids)
        clean_data = {key: data[key] for key in self.valid_columns}       
        return clean_data
        

class rules(base_extension):
    def __init__(self, **kargs ):
        super().__init__(**kargs)
        #for post, put and patch
        self.valid_columns = 'description is_whitelist template additional_conditions source_conditions \
            detection detection_category triage_category'.split()
        self.data_prim_keys = 'description'.split()
        self.clmns_bool = 'enabled is_whitelist template'.split()
        self.clmns_dict =  'source_conditions additional_conditions'.split()

    #doc def tosend_clean_data(self,data): prepare data to send for upload
    def tosend_clean_data(self, data : dict, mode : str = 'patch') -> dict:
        #doc this apply only for host
        data = self.data_typing(data)
        clean_data = {key: data[key] for key in self.valid_columns}
        return  clean_data


class getter(base_extension):
    def __init__(self, **kargs):
        super().__init__(**kargs)



def get_exts() -> dict:
    exts = { 'groups' : {
            'cls' : groups, 
            'modes' :  'get post patch delete'.split() 
                 },
            'rules' : {
            'cls' : rules, 
            'modes' :  'get post patch delete'.split() 
                 },
    }
            
    getter_exts = 'accounts assignments assignment_outcomes audits campaigns detections \
             health hosts ip_addresses lockdown/account lockdown/host proxies search/hosts search/detections search/accounts  \
             sensor_token settings subnets tagging threatFeeds traffic usage/detect users \
             vectramatch/enablement vectra-match/status vectramatch/availabledevices vectra-match/rules \
              vectramatch/assignment vectra-match/alertstats vsensor'.split()
    for ext in getter_exts:
        exts[ext] = {'cls' : getter, 'modes' : ['get']}
    return exts
        
