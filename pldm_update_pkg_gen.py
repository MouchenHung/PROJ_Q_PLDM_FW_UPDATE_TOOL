#!/usr/bin/env python3

import sys, subprocess, os

import lib.json_cfg as json_lib
from lib.common_lib import Common_msg, Common_file

APP_NAME = "PLDM UPDATE PACKAGE GENERATOR"
APP_AUTH = "Mouchen"
APP_RELEASE_VER = "1.3.0"
APP_RELEASE_DATE = "2023/03/07"

PLATFORM_PATH = "./platform"
CONFIG_FILE = "pldm_cfg.json"
DEF_PKG_FILE = "default_package.pldm"

OEM_KEY = 65535 #0xFFFF

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
comm_file = Common_file()
is_file_exist = comm_file.is_file_exist
resource_path = comm_file.resource_path

def APP_HELP():
    msg_hdr_print("n", "--------------------------------------------------------------------", "\n")
    msg_hdr_print("n", "HELP:")
    msg_hdr_print("n", "-p      Platform select.")
    msg_hdr_print("n", "          [gt] GrandTeton")
    msg_hdr_print("n", "-b      Board select.")
    msg_hdr_print("n", "          [swb] SwitchBoard")
    msg_hdr_print("n", "-s      Stage select.")
    msg_hdr_print("n", "          [poc/evt/dvt/pvt/mp]")
    msg_hdr_print("n", "-c      Component id select.")
    msg_hdr_print("n", "          Please follow spec, could be list.")
    msg_hdr_print("n", "-v      Component version string select.")
    msg_hdr_print("n", "          Please follow spec, could be list.")
    msg_hdr_print("n", "-i      Component image select.")
    msg_hdr_print("n", "          Please follow spec, could be list.")
    msg_hdr_print("n", "")
    msg_hdr_print("n", "--------------------------------------------------------------------")

def APP_HEADER():
    msg_hdr_print("n", "========================================================")
    msg_hdr_print("n", "* APP name:    "+APP_NAME)
    msg_hdr_print("n", "* APP auth:    "+APP_AUTH)
    msg_hdr_print("n", "* APP version: "+APP_RELEASE_VER)
    msg_hdr_print("n", "* APP date:    "+APP_RELEASE_DATE)
    msg_hdr_print("n", "* NOTE: This APP is based on pldm_fwup_pkg_creator.py")
    msg_hdr_print("n", "========================================================")

