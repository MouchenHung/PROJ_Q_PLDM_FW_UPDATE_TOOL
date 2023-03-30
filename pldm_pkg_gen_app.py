#!/usr/bin/env python3

from pickle import TRUE
import sys, os, subprocess
from PyQt5 import QtCore, QtGui
import lib.json_cfg as json_lib
from lib.common_lib import Common_file, Common_time, System_ctrl

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import pldm_update_pkg_gen_ui

comm_file = Common_file()
is_file_exist = comm_file.is_file_exist
resource_path = comm_file.resource_path
log_record = comm_file.log_record

comm_time = Common_time()
get_time = comm_time.get_time

comm_sys = System_ctrl()
platform_os = comm_sys.os_name.lower()

DBG_EN = False

# Version
RELEASE_VER = "v1.0.1"
RELEASE_DATE = "2023.03.30"
VERSION_STR = RELEASE_VER + " - " + RELEASE_DATE

PLATFORM_PATH = "./platform"
platform_cfg_prefix = PLATFORM_PATH + "/cfg_"
LOG_FILE = "./log.txt"

# How to use text file
HTU_FILE = "./htu.txt"

# EXE file
EXE_WIN_FILE = "pldm_update_pkg_gen.exe"
EXE_LINUX_FILE = "./pldm_update_pkg_gen"

TABLE_DISPLAY_LST = [
    "id",
    "version",
    "image",
]

STAGE_LST = [
    "evt",
    "dvt",
    "pvt",
    "mp",
]

platform_lst = []
board_lst = []

id_lst = []
version_lst = []
img_lst = []

cur_cfg_file = ""

if platform_os == "windows":
    command_prefix = EXE_WIN_FILE
    if not is_file_exist(EXE_WIN_FILE):
        print("Can't find exe file " + EXE_WIN_FILE)
        log_record(LOG_FILE, "append", "Can't find exe file " + EXE_WIN_FILE + "\n")
        sys.exit(1)
elif platform_os == "linux":
    command_prefix = EXE_LINUX_FILE
    if not is_file_exist(EXE_LINUX_FILE):
        print("Can't find exe file " + EXE_LINUX_FILE)
        log_record(LOG_FILE, "append", "Can't find exe file " + EXE_LINUX_FILE + "\n")
        sys.exit(1)
else:
    print("Current os " + platform_os + " is not supported!")
    log_record(LOG_FILE, "append", "Current os " + platform_os + " is not supported!\n")
    sys.exit(1)

if DBG_EN == True:
    command_prefix = "python pldm_update_pkg_gen.py"

# ===================================================== HOW_TO_USE PAGE ====================================================
class HowToUsePage(QMainWindow):
    def __init__(self):
        super(HowToUsePage, self).__init__()

        self.setWindowTitle("Release Note")
        self.setGeometry(0, 0, 1000, 1000)

        self.TITLE = QLabel("<< Welcome to PLDM PACKAGE GENERATOR APP user guide >>", self)
        self.TITLE.setGeometry(QtCore.QRect(0, 20, 1000, 20))

        self.TITLE.setFont(QtGui.QFont('Times', 14))
        self.TITLE.setAlignment(QtCore.Qt.AlignHCenter)

        self.CONTENT = QLabel("§ USAGE", self)
        self.CONTENT.setGeometry(QtCore.QRect(20, 40, 780, 980))
        self.CONTENT.setFont(QtGui.QFont('Times', 12))
        self.CONTENT.setAlignment(QtCore.Qt.AlignLeft)

        self.UI_openFileDialog()

    def UI_openFileDialog(self):
        global HTU_FILE
        f = open(resource_path(HTU_FILE),'r')

        with f:
            data = f.read()
            self.CONTENT.setText(data)

