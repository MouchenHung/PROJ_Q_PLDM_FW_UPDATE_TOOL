# PROJ_Q_PLDM_FW_UPDATE_TOOL
Package generator for pldm fw update.

### Purpose:
    Tools that used to generate package image for pldm fw update.

### First rlease date:
    * pldm_update_pkg_gen: v1.0.0 - 2023/01/11
    * pldm_fwup_pkg_creator: v1.0.0 - 2022/12/14

### Version:
pldm_update_pkg_gen
- 1.3.0 - Modify output package nameing format - 2023/03/07
  - Feature:
  	- Modify output package nameing format to **<project_name>** _ **<board_name>** _ **<component_version>** .pldm
	- Add Board name option **-b**.
  - Bug:
  	- none
- 1.2.0 - Support EXE(user do not need to download python) - 2023/01/31
  - Feature:
  	- Change UUID from v1.0.x to v1.1.0
	- Given release package only contains EXE file **pldm_update_pkg_gen**.
  - Bug:
  	- none
- 1.1.0 - Support Auto-GEN - 2023/01/17
  - Feature:
  	- Move platform config outside from code by creating folder 'platform'.
	- Add key '-i' for image path list
	- Support AUTO-GEN which could link with pldm_fwup_pkg_creator after json created.
  - Bug:
  	- Fix list element could not include '-' bug.
- 1.0.0 - First commit - 2023/01/11
  - Feature:
  	- none
  - Bug:
  	- none

pldm_fwup_pkg_creator
- 1.0.0 - First commit - 2022/12/14
  - Feature:
  	- Add MD5 at the end of package with 16bytes.
  - Bug: none

### Required:
- OS
  - Linux: support
  - Windows: support
- Enviroment
  - python3

### Usage
  - **STEP1. Create json config file**\
  Format: python3 pldm_update_pkg_gen.py -p **<project_name>** -b **<board_name>** -s **<project_stage>** -c **<component_id>** -v **<component_version>** -i **<component_image>**
    - project_name: Project name
    - board_name: Board name
    - project_stage: poc/evt/dvt/pvt/mp
    - component_id: should follow project spec
    - component_version: should follow project spec
    - component_image: binary image
```
mouchen@mouchen-System-Product-Name: pldm_update_pkg_gen -p gt -b swb -s pvt -c 0 -v GT_BIC_V?? -i GT_img.bin
========================================================
* APP name:    PLDM UPDATE PACKAGE GENERATOR
* APP auth:    Mouchen
* APP version: 1.3.0
* APP date:    2023/03/07
* NOTE: This APP is based on pldm_fwup_pkg_creator.py
========================================================
[STEP1]] Generate pldm config file
--> SUCCESS!

[STEP2]] Generate pldm package file
============================================================================================
* APP name:     PLDM FWUPDATE PACKAGE CREATOR
* APP auth:     opensource
* APP version:  1.0.0
* APP date:     2022/12/14
* OEM features:
  1. Support string type for data in vendor defined descriptors.
  2. Support MD5 hex parsing to last 16 bytes.
* NOTE: 
* 1. More detail, please check [https://github.com/openbmc/pldm/tree/master/tools/fw-update]
============================================================================================
--> SUCCESS!
```

### Note
- 1: none.

