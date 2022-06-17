import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions
class ims():
    def __init__(self,driver):
        self.driver = driver

    def login(self,name,pwd):
        username = self.driver.find_element_by_id('com.design.land:id/edt_username')
        passwd = self.driver.find_element_by_id('com.design.land:id/edit_password')
        username.send_keys(name)
        passwd.send_keys(pwd)
        loging_btn = self.driver.find_element_by_id('com.design.land:id/btn_login')
        loging_btn.click()
        try:
            time.sleep(0.5)
            ele = self.driver.find_element(By.XPATH,  ".//*[contains(@text,'密码错误')]")
            print(ele.text)
        except selenium.common.exceptions.NoSuchElementException:
            return False
        else:
            return True

    def by_text(self,text):
        ele = WebDriverWait(self.driver,10,0.5).until(lambda x:x.find_element_by_xpath(f"//*[@text='{text}']"))
        return ele
    
    def type(self,text, word):
        ele = WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element_by_xpath(f"//*[@text='{text}']"))
        ele.send_keys(word)

    def find_ele(self, text):
        try:
            self.driver.find_element(By.XPATH, f"//*[@text='{text}']")
        except selenium.common.exceptions.NoSuchElementException:
            return True
        else:
            return False

