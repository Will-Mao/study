import time
import re
import uiautomation as ui

def daily_paper_check():
    ding_window = ui.WindowControl(searchDepth=1, Name='钉钉')
    ding_window.Maximize()
    ding_window.SetTopmost()
    ding_window.WindowControl(searchDepth=1,foundIndex=3).WindowControl(searchDepth=1,foundIndex=2).EditControl(searchDepth=1,Name='搜索').Click(simulateMove=False)
    # ui.SendKeys('工作汇报(日志)')
    # ding_window.WindowControl(searchDepth=1, Name='advancedSearch').DocumentControl(Depth=3,Name='advancedSearch').GroupControl(Depth=2, foundIndex=2).GroupControl(Depth=5, foundIndex=1).TextControl(Depth=3, Name='工作汇报(日志)').Click()
    time.sleep(1)
    # ui.SendKeys("{Enter}")
    ding_window.WindowControl(searchDepth=1, Name='advancedSearch').DocumentControl(Depth=3, Name='advancedSearch').GroupControl(Depth=2,foundIndex=2).GroupControl(Depth=5,foundIndex=3).TextControl(Depth=3, Name='工作汇报(日志)').Click()
    time.sleep(3)
    daily_window = ui.WindowControl(searchDepth=1, Name='独立窗口').WindowControl(searchDepth=1, ClassName='UrlBrowserAppHost')
    group_1 = daily_window.GroupControl(Depth=6,foundIndex=2).GroupControl(Depth=2, foundIndex=3).GroupControl(searchDepth=1,foundIndex=1).GroupControl(searchDepth=1, foundIndex=1)
    staff = group_1.GetFirstChildControl()
    staff_name = []
    while True:
        staff = staff.GetNextSiblingControl()
        if staff.Name == '昨天':
            continue
        elif staff.Name == '前天':
            break
        elif '星期六' in staff.Name:
            break
        name = staff.TextControl(searchDepth=1,SubName='测试部门工作日志').Name
        staff_name.append(re.match("(.*?)的",name).group(1))

    all_name = {'张戈', '汪超', '李林', '何小林', '梁文斌', '毛伟任', '涂静璇', '秦玉嘉', '杨文卓', '李玲英', '雷小倩', '苏云鸿'}
    read_name = set(staff_name)
    result = list(all_name - read_name)
    if len(result) > 0:
        ding_window.WindowControl(searchDepth=1,foundIndex=3).WindowControl(searchDepth=1,foundIndex=2).EditControl(searchDepth=1,Name='搜索').Click(simulateMove=False)
        # ui.SendKeys('测试二组')
        ding_window.WindowControl(searchDepth=1, Name='advancedSearch').DocumentControl(Depth=3,
                                                                                        Name='advancedSearch').GroupControl(
            Depth=2, foundIndex=2).GroupControl(Depth=5, foundIndex=3).TextControl(Depth=3, Name='测试二组').Click()
        time.sleep(2)
        # ui.SendKeys("{Enter}")
        # ding_window.WindowControl(searchDepth=1,foundIndex=2).WindowControl(searchDepth=1,foundIndex=3).WindowControl(Depth=2,foundIndex=4).EditControl(Depth=2,Name='请输入消息').Click()
        ding_window.EditControl(Depth=6, Name='请输入消息').Click(simulateMove=False)
        ui.SendKeys((" ".join(result))+"没有提交工作日报")
        # 工作汇报(日志)工作汇报(日志)ui.SendKeys("{Enter}")


if __name__ == '__main__':
    daily_paper_check()