# 元素定位
1. Name，
2. classname，
3. AutomationId，
4. ProcessId

# 控件类型
1. WindowControl，
2. EditControl，
3. ButtonControl，
4. TextControl
5. ListControl
6. MenuItemControl 菜单按钮
7. ComboBoxControl(searchFromControl,AutomationI)  查找下拉框，然后在此基础上用Select("name")方法来选择需要的选项

# 鼠标操作
1. 滚轮
uiautomation.WheelUp()
uiautomation.WheelDown()
auto.mouse_event(auto.MouseEventFlag.Wheel, 0, 0, -435, 0)
`# 滚动条未到顶就使鼠标滑轮不停往上滑`
`while treeScrollPattern.VerticalScrollPercent > 0:`
`tree.WheelUp(waitTime=0.01)`
 `# 滚动条未到底就使鼠标滑轮不停往下滑`
`while treeScrollPattern.VerticalScrollPercent < 100:`
`tree.WheelDown(waitTime=0.01)`
2. Click()     点击；
3. RighClik()       右键点击
4. auto.DragDrop(x1, y1, x2, y2, moveSpeed=1)   鼠标拖拽

# 键盘操作
1. SendKeys
auto.SendKeys("{PAGEDOWN}") # 向下翻页键
如果已在编辑位置，则可用此方法来输入值，{Ctrl}为ctrl键，其他类似；{@  8}格式可输入8个@，对于数字也可实现此功能，但对于字母不能...;
2. SetValue()      传值，一般对EditControl用；
3. auto.IsKeyPressed(auto.Keys.VK_F12)  检测某个按键是否被按下