class APP_ARG():
    def __init__(self, argv):
        self.argv = argv
        self.argc = len(self.argv)
        self.platform_select = "na"
        self.board_select = "na"
        self.stage_select = "na"
        self.comp_id_lst = []
        self.comp_verstr_lst = []
        self.comp_img_lst = []

    def arg_parsing(self):
        #collect_flag = [0,0,0,0,0]
        keyword_lst = ["-p", "-b", "-s", "-c", "-v", "-i"]
        collect_flag = [0] * len(keyword_lst)
        for i in range(self.argc):
            if self.argv[i] == "-p":
                if i+1 < self.argc:
                    if "-" not in self.argv[i+1]:
                        self.platform_select = self.argv[i+1]
                        i+=1
                        collect_flag[0] = 1

            if self.argv[i] == "-b":
                if i+1 < self.argc:
                    if "-" not in self.argv[i+1]:
                        self.board_select = self.argv[i+1]
                        i+=1
                        collect_flag[1] = 1

            if self.argv[i] == "-s":
                if i+1 < self.argc:
                    if "-" not in self.argv[i+1]:
                        self.stage_select = self.argv[i+1]
                        i+=1
                        collect_flag[2] = 1

            if self.argv[i] == "-c":
                if i+1 < self.argc:
                    for j in range(i+1, self.argc, 1):
                        if self.argv[j] in keyword_lst:
                            break
                        else:
                            self.comp_id_lst.append(int(self.argv[j], 10))
                    i += len(self.comp_id_lst)
                    collect_flag[3] = 1

            if self.argv[i] == "-v":
                if i+1 < self.argc:
                    for j in range(i+1, self.argc, 1):
                        if self.argv[j] in keyword_lst:
                            break
                        else:
                            self.comp_verstr_lst.append(self.argv[j])
                    i += len(self.comp_verstr_lst)
                    collect_flag[4] = 1

            if self.argv[i] == "-i":
                if i+1 < self.argc:
                    for j in range(i+1, self.argc, 1):
                        if self.argv[j] in keyword_lst:
                            break
                        else:
                            self.comp_img_lst.append(self.argv[j])
                    i += len(self.comp_img_lst)
                    collect_flag[5] = 1
        
        for flag in collect_flag:
            if flag == 0:
                msg_hdr_print('e', "Input argments lost.")
                return 1

        if len(self.comp_id_lst) != len(self.comp_verstr_lst) or len(self.comp_verstr_lst) != len(self.comp_img_lst):
            msg_hdr_print('e', "component id, version, image count should be the same")
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
        select_board = app_arg.board_select
        select_stage = app_arg.stage_select
        select_comp_id_lst = app_arg.comp_id_lst
        select_comp_version_lst = app_arg.comp_verstr_lst
        select_comp_img_lst = app_arg.comp_img_lst
    else:
        APP_HELP()
        sys.exit(0)

    PACKAGE_CONFIG = []
    DESC_INFO = []
    COMP_INFO = []

    cfg_file = resource_path(PLATFORM_PATH + "/cfg_" + str(select_platform) + "_" + str(select_board) + ".json")
    if not is_file_exist(cfg_file):
        msg_hdr_print('e', "Can't find config file of platform [" + str(select_platform) + "] board [" + str(select_board) + "]")
        sys.exit(0)

    PLAT_INFO = json_lib.TOOL_pldm_plat_cfg_R(cfg_file)
    DESC_INFO = PLAT_INFO[0]

    try:
        DESC_INFO[3]["VendorDefinedDescriptorData"] = STAGE_CFG[select_stage]
    except:
        msg_hdr_print('e', "Invalid given stage [" + str(select_stage) + "]")
        APP_HELP()
        sys.exit(0)

    package_name_lst = []
    found_verify_flag = 0
    for i in range(len(select_comp_id_lst)):
        for comp in PLAT_INFO[1]:
            if select_comp_id_lst[i] in comp["CompID"]:
                version_prefix = comp["Device"]
                if version_prefix in select_comp_version_lst[i]:
                    found_verify_flag = 1
                    break
        
        if not found_verify_flag:
            msg_hdr_print('e', "Can't find support device by given component version [" + str(select_comp_version_lst[i]) + "]")
            sys.exit(0)

        package_name_lst.append(str(select_platform) + "_" + str(select_board) + "_" + str(select_comp_version_lst[i]) + comp["pkg_suffix"])

        COMP_INFO.append({
            "ComponentClassification" : OEM_KEY,
            "ComponentIdentifier" : select_comp_id_lst[i],
            "ComponentOptions" : [1],
            "RequestedComponentActivationMethod" : [0],
            "ComponentVersionString" : select_comp_version_lst[i]
        })

    PACKAGE_CONFIG = [
        DESC_INFO,
        COMP_INFO
    ]

    msg_hdr_print("n", "[STEP1]] Generate pldm config file")
    json_lib.TOOL_pldm_json_WR('w', CONFIG_FILE, PACKAGE_CONFIG)

    msg_hdr_print("n", "--> SUCCESS!")

    msg_hdr_print("n", "\n[STEP2]] Generate pldm package file")

    if len(select_comp_id_lst) != 1:
        pkg_file_name = DEF_PKG_FILE
        msg_hdr_print("n", "Using default package file name " + DEF_PKG_FILE + ", cause of muti-comp case.")
    else:
        pkg_file_name = package_name_lst[0]

    cmd_line = ["python3", resource_path("pldm_fwup_pkg_creator.py"), pkg_file_name, CONFIG_FILE]
    for img in select_comp_img_lst:
        if not is_file_exist(img):
            msg_hdr_print('e', "Invalid given image [" + str(img) + "]")
            sys.exit(0)
        cmd_line.append(img)

    subprocess.run(cmd_line)
