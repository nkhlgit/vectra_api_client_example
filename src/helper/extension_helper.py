import json
from helper.settings import conf, pnt, constants 
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import logging
log = logging.getLogger(__name__)


class portal():
    def __init__(self) -> None:
        self.get_req_param()
        self.TIMEOUT = 10

    def get_req_param(self):
        rq = {
        'api_version' :  conf.get('vec_api_version', constants.get('max_vec_api_version')),
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
        msg = f'sending GET with {query=} request to {url_final=}'
        log.info(msg)
        print(pnt.info(msg))
        while send_query is not None:
            payload['page'] += 1 
            if conf.get('max_page_number', 500) <  payload['page']:
                log.info('Stopping at Maximum page count of intetration: {}'.format(conf.get('max_page_number', 500)))
                print(pnt.info('Stopping at Maximum page count of intetration: {}'.format(conf.get('max_page_number', 500))))
                break
            try:
                response = requests.get(url=url_final, 
                                        params=payload, 
                                        verify=False, 
                                        headers=self.rq['headers'], 
                                        timeout=self.TIMEOUT,
                                        )
                if response.ok:
                    log.debug(f'Request sucessfull: {response.text=}')
                else:
                    err_msg = f'Got some error in response: {response.text=}'
                    print(pnt.error(err_msg))
                    log.error(err_msg)
                    break
            except Exception as e:
                err_msg = f'Error offcured in request: {e}'
                print(pnt.error(err_msg))
                log.error(err_msg)
                break
            result = response.json()
            if not result or result is None:
                continue
            send_query = result.get('next', None)
            result_results = result.get('results')
            if result_results is not None:
                result_data.extend(result_results)
                continue
        return result_data
    
    def post_one(self, ext, data):
        data_json = json.dumps(data)
        url_final = self.rq['vec_base_url'] + f'/{ext}'
        msg = f'sending POST request to {url_final=}'
        log.info(msg)
        print(pnt.info(msg))
        try:
            response = requests.post(url=url_final, data=data_json, verify=False, headers=self.rq['headers'],timeout=self.TIMEOUT)
            if response.ok:
                log.debug(f'Request sucessfull: {response.text=}')
            else:
                err_msg = f'Got some error in response: {response.text=}'
                print(pnt.error(err_msg))
                log.error(err_msg)
        except Exception as e:
            err_msg = f'Error offcured in request: {e}'
            print(pnt.error(err_msg))
            log.error(err_msg)

    def patch_one(self, ext, id, data):
        data_json = json.dumps(data)
        url_final = self.rq['vec_base_url'] + f'/{ext}/{id}'
        msg = f'sending PATCH request to {url_final=}'
        log.info(msg)
        print(pnt.info(msg))
        try:
            response = requests.patch(url=url_final, data=data_json, verify=False, headers=self.rq['headers'], timeout=self.TIMEOUT)
            if response.ok:
                log.debug(f'Request sucessfull: {response.text=}')
            else:
                err_msg = f'Got some error in response: {response.text=}'
                print(pnt.error(err_msg))
                log.error(err_msg)
        except Exception as e:
            err_msg = f'Error offcured in request: {e}'
            print(pnt.error(err_msg))
            log.error(err_msg)

    def delete_one(self, ext, id):
        url_final = self.rq['vec_base_url'] + f'/{ext}/{id}'
        msg = f'sending DELETE request to {url_final=}'
        log.info(msg)
        print(pnt.info(msg))
        try:
            response = requests.delete(url=url_final, verify=False, headers=self.rq['headers'], timeout=self.TIMEOUT)
            if response.ok:
                log.debug(f'Request sucessfull: {response.text=}')
            else:
                err_msg = f'Got some error in response: {response.text=}'
                print(pnt.error(err_msg))
                log.error(err_msg)
        except Exception as e:
            err_msg = f'Error offcured in request: {e}'
            print(pnt.error(err_msg))
            log.error(err_msg)

