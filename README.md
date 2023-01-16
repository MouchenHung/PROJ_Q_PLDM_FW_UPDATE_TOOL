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
           --> python3 pldm_update_pkg_gen.py -p gt -s <STAGE> -c 0 -v <CUSTOM>
```
mouchen@mouchen-System-Product-Name: python3 pldm_update_pkg_gen.py -p gt -s pvt -c 3 4 5 6 -v broadcom_pex89000_v5 broadcom_pex89000_v5 broadcom_pex89000_v5 broadcom_pex89000_v5            ========================================================
* APP name:    PLDM UPDATE JSON CONFIG GENERATOR
* APP auth:    Mouchen
* APP version: 1.0.0
* APP date:    2023/01/11
========================================================
pldm config file generate success!
please check output file pldm_cfg.json
```

  - **STEP2. Generate package by json config file and images**
    - block_unit: Output image's block unit for last image padding, using k(1024b) as base
    - output_path: Final combine-image path
    - encryption: MD5 16bytes adding or not("enable" to active)
    - name: One image name(should not modify!)
    - path: One image path
    - offset: One image start offset(This might cause some problem if set in wrong address)

  - **STEP3. Run**\
           --> python img_comb.py --> choose mode[1] to use cfg-offset mode
           --> python img_comb.py -m 1 --> to choose mode[1] to use cfg-offset mode
```
mouchen@mouchen-System-Product-Name: ./img_comb
========================================================
* APP name:    IMAGES COMBINE SCRIPT
* APP auth:    Mouchen
* APP version: 1.1.1
* APP date:    2022.11.03
========================================================
<system> Mode select
         [0] Create an demo config file.
         [1] Combine images with offset in config file.
         [2] Combine images automatic by padding offset.
         * Note: [1]/[2] config file required!
>> mode: 1
<system> Start combine images task by given offset.

<system> Reading config file...
[Common config]
* block_unit:   64
* output_path:  output_img.bin
* encryption:   enable
[Image config]
* Img0:
       path:    ./img/test_img0.bin
       exist:   O
       offset:  0x24
       size:    274k(280792 bytes)
* Img1:
       path:    ./img/test_img1.bin
       exist:   O
       offset:  0x4b024
       size:    274k(280792 bytes)
* Img2:
       path:    ./img/test_img2.bin
       exist:   O
       offset:  0x96024
       size:    274k(280792 bytes)
* Img3:
       path:    ./img/test_img3.bin
       exist:   O
       offset:  0xe1024
       size:    274k(280792 bytes)

<system> Adding header to image...

<system> Start combine binary files...
         Combine Img_0...
         Combine Img_1...
         Combine Img_2...
         Combine Img_3...

<system> Adding MD5 encryption bytes to image...

<system> Image combine success with 1216k(1245200b).
         Please check output file named "output_img.bin"
```
\
           --> python img_comb.py --> choose mode[2] to use auto-offset mode
           --> python img_comb.py -m 2 --> to choose mode[2] to use auto-offset mode
```
mouchen@mouchen-System-Product-Name: ./img_comb
========================================================
* APP name:    IMAGES COMBINE SCRIPT
* APP auth:    Mouchen
* APP version: 1.1.1
* APP date:    2022.11.03
========================================================
<system> Mode select
         [0] Create an demo config file.
         [1] Combine images with offset in config file.
         [2] Combine images automatic by padding offset.
         * Note: [1]/[2] config file required!
>> mode: 2
<system> Start combine images task by padding offset with interval 16 bytes.

<system> Reading config file...
[Common config]
* block_unit:   64
* output_path:  output_img.bin
* encryption:   enable
[Image config]
* Img0:
       path:    ./img/test_img0.bin
       exist:   O
       offset:  0x24
       size:    274k(280792 bytes)
* Img1:
       path:    ./img/test_img1.bin
       exist:   O
       offset:  0x4490c
       size:    274k(280792 bytes)
* Img2:
       path:    ./img/test_img2.bin
       exist:   O
       offset:  0x891f4
       size:    274k(280792 bytes)
* Img3:
       path:    ./img/test_img3.bin
       exist:   O
       offset:  0xcdadc
       size:    274k(280792 bytes)

<system> Adding header to image...

<system> Start combine binary files...
         Combine Img_0...
         Combine Img_1...
         Combine Img_2...
         Combine Img_3...

<system> Adding MD5 encryption bytes to image...

<system> Image combine success with 1152k(1179664b).
```

### Note
- 1: Please choose mode[0] to create folder ***./img*** and demo config file ***config.txt*** if first using this APP.
- 2: Only need to modify ***config.txt*** and choose mode[1] after finished mode[0].
- 3: Images in ***./img*** folder is just demo, please add your own images into it.
- 4: Images must only put in ***./img*** folder.
- 5: If you have no idea how to set offsets of 4 images, then **mode[2] is recommended!** Instead of setting offsets in config file.

