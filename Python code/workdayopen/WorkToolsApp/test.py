# _\*_coding:UTF-8_\*_

import os
import subprocess
from functools import partial
import uiautomation as ui
import sys, time
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import *
import database
import work_tools2
import create_test_data
from ast import literal_eval


class EmitStr(QObject):
    '''
    定义一个信号类，
    sys.stdout有个write方法，通过重定向，
    每当有新字符串输出时就会触发下面定义的write函数，
    进而发出信号
    text：新字符串，会通过信号传递出去
    '''
    textWrit = pyqtSignal(str)
    def write(self, text):
        self.textWrit.emit(str(text))


class MyWidget(work_tools2.Ui_MainWindow, QMainWindow):    # 定义一个窗体类，继承于QWidget
    def __init__(self, mainwindow):
        super().__init__()
        self.setupUi(mainwindow)     # 构建一个QTextEdit， 以及对窗体的一些基本设置
        self.mythread = MyThread()
        sys.stdout = EmitStr(textWrit=self.onUpdateText)     # 输出结果重定向
        sys.stderr = EmitStr(textWrit=self.onUpdateText)     # 错误输出重定向
        self.pushButton.clicked.connect(self.slotstart)

    # 将文本写入textbroswer进行显示
    def onUpdateText(self, text):
        cursor = self.textbroswer.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textbroswer.setTextCursor(cursor)
        self.textbroswer.ensureCursorVisible()

    def slotstart(self):
        # try:
        self.mythread.start()
        # if self.mythread.error_code == 1:
        #     raise self.mythread.error_msg
        # except Exception as e:
        #     print(111)
        #     QMessageBox.information(self, '提示', str(e))

    def msgbox(self, e):
        QMessageBox.information(self, '提示', str(e))
    # def outputWrite(self, text):
    #     self.textbroswer.append(text)       # 输出的字符追加到 QTextEdit 中




class MyThread(QThread):
    def __init__(self):
        super().__init__()
        self.error_code = 0
        self.error_msg = None

    # 创建数据UI
    def run(self):
        user = win.lineEdit_15.text()
        pwd = win.lineEdit_16.text()
        f = win.comboBox_2.currentText()
        cust = win.textEdit_1.toPlainText()
        win.label_6.setStyleSheet("color:red")
        win.label_6.setWordWrap(True)
        if user == '':
            win.label_6.setText('必须输入账户！')
        # elif f != '客户登记' and cust == '':
        #     win.label_6.setText('非客户登记必须输入客户！')
        else:
            win.label_6.setText('')
            if cust == '':
                cust = win.spinBox.text()
            try:
                self.create_data(user, pwd, f, str(cust))
            except Exception as e:
                self.error_code = 1
                self.error_msg = e
                print(e)
                # return e



    def create_data(self, user, pwd, func, cust):
        num = win.spinBox.text()
        # if '，' not in cust:
        #     custs = [f"{cust}"]
        # else:
        #     custs = cust.split('，')
        func_dict = {'客户登记': "customersave", '合同登记': "contactadd", '合同优惠单登记': "adddiscount",
                     '开工预案': "contstartplanadd", '设计见面': "custmeet",'开工申请': "contstart",
                     '报价单': "creatoffer", '开工申请（UI）': "kaigong", '核算单（UI）': "hesuandan"}
        p = database.get_yaml_data('Port')
        ims_desk = create_test_data.ImsData(user, p)
        if cust and func != "客户登记":
            custs = literal_eval(cust)
            getattr(ims_desk, func_dict[func])(custs)
        elif func == "客户登记":
            ims_desk.customersave(num)
            #     ims_desk.test_show()
        else:
            print("必须输入客户名！进行相应操作")
        print(ims_desk.kehu)
#
# def create_data(user, pwd, func, cust):
#     num = win.spinBox.text()
#     if '，' not in cust:
#         custs = [f"{cust}"]
#     else:
#         custs = cust.split('，')
#     func_dict = {'客户登记': "customersave", '合同登记': "contactadd", '合同优惠单登记': "adddiscount",
#                  '开工预案（UI）': "contstartplanadd_ui", '设计见面': "custmeet",
#                  '报价单（UI）': "baojiadan", '开工申请（UI）': "kaigong", '核算单（UI）': "hesuandan"}
#     ims_desk = create_test_data.ImsData(user)
#     if func == "客户登记":
#         for _ in range(int(num)):
#             ims_desk.customersave()
#     else:
#         for c in custs:
#             getattr(ims_desk, func_dict[func])(c)

