import pymssql

server = "10.10.55.130"
user = "sa"
password = "sa123456"


# 创建表
# cursor.execute("""
# IF OBJECT_ID('persons', 'U') IS NOT NULL
#     DROP TABLE persons
# CREATE TABLE persons (
#     id INT NOT NULL,
#     name VARCHAR(100),
#     salesrep VARCHAR(100),
#     PRIMARY KEY(id)
# )
# """)　　

# 插入多行数据
# cursor.executemany(
#     "INSERT INTO persons VALUES (%d, %s, %s)",
#     [(1, 'John Smith', 'John Doe'),
#      (2, 'Jane Doe', 'Joe Dog'),
#      (3, 'Mike T.', 'Sarah H.')])
# # 你必须调用 commit() 来保持你数据的提交如果你没有将自动提交设置为true
# conn.commit()

# # 查询数据
# cursor.execute("SELECT * FROM EngManageMsgDelaySet WHERE UserSpId IN (SELECT NewSpID FROM StaffEntry WHERE StfID IN (SELECT ID FROM Staff WHERE Name IN ('苏轼','TEST','胡汉三','耳','小陈装修管家')))")
#

# 返回一条数据的
def runsql(sql):
    conn = pymssql.connect(server, user, password, "ltsysdbRelease", charset="utf8")  # 获取连接
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise NameError(f"{sql} 没有查找到值")
    return row

# 执行增删改的SQL
def run_zsg_sql(sql):
    conn = pymssql.connect(server, user, password, "ltsysdbRelease", charset="utf8")  # 获取连接
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 返回多条数据的
def runallsql(sql):
    conn = pymssql.connect(server, user, password, "ltsysdbRelease", charset="utf8")  # 获取连接
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    conn.close()
    if row is None:
        raise NameError(f"{sql} 没有查找到值")
    return row


# 随机获取合同ID
def contid():
    contid_sql = "SELECT TOP 1 ID, CustName FROM Contract WHERE StartDate IS NOT NULL ORDER BY NEWID()"
    coid = runsql(contid_sql)
    return coid

# 根据用户名获取合同ID
def selectcontid(name):
    selectcontid_sql = f"SELECT ID FROM Contract WHERE CustName='{name}'"
    coid = runsql(selectcontid_sql)
    return coid[0]


def get_recordid(name):
    recordid_sql = f"SELECT ID FROM AfterSaleRecord WHERE CustName='{name}'"
    recid = runsql(recordid_sql)
    return recid[0]

# def get_building():
#     building_sql = 'SELECT TOP 1 Name, AreaID, ID FROM  Buildings ORDER BY NEWID()'
#     build = runsql(building_sql)
#     return build
def get_building():
    building_sql = f"SELECT TOP 1 Name, AreaID, ID FROM  Buildings ORDER BY NEWID()"
    build = runsql(building_sql)
    return build

# 通过bldid获取楼盘名字
def get_bldname(bldid):
    bld_ssql = f"SELECT Name FROM Buildings WHERE ID='{bldid}'"
    bld_name = runsql(bld_ssql)
    return bld_name[0]

# 随机获取客户意向ID
def customerindent():
    simple_sql = 'SELECT TOP 1 ID FROM SimpleType WHERE Catg=4 AND State=2 ORDER BY NEWID()'
    simple = runsql(simple_sql)
    return simple[0]


# 随机获取客户标签
def custlevelid():
    level_sql = 'SELECT TOP 1 ID FROM SimpleType WHERE Catg=3 AND State=2 ORDER BY NEWID()'
    level = runsql(level_sql)
    return level[0]


# 随机获取客户来源
def custsource(*args):
    if args:
        source_sql = f"SELECT Name FROM SimpleType WHERE ID='{args[0]}'"
    else:
        source_sql = 'SELECT TOP 1 ID FROM SimpleType WHERE Catg=5 AND State=2 ORDER BY NEWID()'
    source = runsql(source_sql)
    return source[0]


