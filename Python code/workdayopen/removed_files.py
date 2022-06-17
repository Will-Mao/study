import os, tkinter , shutil


def shutil_del_files(data_path):
    for p in data_path:
        try:
            shutil.rmtree(p)
        except FileNotFoundError:
            continue


def shutil_del_files2(data_path):
    for p in data_path:
        try:
            shutil.rmtree(p)
        except FileNotFoundError:
            continue
    window.destroy()


def new_button(*args):
    if args[0] == "点击关闭窗口":
        button = tkinter.Button(fm2, text=args[0], command=lambda: close_window(), bg=args[1],
                                activeforeground="black", relief="sunken", bd=4,width=30,height=3, font=("黑体",16))
    elif args[0] == "保存":
        button = tkinter.Button(fm2, text=args[0], command=lambda :window.destroy(), bg=args[1],
                                activeforeground="black", relief="sunken", bd=4,width=30,height=3,font=("黑体",16))
    else:
        button = tkinter.Button(fm2,text=args[0],command=lambda :shutil_del_files(dirs),bg=args[1],
                                activeforeground="black",relief="sunken",bd=4,width=30,height=3,font=("黑体",16))
    button.grid(row=args[2], column=args[3])


def close_window():
    for d in dirs:
        try:
            os.listdir(d)
            shutil.rmtree(d)
        except FileNotFoundError:
            continue
    window.destroy()


dirs = ["C:\AAA\新建文件夹", "E:\新建文件夹", "F:\新建文件夹"]
window = tkinter.Tk()
window.title("请选择点击")
window.wm_attributes("-alpha",1.0)
window.wm_attributes("-topmost",True)
window.attributes("-toolwindow",1)
window.resizable(0,0)
width = 1900
height = 1000
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws/2)-(width/2)
y = (hs/2)-(height/2)
window.geometry('%dx%d+%d+%d' % (width,height,x,y))
window.overrideredirect(1)
fm = tkinter.Frame(window,bg='LightSkyBlue')
fm.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.2)
lb = tkinter.Label(fm,text="欢迎使用本半智能系统！",bg='LightSkyBlue',fg='White',font=("黑体",40))
lb.pack(expand="yes")
fm2 = tkinter.Frame(window)
fm2.place(relx=0.0, rely=0.2, relwidth=0.2, relheight=0.8)
button_list = [("关闭此窗口",'Red',0,0),("开始使用电脑",'Orange',1,0),("杀毒",'Yellow',2,0),("关机",'Green',3,0),
               ("清理电脑",'Cyan',4,0),("删除",'blue',5,0),("新建",'blue',6,0),("保存",'blue',7,0),("执行",'blue',8,0)]
for b in button_list:
    new_button(*b)
fm3 = tkinter.Frame(window)
fm3.place(relx=0.2, rely=0.2, relwidth=0.8, relheight=0.8)
lb2 = tkinter.Label(fm3,text="忆秦娥·娄山关",fg='black',font=("楷体",40))
lb2.pack()
lb3 = tkinter.Label(fm3,text="西风烈，长空雁叫霜晨月。",fg='black',font=("楷体",40))
lb3.pack()
lb4 = tkinter.Label(fm3,text="霜晨月，马蹄声碎，喇叭声咽。",fg='black',font=("楷体",40))
lb4.pack()
lb5 = tkinter.Label(fm3,text="雄关漫道真如铁，而今迈步从头越。",fg='black',font=("楷体",40))
lb5.pack()
lb6 = tkinter.Label(fm3,text="从头越，苍山如海，残阳如血。",fg='black',font=("楷体",40))
lb6.pack()

window.protocol("WM_DELETE_WINDOW",lambda :shutil_del_files2(dirs))
window.mainloop()



