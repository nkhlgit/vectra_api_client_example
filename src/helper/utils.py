import os
import json
import csv
from pathlib import Path
from helper.csv_util import to_csv
from .settings import conf
import logging
log = logging.getLogger(__name__)

class pathfinder():

    def __init__(self) -> None:
        self.script_dir = os.path.realpath(os.path.dirname(__file__))
        self.log_file = f'{self.get_work_dir(create = True)}/api_logs.log'
        self.file_type = ['json','csv']
                        
    def get_work_dir(self, create: bool = False) -> Path:
        work_dir = conf.get('work_dir', f'{self.script_dir}/api_work')
        if Path(work_dir).is_dir():
            return work_dir
        elif not create:
            return None
        Path(work_dir).mkdir(parents=True, exist_ok=True)
        return work_dir
    
    def save_csv(self, ext, data_list: list, output_file ):
        field_names = data_list[0].keys()
        csv_writer = csv.DictWriter(output_file, fieldnames=field_names)
        csv_writer.writeheader()
        data_list_csv = to_csv(ext ,data_list)
        csv_writer.writerows(data_list_csv)

    def save_to_file(self,ext : str, data_list : list) -> None:
        work_dir = self.get_work_dir(create= True)
        if len(data_list) < 1 or len(self.file_type) < 1:
            log.error(f'Cannot save the result : {data_list=} ; {self.file_type=}')
            return
        output_file_suffix = conf.get('output_file_suffix', 'output')
        output_file_suffix_ext = f'{output_file_suffix}_{ext}'
        for t in self.file_type:
            output_file_name = f'{output_file_suffix_ext}_{t}.{t}'
            output_file = open(f'{work_dir}/{output_file_name}', 'w+', newline='')
            if t == 'csv':
                self.save_csv(ext, data_list, output_file)
            if t == 'json':
                json.dump(data_list, output_file)
            output_file.close()
            log.info(f'saved the result in {work_dir}/{output_file_name}')

    def get_input(self,method : str, ext : str) -> list :
        if (work_dir := self.get_work_dir(create=False)) is None:
            log.info(f'{work_dir=}" do not exist')
            return
        in_file_key = f'{method}_{ext}_csv'
        post_csv =  work_dir + '/' + conf.get(in_file_key ,f'{in_file_key}.csv') 
        post_csv_file = open(post_csv,'r', newline='')
        csv_reader = csv.DictReader(post_csv_file)
        data_list = list(csv_reader)
        for data in data_list:
            data['members'] = data['members'].split(',')
        if len(data_list) < 1:
            log.info(' Zero input read from file : {data_list}')
        return data_list
