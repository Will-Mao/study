from selenium import webdriver
from pywinauto import application


class WorkDay:
    def __init__(self):
        self.js = "window.open('{}','_blank');"
        option = webdriver.ChromeOptions()
        option.add_argument(r'user-data-dir=C:\Users\青岚\AppData\Local\Google\Chrome\User Data2')
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        self.driver = webdriver.Chrome(options=option)
        self.first = True

    def openbrowes(self, url):
        if self.first:
            self.driver.get(url)
            self.first = False
        else:
            self.driver.execute_script(self.js.format(url))
            self.driver.switch_to.window(self.driver.window_handles[-1])

    @staticmethod
    def openapp(app_locat):

        app = application.Application(backend='uia').start(app_locat)
        return app

    @staticmethod
    def login(app, ele_name, ele_pwd, name, pwd):
        app[ele_name].type_keys(name)
        app[ele_pwd].type_keys(pwd)
        loging_btn = app['登录']
        loging_btn.click()


if __name__ == "__main__":
    w = WorkDay()
    w.openbrowes('https://www.baidu.com')