import time
import uiautomation as ui
import os
import pyautogui


def open_page():
    imswin.SetTopmost()
    imswin.EditControl(Depth=6, AutomationId="teSearch").GetValuePattern().SetValue("员工用户管理")
    imswin.Click(50, 130, simulateMove=False)
    layout = imswin.PaneControl(searchDepth=1).PaneControl(searchDepth=1, foundIndex=2).PaneControl(searchDepth=1,
                                                                                                    AutomationId='UCUserManage').PaneControl(
        Depth=3, AutomationId='layoutControl1')
    return layout

def gui_close(img):
    i = 0
    while True:
        location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
        if location is not None:
            pyautogui.click(location.x, location.y, clicks=1, interval=0.2, duration=0.2, button="left")
            break
        print(f"未找到匹配图片 {img},1秒后重试")
        i += 1
        if i > 2:
            os.system("pause")
        time.sleep(1)

imswin = ui.WindowControl(searchDepth=1, Name="幸福毛经理 岚庭ERP ")
main_page_tool = imswin.PaneControl(Depth=5, Name='pnlContainer').PaneControl(searchDepth=1, Name='pnlToolbar').ToolBarControl(Depth=3,Name='Custom 2')
main_page_tool.ButtonControl(searchDepth=1, Name='新建').Click(simulateMove=False)
time.sleep(3)
detail_page_layout = imswin.PaneControl(Depth=2, foundIndex=2).PaneControl(Depth=4, Name='The XtraLayoutControl')
detail_page_layout.EditControl(searchDepth=1,AutomationId='hlinkMeetCust').Click(simulateMove=False)
imswin.WindowControl(searchDepth=1).PaneControl(Depth=3, Name='panelControl1').EditControl(Depth=2, AutomationId='myName').SendKeys('啼澹见')
ui.SendKeys("{Enter}")
imswin.WindowControl(searchDepth=1).PaneControl(Depth=3, Name='panelControl2').ButtonControl(Depth=4, Name='选择').Click(simulateMove=False)
detail_page_layout.EditControl(searchDepth=1, AutomationId='hlinkOfferGoodsSet').Click(simulateMove=False)
gui_close('bj.jpg')
imswin.WindowControl(searchDepth=1).PaneControl(Depth=3, Name='myOperatePanel').ButtonControl(Depth=2, Name='确定').Click(simulateMove=False)
detail_page_layout.EditControl(searchDepth=1, AutomationId='tbxSignAmount').SendKeys('100000')
detail_page_layout.EditControl(searchDepth=1, AutomationId='tbxTimeLimit').SendKeys('5')
detail_page_layout.EditControl(searchDepth=1, AutomationId='gluHouseStructure').SendKeys('平层')
ui.SendKeys("{Enter}")
detail_page_layout.EditControl(searchDepth=1, AutomationId='cbxHouseCatg').SendKeys('现房')
ui.SendKeys("{Enter}")
detail_page_layout.PaneControl(searchDepth=1, AutomationId='dateExpectStartDate').Click(simulateMove=False)
ui.SendKeys("{Space}")
detail_page_layout.PaneControl(searchDepth=1, AutomationId='dateExpFrameDiagramDate').Click(simulateMove=False)
ui.SendKeys("{Space}")
detail_page_layout.PaneControl(searchDepth=1, AutomationId='dateExpRenderPicDate').Click(simulateMove=False)
ui.SendKeys("{Space}")
detail_page_layout.GetNextSiblingControl().ButtonControl(Depth=2, Name='保存')

