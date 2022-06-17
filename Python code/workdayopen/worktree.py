import time
import uiautomation as ui
import sqlserver_act as SQL
import IMS_App


def open_page():
    imswin.SetTopmost()
    imswin.EditControl(Depth=6, AutomationId="teSearch").GetValuePattern().SetValue("员工用户管理")
    imswin.Click(50, 130, simulateMove=False)
    layout = imswin.PaneControl(searchDepth=1).PaneControl(searchDepth=1, foundIndex=2).PaneControl(searchDepth=1,
                                                                                                    AutomationId='UCUserManage').PaneControl(
        Depth=3, AutomationId='layoutControl1')
    return layout


namelist = []
imswin = ui.WindowControl(searchDepth=1, Name="毛伟人 岚庭ERP ")
datapanel = imswin.PaneControl(searchDepth=1).PaneControl(searchDepth=1).PaneControl(searchDepth=1, AutomationId='UCStaff').TableControl(Depth=4).CustomControl(searchDepth=1, Name='Data Panel')
for item, depth in ui.WalkControl(datapanel, includeTop=False,maxDepth=1):
    name = item.DataItemControl(searchDepth=1, SubName='编号').GetValuePattern().Value
    namelist.append(name)
# 初始化密码
'''
open_page()
'''
driver = IMS_App.ims_app()
t = 15
for n in namelist:
    '''
    resetpwd()
    '''
    d, k = IMS_App.login(driver, n, 'a1234567890')
    if k:
        if not SQL.initpwd(n):
            time.sleep(3)
            continue
        time.sleep(3)
        d, k = IMS_App.login(driver, n, 'a1234567890')
    IMS_App.choice_pos(d, driver, n)
    IMS_App.baobei(d, driver, t, n, 'a1234567890')
    IMS_App.loginout(d, driver)
    t = 1

