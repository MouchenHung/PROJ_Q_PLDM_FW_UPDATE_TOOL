#!/usr/bin/env python3

import sys

import lib.json_cfg as json_lib
from lib.common_lib import Common_msg

APP_NAME = "PLDM UPDATE JSON CONFIG GENERATOR"
APP_AUTH = "Mouchen"
APP_RELEASE_VER = "1.0.0"
APP_RELEASE_DATE = "2023/01/11"

CONFIG_FILE = "pldm_cfg.json"

OEM_KEY = 65535 #0xFFFF
COMP_IMG_SET_VER_STR = "SWITCH_BOARD_DEVICE"
DESC_COM_IANA = "0000A015"

STAGE_CFG = {
    "poc" : "POC",
    "evt" : "EVT",
    "dvt" : "DVT",
    "pvt" : "PVT",
    "mp" : "MP",
}

# import common library
comm_msg = Common_msg()
msg_hdr_print = comm_msg.msg_hdr_print

# PACKAGE INFO - GrandTeton(SwitchBoard)
DESC_INFO_GT = [
    {
        "DescriptorType" : 1,
        "DescriptorData" : DESC_COM_IANA
    },
    {
        "DescriptorType" : OEM_KEY,
        "VendorDefinedDescriptorTitleString" : "Platform",
        "VendorDefinedDescriptorData" : "GrandTeton"

    },
    {
        "DescriptorType" : OEM_KEY,
        "VendorDefinedDescriptorTitleString" : "BoardID",
        "VendorDefinedDescriptorData" : "SwitchBoard"
    },
    {
        "DescriptorType" : OEM_KEY,
        "VendorDefinedDescriptorTitleString" : "Stage",
        "VendorDefinedDescriptorData" : "na"
    }
]
COMP_INFO = []

def APP_HELP():
    msg_hdr_print("n", "--------------------------------------------------------------------", "\n")
    msg_hdr_print("n", "HELP:")
    msg_hdr_print("n", "-p      Platform select.")
    msg_hdr_print("n", "          [gt] GrandTeton")
    msg_hdr_print("n", "-s      Stage select.")
    msg_hdr_print("n", "          [poc/evt/dvt/pvt/mp]")
    msg_hdr_print("n", "-c      Component id select.")
    msg_hdr_print("n", "          Please follow spec.")
    msg_hdr_print("n", "-v      Component version string select.")
    msg_hdr_print("n", "          Please follow spec, could be list.")
    msg_hdr_print("n", "")
    msg_hdr_print("n", "--------------------------------------------------------------------")

def APP_HEADER():
    msg_hdr_print("n", "========================================================")
    msg_hdr_print("n", "* APP name:    "+APP_NAME)
    msg_hdr_print("n", "* APP auth:    "+APP_AUTH)
    msg_hdr_print("n", "* APP version: "+APP_RELEASE_VER)
    msg_hdr_print("n", "* APP date:    "+APP_RELEASE_DATE)
    msg_hdr_print("n", "========================================================")

class APP_ARG():
    def __init__(self, argv):
        self.argv = argv
        self.argc = len(self.argv)
        self.platform_select = "na"
        self.stage_select = "na"
        self.comp_id_lst = []
        self.comp_verstr_lst = []

    def arg_parsing(self):
        collect_flag = [0,0,0,0]
        for i in range(self.argc):
            if self.argv[i] == "-p":
                if i+1 < self.argc:
                    if "-" not in self.argv[i+1]:
                        self.platform_select = self.argv[i+1]
                        i+=1
                        collect_flag[0] = 1

            if self.argv[i] == "-s":
                if i+1 < self.argc:
                    if "-" not in self.argv[i+1]:
                        self.stage_select = self.argv[i+1]
                        i+=1
                        collect_flag[1] = 1

            if self.argv[i] == "-c":
                if i+1 < self.argc:
                    for j in range(i+1, self.argc, 1):
                        if "-" in self.argv[j]:
                            break
                        else:
                            self.comp_id_lst.append(int(self.argv[j], 10))
                    i += len(self.comp_id_lst)
                    collect_flag[2] = 1

            if self.argv[i] == "-v":
                if i+1 < self.argc:
                    for j in range(i+1, self.argc, 1):
                        if "-" in self.argv[j]:
                            break
                        else:
                            self.comp_verstr_lst.append(self.argv[j])
                    i += len(self.comp_verstr_lst)
                    collect_flag[3] = 1
        
        for flag in collect_flag:
            if flag == 0:
                return 1

        if len(self.comp_id_lst) != len(self.comp_verstr_lst):
            msg_hdr_print('e', "component id count need to equal to component version count")
            return 1

        return 0

if __name__ == '__main__':
    APP_HEADER()

    if len(sys.argv) != 1:
        app_arg = APP_ARG(sys.argv)
        if app_arg.arg_parsing() == 1:
            msg_hdr_print('e', "Input argments error.")
            sys.exit(0)
        select_platform = app_arg.platform_select
        select_stage = app_arg.stage_select
        select_comp_id_lst = app_arg.comp_id_lst
        select_comp_version_lst = app_arg.comp_verstr_lst
    else:
        APP_HELP()
        sys.exit(0)

    PACKAGE_CONFIG = []
    DESC_INFO = []
    COMP_INFO = []

    if select_platform == "gt":
        DESC_INFO_GT[3]["VendorDefinedDescriptorData"] = STAGE_CFG[select_stage]
        DESC_INFO = DESC_INFO_GT

        for i in range(len(select_comp_id_lst)):
            COMP_INFO.append({
                "ComponentClassification" : OEM_KEY,
                "ComponentIdentifier" : select_comp_id_lst[i],
                "ComponentOptions" : [1],
                "RequestedComponentActivationMethod" : [0],
                "ComponentVersionString" : select_comp_version_lst[i]
            })
    else:
        msg_hdr_print('e', "Non-support platform " + str(select_platform))
        sys.exit(0)

    PACKAGE_CONFIG = [
        DESC_INFO,
        COMP_INFO
    ]

    json_lib.TOOL_pldm_json_WR('w', CONFIG_FILE, PACKAGE_CONFIG)

    msg_hdr_print("n", "pldm config file generate success!")
    msg_hdr_print("n", "please check output file " + CONFIG_FILE)
