## xml文件
```xml
<collection shelf=``"New Arrivals"``>

    <``class` `className=``"1班"``>

       <code>2022001</code>
       
       <number>10</number>
       
       <teacher>小白</teacher>

    </``class``>

    <``class` `className=``"2班"``>

       <code>2022002</code>

       <number>20</number>

       <teacher>小红</teacher>

    </``class``>

    <``class` `className=``"3班"``>

       <code>2022003</code>

       <number>30</number>

       <teacher>小黑</teacher>

    </``class``></collection>
```

# Python解析xml有两种方式
## 1、ElementTree 方式（此方法遇到命名空间有难以处理的问题，建议使用lxml）
##### ***注：ElementTree查找节点是一层一层往下找，不能直接找到某个节点***
## 导入包
```python
 import xml.etree.ElementTree as ET
```
## 加载需要处理的xml文档
```python
# 第一种方式，返回elementtree元素
tree = ET.ElementTree(file='1.xml')
# 第二种方式，返回elementtree元素
tree = ET.parse('1.xml')
# 对于加载字符串类型的xml,此方法可以直接获取到根节点，返回element元素
tree = ET.fromstring(xml)
```
## 获取根元素
```python
# 处理xml数据第一步就是获取根元素（使用fromstring方法的可省略这一步，因为他已经获取到根节点）
# 由于ElementTree查找节点是一层一层往下找，所以这一步是必须
root = tree.getroot()
# <Element 'collection' at 0x000001FCC9BBFA90>
```
## 探索节点下有哪些直接子节点
```python
print(list(root)
```
## 根元素（root）是一个Element对象。我们看看根元素都有哪些属性
```python
root = tree.getroot()
root.tag, root.attrib
('collection', {'shelf': 'New Arrivals'})
```
## 根元素也具备遍历其直接子元素的接口
```python
for child_of_root in root:... 
```
## 通过索引值来访问特定的子元素
```python
root[0].tag, root[0].text
```
## 查找需要的元素
```python
# Element对象有一个iter方法，可以对某个元素对象之下所有的子元素进行深度优先遍历（DFS）。
# ElementTree对象同样也有这个方法。下面是查找XML文档中所有元素的最简单方法：
for elem in tree.iter():... 
	print(elem.tag, elem.attrib)
```
## iter方法可以接受tag名称，然后遍历所有具备所提供tag的元素：
```python
for elem in tree.iter(tag='teacher'):... 
```
## 通过xpath查找
```python
for elem in tree.iterfind('class/teacher'):...
```
## 查找所有具备某个name属性的className元素：
```python
for elem in tree.iterfind('class[@className="1班"]'):... 
```
## 使用Element.find(path)
根据传入的标签名称或标签路径查找第一个匹配的子元素(子标签)
语法：Element.find(pattern, namespaces=None)
⑴path：待查找标签的标签名或其路径(字符串，必填参数)
⑵namespaces：是从名称空间前缀到全名的可选映射(可选参数)
可以使用标签路径查找
```python
xml = """  
<MatlChklEdit>  
    <se xmlns="http://tempuri.org/">        <b>bbbb</b>        <a>aaa</a>    </se></MatlChklEdit>  
    """tree = et.fromstring(xml)  
# root = tree.getroot()  
s = tree.find("{http://tempuri.org/}se/{http://tempuri.org/}b")  
# b = s.find("{http://tempuri.org/}b")  
print(s)
```
如果当前元素有命名空间，例如MatlChklEdit标签中的xmlns(xml namespace)
```xml
<MatlChklEdit xmlns="http://tempuri.org/">  
    <se>  
        <a>aaa</a>  
    </se>
</MatlChklEdit>    
```
此时使用Element.find('se')无法找到节点，需加上命名空间，例如
element.find("{http://tempuri.org/}se"), 如果将xmlns改成aaa就可以直接查找，不用加命名空间

方法|属性名
:-|-
Element.iter(tag=None)|遍历该Element所有后代，也可以指定tag进行遍历寻找。
Element.iterfind(path, namespaces=None)| 根据tag或path查找所有的后代。
Element.itertext() |遍历所有后代并返回text值。
Element.findall(path)|查找当前元素下tag或path能够匹配的直系节点
Element.findtext(path, default=None, namespaces=None)  |寻找第一个匹配子元素，返回其text值。匹配对象可以为tag或path。
Element.find(path) |查找当前元素下tag或path能够匹配的首个直系节点
Element.text |获取当前元素的text值。
Element.get(key, default=None) |获取元素指定key对应的属性值，如果没有该属性，则返回default值。
Element.keys()  |返回元素属性名称列表
Element.items() |返回(name,value)列表
Element.getchildren()|
Element.getiterator(tag=None)|
Element.getiterator(self, tag=None)|