# 随机获取房屋类型
def housetype():
    house_sql = 'WITH cs AS (SELECT DISTINCT ParentID FROM HouseType WHERE ParentID IS NOT NULL) ' \
                'SELECT TOP 1 ID FROM HouseType WHERE State=2 AND ID NOT IN  (SELECT * FROM cs) ORDER BY NEWID()'
    house_type = runsql(house_sql)
    return house_type[0]


# 随机获取客户户型
def custhousetype():
    custhouse_sql = 'WITH cs AS (SELECT DISTINCT ParentID FROM CustomerHouseType WHERE ParentID IS NOT NULL) ' \
                    'SELECT TOP 1 ID FROM CustomerHouseType WHERE State=2 AND ID NOT IN  (SELECT * FROM cs) ORDER BY NEWID()'
    custhousety = runsql(custhouse_sql)
    return custhousety[0]


# 随机获取客户年龄段
def custages():
    custage_sql = 'SELECT TOP 1 ID FROM SimpleType WHERE Catg=6 AND State=2 ORDER BY NEWID()'
    custage = runsql(custage_sql)
    return custage[0]


# 随机获取客户渠道
def custchannel():
    custchannel_sql = 'WITH cs AS (SELECT ParentID FROM CustChannel WHERE ParentID IS NOT NULL) ' \
                      'SELECT TOP 1 ID FROM CustChannel WHERE Catg=5 AND State=2 AND ID NOT IN  (SELECT * FROM cs) ORDER BY NEWID()'
    channel = runsql(custchannel_sql)
    return channel[0]


# 随机获取跟进方式
def custfollowway():
    followway_sql = 'SELECT TOP 1 ID FROM CustomerFollowWay WHERE State=2 ORDER BY NEWID()'
    followway = runsql(followway_sql)
    return followway[0]


# 随机选取几条售后问题分类
def get_problem(num):
    name = []
    ID = []
    u_name = []
    problem_sql = f'SELECT TOP {num} Name, ID FROM AfterSaleProblem WHERE ID NOT IN (SELECT ParentID FROM AfterSaleProblem WHERE ParentID IS NOT NULL) AND State=2 ORDER BY NEWID()'
    problem = runallsql(problem_sql)
    for i in problem:
        name.append(i[0])
        ID.append(i[1])

    for n in name:
        all_name = runallsql(f'EXEC abc {n}')
        l = [s[0] for s in all_name]
        l.reverse()
        union_name = '/'.join(l)
        u_name.append(union_name)
    p_id = ','.join([str(k) for k in ID])
    p_name = ','.join(u_name)
    return p_id, p_name


def housetypeid(c_id):
    housetypeid_sql = f"SELECT HouseTypeID FROM Contract WHERE ID='{c_id}'"
    h_id = runsql(housetypeid_sql)
    return h_id[0]


# 获取客户相关信息
def budid(name):
    buildid_sql = f"SELECT BuildingsID,AreaID,ID,ContactWays,CustomerHouseType,Address,HouseArea,HouseTypeID FROM Customer WHERE Name='{name}'"
    builds = runsql(buildid_sql)
    return builds

# 根据客户名字获取客户ID、电话、公司ID
def customerid(Name):
    custid_sql = f"SELECT ID,CoID,ContactWays FROM Customer WHERE Name='{Name}'"
    custid = runsql(custid_sql)
    return custid


def discountid(custid):
    discountid_sql = f"SELECT ID FROM Discount WHERE CustID='{custid}'"
    id = runsql(discountid_sql)
    return id[0]


# 获取客户相关信息
def custcretime(name):
    custcretime_sql = f"SELECT CreTime,ID,UpdtTime,Address,AreaID,BuildingsID,ContactWays,CustIntentID,CustLevelID,CustSourceID,CustomerHouseType,HandInDate,HouseTypeID,No,AgeGroupID,ChannelID,AppSpID,OperID,CoID FROM Customer WHERE Name='{name}'"
    cretime = runsql(custcretime_sql)
    return cretime


