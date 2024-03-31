# vectra_api_client_example
Example for vectra_api_client to export and import data to/from csv format

## Important Note: 
  This is not Vectra's official repo. I have created it out of my onw intrest. It's  pupose is to show example of ways to export and import files. I have performed very basic testing. Please read the code carefully and do your own research and testing before adopting it. 

Tested extension(mode) are:
* hosts (get)
* groups (get post patch)
* rules ( get post)


## Usage:
  1.Configure the file "./src/conf/config.json". Refer configuration:
  
  2.  Refer to INPUT section of the document:
 
  4.  Python3 run.py  -e <extension> -m <mode>.
     
```
python .\run.py --help
start_vapi_client
usage: run.py [-h] --extension EXTENSION --mode {get,post,patch,put,delete}

Make API calls for bulk operation on Vectra Brain

options:
  -h, --help            show this help message and exit
  --extension EXTENSION, -e EXTENSION
                        Extension of API: groups rules accounts assignments assignment_outcomes audits campaigns detections health hosts ip_addresses lockdown/account
                        lockdown/host proxies search sensor_token settings subnets tagging threatFeeds traffic usage/detect users vectramatch/enablement vectra-match/status      
                        vectramatch/availabledevices vectra-match/rules vectramatch/assignment vectra-match/alertstats vsensor
  --mode {get,post,patch,put,delete}, -m {get,post,patch,put,delete}
                        Mode of operaton. Most of extension support only get mode. The overall options are: get post patch put delete.
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
* push: push_groups_csv: The data to create new extension objects per row in file.
  Mandotery : Name
  * name: Name of the group
  * description:description
  * type: host or domainor ip
  * members: menebers of groups. For hosts please use the id of host.
  * member_name: name of the memeber. It apply onlky to host type.
    
* patch: patch_groups_csv The data to update extension objects per row in file.
  Mandotery: One of id, name, description (perference in exact sequence) to find the refernce group.
  * id: of the group .
  * name: Name of the group
  * description:description
  * type: host or domainor ip
  * members: menebers of grousp. For hosts please use the id of host.
     Note: if the folwing feild ( ID or Name or description) must be present .

## Output
  The files are saved in conf directory with 
  1. Output: output_groups_csv.csv contain all the details sepcifc extension. I have tsted it only with hosts and groups.
     Columns : Dynamic ; created based on keys in response .  

