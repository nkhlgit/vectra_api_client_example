# vectra_api_client_example
Example for vectra_api_client to export and import data to/from csv format

## Important Note: 
  This is not Vectra's official repo. I have created it out of my onw intrest. It's  pupose is to show example of ways to export and import files. I have performed very basic testing. Please read the code carefully and do your own research and testing before adopting it. 

## Usage:
  1.Configure the  
    - conf/config.json. Refer configuration:
  
  2. unhash run.py  for specific function operation.
     - get_mamanger =  to pull the data in bulk
     - push_manager = To created data in bulk. create input file. refer Input/Output: push_groups_csv file
     - Patch manager to edit data in bulk  
  3. Python3 ./src/run.py

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

## Input/Output
  The files are saved in conf directory with 
  1. Output: output_groups_csv.csv contain all the details sepcifc extension. I have tsted it only with hosts and groups.
     Columns : Dynamic ; created based on keys in response .  
  2. push_groups_csv: The data to create new extension objects per row in file.
     Exampe for Group:
     name: Name of the group
     description:description
     type: host or domainor ip
     members: menebers of grousp. For hosts please use the id of host.
       
  3. patch_groups_csv The data to update extension objects per row in file.
     Exampe for Group: 
     id: of the group . 
     name: Name of the group
     description:description
     type: host or domainor ip
     members: menebers of grousp. For hosts please use the id of host.
     Note: if the folwing feild ( ID or Name or description) must be present .
