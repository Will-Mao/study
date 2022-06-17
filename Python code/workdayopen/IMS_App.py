import selenium.common.exceptions
import time
from appium import webdriver
from tools import ims
from selenium.webdriver.common.by import By
import sqlserver_act as SQL
import requests
import re
from time import sleep

def ims_app():
    desired_caps = {
        'platformName': 'Android',
        'deviceName': '127.0.0.1:21513',
        'platformVersion': '7.1',
        'appPackage': 'com.design.land',
        'appActivity': 'com.design.land.mvp.ui.login.activity.LoginActivity'
    }
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    return driver


def login( driver, user, pwd):
    d = ims(driver)
    k = d.login(user, pwd)
    return d, k


def reset_pwd(d, newpwd):
    d.by_text("新密码").send_keys(newpwd)
    d.by_text("确认新密码").send_keys(newpwd)
    d.by_text("完成").click()


def baobei(d, driver, t, user, pwd):
    try:
        time.sleep(0.1)
        ele = driver.find_element(By.XPATH, ".//*[contains(@text,'未分配角色')]")
        print(ele.text)
    except selenium.common.exceptions.NoSuchElementException:
        pass
    else:
        print('未分配角色')
        s = SQL.get_session('01210281')
        pos_id = SQL.get_posid(user)
        select_role('7078', s[1], s[0], pos_id[0])
        loginout(d, driver)
        login(driver, user, pwd)
    choice_pos(d, driver, user)
    d.by_text("工作").click()
    try:
        d.by_text("工人需求报备").click()
    except selenium.common.exceptions.TimeoutException:
        return
    time.sleep(t)
    while True:
        driver.tap([(1000, 90)], 500)
        driver.tap([(1010, 100)])
        try:
            d.by_text("现在可接新单").click()
            d.by_text("确定").click()
        except selenium.common.exceptions.TimeoutException:
            continue
        time.sleep(0.5)
        driver.keyevent(4)
        break


def loginout(d, driver):
    d.by_text("我").click()
    time.sleep(2)
    driver.swipe(500, 1500, 500, 200, 500)
    d.by_text("设置").click()
    d.by_text("退出登录").click()
    d.by_text("确定").click()


def choice_pos(d, driver, user):
    if d.find_ele('选择职位'):
        pass
    else:
        dept = SQL.get_posid(user)
        # re.search(f"{dept[1]}.*?～)", )
        eles = driver.find_elements(By.XPATH, "//android.widget.TextView[@resource-id='com.design.land:id/item_tv_name']")
        for i in eles:
            if re.search(f"{dept[1]}.*?～[)]", i.text):
                i.click()
                d.by_text("确定").click()


def select_role(port, LoginStafPosID, SessionID, posid):
    url = f"https://dv.lantingroup.cn:{port}/PC/RightManage/RightManageService.svc"
    header = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': '"http://tempuri.org/IRightManageErp/StaffPosRoleModify"',
        'Host': f'dv.lantingroup.cn:{port}',
        'Content-Length': '872',
        'Expect': '100-continue',
        'Accept-Encoding': 'gzip, deflate'
    }
    body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><StaffPosRoleModify xmlns="http://tempuri.org/">' \
           '<staffPosRoleForchange xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
           '<a:CustomParas i:nil="true"/><a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight">' \
           f'<b:LoginStafPosID>{LoginStafPosID}</b:LoginStafPosID><b:RegisterID i:nil="true"/><b:SessionID>{SessionID}</b:SessionID>' \
           f'<b:Sign i:nil="true"/><b:UniqueID>{SessionID}</b:UniqueID></a:Session><a:RoleID>e1da41b9-5785-4e39-983f-a17675a2885a</a:RoleID>' \
           f'<a:StfPosID>{posid}</a:StfPosID></staffPosRoleForchange></StaffPosRoleModify></s:Body></s:Envelope>'
    cmpl = requests.post(url, headers=header, data=body.encode('utf-8'))
    if re.search("<a:IsSuccess>true</a:IsSuccess>", cmpl.text, re.S):
        print("分派角色成功")
    else:
        print(cmpl.text)


if __name__ == '__main__':
    pass