方法|属性名
:-|-
Element.tag|节点名（tag）(str)
Element.attrib|属性（attributes）(dict)
Element.text|文本（text）(str)
Element.tail|附加文本（tail） (str)
Element[:]|子节点列表(list)

## 2、DOM方式（一次性读入文件，消耗内存，不推荐）
DOM (Document Object Model)将XML文档作为一棵树状结构进行分析，获取节点的内容以及相关属性，或是新增、删除和修改节点的内容。XML解析器在加载XML文件以后，DQM模式将XML文件的元素视为一个树状结构的节点，一次性读入内存。

## 导入包
```python
from xml.dom.minidom import parse
```
## 读取文件
```python
dom = parse('1.xml')
```

```python
# 获取文档元素对象
elem = dom.documentElement
# 通过tagname获取标签 
classclass_list_obj = elem.getElementsByTagName('class')
print(class_list_obj)
print(type(class_list_obj))
for class_element in class_list_obj:
# 获取标签中内容
code = class_element.getElementsByTagName('code')[0].childNodes[0].nodeValue

number = class_element.getElementsByTagName('number')[0].childNodes[0].nodeValue

teacher = class_element.getElementsByTagName('teacher')[0].childNodes[0].nodeValue    print('code:', code, ', number:', number, ', teacher:', teacher)
```
## 输出结果
```python
[<DOM Element: class at 0x20141bc5c10>, <DOM Element: class at 0x20141bdf940>, <DOM Element: class at 0x20141bdfb80>]<class 'xml.dom.minicompat.NodeList'>code: 2022001 , number: 10 , teacher: 小白

code: 2022002 , number: 20 , teacher: 小红

code: 2022003 , number: 30 , teacher: 小黑
```
## 修改和删除节点
【修改和删除内容只在内存中修改，没有存到文件中，都要重新保存文件】
1. 修改节点
```python
#修改rank文本 
rank.text = "999" 
tree = ET.ElementTree(root) 
tree.write("new.xml", encoding='utf-8')
```
2. 修改属性节点
```python
#修改rank属性 
rank.set('update', '2020-11-11') 
tree = ET.ElementTree(root) 
tree.write("new.xml", encoding='utf-8')
```
3. 保存文件
```python
tree = ET.ElementTree(root) 
tree.write("new.xml", encoding='utf-8')
```
4. 删除节点
```python
root.remove( root.find('country') ) 
tree = ET.ElementTree(root) 
tree.write("new.xml", encoding='utf-8')
```
# 3. 使用lxml
## 加载需要处理的xml文档
```python
# 第一种方式，返回elementtree元素
tree = lxml.etree.parse('1.xml')
# 对于加载字符串类型的xml,此方法可以直接获取到根节点，返回element元素
tree = lxml.etree.fromstring(xml)
```
## 获取根元素
```python
# 处理xml数据第一步就是获取根元素（使用fromstring方法的可省略这一步，因为他已经获取到根节点）
# 由于ElementTree查找节点是一层一层往下找，所以这一步是必须
root = tree.getroot()
# <Element 'collection' at 0x000001FCC9BBFA90>
#获取属性
print(root.items()) #获取全部属性和属性值
print(root.keys())  #获取全部属性
print(root.get('version', '')) #
```
## 节点操作
1. 创建节点
```python
root = etrre.Element('root') 
print(root)
```
2. 获取节点名称
```python
print(root.tag)
```
3. 添加子节点
```python
# 第一种使用SubElement方法添加
child_sub = etree.SubElement(root, 'child_sub')
# 第二种使用append方法添加
child_append = etree.Element('child_append') 
root.append(child_append)
# 第三种使用insert方法添加
child_insert = etree.Element('child_insert') 
root.insert(0, child_append) 
# 第一个参数为添加的位置，第二个参数为添加的Element对象
```
4. 删除子节点
```python
root.remove(child_sub) # 删除名字为child_sub节点 
root.clear() # 清空root的所有子节点
```
5. 访问节点
```python
# 第一种通过列表的方式来访问节点
child_sub = root[0]  # 通过下标来访问子节点
child_sub = root[0: 1][0]  # 通过切片的方式来访问节点
for c in root:  # 通过遍历来获取所有节点
    print(c.tag)
    
c_append_index = root.index(child_append)  # 获取节点的索引
print(len(root))  # 获取子节点的数量
# 第二种通过方法来访问节点
print(child_sub.getparent().tag)  # 查询父节点
print(root.getchildren())  # 查询所有子节点
print(root.getroot())  # 获取根节点
print(root.find('b'))  # 查询第一个b标签
print(root.findall('.//b'))  # 查询所有b标签
# 第三种，通过Xpath（后面介绍）
```
## 属性操作
在Element中，节点的属性是以字典的形式存储的
```python
# 创建属性的两种方法
root = etree.Element('root', language='中文') # 创建节点时创建属性 
root.set('hello', 'python') # 使用set方法为root节点添加属性
# 获取属性
print(root.get('language')) # 使用get方法获取属性 
print(root['language']) 
print(root.keys()) 
print(root.values()) 
print(root.items())
# 修改属性
root['language'] = 'English'
```
## 文本操作
在lxml中访问xml文本的方式有多种，可以使用text、tail属性的方式访问文本。也可以使用[xpath](https://so.csdn.net/so/search?q=xpath&spm=1001.2101.3001.7020)语法访问文本。这里只介绍使用text和tail获取和设置文本的属性的方法。xpath后面会具体介绍。
text和tail属性 的区别：
xml中标签一般是成对出现的。但在HTML中则可能会出现单标签，如`<html><body>text<br/>tail</body></html>`。
-   text属性用于成对便签的读取和设置
-   tail属性用于单一标签的读取和设置
```python
html = etree.Element('html')
body = etree.SubElement(html, 'body')
body.text = 'text'  # 给body标签内写入text文本内容

br = etree.SubElement('body', 'br')
br.tail = 'tail'  # 在br标签中写入tail文本内容
```
## xml文件解析与序列化
**1. xml文件解析的方法**
xml文件解析的方法有多种，常用的有fromstring、XML、HTML、parse。其中XML和HTML的参数既可以是字符串、也可以是二进制的字节码。

fromstring、XML、parse：返回的是一个Element对象，是一个节点。主要用于解析文档碎片。

parse()： 返回值是一个ElementTree类型的对象，完整的xml树结构。parse主要用来解析完整的文档，而不是Element对象。

参数：
打开的文件或文件类型对象（建议以二进制形式打开
文件名或字符串
HTTP或者FTP的url。

注意：从文件名或者url解析通常比从文件对象解析要快。
```python
xml_data = '<root>data</root>'

 # fromstring
root_str = etree.formstring(xml_data)
print(root_str.tag)

 # XML
root_xml = etree.XML(xml_data)
print(root_xml.tag)

 # HTML，如果没有<html>和<body>标签，则会自动补上
 root_html = etree.HTML(xml_data)
 print(root_html.tag)
 
 # parse中的参数应该是一个完整的xml或html,同样返回值是一个ElementTree类型的对象，完整的xml树结构。parse主要用来解析完整的文档。
tree =etree.parse('text')   #文件解析成元素树
root = tree.getroot()      #获取元素树的根节点
print etree.tostring(root, pretty_print=True)
```
**2. xml文件序列化的方法**
我们在生成一个xml文件是有两种方式：
1、将Element对象转换成一个xml字符串，然后将其写入到文件中。
2、使用ElementTreee对象中的write()方法直接将xml写入文件。
```python
root = '<root>data</root>'

# 将Element对象转换成xml字符串写入文件
root_str = element.tostring(root, pretty_print=True, xml_declartion=True, encoding='utf-8')
with open('text.xml', 'w', encoding='utf-8') as f:
    f.write(root_str)


# 将节点（Element对象）转为ElementTree对象。
tree = etree.ElementTree(root)
tree.write('text.xml', pretty_print=True, xml_declartion=True, encoding='utf-8')

```
参数含义：
-   第一个参数是xml保持的路径（包括文件名）
-   pretty_print：是否格式化xml(美化)
-   xml_declaration：是否写入xml声明，就是xml中开头第一行文字。
-   encoding：编码格式
## lxml命名空间的处理
```python
from lxml import etree

str_xml = """
<A xmlns="http://This/is/a/namespace">
    <B>dataB1</B>
    <B>dataB2</B>
    <B><C>datac</C></B>
</A>
"""

xml = etree.fromstring(str_xml)  # 解析字符串
ns = xml.nsmap  # 获取命名空间
print(ns)
print(ns[None])

>>> {None: 'http://This/is/a/namespace'}
>>> http://This/is/a/namespace

ns = xml.nsmap[None]  # 获取命名空间xmlns

# 1. 使用findall方法查找指定节点。
for item in xml.findall(f'{ns}b')
	print(item.text)
    
# 2. 使用xpath语法加命名空间查找指定节点
ns = {'x':root.nsmap[None]}  # 获取命名空间
b = root.xpath("//x:B", namespaces=ns)
print(b)

C = root.xapth("//x:B/X:C", namespaces=ns)
print(c)

```
**注意：当xml携带有命名空间（xmlns）的时候，在查找节点时，每一级节点都需要加上命名空间。如果不携带命名空间，是无法查询到该节点的。**