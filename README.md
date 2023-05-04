[comment]: # "Auto-generated SOAR connector documentation"
# ReversingLabs TitaniumScale v2

Publisher: ReversingLabs  
Connector Version: 1.0.1  
Product Vendor: ReversingLabs  
Product Name: TitaniumScale  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 5.5.0  

App integrates with ReversingLabs TitaniumScale APIs

[comment]: # " File: README.md"
[comment]: # " Copyright (c) ReversingLabs, 2023"
[comment]: # ""
[comment]: # " Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # " you may not use this file except in compliance with the License."
[comment]: # " You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "     http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # " Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # " the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # " either express or implied. See the License for the specific language governing permissions"
[comment]: # " and limitations under the License. "



### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a TitaniumScale asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**url** |  required  | string | TitaniumScale URL
**token** |  required  | password | TitaniumScale token
**wait_time** |  optional  | numeric | Wait time (seconds)
**retries** |  optional  | numeric | Number of retries

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[detonate file and get report](#action-detonate-file-and-get-report) - Detonate file and return report  
[get report](#action-get-report) - Query for results of an already completed detonation  
[detonate file](#action-detonate-file) - Detonate file  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

Validate the asset configuration for connectivity using supplied configuration.

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'detonate file and get report'
Detonate file and return report

Type: **generic**  
Read only: **False**

Detonates file and returns report.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vault_id** |  required  | Vault ID of file to detonate | string |  `pe file`  `pdf`  `flash`  `apk`  `jar`  `doc`  `xls`  `ppt` 
**full_report** |  optional  | Return full report | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.vault_id | string |  `pe file`  `pdf`  `flash`  `apk`  `jar`  `doc`  `xls`  `ppt`  |  
action_result.parameter.full_report | boolean |  |  
action_result.data | string |  |  
action_result.status | string |  |   success  failed 
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |  
action_result.summary | string |  |    

## action: 'get report'
Query for results of an already completed detonation

Type: **investigate**  
Read only: **True**

Querys for results of an already completed detonation.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**task_url** |  required  | Task URL to get the report of | string | 
**full_report** |  optional  | Get full report | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.task_url | string |  |  
action_result.parameter.full_report | boolean |  |  
action_result.data | string |  |  
action_result.status | string |  |   success  failed 
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |  
action_result.summary | string |  |    

## action: 'detonate file'
Detonate file

Type: **generic**  
Read only: **False**

Detonates file and returns task ID (URL to get the report from).

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vault_id** |  required  | Vault ID of the file | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.vault_id | string |  |  
action_result.data | string |  |  
action_result.status | string |  |   success  failed 
action_result.message | string |  |  
summary.total_objects | numeric |  |  
summary.total_objects_successful | numeric |  |  
action_result.summary | string |  |  