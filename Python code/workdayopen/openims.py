import subprocess
import time
import uiautomation as ui
import tkinter as tk
import os

def openims(user,pwd):
    subprocess.Popen(r'F:\test\TestClient\IMS\release_5\LandErp.Client.exe')
    imswindow = ui.WindowControl(searchDepth=1, Name="Land IMS 1.3.2")
    imswindow.EditControl(Name="账号:").SendKeys(user)
    imswindow.EditControl(Name="密码:").SendKeys(pwd)
    imswindow.ButtonControl(Name="登录").Click(simulateMove=False)

def updateims():
    os.system(r'start "" "F:\test\TestClient\IMS"')
    imsgit = ui.WindowControl(searchDepth=1, Name="IMS")
    x = imsgit.BoundingRectangle.right
    y = imsgit.BoundingRectangle.bottom
    ui.RightClick(x-200,y-100)
    ui.MenuControl(searchDepth=1, Name='上下文').MenuItemControl(searchDepth=1, foundIndex=10).Click()
    time.sleep(2)
    ui.SendKeys('git pull')
    ui.SendKeys("{Enter}")

def create_window():
    root_window = tk.Tk()
    root_window.title('打开IMS客户端')
    root_window.geometry('45x450')
    root_window.iconbitmap('1.ico')
    tk.Button(root_window, text="关闭", command=root_window.quit).grid(row=10, column=0,sticky='s', padx=10, pady=5)
    tk.Button(root_window, text="毛伟人", command=lambda:openims('01210281', 'a1234567')).grid(row=1, column=0, sticky="w", padx=5, pady=5, ipadx=20, ipady=10)
    tk.Button(root_window, text="TEST", command=lambda: openims('02170242', 'a1111111')).grid(row=2, column=0,
                                                                                             sticky="w", padx=5, pady=5, ipadx=20, ipady=10)
    tk.Button(root_window, text="幸福毛经理", command=lambda: openims('16210025', 'a1234567890')).grid(row=3, column=0,
                                                                                             sticky="w", padx=5, pady=5, ipadx=20, ipady=10)
    tk.Button(root_window, text="幸福副总", command=lambda: openims('16210024', 'a1234567890')).grid(row=4, column=0,
                                                                                             sticky="w",padx=5, pady=5, ipadx=20, ipady=10)
    tk.Button(root_window, text="工种经理", command=lambda: openims('01200051', 'a1234567890')).grid(row=5, column=0,
                                                                                                 sticky="w", padx=5, pady=5, ipadx=20, ipady=10)
    tk.Button(root_window, text="更新IMS", command=updateims).grid(row=6, column=0,
                                                                                                 sticky="w", padx=5,
                                                                                                 pady=5, ipadx=20,
                                                                                                 ipady=10)
    root_window.mainloop()


if __name__ == '__main__':
    create_window()