# vectra_api_client_example
Example for vectra_api_client to export and import data to/from csv format

## Important Note: 
  This is not Vectra's official repo. I have created it out of my own interest. It's  pupose is to show example to perform  bulk export and import data to and from vectra( with csv file) quaderent UX using API. I have performed very basic testing. Please read the code carefully and do your own research and testing before adopting it. 

# Tested extension(mode) are:
* hosts (get)
* groups (get post patch)
* rules ( get post)
* search/\[hosts,detection,accounts]


# How ot run:
  1.Configure the file "./src/conf/config.json". Refer configuration:
  
  2.  Refer to INPUT section of the document:
 
  4.  Python3  run.py  --extension EXTENSION --mode {get,post,patch,put,delete}
     
```
# python .\run.py --help
start_vapi_client
usage: run.py [-h] --extension EXTENSION --mode {get,post,patch,put,delete} [--query QUERY] [--payload PAYLOAD]

Make API calls for bulk operation on Vectra Brain

options:
  -h, --help            show this help message and exit
  --extension EXTENSION, -e EXTENSION
                        Extension of API: groups rules accounts assignments assignment_outcomes audits campaigns detections health hosts        
                        ip_addresses lockdown/account lockdown/host proxies search/hosts search/detections search/accounts sensor_token settings
                        subnets tagging threatFeeds traffic usage/detect users vectramatch/enablement vectra-match/status
                        vectramatch/availabledevices vectra-match/rules vectramatch/assignment vectra-match/alertstats vsensor
  --mode {get,post,patch,put,delete}, -m {get,post,patch,put,delete}
                        Mode of operaton. Most of extension support only get mode. The overall options are: get post patch put delete.
  --query QUERY, -q QUERY
                        To use query with search extension
  --payload PAYLOAD, -p PAYLOAD
                        To update the default payload```  

# Example:
- hosts - with default payload:
```
python .\run.py -e hosts -m get
start_vapi_client
args are : {'extension': 'hosts', 'mode': 'get', 'query': None, 'payload': None}
sending GET with payload={'page_size': 500, 'page': 0} request to url_final='https://myserver/api/v2.5/hosts'
saved the result in /tmp/api_work/output_hosts_240411233553_json.json
saved the result in /tmp/api_work/output_hosts_240411233553_csv.csv
FYI only: No member_name queried
stop_vapi_client
Script finished! The operation logs are /tmp/api_work/api_logs.log
```
- hosts - With updated payload
```
#python .\run.py -e hosts -m get -p  '{\"state\":\"active\"}'

start_vapi_client
args are : {'extension': 'hosts', 'mode': 'get', 'query': None, 'payload': '{"state":"active"}'}
sending GET with payload={'page_size': 500, 'page': 0, 'state': 'active'} request to url_final='https://myserver/api/v2.5/hosts'
saved the result in /tmp/api_work/output_hosts_240411233047_json.json
saved the result in /tmp/api_work/output_hosts_240411233047_csv.csv
FYI only: No member_name queried
stop_vapi_client
Script finished! The operation logs are /tmp/api_work/api_logs.log
``` 
  -  search/hosts :
```
>> python .\run.py -e search/hosts -m get -q host.name:7_ghost
start_vapi_client
{'extension': 'search/hosts', 'mode': 'get', 'query': 'host.name:7_ghost'}
sending GET with query={'query_string': 'host.name:7_ghost'} request to url_final='https://myserver/api/v2.5/search/hosts'
saved the result in /tmp/api_work/output_search_hosts_240402013418_json.json
saved the result in /tmp/api_work/output_search_hosts_240402013418_csv.csv
FYI only: No member_name queried
stop_vapi_client
Script finished! The operation logs are /tmp/api_work/api_logs.log
```
  -  groups
```
python .\run.py -e groups -m post  
start_vapi_client
args are : {'extension': 'groups', 'mode': 'post', 'query': None}
sending GET with query={'query_string': 'host.name:"13_ghost_1"'} request to url_final='https://myserver/api/v2.5/search/hosts'
sending GET with query={'query_string': 'host.name:11_ghost_*'} request to url_final='https://myserver/api/v2.5/search/hosts'
sending POST request to url_final='https://192.168.52.185/api/v2.5/groups'
Request sucessfull: response.text='{"group": {"id": 31}}'
sending GET with query={'query_string': 'host.name:"12_ghost_1"'} request to url_final='https://myserver/api/v2.5/search/hosts'
sending GET with query={'query_string': 'host.name:10_ghost_*'} request to url_final='https://myserver/api/v2.5/search/hosts'
sending POST request to url_final='https://192.168.52.185/api/v2.5/groups'
Request sucessfull: response.text='{"group": {"id": 32}}'
saved the result in /tmp/api_work/output_groups_member_name_searched_240402013951_json.json
saved the result in /tmp/api_work/output_groups_member_name_searched_240402013951_csv.csv
4 memeber names searched. result are saved in :groups_member_name_searched
stop_vapi_client
Script finished! The operation logs are /tmp/api_work/api_logs.log
```


## Configuration:
  1. conf/config.json
- "vec_he": Vectra Brain IP or FQDN
- "vec_api_token": Vectra_api_token
-  "max_page_number" : Maxumum number of pages 
-   max_page_size" : Maxumum result per page
-   vec_api_version" :  "v2.5"
- "work_dir": The directory of result or imput files. Default is{ Linux: "/tmp/api_work" , Windows: "c:/tmp/api_work" 
- "output_file_suffix" : "output",
- "push_csv": "push_csv.csv"

## Input
For POST and PATCH configure the file at location specified in key "work_dir" in [config.json](/src/conf/config.json). Please refer the example from [input_example](input_example) folder.
- File Name: The file 'name'should be like {mode}_{extension}_csv.CSV and steacture are static.Here is example:
        For
       - {extnsion : groups , mode : post} ;  the file should be "post_groups_csv.csv"
       - {extnsion ; groups,  mode : patch ;  the file should be "patch_groups_csv.csv"
- File Format: Refer to input feild from API document as set them as column.
  Once extra columns is 'member_name' to add the memebers of specific name.

#### Groups 
* Feature:  "member_name"  alow to add hosts by name and it supports "wildcard"(*) 

* push: push_groups_csv: The data to create new extension objects per row in file.
  Mandotery : Name
  * name: Name of the group
  * description:description
  * type: host or domainor ip
  * members: menebers of groups. For hosts please use the id of host.
  * member_name: name of the memeber. It apply only to host type. I allows wildcard.
    
* patch: patch_groups_csv The data to update extension objects per row in file.
  Mandotery: One of id, name, description (perference in exact sequence) to find the refernce group.
  * id: of the group .
  * name: Name of the group
  * description:description
  * type: host or domainor ip
  * members: menebers of grousp. For hosts please use the id of host.
  * member_name:  name of the memeber. It apply only to host type. I allows wildcard.

    

## Output
  The files are saved in conf directory with 
  1. Output: output_groups_csv.csv contain all the details sepcifc extension. I have tsted it only with hosts and groups.
     Columns : Dynamic ; created based on keys in response .  