# 获取地址名，例如 四川省/成都市/青白江区 /清泉镇
def areaname(n):
    areaname_sql = f"WITH cte(Name,ParentID) AS(SELECT Name, ParentID FROM Area WHERE ID = '{n}' UNION all SELECT D.Name, D.ParentID FROM cte C, Area D WHERE C.ParentID=D.ID)" \
                   'SELECT * FROM cte'
    names = runallsql(areaname_sql)
    ll = [s[0] for s in names]
    ll.reverse()
    union_name = '/'.join(ll)
    return union_name


# 获取建筑所在位置
def custbldname(areaid):
    bldname_sql = f"SELECT Name FROM Buildings WHERE ID='{areaid}'"
    bldname = runsql(bldname_sql)
    return bldname[0]


# 获取客户联系方式创建时间
def custcontactway(custid):
    contact_sql = f"SELECT CreTime,UpdtTime FROM CustContactWay WHERE CustID='{custid}'"
    contacts = runsql(contact_sql)
    return contacts


# 获取客户意向
def custindent(indentid):
    indent_sql = f"SELECT Name FROM SimpleType WHERE ID='{indentid}'"
    indentname = runsql(indent_sql)
    return indentname[0]


# 获取家装顾问相关信息
def custperson(custid):
    custper_sql = f"SELECT UserID,UserSpID,ID,OperID,CreTime,UpdtTime FROM CustPerson WHERE CustID='{custid}'"
    custpers = runsql(custper_sql)
    return custpers


# 获取家装顾问全称
def custfullname(userspid):
    staffpos_sql = f"SELECT DeptID,PosID,StfID,State,TenureType FROM StaffPos WHERE ID='{userspid}'"
    staffpos = runsql(staffpos_sql)
    dept_name = runallsql(f"EXEC abcde '{staffpos[0]}'")
    ll = [s[0] for s in dept_name]
    company_id = [s[1] for s in dept_name].pop()
    company = runsql(f"SELECT ShortName FROM Department WHERE ID='{company_id}'")[0]
    company = '【' + company + '】'  # 获取所属公司
    ll.reverse()
    # 获取职位，例如装修管家
    position_sql = f"SELECT Name FROM Position WHERE ID='{staffpos[1]}'"
    position = runsql(position_sql)[0]
    ll.append(position)
    # 获取员工姓名
    custname_sql = f"SELECT Name FROM Staff WHERE ID='{staffpos[2]}'"
    cname = runsql(custname_sql)[0]
    if staffpos[3] == 3:
        state = "正式"
    else:
        raise Exception("登录职位非正式职位！")
    if staffpos[4] == 2:
        typ = "兼职"
        custname = f"{cname}({state}/{typ})"
    else:
        custname = f"{cname}({state})"

    ll.append(custname)
    fullname = '/'.join(ll)
    n = company + fullname
    return n, cname


# 获取housetypename
def housetypename(housetypeid):
    typename_sql = f"WITH cte(Name,ParentID) AS(SELECT Name, ParentID FROM CustomerHouseType WHERE ID = '{housetypeid}' UNION all SELECT D.Name, D.ParentID FROM cte C, CustomerHouseType D WHERE C.ParentID=D.ID)" \
                   'SELECT * FROM cte'
    names = runallsql(typename_sql)
    ll = [s[0] for s in names]
    ll.reverse()
    union_name = '/'.join(ll)
    return union_name


# 获取房屋类型，例如精装别墅区/现代化别墅3/新式别墅
def gethousetype(houseid):
    housetype_sql = f"WITH cte(Name,ParentID) AS(SELECT Name, ParentID FROM HouseType WHERE ID = '{houseid}' UNION all SELECT D.Name, D.ParentID FROM cte C, HouseType D WHERE C.ParentID=D.ID)" \
                    'SELECT * FROM cte'
    names = runallsql(housetype_sql)
    ll = [s[0] for s in names]
    ll.reverse()
    union_name = '/'.join(ll)
    return union_name


