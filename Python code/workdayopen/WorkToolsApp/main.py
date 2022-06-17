import sys, os, time
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QThread
# from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow
import work_tools2
import uiautomation as ui
import subprocess
from functools import partial
import database
import create_test_data

# Python -m PyQt5.uic.pyuic untitled.ui -o work_tools2.py

def create_data(user, pwd, func, cust):
    num = win.spinBox.text()
    if '，' not in cust:
        custs = [f"{cust}"]
    else:
        custs = cust.split('，')
    func_dict = {'客户登记': "customersave", '合同登记': "contactadd", '合同优惠单登记': "adddiscount", '开工预案（UI）': "contstartplanadd_ui", '设计见面': "custmeet",
            '报价单（UI）': "baojiadan", '开工申请（UI）': "kaigong", '核算单（UI）': "hesuandan"}
    ims_desk = create_test_data.ImsData(user)
    if func == "客户登记":
        for _ in range(int(num)):
            ims_desk.customersave()
    else:
        for c in custs:
            getattr(ims_desk, func_dict[func])(c)


def validate():
    user = win.lineEdit_15.text()
    pwd = win.lineEdit_16.text()
    f = win.comboBox_2.currentText()
    cust = win.textEdit_1.toPlainText()
    win.label_6.setStyleSheet("color:red")
    win.label_6.setWordWrap(True)
    if user == '':
        win.label_6.setText('必须输入账户！')
    elif f != '客户登记' and cust == '':
        win.label_6.setText('非客户登记必须输入客户！')
    else:
        win.label_6.setText('')
        create_data(user, pwd, f, cust)


def updateims():
    os.system(r'start "" "F:\test\TestClient\IMS"')
    imsgit = ui.WindowControl(searchDepth=1, Name="IMS")
    x = imsgit.BoundingRectangle.right
    y = imsgit.BoundingRectangle.bottom
    ui.RightClick(x-200, y-100)
    ui.MenuControl(searchDepth=1, Name='上下文').MenuItemControl(searchDepth=1, foundIndex=10).Click()
    time.sleep(2)
    ui.SendKeys('git pull')
    ui.SendKeys("{Enter}")


def openims(user, pwd, k, login_name):
    line_text = 'lineEdit_' + k
    pages = eval(f'win.{line_text}.text()')
    if '，' not in pages:
        pages = [f"{pages}"]
    else:
        pages = pages.split('，')
    release = win.comboBox.currentText()
    subprocess.Popen(rf'F:\test\TestClient\IMS\{release}\LandErp.Client.exe')
    imswindow = ui.WindowControl(searchDepth=1, Name="Land IMS 1.3.2")
    imswindow.EditControl(Name="账号:").SendKeys(user)
    imswindow.EditControl(Name="密码:").SendKeys(pwd)
    imswindow.ButtonControl(Name="登录").Click(simulateMove=False)
    # imswin.SetTopmost()
    if len(pages[0]) > 0:
        imswin = ui.WindowControl(searchDepth=1, Name=f"{login_name} 岚庭ERP ")
        for p in pages:
            if imswin.EditControl(Depth=6, AutomationId="teSearch").Exists(10, 2):
                imswin.EditControl(Depth=6, AutomationId="teSearch").GetValuePattern().SetValue(p)
                imswin.Click(50, 130, simulateMove=False)
                time.sleep(1)


def openims2(k, u):
    users = {'冯*':'01200526','苏*':'01190414','左*':'02150042','周*培':'01210496','张*婷':'01140125','曹*松':'01150424','张*军':'01210683','唐*':'01130126'}
    for i in users.keys():
        if i in u:
            break
    user = users[i]
    line_text = 'lineEdit_' + k
    pages = eval(f'win.{line_text}.text()')
    if '，' not in pages:
        pages = [f"{pages}"]
    else:
        pages = pages.split('，')
    subprocess.Popen(r'C:\Users\青岚\Videos\release_pre\release_pre\LandErp.Client.exe')
    imswindow = ui.WindowControl(searchDepth=1, Name="Land IMS 1.3.2")
    imswindow.EditControl(Name="账号:").SendKeys(user)
    imswindow.EditControl(Name="密码:").SendKeys('a1111111')
    imswindow.ButtonControl(Name="登录").Click(simulateMove=False)
    if len(pages[0]) > 0:
        imswin = ui.WindowControl(searchDepth=1, Name=f"{i} 岚庭ERP ")
        for p in pages:
            if imswin.EditControl(Depth=6, AutomationId="teSearch").Exists(10, 2):
                imswin.EditControl(Depth=6, AutomationId="teSearch").GetValuePattern().SetValue(p)
                imswin.Click(50, 130, simulateMove=False)
                time.sleep(1)


def openapp(app_loc):
    subprocess.Popen(app_loc)


def connect():
    win.pushButton_23.clicked.connect(updateims)
    win.pushButton_1.clicked.connect(partial(openims, '01210281', 'a1234567890','1', win.pushButton_1.text()))
    win.pushButton_2.clicked.connect(partial(openims, '02170242', 'a1111111','2', win.pushButton_2.text()))
    win.pushButton_3.clicked.connect(partial(openims, '16210025', 'a1234567890','3', win.pushButton_3.text()))
    win.pushButton_4.clicked.connect(partial(openims, '16210024', 'a1234567890','4', win.pushButton_4.text()))
    win.pushButton_5.clicked.connect(partial(openims, '01200051', 'a1234567890','5', win.pushButton_5.text()))
    win.pushButton_7.clicked.connect(partial(openims, '01210123', 'a1234567890','7', win.pushButton_7.text()))
    win.pushButton_6.clicked.connect(partial(openims, '55220011', 'a1234567890','6', win.pushButton_6.text()))
    win.pushButton_21.clicked.connect(partial(openapp, r'E:\Program Files\HeidiSQL\heidisql.exe'))
    win.pushButton_22.clicked.connect(partial(openapp, r'E:\Program Files\Fiddler\Fiddler.exe'))
    win.pushButton_24.clicked.connect(partial(openapp, r'E:\Program Files\Microvirt\MEmu\MEmuConsole.exe'))
    win.pushButton_26.clicked.connect(partial(openapp, r'C:\Users\青岚\AppData\Local\Obsidian\Obsidian.exe'))
    win.pushButton_25.clicked.connect(partial(openapp, r'E:\Program Files\PyCharm Community Edition 2021.1\bin\pycharm64.exe'))
    # 下拉列表选择时触发，并将选择的数据发送到槽函数
    win.comboBox.activated[str].connect(partial(database.set_yaml_data, 'Release'))
    win.comboBox_3.activated[str].connect(partial(openims2, '10'))
    win.pushButton.clicked.connect(validate)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = QMainWindow()
    win = work_tools2.Ui_MainWindow()
    win.setupUi(mainwindow)
    mainwindow.setWindowTitle("工作常用工具")
    mainwindow.setWindowIcon(QtGui.QIcon("1.ico"))
    connect()
    mainwindow.show()
    sys.exit(app.exec_())