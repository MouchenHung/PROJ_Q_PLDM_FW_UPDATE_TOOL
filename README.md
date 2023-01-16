# PROJ_Q_PLDM_FW_UPDATE_TOOL
Package generator for pldm fw update.

### Purpose:
    Tools that used to generate package image for pldm fw update.

### First rlease date:
    * pldm_update_pkg_gen: v1.0.0 - 2023/01/11
	  * pldm_fwup_pkg_creator: v1.0.0 - 2022/12/14

### Version:
* pldm_update_pkg_gen
- 1.0.0 - First commit - 2023/01/11
  - Feature: none
  - Bug: none

* pldm_fwup_pkg_creator
- 1.0.0 - First commit - 2022/12/14
  - Feature: none
  - Bug: none

### Required:
- OS
  - Linux: support
  - Windows: support
- Enviroment
  - python3

### Usage
  - **STEP1. Create json config file**\
  Format: python3 pldm_update_pkg_gen.py -p **<project_name>** -s **<project_stage>** -c **<component_id>** -v **<component_version>**
    - project_name: Project name
    - project_stage: poc/evt/dvt/pvt/mp
    - component_id: should follow project spec
    - component_version: should follow project spec
```
mouchen@mouchen-System-Product-Name: python3 pldm_update_pkg_gen.py -p gt -s pvt -c 0 -v GT_BIC_V??
========================================================
* APP name:    PLDM UPDATE JSON CONFIG GENERATOR
* APP auth:    Mouchen
* APP version: 1.0.0
* APP date:    2023/01/11
========================================================
pldm config file generate success!
please check output file pldm_cfg.json
```

  - **STEP2. Generate package by json config file and images**\
  Format: python3 pldm_fwup_pkg_creator.py **<package_name>** **<json_path>** **<image_path(s)>**
    - package_name: output package image name
    - json_path: json config file(should always given "pldm_cfg.json")
    - image_path: fw image(s)
```
mouchen@mouchen-System-Product-Name: python3 pldm_fwup_pkg_creator.py pldm_bic.bin pldm_cfg.json bic_image.bin 
===============================================================
* version:  1.0.0
* date:     2022/12/14
* features:
  1. Support string type for data in vendor defined descriptors.
  2. Support MD5 hex parsing to last 16 bytes.
===============================================================
--> SUCCESS!
```

### Note
- 1: none.