# 获取客户渠道
def getcustchanel(chanelid):
    channel_sql = f"WITH cte(Name,ParentID) AS(SELECT Name, ParentID FROM CustChannel WHERE ID = '{chanelid}' UNION all SELECT D.Name, D.ParentID FROM cte C, CustChannel D WHERE C.ParentID=D.ID)" \
                  'SELECT * FROM cte'
    names = runallsql(channel_sql)
    ll = [s[0] for s in names]
    ll.reverse()
    union_name = '/'.join(ll)
    return union_name


# 获取操作人信息，即登录人
def getopers(posid):
    opers_sql = f"SELECT ID,Name FROM Staff WHERE ID=(SELECT StfID FROM StaffPos WHERE ID='{posid}')"
    opers = runsql(opers_sql)
    return opers


# 获取公司ID
def getcoid(posid):
    coid_sql = f"SELECT CoID FROM StaffPos WHERE ID='{posid}'"
    coid = runsql(coid_sql)
    return coid[0]


# 获取公司缩写名称
def getconame(coid):
    coname_sql = f"SELECT ShortName FROM Department WHERE ID='{coid}'"
    coname = runsql(coname_sql)
    return coname[0]


# 获取客户的创建人员
def custoper(operid):
    custoper_sql = f"SELECT Name FROM Staff WHERE ID=(SELECT StfID FROM StaffPos WHERE ID='{operid}')"
    deptname_sql = f"SELECT Name FROM Department WHERE ID=(SELECT DeptID FROM StaffPos WHERE ID='{operid}')"
    oper = runsql(custoper_sql)
    deptname = runsql(deptname_sql)
    fullname = deptname[0] + '/' + oper[0]
    return oper[0], fullname


# 获取优惠产品信息
def discounts(itemid):
    disct_sql = f"SELECT Name,Content,Price,ChkPrice,Count,DiscSetID FROM DiscItem WHERE ID='{itemid}'"
    disc = runsql(disct_sql)
    return disc


# 获取材料产品系列名
def prodname(itemid):
    prod_sql = f"SELECT NameText,Catg FROM OffcGoods WHERE id=(SELECT ProdID FROM DiscItem WHERE ID='{itemid}')"
    prod = runsql(prod_sql)
    return prod


# 根据登录人获取登录人公司全称
def logincompany(loginid):
    com_sql = f"SELECT Name FROM Department WHERE ID=(SELECT CoID FROM StaffPos WHERE ID='{loginid}')"
    comp = runsql(com_sql)
    return comp[0]


# 通过积分单号获取积分详情单ID
def degnintegralid(jfd):
    dsginte_sql = f"SELECT ID FROM DsgnIntegralDetail WHERE DsgnBillNo='{jfd}'"
    dsgninte = runsql(dsginte_sql)
    return dsgninte[0]


# 随机返回一个设计师ID
def liaisondsgnid():
    liai_sql = "SELECT TOP 1 ID FROM StaffPos WHERE PosID IN (SELECT ID FROM Position WHERE Name IN ('方案设计师','空间设计师','深化设计师') AND CoID='{09A055C1-4885-47E7-A5CA-7066F16C4537}') AND State IN ('2','3') ORDER BY NEWID()"
    liaiid = runsql(liai_sql)
    return liaiid[0]


# 随机获取联络类型
def liaisontype():
    liaison_sql = "SELECT TOP 1 ID FROM LiaisonType ORDER BY NEWID()"
    liaison = runsql(liaison_sql)
    return liaison[0]


# 获取合同优惠单
# def discount(name):
#     dic_sql = f"SELECT ID FROM Discount WHERE CustID=(SELECT ID FROM Customer WHERE Name='{name}')"
#     discid = runsql(dic_sql)
#     return discid[0]

