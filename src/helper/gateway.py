import json
from helper.utils import conf 
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class portal():
    def __init__(self) -> None:
        self.get_req_param()

    def get_req_param(self):
        rq = {
        'api_version' :  conf.get('api_version', 'v2.5'),
        'vec_he' : conf.get('vec_he', 'localhost'),
        'vec_auth_token' : conf.get('vec_api_token'),
        }
        rq['headers'] = {'Content-Type': 'application/json', 'Authorization': f'Token {rq["vec_auth_token"]}'}
        rq['vec_base_url'] = 'https://' + rq['vec_he'] + '/api/' + rq['api_version']
        self.rq = rq
        

    def get_many(self, ext, query = None):
        payload = { 'page_size' : conf.get('max_page_size',5000) , 'page': 0}
        if query is not None:
            payload.update(query)
        result_data = []
        send_query = 'yes'
        url_final = self.rq['vec_base_url'] + f'/{ext}'
        #print(f'sensing request to {url_final=}')
        while send_query is not None:
            payload['page'] += 1 
            if conf.get('max_page_number', 500) <  payload['page']:
                print('Stopping at Maximum page count of intetration: {}'.format(conf.get('max_page_number', 500)))
                break
            response = requests.get(url=url_final, params=payload, verify=False, headers=self.rq['headers'])
            #print(response)
            result = response.json()
            if result is None:
                continue
            send_query = result.get('next')
            result_results = result.get('results')
            if result_results is None:
                result_data.append(result_results)
                continue
        return result_results
    
    def post_one(self, ext, data):
        data_json = json.dumps(data)
        url_final = self.rq['vec_base_url'] + f'/{ext}'
        response = requests.post(url=url_final, data=data_json, verify=False, headers=self.rq['headers'])
        if response.ok:
            #print(f'Request sucessfull: {response.text=}')
            pass
        else:
            print(f'Got some error in response: {response.text=}')

    def patch_one(self, ext, id, data):
        data_json = json.dumps(data)
        url_final = self.rq['vec_base_url'] + f'/{ext}/{id}'
        print(f'sensing request to {url_final=}')
        response = requests.patch(url=url_final, data=data_json, verify=False, headers=self.rq['headers'])
        if response.ok:
            #print(f'Request sucessfull: {response.text=}')
            pass
        else:
            print(f'Got some error in response: {response.text=}')




