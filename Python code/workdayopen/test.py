# coding:utf-8
import random
import pyautogui
import time
import os
import uiautomation as ui
import sqlserver_act as sql
# imswindow = ui.WindowControl(searchDepth=1, Name="毛伟人 岚庭ERP ")
# imswindow.SetTopmost(isTopmost=False)
# ui.uiautomation.SetGlobalSearchTimeout(2)
# time.sleep(3)
#
# tree = imswindow.ListControl(Depth=3, Name='处理装修管家问题1')
# for item, depth in ui.WalkControl(tree, includeTop=False):
#     if not isinstance(item, ui.CheckBoxControl):
#         continue
#     print(item.Name)
# 下方完整运行
# text = ['说的没错','是这样','原来是这样的啊','嗯对']
# wechat = ui.WindowControl(searchDepth=1, Name='微信')
# conversion = wechat.ListControl(Depth=8, Name='会话')
# type_area = wechat.PaneControl(Depth=3, foundIndex=4).EditControl(Depth=10, Name='输入')
# print(type_area)
# for t in text:
#     l = conversion.ListItemControl(searchDepth=1, RegexName='.*?格物致知.*?').TextControl(Depth=2).Exists()
#     if l:
#         conversion.ListItemControl(searchDepth=1, RegexName='.*?格物致知.*?').PaneControl(searchDepth=1).Click(simulateMove=False)
#         type_area.Click()
#         ui.SendKeys(t)
#         ui.SendKeys("{Enter}")
#     time.sleep(30)
def closepic():
    i = 0
    while True:
        location = pyautogui.locateCenterOnScreen('woker1.jpg', confidence=0.9)
        if location is not None:
            pyautogui.click(location.x, location.y, clicks=2, interval=0.2, duration=0.2, button="left")
            ui.SendKeys("{Space}")
            break
        print("未找到匹配图片,1秒后重试")
        i += 1
        if i > 2:
            os.system("pause")
        time.sleep(1)
ID = []
imswin = ui.WindowControl(searchDepth=1, Name="毛伟人 岚庭ERP ")
malt= imswin.PaneControl(searchDepth=1).PaneControl(Depth=2, AutomationId='UCMainModuleBase')
tools = malt.PaneControl(Depth=3, AutomationId='UCMatlProdBase').PaneControl(searchDepth=1, Name='panToolbar').PaneControl(searchDepth=1, AutomationId='UCPaging').PaneControl(searchDepth=1, Name='The XtraLayoutControl')
button = tools.PaneControl(searchDepth=1, Name='pnlButtonList').ToolBarControl(Depth=3, Name='Custom 2').ButtonControl(searchDepth=1, Name='下页')
for _ in range(7):
    ids = malt.PaneControl(Depth=6, AutomationId='myPanlTable').TableControl(searchDepth=1).CustomControl(searchDepth=1, Name='Data Panel')
    for item, depth in ui.WalkControl(ids, includeTop=False,maxDepth=1):
        name = item.DataItemControl(searchDepth=1, SubName='编号').GetValuePattern().Value
        ID.append(name)
    button.Click(simulateMove=False)
sql_ids = sql.ss()
l = []
for i in sql_ids:
    l.append(i[0])
print(set(l)-set(ID))