# for r in row:
#     print(r)nt(row)
#
# while row:
#     print("ID=%d, Name=%s" % (row[0], row[1]))
#     row = cursor.fetchone()
# # 遍历数据（存放到元组中） 方式2
# for row in cursor:
#     # print('row = %r' % (row,))
#     print(row)


# 遍历数据（存放到字典中）
# cursor = conn.cursor(as_dict=True)
#
# cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
# for row in cursor:
#     print("ID=%d, Name=%s" % (row['id'], row['name']))
#
# conn.close()
# 关闭连接

# 根据设计师POSID随机选择一个合同
def getdsgncont(dsgnid):
    dsgn_sql = f"SELECT TOP 1 No,ID FROM Contract WHERE DesnID='{dsgnid}' AND State IN (2,3,4,6,7,9) ORDER BY NEWID()"
    dsgncont = runsql(dsgn_sql)
    return dsgncont


def getcailiao():
    data_list = []
    cl_sql = "SELECT DISTINCT(c.No),c.CoID FROM MatlPur m INNER JOIN Contract c ON m.ContID=c.ID INNER JOIN SupplierManage s ON m.BrandId=s.BrandId AND m.CoID=s.CoID WHERE s.TargetCoId='{5F361789-A535-4024-8C84-8A9BEFC09C6F}' AND c.State='4'"
    conn = pymssql.connect(server, user, password, "ltsysdbRelease", charset="utf8")  # 获取连接
    cursor = conn.cursor()
    cursor.execute(cl_sql)
    row = cursor.fetchall()
    conn.close()
    if row is None:
        raise NameError(f"{cl_sql} 没有查找到值")
    for i in range(len(row)):
        data_list.append(row[i][0])
    return data_list


# 根据合同ID获取合同人员ID，也可获取其他相关合同人员
def contperson(contid, person):
    # budgeterspid = 15 # 预算员
    person_dict = {'budgeterspid': 15, }
    pcatg = person_dict.get(person)
    contp_sql = f"SELECT UserSpID FROM ContPerson WHERE ContID='{contid}' AND PersonCatg='{pcatg}'"
    cont_person = runsql(contp_sql)
    return cont_person[0]


# 根据人员staffpos ID获取人员姓名
def person_name(personid):
    personname_sql = f"SELECT Name FROM Staff WHERE ID=(SELECT stfid FROM StaffPos WHERE id='{personid}')"
    personname = runsql(personname_sql)
    return personname[0]


# 获取合同编号
def contno(name):
    contno_sql = f"SELECT No FROM Contract WHERE CustName='{name}'"
    cont_no = runsql(contno_sql)
    return cont_no[0]


# 根据staffPOS ID获取员工直属部门，并与员工姓名拼接如：设四9组/苏轼
def deptstaff(pos, contno):
    posdict = {'设计师': 'DesnID', '管家': 'PMID'}
    p = posdict.get(pos)
    posid = runsql(f"SELECT {p} FROM Contract WHERE No='{contno}'")
    dept_sql = f"SELECT Name FROM Department WHERE ID=(SELECT DeptID FROM StaffPos WHERE id='{posid[0]}')"
    deptname = runsql(dept_sql)
    staff_sql = f"SELECT Name FROM staff WHERE ID=(SELECT stfid FROM StaffPos WHERE id='{posid[0]}')"
    staffname = runsql(staff_sql)
    ds = deptname[0]+'/'+staffname[0]
    return ds, posid[0]