# def connect(va):
#     # win.pushButton_23.clicked.connect(updateims)
#     # win.pushButton_1.clicked.connect(partial(openims, '01210281', 'a1234567890','1', win.pushButton_1.text()))
#     # win.pushButton_2.clicked.connect(partial(openims, '02170242', 'a1111111','2', win.pushButton_2.text()))
#     # win.pushButton_3.clicked.connect(partial(openims, '16210025', 'a1234567890','3', win.pushButton_3.text()))
#     # win.pushButton_4.clicked.connect(partial(openims, '16210024', 'a1234567890','4', win.pushButton_4.text()))
#     # win.pushButton_5.clicked.connect(partial(openims, '01200051', 'a1234567890','5', win.pushButton_5.text()))
#     # win.pushButton_7.clicked.connect(partial(openims, '01210123', 'a1234567890','7', win.pushButton_7.text()))
#     # win.pushButton_6.clicked.connect(partial(openims, '55220011', 'a1234567890','6', win.pushButton_6.text()))
#     # win.pushButton_21.clicked.connect(partial(openapp, r'E:\Program Files\HeidiSQL\heidisql.exe'))
#     # win.pushButton_22.clicked.connect(partial(openapp, r'E:\Program Files\Fiddler\Fiddler.exe'))
#     # win.pushButton_24.clicked.connect(partial(openapp, r'E:\Program Files\Microvirt\MEmu\MEmuConsole.exe'))
#     # win.pushButton_26.clicked.connect(partial(openapp, r'C:\Users\青岚\AppData\Local\Obsidian\Obsidian.exe'))
#     # win.pushButton_25.clicked.connect(partial(openapp, r'E:\Program Files\PyCharm Community Edition 2021.1\bin\pycharm64.exe'))
#     # 下拉列表选择时触发，并将选择的数据发送到槽函数
#     # win.comboBox.activated[str].connect(partial(database.set_yaml_data, 'Release'))
#     # win.comboBox_3.activated[str].connect(partial(openims2, '10'))
#     win.pushButton.clicked.connect(va)

# class MainUi(work_tools2.Ui_MainWindow, QMainWindow):
#     def __init__(self, mainwindow):
#         super().__init__()
#         self.setupUi(mainwindow)
#         self.th = MyThread()
#         self.pushButton.clicked.connect(self.genMastClicked)
#         self.th.signalForText.connect(self.onUpdateText)
#         sys.stdout = self.th
#
#     def onUpdateText(self, text):
#         cursor = self.textbroswer.textCursor()
#         cursor.movePosition(QTextCursor.End)
#         cursor.insertText(text)
#         self.textbroswer.setTextCursor(cursor)
#         self.textbroswer.ensureCursorVisible()
#
#     def search(self):
#         try:
#             self.t = MyThread()
#             self.t.start()
#         except Exception as e:
#             raise e
#
#     def genMastClicked(self):
#         """Runs the main function."""
#         print('Running...')
#         self.search()
#         loop = QEventLoop()
#         QTimer.singleShot(2000, loop.quit)
#         loop.exec_()
#
#     def closeEvent(self, event):
#         """Shuts down application on close."""
#         # Return stdout to defaults.
#         sys.stdout = sys.__stdout__
#         super().closeEvent(event)

# PyQt5的线程使用，继承于QThread，并实现其run（）方法即可，run方法中是线程执行函数相关代码。使用线程时，只用先实例化，然后调用start（）方法，就会自动调用run方法。
# class MyThread(QThread):
#     signalForText = pyqtSignal(str)
#
#     def __init__(self,data=None, parent=None):
#         super(MyThread, self).__init__(parent)
#         self.data = data
#
#     def write(self, text):
#         self.signalForText.emit(str(text))  # 发射信号
#
#     def run(self):
#         user = win.lineEdit_15.text()
#         pwd = win.lineEdit_16.text()
#         f = win.comboBox_2.currentText()
#         cust = win.textEdit_1.toPlainText()
#         win.label_6.setStyleSheet("color:red")
#         win.label_6.setWordWrap(True)
#         if user == '':
#             win.label_6.setText('必须输入账户！')
#         elif f != '客户登记' and cust == '':
#             win.label_6.setText('非客户登记必须输入客户！')
#         else:
#             win.label_6.setText('')
#             self.create_data(user, pwd, f, cust)
#
#     def create_data(self, user, pwd, func, cust):
#         num = win.spinBox.text()
#         if '，' not in cust:
#             custs = [f"{cust}"]
#         else:
#             custs = cust.split('，')
#         func_dict = {'客户登记': "customersave", '合同登记': "contactadd", '合同优惠单登记': "adddiscount",
#                      '开工预案（UI）': "contstartplanadd_ui", '设计见面': "custmeet",
#                      '报价单（UI）': "baojiadan", '开工申请（UI）': "kaigong", '核算单（UI）': "hesuandan"}
#         ims_desk = create_test_data.ImsData(user)
#         if func == "客户登记":
#             for _ in range(int(num)):
#                 ims_desk.customersave()
#         else:
#             for c in custs:
#                 getattr(ims_desk, func_dict[func])(c)
#
#     def flush(self):
#         pass

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
    # with open(rf'F:\test\TestClient\IMS\{release}\LastLoginUser.txt', 'w') as f:
    #     f.write(user+':'+pwd)
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
        if i not in u:
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