# ===================================================== MAIN PAGE ====================================================
class Main(QMainWindow, pldm_update_pkg_gen_ui.UI_MainPage):
    def __init__(self, parent=None):
        super(Main, self).__init__()
        self.setupUi(self)
        self.time_access = QtCore.QDateTime.currentDateTime()

        # Set version
        self.lb_version.setText(VERSION_STR)

        # Create sub-window
        self.WINDOW_HTU = HowToUsePage()

        # Timmer config
        # TIMER1 | Check Starus report | 5sec
        self.timer1 = QtCore.QTimer(self)                               
        self.timer1.timeout.connect(self.TASK1_TIMER_normalStatus)
        self.timer1.start(5000)

        # Table widget config
        self.cur_sel_row = -1
        self.tw_complist.setColumnCount(len(TABLE_DISPLAY_LST))

        self.tw_complist.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tw_complist.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tw_complist.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        for i in range(len(TABLE_DISPLAY_LST)):
            item = QTableWidgetItem()
            self.tw_complist.setHorizontalHeaderItem(i, item)
            item = self.tw_complist.horizontalHeaderItem(i)
            item.setText(TABLE_DISPLAY_LST[i])
        self.tw_complist.setEditTriggers(QTableWidget.NoEditTriggers)

        self.horizontalHeader = self.tw_complist.horizontalHeader()
        self.keywords = dict([(i, []) for i in range(self.tw_complist.columnCount())])

        for platform in platform_lst:
            self.cb_platform.addItem(platform)

        for stage in STAGE_LST:
            self.cb_stage.addItem(stage)

        self.UI_Change_Info()
        self.UI_Compid_Change()

        self.tw_complist.itemClicked.connect(self.UI_Row_Select)
        self.pb_insert.clicked.connect(self.UI_Component_Insert)
        self.cb_platform.currentTextChanged.connect(self.UI_Change_Info)
        self.cb_board.currentTextChanged.connect(self.UI_Change_Info)
        self.cb_compid.currentTextChanged.connect(self.UI_Compid_Change)
        self.pb_browse.clicked.connect(self.File_Browse)
        self.pb_generate.clicked.connect(self.Generate_Package)
        self.pb_delete.clicked.connect(self.UI_Remove_All_Component)
        self.ac_howtouse.triggered.connect(self.UI_HowToUseWindowShow)

    def closeEvent(self, event):
        global APP_KILL
        APP_KILL = 1
        print("All process in APP are killed!")

    def File_Browse(self):
        fileName = QFileDialog.getOpenFileName(self,'Single File','./')[0]
        self.le_comppath.setText(fileName)

    def UI_HowToUseWindowShow(self):
        self.WINDOW_HTU.show()
    
    # Task1 polling every 5 sec
    def TASK1_TIMER_normalStatus(self):
        if self.lb_status.text() != "< idle >":
            myFont=QtGui.QFont()
            myFont.setBold(False)
            self.lb_status.setFont(myFont)
            self.lb_status.setStyleSheet("color: rgb(0, 0, 0)")
            self.lb_status.setText("< idle >")

    def UI_Row_Select(self):
        cur_row = self.tw_complist.currentRow()
        self.cur_sel_row = cur_row

    def UI_Remove_All_Component(self):
        for i in range(self.tw_complist.rowCount()):
            self.tw_complist.removeRow(0)
        
        global id_lst, version_lst, img_lst
        id_lst = []
        version_lst = []
        img_lst = []
    
    def UI_Change_Info(self):
        platform_idx = platform_lst.index(self.cb_platform.currentText())

        self.cb_board.clear()
        for board in board_lst[platform_idx]:
            self.cb_board.addItem(board)

        cur_cfg_file = platform_cfg_prefix + self.cb_platform.currentText() + '_' + self.cb_board.currentText() + ".json"
        PLAT_INFO = json_lib.TOOL_pldm_plat_cfg_R(resource_path(cur_cfg_file))
        COMP_INFO = PLAT_INFO[1]

        comp_id_lst = []
        for comp in COMP_INFO:
            cur_id_lst = comp["CompID"]
            for id in cur_id_lst:
                if id not in comp_id_lst:
                    comp_id_lst.append(id)
        
        comp_id_lst.sort()
        for id in comp_id_lst:
            device_info_lst = []
            for comp in COMP_INFO:
                if id in comp["CompID"]:
                    device_info_lst.append(comp["Vendor"] + "   " + comp["Device"])

            for device in device_info_lst:
                self.cb_compid.addItem(str(id) + "  " + device)

    def UI_Compid_Change(self):
        self.le_compver.setText("")

    def UI_Component_Insert(self):
        if self.cb_compid.currentText() == "na":
            self.lb_status.setText("Component id lost!")
            self.lb_status.setStyleSheet("color: rgb(255, 0, 0)")
            return
        if self.le_compver.text() == "na" or self.le_compver.text() == "":
            self.lb_status.setText("Component version lost!")
            self.lb_status.setStyleSheet("color: rgb(255, 0, 0)")
            return
        if self.le_comppath.text() == "na" or self.le_comppath.text() == "":
            self.lb_status.setText("Component path lost!")
            self.lb_status.setStyleSheet("color: rgb(255, 0, 0)")
            return

        cur_id = self.cb_compid.currentText().split(' ')[0]
        if cur_id in id_lst:
            self.lb_status.setText("Given existed component id!")
            self.lb_status.setStyleSheet("color: rgb(255, 0, 0)")
            self.le_comppath.setText("")
            return

        id_lst.append(cur_id)
        device_name = self.cb_compid.currentText().split('   ')[-1]
        version_lst.append(device_name + " " + self.le_compver.text())
        img_lst.append(self.le_comppath.text())

        row = self.tw_complist.rowCount()
        self.tw_complist.insertRow(row)
        self.tw_complist.setItem(row,0,QTableWidgetItem(cur_id))
        self.tw_complist.setItem(row,1,QTableWidgetItem(self.le_compver.text()))
        self.tw_complist.setItem(row,2,QTableWidgetItem(self.le_comppath.text().split('/')[-1]))

        self.le_comppath.setText("")

    def Generate_Package(self):
        if self.cb_platform.currentText() == "":
            self.lb_status.setText("Given empty platform!")
            self.lb_status.setStyleSheet("color: rgb(255, 0, 0)")
            return
        if self.cb_board.currentText() == "":
            self.lb_status.setText("Given empty board!")
            self.lb_status.setStyleSheet("color: rgb(255, 0, 0)")
            return
        if self.cb_stage.currentText() == "":
            self.lb_status.setText("Given empty stage!")
            self.lb_status.setStyleSheet("color: rgb(255, 0, 0)")
            return
        row = self.tw_complist.rowCount()
        if row == 0:
            self.lb_status.setText("Given empty component!")
            self.lb_status.setStyleSheet("color: rgb(255, 0, 0)")
            return

        id_str_lst = ""
        for id in id_lst:
            id_str_lst = id_str_lst + id + " "

        version_str_lst = ""
        for ver in version_lst:
            version_str_lst = version_str_lst + '"' + ver + '"' + " "

        img_str_lst = ""
        for img in img_lst:
            img_str_lst = img_str_lst + '"' + img + '"' + " "

        command = command_prefix + \
            " -p " + self.cb_platform.currentText() + \
            " -b " + self.cb_board.currentText() + \
            " -s " + self.cb_stage.currentText() + \
            " -c " + id_str_lst + \
            " -v " + version_str_lst + \
            " -i " + img_str_lst

        print("Input command: ", command)
        a = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
        res = a.communicate()
        
        if a.returncode != 0:
            self.lb_status.setText("Generate failed! Please look at error log ["+ LOG_FILE +"]")
            self.lb_status.setStyleSheet("color: rgb(255, 0, 0)")
            log_record(LOG_FILE, "append", res[0])

        else:
            if len(version_lst) == 1:
                outputfile_name = self.cb_platform.currentText() + "_" + self.cb_board.currentText() + "_" + version_lst[0].replace(" ", "_") + ".pldm"
            else:
                outputfile_name = "default_package.pldm"

            self.lb_status.setText("Generate success! Please look at package file " + outputfile_name)
            self.lb_status.setStyleSheet("color: rgb(0, 255, 0)")
            print("Generate success! Please look at package file " + outputfile_name)

def MAIN_APP():
    platform_cfg_lst = os.listdir(resource_path(PLATFORM_PATH))

    for cfg in platform_cfg_lst:
        cur_platform = cfg.split('_')[1]
        cur_board = cfg.split('_')[2].replace(".json", "")
        if cur_platform not in platform_lst:
            platform_lst.append(cur_platform)
        
        platform_index = platform_lst.index(cur_platform)
        if len(board_lst) <= platform_index:
            board_lst.append([cur_board])
        else:
            board_lst[platform_index].append(cur_board)

    print("Platform list", platform_lst)
    print("Board list:", board_lst)

    # Open GUI format
    app = QApplication(sys.argv)
    MAIN_WINDOW = Main()
    MAIN_WINDOW.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    MAIN_APP()