# 窗口相关
1. window.Close()    　　　　　 　 关闭窗口；
2. Window.GetWindowPattern().Close()  关闭窗口
3. window.SetActive()       　　　　使用；
4. window.SetTopMost()   　　　　设置为顶层
5. window.ShowWindow(uiautomation.ShowWindow.Maximize)  窗口最大化
6. automation.ShowDesktop() 显示桌面；
7. 移动窗口的位置，前两个参数表示左上角的位置，后两个参数表示窗口大小`
    - note.MoveWindow(300, 700,400,500）
    - 此种方式对CMD这种窗口无效，需要使用其他方法
```python
transform_win = win.GetTransformPattern() # 先获取TransformPattern
transform_win.Move(rect.left, rect.top)   # 然后move
transform_win.Resize(rect.width()//2, rect.height()-30) # 最后resize
```
8. 获取屏幕大小
    - auto.GetScreenSize()       result：（1920，1080） 
    - auto.GetMonitorsRect()   此方法具体作用还需研究
9. 获取本地窗口句柄
    - win.NativeWindowHandle
10. 根据窗口句柄获取窗口对象
    - win2 = auto.ControlFromHandle(win.NativeWindowHandle)
11. 隐藏、显示、最小化、最大化窗口
    - win.Hide(0)
    - win.Show(0)
    - win.Minimize()
    - win.Maxmize
12. 判断窗口是否最小化
    - auto.IsIconic(win.NativeWindowHandle)
    - 

# 伪代码举例
window = uiautomation.WindowControl(searchDepth=1, Name="Land IMS 1.3.2")

## 获取子节点
window.GetChildren()
返回一个节点列表
同理，可获取其他相对关系的节点如，父节点

## 获取节点控件类型
if window.ControlTypeName == 'ListControl':
	...

## 判断窗口是否存在
IMSwindow.Exists()

## 获取窗口句柄
handle = IMSwindow.NativeWindowHandle

## 获取窗口对象
1. 获取桌面对象
c = auto.GetRootControl()
2. 获取当前Python程序控制台窗口对象
cmdWindow = auto.GetConsoleWindow()

## 切换窗口句柄
uiautomation.SwitchToThisWindow(handle)

## 窗口重新搜索
举例：
/# 先查找到一个窗口控件
window = auto.WindowControl(Name='test')
/# 然后窗口关闭
此时window同样有上面这个窗口值，只是窗口已经不再
/# 再次打开窗口后，使用refind方法重新搜索即可
Window.Refind()

## 获取元素坐标位置
1. 获取底部坐标
window.BoundingRectangle.bottom  
2. 获取上部坐标
window.BoundingRectangle.top
3. left 左坐标
4. right 右坐标
5. MoveCursorToMyCenter() 获取元素中心坐标位置

## 截图
window.CaptureToImage()

## 设置全局搜索时间（单位秒）
auto.uiautomation.SetGlobalSearchTimeout(1)

## 控制滚动条
treeScrollPattern = tree.GetScrollPattern()

**移动到底部**
treeScrollPattern.SetScrollPercent(-1, 0)

SetScrollPercent传入的两个参数表示将滚动条移动到指定百分比位置：
-   **horizontalPercent**: 横向位置百分比
-   **verticalPercent**: 纵向位置百分比
传入-1表示不移动，由于没有横向滚动条，所以第一个参数传入了-1。

**移动到顶部**
treeScrollPattern.SetScrollPercent(-1, 100)

## 处理下拉列表
```python
# 获取下拉列表
combo = windowFont.ComboBoxControl(AutomationId='1140') 
# 获取对应Pattern
pattern = combo.GetExpandCollapsePattern()
# 判断是否在折叠状态，是就展开
if pattern.ExpandCollapseState == auto.ExpandCollapseState.Collapsed:
    pattern.Expand(waitTime=0)
# 展开后遍历
for item, depth in auto.WalkControl(combo, includeTop=True, maxDepth=2):
    if depth != 2 or item.ControlType != auto.ControlType.ListItemControl:
        continue
    print(item.Name)
```

## 遍历控件
### 第一种方式WalkTree
除了`auto.WalkTree`遍历目标控件外，还有`auto.WalkControl`遍历控件，区别在于`auto.WalkTree`必须传入自定义函数指定遍历的行为。`auto.WalkControl`将会在后面涉及可折叠类型的控件遍历时进行演示，WalkTree返回三个值：
- control：元素节点
- depth：查询深度
- remain：循环树节点剩余数量 int
下面给出一个简单的通过WalkTree遍历桌面的示例：
```python
import uiautomation as auto
def GetFirstChild(control):
    return control.GetFirstChildControl()
def GetNextSibling(control):
    return control.GetNextSiblingControl()
desktop = auto.GetRootControl()
for control, depth in auto.WalkTree(desktop, getFirstChild=GetFirstChild, getNextSibling=GetNextSibling,
                                    includeTop=True, maxDepth=2):
    if not control.Name:
        continue
    print(' ' * depth * 4, control.Name)
```
`maxDepth`指定了遍历深度，除了指定这两个方法以外还可以只转入`getChildren`方法：
```python
def GetChildren(control):
    return control.GetChildren()
for control, depth, remain in auto.WalkTree(desktop,
                                            getChildren=GetChildren,
                                            includeTop=True,
                                            maxDepth=2):
    if not control.Name:
        continue
    print(' ' * depth * 4, control.Name)
```
结果过滤的方逻辑我们还可以写到`yieldCondition`的传入函数中（GetChildren方法的结果再传到yieldcondition来二次处理）：
```python
def yieldCondition(control, depth):
    if control.Name:
        return True
for control, depth, remain in auto.WalkTree(desktop,
                                            getChildren=GetChildren,
                                            yieldCondition=yieldCondition,
                                            includeTop=True,
                                            maxDepth=2):
    print(' ' * depth * 4, control.Name)
```
在我电脑当前执行结果均为：
```
桌面 1
     任务栏
         开始
         在这里输入你要搜索的内容
         开始
         在这里输入你要搜索的内容
         系统时钟, 23:02, 2021/11/15
     test - Jupyter Notebook - 360安全浏览器 13.1
         Chrome Legacy Window
     一文掌握uiautomation的经典案例.md• - Typora
         Typora
     UIAutomation_demos – clipboard_test.py PyCharm
     Program Manager
```
WalkTree的规则是当设置getChildren函数时，忽略getFirstChild和getNextSibling，否则使用这两个函数。设置yieldCondition函数时则开启额外的过滤。
甚至可以**使用WalkTree方法计算全排列问题：**
```python
def NextPermutations(aTuple):
    left, permutation = aTuple
    ret = []
    for i, item in enumerate(left):
        nextLeft = left[:]
        del nextLeft[i]
        nextPermutation = permutation + [item]
        ret.append((nextLeft, nextPermutation))
    return ret
uniqueItems = list("abc")
n = len(uniqueItems)
count = 0
for (left, permutation), depth, remain in auto.WalkTree((uniqueItems, []), NextPermutations,
                                                        yieldCondition=lambda c, d: d == n):
    count += 1
    print(count, permutation)
```

### 第二种方式WalkControl
```python
tree = mmcWindow.TreeControl()
for item, depth in auto.WalkControl(tree, includeTop=False):
    if not isinstance(item, auto.TreeItemControl):
        continue
    item.GetSelectionItemPattern().Select(waitTime=0.01)
    pattern = item.GetExpandCollapsePattern()
    if pattern.ExpandCollapseState == auto.ExpandCollapseState.Collapsed:
        pattern.Expand(waitTime=0.01)
    print(' ' * (depth - 1) * 4, item.Name)
```
部分结果：
```
DESKTOP-IS8QJHF
     IDE ATA/ATAPI 控制器
         Intel(R) 300 Series Chipset Family SATA AHCI Controller
     便携设备
         Seagate1.81TB
	 .....
     音频输入和输出
         24B1W1G5 (英特尔(R) 显示器音频)
         Realtek Digital Output (Realtek High Definition Audio)
         立体声混音 (Realtek High Definition Audio)
         扬声器 (Realtek High Definition Audio)
```