def openheidisql(app_loc):
    openapp(app_loc)
    try:
        main_page = ui.WindowControl(searchDepth=1, Name='Session manager')
        main_page.ButtonControl(searchDepth=1, Name="Open").Click(simulateMove=False)
        ui.WindowControl(searchDepth=1, Name='HeidiSQL - Unnamed').ButtonControl(searchDepth=1, Name='Login').Click(simulateMove=False)
        main_page.WindowControl(searchDepth=1, Name='Warning').ButtonControl(Depth=2, Name='确定').Click(simulateMove=False)
    except Exception as e:
        print(e)


def connect():
    win.pushButton_23.clicked.connect(updateims)
    win.pushButton_1.clicked.connect(partial(openims, '01210281', 'a1234567','1', win.pushButton_1.text()))
    win.pushButton_2.clicked.connect(partial(openims, '02170242', 'a1111111','2', win.pushButton_2.text()))
    win.pushButton_3.clicked.connect(partial(openims, '16210025', 'a1234567890','3', win.pushButton_3.text()))
    win.pushButton_4.clicked.connect(partial(openims, '16210024', 'a1234567890','4', win.pushButton_4.text()))
    win.pushButton_5.clicked.connect(partial(openims, '01200051', 'a1234567890','5', win.pushButton_5.text()))
    win.pushButton_7.clicked.connect(partial(openims, '01210123', 'a1234567890','7', win.pushButton_7.text()))
    win.pushButton_6.clicked.connect(partial(openims, '55220011', 'a1234567890','6', win.pushButton_6.text()))
    win.pushButton_8.clicked.connect(partial(openims, '01190131', 'a1234567890', '8', win.pushButton_8.text()))
    win.pushButton_9.clicked.connect(partial(openims, '11117210007', '1234567890a', '9', win.pushButton_9.text()))
    win.pushButton_21.clicked.connect(partial(openheidisql, r'E:\Program Files\HeidiSQL\heidisql.exe'))
    win.pushButton_22.clicked.connect(partial(openapp, r'E:\Program Files\Fiddler\Fiddler.exe'))
    win.pushButton_24.clicked.connect(partial(openapp, r'E:\Program Files\Microvirt\MEmu\MEmuConsole.exe'))
    win.pushButton_26.clicked.connect(partial(openapp, r'C:\Users\青岚\AppData\Local\Obsidian\Obsidian.exe'))
    win.pushButton_25.clicked.connect(partial(openapp, r'E:\Program Files\PyCharm Community Edition 2021.1\bin\pycharm64.exe'))
    win.pushButton_27.clicked.connect(
        partial(openapp, r'E:\Program Files\iTools 4\iTools4.exe'))
    win.lineEdit_17.textChanged.connect(lambda current_text: database.set_yaml_data('Port', current_text))
    # 下拉列表选择时触发，并将选择的数据发送到槽函数
    win.comboBox.activated[str].connect(partial(database.set_yaml_data, 'Release'))
    win.comboBox_3.activated[str].connect(partial(openims2, '10'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.aboutToQuit.connect(app.deleteLater)
    mainwindow = QMainWindow()
    # win = MainUi(mainwindow)  # 方案二
    win = MyWidget(mainwindow)
    # win.setupUi(mainwindow)
    connect()
    mainwindow.setWindowTitle("工作常用工具")
    mainwindow.setWindowIcon(QtGui.QIcon("1.ico"))
    # mythread = MyThread()
    # connect(mythread.start)
    mainwindow.show()
    sys.exit(app.exec_())