# 根据合同id获取合同内部分信息
def contmsg(no):
    contmsg_sql = f"SELECT TimeLimit,StartDate,ExpectCmplDate,ExpectStartDate FROM Contract WHERE No='{no}'"
    cont_msg = runsql(contmsg_sql)
    st = cont_msg[1].strftime("%Y-%m-%d %H:%M:%S")
    st2 = st.replace(' ', 'T')
    ct = cont_msg[2].strftime("%Y-%m-%d %H:%M:%S")
    ct2 = ct.replace(' ', 'T')
    esd = cont_msg[3].strftime("%Y-%m-%d %H:%M:%S")
    esd2 = esd.replace(' ', 'T')
    return cont_msg[0], st2, ct2, esd2


# 设置用户密码为’a1234567890‘
def initpwd(user_id):
    userinfo_sql = f"SELECT LoginTime FROM  [ltsysdbRelease].[dbo].[User]  WHERE LoginID ='{user_id}'"
    logintime = runsql(userinfo_sql)
    if '2022' in str(logintime):
        return False
    userid_sql = f"UPDATE [ltsysdbRelease].[dbo].[User] Set Password='ddbbf0170dc08fddc028c929a5a33205' WHERE LoginID ='{user_id}'"
    run_zsg_sql(userid_sql)
    return True


# 分配角色
def select_role(user_id):
    role_sql = f"UPDATE StaffPos Set RoleID='E1DA41B9-5785-4E39-983F-A17675A2885A' WHERE stfID = (SELECT ID FROM Staff WHERE No='{user_id}')"
    run_zsg_sql(role_sql)


# 获取用户登录session
def get_session(user_id):
    try:
        session_sql = f"SELECT TOP 1 ID, staffPosID FROM LoginSession WHERE staffposid in (SELECT ID FROM StaffPos WHERE stfID =(SELECT ID FROM Staff WHERE No='{user_id}')) ORDER BY LastTime DESC"
        sesion_id = runsql(session_sql)
    except NameError:
        return False
    else:
        return sesion_id


# 根据用户ID获取用户主职POSID与主职部门
def get_posid(user_id):
    posid_sql = f'''
SELECT s.ID ,d.Name FROM StaffPos s
INNER JOIN Department d ON s.deptID = d.ID
INNER JOIN Staff st ON s.StfID=st.ID
WHERE st.No = '{user_id}'
AND s.QuitDate IS null
AND s.TenureType = 1
    '''
    result = runsql(posid_sql)
    return result

def get_flow(node_name):
    flow_sql = f"select TOP 1 LogID,ID from FlowNodeLog where  NodeName like '%{node_name}%' order by CreTime DESC"
    node = runsql(flow_sql)
    return node

# 通过客户名获取客户见面创建时间、方案设计师POSID,设计师ID
def get_meettime(c_name):
    meet_sql = f"SELECT cretime,SchemeDsgnSpID,DsgnSpID,ID FROM CustMeet WHERE custid=(SELECT TOP 1 ID FROM Customer WHERE Name='{c_name}')"
    t = runsql(meet_sql)
    return t

# 上传图片需要的relateID
def pic_relateid(contid, t):
    pic_sql = f"select top 1 ContStartPlanFatta.ID from ContStartPlan inner join ContStartPlanFatta on ContStartPlan.ID=ContStartPlanFatta.ContStartPlanID where ContStartPlanFatta.FattaType={t} and ContID='{contid}'order by ContStartPlan.CreTime desc "
    relateid = runsql(pic_sql)
    return relateid[0]

# 根据流程ID查询此流程所有通知节点ID，用于处理流程通知
def update_flow(logid):
    update_sql = f"UPDATE FlowNodeLog Set HandlerID='D1849E4B-49AC-488B-81C8-00254AD82436', HandleTime='2022-06-14 15:51:41.863' ,State=7 WHERE LogID='{logid}' and IsCopy='True' and HandlerID is null"
    run_zsg_sql(update_sql)

def ss():
    cl_sql = "SELECT No FROM OffcGoods WHERE State=2 AND catg=3"
    clid = runallsql(cl_sql)
    return clid

if __name__ == "__main__":
    update_flow('{992BCE96-D83E-4E1C-89FE-A22F169843DB}')