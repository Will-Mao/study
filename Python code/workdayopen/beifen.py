# encoding=utf-8
import requests, pprint
import random, time
import sqlserver_act as SQL
import datetime
import re, yaml
import multiprocessing




# 随机生成一个名字
def get_name():
    name_word = "海客谈瀛洲烟涛微茫信难求越人语天姥云霞明灭或可睹天姥连天向天横势拔五岳掩赤城天台四万八千丈对此欲倒东南倾我欲因之梦吴越一夜飞度" \
                "镜湖月湖月照我影送我至剡溪谢公宿处今尚在渌水荡漾清猿啼脚著谢公屐身登青云梯半壁见海日空中闻天鸡千岩万转路不定迷花倚石忽已暝熊咆" \
                "龙吟殷岩泉栗深林兮惊层巅云青青兮欲雨水澹澹兮生烟列缺霹雳丘峦崩摧洞天石扉訇然中开青冥浩荡不见底日月照耀金银台霓为衣兮风为马云之" \
                "君兮纷纷而来下虎鼓瑟兮鸾回车仙之人兮列如麻忽魂悸以魄动恍惊起而长嗟惟觉时之枕席失向来之烟霞世间行乐亦如此古来万事东流水别君去兮" \
                "何时还且放白鹿青崖间须行即骑访名山安能摧眉折腰事权贵使我不得开心颜"
    n = random.sample(name_word, 3)
    custname = ''.join(n)
    return custname


# 添加售后登记
def add_aftersalerecord():
    global contID
    phone = random.randint(10000000000, 20000000000)
    num = random.randint(1, 5)
    contID = SQL.contid()
    coid = SQL.getcoid(LoginStafPosID)
    p_id, p_name = SQL.get_problem(num)
    as_cretime = modifydatetime('now')
    url = f"https://dv.lantingroup.cn:{port}/PC/AfaterSale/AfterSaleService.svc"
    header = {'Content-Type': 'text/xml; charset=utf-8',
              'Host': f'dv.lantingroup.cn:{port}',
              'Expect': '100-continue',
              'Accept-Encoding': 'gzip,deflate',
              'SOAPAction': '"http://tempuri.org/IAfterSaleRecord/AddAfterSaleRecord"'}

    body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><AddAfterSaleRecord xmlns="http://tempuri.org/">{session}\
    <afterSaleRecord xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">\
            <a:CoID>{coid}</a:CoID><a:CoName i:nil="true"/><a:CreTime>{as_cretime}+08:00</a:CreTime>\
            <a:ID i:nil="true"/><a:Oper i:nil="true"/><a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/>\
            <a:UpdtOperId i:nil="true"/><a:UpdtTime>{as_cretime}+08:00</a:UpdtTime><a:AfterSaleCharges i:nil="true"/>\
            <a:AfterSaleComplains i:nil="true"/><a:AfterSaleCosts i:nil="true"/><a:AfterSaleFollows i:nil="true"/><a:AfterSalePersons i:nil="true"/>\
            <a:Attach/><a:CommunicateTime>111222333</a:CommunicateTime><a:ContAmt i:nil="true"/><a:ContBldName i:nil="true"/><a:ContCustName i:nil="true"/>\
            <a:ContCustPhone i:nil="true"/><a:ContDesnName i:nil="true"/><a:ContGuWenName i:nil="true"/><a:ContID>{contID[0]}</a:ContID>\
            <a:ContNo i:nil="true"/><a:ContPersonList i:nil="true"/><a:ContPjtAddr i:nil="true"/><a:ContPmName i:nil="true"/><a:ContState>0</a:ContState>\
            <a:Content>121212232323</a:Content><a:Contract i:nil="true"/><a:CustName>{contID[1]}</a:CustName><a:CustPhone>{phone}</a:CustPhone>\
            <a:Defendant i:nil="true"/><a:FinishTime i:nil="true"/><a:IsExistComplain>false</a:IsExistComplain><a:IsSubcont>false</a:IsSubcont><a:No i:nil="true"/>\
            <a:ProblemID>{p_id}</a:ProblemID><a:ProblemName>{p_name}</a:ProblemName>\
            <a:Responsibility i:nil="true"/><a:ShuiDianAmt i:nil="true"/><a:SourceID>550a90b3-8305-41e7-a5a0-5813b9499b9c</a:SourceID><a:State>0</a:State>\
            <a:SupplierIDList i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:WarrantyCardID i:nil="true"/>\
            <a:WarrantyCardInfo i:nil="true"/></afterSaleRecord></AddAfterSaleRecord></s:Body></s:Envelope>'

    r = requests.post(url, headers=header, data=body.encode('utf-8'))
    # r.encoding = 'gb2312'
    if contID[1] in r.text:
        print('add_aftersale Pass \n')
    else:
        print(r.text)
        raise NameError(f"{contID[1]} 没有完成")
    # print(r.text)


# 完成售后登记
def completerecord():
    # global contID
    record_id = SQL.get_recordid(contID[1])
    url = f"https://dv.lantingroup.cn:{port}/PC/AfaterSale/AfterSaleService.svc"
    c_header = {'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': '"http://tempuri.org/IAfterSaleRecord/FinishAfterSaleRecord"',
                'Host': f'dv.lantingroup.cn:{port}',
                'Content-Length': '632',
                'Expect': '100-continue',
                'Accept-Encoding': 'gzip, deflate'}

    c_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body>\
        <FinishAfterSaleRecord xmlns="http://tempuri.org/">{session}\
        <afterSaleRecordID>{record_id}</afterSaleRecordID></FinishAfterSaleRecord></s:Body></s:Envelope>'
    r = requests.post(url, headers=c_header, data=c_body.encode('utf-8'))
    if contID[1] in r.text:
        print('complete Pass \n')
    else:
        print(r.text)
        raise NameError(f"{contID[1]} 没有完成")


# 新增客户
def customersave(name):
    address = SQL.get_building()
    cre_time = modifydatetime('now')
    cont_time = modifydatetime(minutes=5)
    follow_time = modifydatetime(days=1)
    c_phone = random.randint(10000000000, 20000000000)
    opers = SQL.getopers(LoginStafPosID)
    coid = SQL.getcoid(LoginStafPosID)
    customindent = SQL.customerindent()
    custlevel = SQL.custlevelid()
    source = SQL.custsource()
    housetype = SQL.housetype()
    custhouse = SQL.custhousetype()
    age = SQL.custages()
    channelid = SQL.custchannel()
    follow_way = SQL.custfollowway()
    url = f'https://dv.lantingroup.cn:{port}/PC/Customer/CustomerService.svc'
    cs_header = {'Content-Type': 'text/xml; charset=utf-8',
                 'SOAPAction': '"http://tempuri.org/ICustomer/CustomerSave"',
                 'Host': f'dv.lantingroup.cn:{port}',
                 'Content-Length': '4779',
                 'Expect': '100-continue',
                 'Accept-Encoding': 'gzip, deflate'}

    cs_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><CustomerSave xmlns="http://tempuri.org/">{session} \
              <customer xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"> \
              <a:CoID>{coid}</a:CoID><a:CoName i:nil="true"/><a:CreTime>{cre_time}+08:00</a:CreTime><a:ID i:nil="true"/>\
              <a:Oper>{opers[1]}</a:Oper><a:OperID>{opers[0]}</a:OperID><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/> \
              <a:UpdtOperId i:nil="true"/><a:UpdtTime>{cre_time}+08:00</a:UpdtTime><a:Address>{address[0]}11栋22单元33层44号</a:Address><a:AppSpID i:nil="true"/> \
              <a:Apper i:nil="true"/><a:AreaID>{address[1]}</a:AreaID><a:AreaName i:nil="true"/><a:Catg>0</a:Catg> \
              <a:CustBldID>{address[2]}</a:CustBldID><a:CustBldName i:nil="true"/><a:CustContactWay i:nil="true"/> \
              <a:CustContactWays><a:SvcCustContactWay><a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{cont_time}+08:00</a:CreTime> \
              <a:ID i:nil="true"/><a:Oper i:nil="true"/><a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/> \
              <a:UpdtTime>{cont_time}+08:00</a:UpdtTime><a:Catg>1</a:Catg><a:CustID i:nil="true"/><a:Sort>0</a:Sort><a:Way>{c_phone}</a:Way></a:SvcCustContactWay> \
              </a:CustContactWays><a:CustDsgnID i:nil="true"/><a:CustDsgner i:nil="true"/><a:CustIntentID>{customindent}</a:CustIntentID> \
              <a:CustIntentName i:nil="true"/><a:CustLevelID>{custlevel}</a:CustLevelID>\
              <a:CustLevelName i:nil="true"/><a:CustName>{name}</a:CustName><a:CustPersons/><a:CustSourceID>{source}</a:CustSourceID> \
              <a:CustSourceName i:nil="true"/><a:CustTels i:nil="true"/><a:CustTelsAllStr i:nil="true"/> \
              <a:CustTelsList i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:CustTelsStr i:nil="true"/> \
              <a:CustomerHouseTypeID>{custhouse}</a:CustomerHouseTypeID><a:CustomerHouseTypeName i:nil="true"/><a:DeptName i:nil="true"/> \
              <a:HandInDate>{cre_time}+08:00</a:HandInDate><a:HouseArea>130</a:HouseArea><a:HouseBuilding>11</a:HouseBuilding><a:HouseFloor>33</a:HouseFloor> \
              <a:HouseNumber>44</a:HouseNumber><a:HouseType/><a:HouseTypeID>{housetype}</a:HouseTypeID><a:HouseTypeName i:nil="true"/> \
              <a:HouseUnit>22</a:HouseUnit><a:IsAreaRepeat i:nil="true"/><a:NextFlwTime i:nil="true"/><a:NextFlwWayID i:nil="true"/><a:NextFlwWayName i:nil="true"/> \
              <a:No i:nil="true"/><a:Remark>客户说明内容</a:Remark><a:RepeatCatg>0</a:RepeatCatg><a:AgeGroupID>{age}</a:AgeGroupID> \
              <a:AssState>3</a:AssState><a:ChannelID>{channelid}</a:ChannelID><a:ChannelName i:nil="true"/><a:ConsultWayID i:nil="true"/> \
              <a:ConsultWayName i:nil="true"/><a:ContAddr i:nil="true"/><a:ContAmt i:nil="true"/><a:ContID i:nil="true"/><a:ContNo i:nil="true"/><a:ContProCatg>0</a:ContProCatg> \
              <a:ContState>0</a:ContState><a:DesignMode i:nil="true"/><a:DesignModeTxt i:nil="true"/><a:DesnID i:nil="true"/><a:DesnName i:nil="true"/> \
              <a:ExtensionManDirectorName i:nil="true"/><a:FlwData><a:AppSpID i:nil="true"/><a:Attachment/><a:Catg>1</a:Catg><a:CustID i:nil="true"/> \
              <a:CustIntention>{customindent}</a:CustIntention><a:CustState>0</a:CustState><a:FollowContent>本次跟进内容</a:FollowContent>' \
              f'<a:FollowType>c056bd76-5016-4dda-8c94-5f0a55a3003d</a:FollowType><a:FollowWay>{follow_way}</a:FollowWay><a:IsCanProtectCustomer>false</a:IsCanProtectCustomer> \
              <a:NextFlowContent>下次跟进内容</a:NextFlowContent><a:NextFollowTime>{follow_time}+08:00</a:NextFollowTime> \
              <a:NextFollowWay>{follow_way}</a:NextFollowWay></a:FlwData>' \
              f'<a:IntentDate i:nil="true"/><a:IsPayCust>false</a:IsPayCust><a:IsReceipt>true</a:IsReceipt><a:IsRepeat>false</a:IsRepeat> \
              <a:KeyWord i:nil="true"/><a:MarketerID>1dc04ef2-7e83-4c61-8162-a07b7f3c46f9</a:MarketerID><a:MatketerName i:nil="true"/><a:OperationManagerName i:nil="true"/> \
              <a:PMID i:nil="true"/><a:PMName i:nil="true"/><a:PromID i:nil="true"/><a:PromName i:nil="true"/><a:PullDeadReason i:nil="true"/>' \
              f'<a:ServiceDirectorName i:nil="true"/><a:ServiceName i:nil="true"/> \
              <a:SiteID i:nil="true"/><a:SiteName i:nil="true"/><a:SitePromName i:nil="true"/><a:SiteUrl i:nil="true"/><a:State>0</a:State></customer></CustomerSave></s:Body></s:Envelope>'
    # 耳A区 marketID：1dc04ef2-7e83-4c61-8162-a07b7f3c46f9 ，C区marketID：5a70e19f-57f3-4d42-84b7-124c96e67806， 湖北marketID：9004b1f3-ef27-4791-9219-eb18a3bae284
    r = requests.post(url, headers=cs_header, data=cs_body.encode('utf-8'))
    if re.search("<IsSuccess.*?true</IsSuccess>", r.text, re.S):
        print(f"客户{name}新增成功")
        custid = re.search("ReturnData.+?>(.*?)</ReturnData>", r.text).group(1)
        time.sleep(2)
        tointent(custid)
        time.sleep(1)
        custmeet(name)
    else:
        print(r.text)


# 转意向客户
def tointent(custid):
    url = f'https://dv.lantingroup.cn:{port}/PC/Customer/CustomerService.svc'
    intent_head = {'Content-Type': 'text/xml; charset=utf-8',
                   'SOAPAction': '"http://tempuri.org/ICustomer/CustomerToIntent"',
                   'Host': f'dv.lantingroup.cn:{port}',
                   'Content-Length': '609',
                   'Expect': '100-continue',
                   'Accept-Encoding': 'gzip, deflate',
                   'Connection': 'Keep-Alive'}

    intent_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><CustomerToIntent xmlns="http://tempuri.org/">{session} \
                  <custID>{custid}</custID><remark/></CustomerToIntent></s:Body></s:Envelope>'
    requests.post(url, headers=intent_head, data=intent_body.encode('utf-8'))


# 设计见面
def custmeet(custname):
    cre_time = modifydatetime('now')
    opers = SQL.getopers(LoginStafPosID)
    # coid = SQL.getcoid(LoginStafPosID)
    custcret = SQL.custcretime(custname)
    coname = SQL.getconame(custcret[18])
    bldname = SQL.custbldname(custcret[5])
    areaname = SQL.areaname(custcret[4])
    oper, fullname = SQL.custoper(custcret[17])
    contacts = SQL.custcontactway(custcret[1])
    indentname = SQL.custindent(custcret[7])
    levelname = SQL.custindent(custcret[8])
    custpers = SQL.custperson(custcret[1])
    username, marketname = SQL.custfullname(custpers[1])
    sourcename = SQL.custsource(custcret[9])
    housetypename = SQL.housetypename(custcret[10])
    housetype = SQL.gethousetype(custcret[12])
    custchanel = SQL.getcustchanel(custcret[15])
    if str(custcret[18]) == '09a055c1-4885-47e7-a5ca-7066f16c4537':  # 岚庭家居
        deepdsgn = '设四9组/杜甫'
        deepid = '5f9b6bdf-967b-4dbd-bba1-cc69884bdb2d'
        schdsgn = '设四9组/苏轼'
        schid = '8ca150bf-7cea-4d0a-a3c4-b650226c71b1'
    # elif str(custid[1]) == '8D92D6FB-C865-4A1F-B375-C0C24CD2DCF5':  # 湖北武汉岚庭
    #     discoutlist = 'e4dd23c9-bde3-4416-827b-e33d065f54c2'
    elif str(custcret[18]) == 'c7cc5de4-efdd-4aa7-9615-7a748785be12':  # 幸福魔方
        deepdsgn = '设计六部4组/6部4组深化设计师'
        deepid = '8ff8c7df-92b8-4288-853b-e986f0ebb26e'
        schdsgn = '设计六部4组/6部4组方案设计师'
        schid = 'cf22e5a8-c0b3-4ebe-abf9-bec40092f7ff'
    else:
        print(str(custcret[18]))
        raise Exception("这是啥公司的客户？")
    url = f'https://dv.lantingroup.cn:{port}/PC/Customer/CustomerService.svc'
    head = {'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': '"http://tempuri.org/ICustMeet/SaveCustMeet"',
            'Host': f'dv.lantingroup.cn:{port}',
            'Content-Length': '6570',
            'Expect': '100-continue',
            'Accept-Encoding': 'gzip, deflate'}
    body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SaveCustMeet xmlns="http://tempuri.org/">{session}' \
           '<custMeet xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
           f'<a:CoID>{custcret[18]}</a:CoID><a:CoName i:nil="true"/><a:CreTime>{cre_time}+08:00</a:CreTime><a:ID i:nil="true"/>' \
           f'<a:Oper>{opers[1]}</a:Oper><a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/>' \
           f'<a:UpdtTime>{cre_time}+08:00</a:UpdtTime><a:AppSpID>{custcret[16]}</a:AppSpID><a:Apper i:nil="true"/>' \
           f'<a:Cust><a:CoID>{custcret[18]}</a:CoID><a:CoName>{coname}</a:CoName><a:CreTime>{modifydatetime(custcret[0])}</a:CreTime>' \
           f'<a:ID>{custcret[1]}</a:ID><a:Oper>{oper}</a:Oper><a:OperID>{LoginStafPosID}</a:OperID>' \
           f'<a:UniqueID>{custcret[1]}</a:UniqueID><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/>' \
           f'<a:UpdtTime>{modifydatetime(custcret[2])}</a:UpdtTime><a:Address>{custcret[3]}</a:Address><a:AppSpID>{custcret[16]}</a:AppSpID>' \
           f'<a:Apper>{fullname}</a:Apper><a:AreaID>{custcret[4]}</a:AreaID><a:AreaName>{areaname}</a:AreaName>' \
           f'<a:Catg>2</a:Catg><a:CustBldID>{custcret[5]}</a:CustBldID><a:CustBldName>{bldname}</a:CustBldName><a:CustContactWay>{custcret[6]}</a:CustContactWay>' \
           f'<a:CustContactWays><a:SvcCustContactWay><a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{modifydatetime(contacts[0])}</a:CreTime><a:ID i:nil="true"/>' \
           f'<a:Oper i:nil="true"/><a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/><a:UpdtTime>{modifydatetime(contacts[1])}</a:UpdtTime>' \
           f'<a:Catg>1</a:Catg><a:CustID>{custcret[1]}</a:CustID><a:Sort>0</a:Sort>' \
           f'<a:Way>{custcret[6]}</a:Way></a:SvcCustContactWay></a:CustContactWays><a:CustDsgnID i:nil="true"/><a:CustDsgner/>' \
           f'<a:CustIntentID>{custcret[7]}</a:CustIntentID><a:CustIntentName>{indentname}</a:CustIntentName><a:CustLevelID>{custcret[8]}</a:CustLevelID>' \
           f'<a:CustLevelName>{levelname}</a:CustLevelName><a:CustName>{custname}</a:CustName><a:CustPersons><a:SvcCustPerson><a:CoID i:nil="true"/><a:CoName i:nil="true"/>' \
           f'<a:CreTime>{modifydatetime(custpers[4])}</a:CreTime><a:ID>{custpers[2]}</a:ID><a:Oper i:nil="true"/><a:OperID>{custpers[3]}</a:OperID>' \
           f'<a:UniqueID>{custpers[2]}</a:UniqueID><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/><a:UpdtTime>{modifydatetime(custpers[5])}</a:UpdtTime>' \
           f'<a:CustID>{custcret[1]}</a:CustID><a:DeptName i:nil="true"/><a:PersonCatg>7</a:PersonCatg><a:Ramark i:nil="true"/>' \
           f'<a:UserID>{custpers[0]}</a:UserID><a:UserName>{username}</a:UserName>' \
           f'<a:UserSpID>{custpers[1]}</a:UserSpID></a:SvcCustPerson></a:CustPersons><a:CustSourceID>{custcret[9]}</a:CustSourceID>' \
           f'<a:CustSourceName>{sourcename}</a:CustSourceName><a:CustTels i:nil="true"/><a:CustTelsAllStr>{custcret[6]}</a:CustTelsAllStr>' \
           f'<a:CustTelsList xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><b:string>{custcret[6]}</b:string></a:CustTelsList><a:CustTelsStr>{custcret[6]}</a:CustTelsStr>' \
           f'<a:CustomerHouseTypeID>{custcret[10]}</a:CustomerHouseTypeID><a:CustomerHouseTypeName>{housetypename}</a:CustomerHouseTypeName><a:DeptName i:nil="true"/>' \
           f'<a:HandInDate>{modifydatetime(custcret[11])}</a:HandInDate><a:HouseArea>130.00</a:HouseArea><a:HouseBuilding>11</a:HouseBuilding><a:HouseFloor>33</a:HouseFloor>' \
           f'<a:HouseNumber>44</a:HouseNumber><a:HouseType/><a:HouseTypeID>{custcret[12]}</a:HouseTypeID><a:HouseTypeName>{housetype}</a:HouseTypeName>' \
           '<a:HouseUnit>22</a:HouseUnit><a:IsAreaRepeat>false</a:IsAreaRepeat><a:NextFlwTime i:nil="true"/><a:NextFlwWayID i:nil="true"/><a:NextFlwWayName i:nil="true"/>' \
           f'<a:No>{custcret[13]}</a:No><a:Remark>客户说明内容</a:Remark><a:RepeatCatg>1</a:RepeatCatg><a:AgeGroupID>{custcret[14]}</a:AgeGroupID>' \
           f'<a:AssState>3</a:AssState><a:ChannelID>{custcret[15]}</a:ChannelID><a:ChannelName>{custchanel}</a:ChannelName><a:ConsultWayID i:nil="true"/>' \
           '<a:ConsultWayName i:nil="true"/><a:ContAddr i:nil="true"/><a:ContAmt i:nil="true"/><a:ContID i:nil="true"/><a:ContNo i:nil="true"/><a:ContProCatg>0</a:ContProCatg>' \
           '<a:ContState>0</a:ContState><a:DesignMode i:nil="true"/><a:DesignModeTxt/><a:DesnID i:nil="true"/><a:DesnName i:nil="true"/><a:ExtensionManDirectorName i:nil="true"/>' \
           '<a:FlwData i:nil="true"/><a:IsPayCust>false</a:IsPayCust><a:IsReceipt>true</a:IsReceipt><a:IsRepeat>false</a:IsRepeat><a:KeyWord i:nil="true"/>' \
           f'<a:MarketerID>{custpers[1]}</a:MarketerID><a:MatketerName>{marketname}</a:MatketerName><a:OperationManagerName i:nil="true"/><a:PMID i:nil="true"/>' \
           '<a:PMName i:nil="true"/><a:PromID i:nil="true"/><a:PromName i:nil="true"/><a:ServiceDirectorName i:nil="true"/><a:ServiceName i:nil="true"/><a:SiteID i:nil="true"/>' \
           f'<a:SiteName i:nil="true"/><a:SitePromName i:nil="true"/><a:SiteUrl i:nil="true"/><a:State>0</a:State></a:Cust><a:CustID>{custcret[1]}</a:CustID>' \
           f'<a:DeepeningDsgnName>{deepdsgn}</a:DeepeningDsgnName><a:DeepeningDsgnSpID>{deepid}</a:DeepeningDsgnSpID>' \
           '<a:DesignMode>cb7a33c5-f428-46f7-b96e-8b2baf4e90aa</a:DesignMode><a:DesignModeTxt i:nil="true"/><a:DsgnName i:nil="true"/><a:DsgnSpID i:nil="true"/>' \
           '<a:FinishTime i:nil="true"/><a:FlowState>1</a:FlowState><a:InvalidTime i:nil="true"/><a:MarkInvalidDate i:nil="true"/>' \
           f'<a:MeetDate>{modifydatetime("date")}+08:00</a:MeetDate><a:MeetingTypeID>d966474e-cba6-405b-85d8-a0ae064ff10f</a:MeetingTypeID><a:No i:nil="true"/><a:Remark/>' \
           f'<a:SchemeDsgnName>{schdsgn}</a:SchemeDsgnName>' \
           f'<a:SchemeDsgnSpID>{schid}</a:SchemeDsgnSpID><a:State>1</a:State><a:SubmitTime i:nil="true"/></custMeet></SaveCustMeet></s:Body></s:Envelope>'
    r = requests.post(url, headers=head, data=body.encode('utf-8'))
    if re.search("<a:IsSuccess.*?true</a:IsSuccess>", r.text, re.S):
        print(f"客户{custname}设计见面成功")
        relateid = re.search("ReturnData>(.*?)</a:ReturnData>", r.text).group(1)
        time.sleep(3)
    else:
        pprint.pprint(r.text)
        raise Exception("设计见面失败！")
    # 传递1
    chuandi_url = f'https://dv.lantingroup.cn:{port}/PC/Workflow/WorkflowService.svc'
    chuandi_head = {'Content-Type': 'text/xml; charset=utf-8',
                    'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                    'Host': f'dv.lantingroup.cn:{port}',
                    'Content-Length': '1344',
                    'Expect': '100-continue',
                    'Accept-Encoding': 'gzip, deflate'}
    chuandi_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
                   '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:BackNodeId i:nil="true"/>' \
                   '<a:Catg>1</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                   '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID i:nil="true"/>' \
                   '<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID i:nil="true"/>' \
                   f'<a:OperResult>2</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                   '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
    r12 = requests.post(chuandi_url, headers=chuandi_head, data=chuandi_body.encode('utf-8'))
    try:
        logid = re.search("<a:ReturnData>(.*?)</a:ReturnData>", r12.text, re.S).group(1)
    except AttributeError:
        print(r12.text)
        raise
    chuandi_head2 = {'Content-Type': 'text/xml; charset=utf-8',
                     'SOAPAction': '"http://tempuri.org/IWorkflow/SelectFlowLogDetail"',
                     'Host': f'dv.lantingroup.cn:{port}',
                     'Content-Length': '632',
                     'Expect': '100-continue',
                     'Accept-Encoding': 'gzip, deflate'}
    chuandi_body2 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectFlowLogDetail xmlns="http://tempuri.org/">{session}' \
                    f'<flowCatg>1</flowCatg><relateID>{relateid}</relateID></SelectFlowLogDetail></s:Body></s:Envelope>'
    r1 = requests.post(chuandi_url, headers=chuandi_head2, data=chuandi_body2.encode('utf-8'))
    nodelogid = re.search("<a:NodeLogs>.*?<a:ID>(.*?)</a:ID>", r1.text, re.S).group(1)
    time.sleep(1)
    # 传递2
    chuandi_head3 = {'Content-Type': 'text/xml; charset=utf-8',
                     'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                     'Host': f'dv.lantingroup.cn:{port}',
                     'Content-Length': '1412',
                     'Expect': '100-continue',
                     'Accept-Encoding': 'gzip, deflate',
                     'Connection': 'Keep-Alive'}
    chuandi_body3 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
                    '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                    '<a:BackNodeId i:nil="true"/><a:Catg>1</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                    f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
                    f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodelogid}</a:NodeLogID>' \
                    f'<a:OperResult>4</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                    '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
    requests.post(chuandi_url, headers=chuandi_head3, data=chuandi_body3.encode('utf-8'))


# 日期生成
def modifydatetime(*args, **kwargs):
    nowtime = datetime.datetime.now()
    if 'minutes' in kwargs:
        dt = nowtime + datetime.timedelta(minutes=kwargs['minutes'])
    elif 'days' in kwargs:
        dt = nowtime + datetime.timedelta(days=kwargs['days'])
    elif args[0] == 'date':
        dt = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")
    elif args[0] == 'now':
        dt = nowtime
    else:
        if '.' in str(args[0]):
            tt = datetime.datetime.strptime(str(args[0]), "%Y-%m-%d %H:%M:%S.%f")
            dt = str(tt)[:-3]
        else:
            dt = args[0]

    return str(dt).replace(' ', 'T')


def contstart():
    contid = ""
    startime = modifydatetime(days=2)
    house_id = SQL.housetypeid(contid)
    url = f'https://dv.lantingroup.cn:{port}/PC/ContStart/ContStartService.svc'
    conts_head = {'Content-Type': 'text/xml; charset=utf-8',
                  'SOAPAction': '"http://tempuri.org/IContStart/ContStartAdd"',
                  'Host': f'dv.lantingroup.cn:{port}',
                  'Content-Length': '1008',
                  'Expect': '100-continue',
                  'Accept-Encoding': 'gzip, deflate'}
    conts_body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartAdd xmlns="http://tempuri.org/">' \
                 '<session xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.UserRight" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                 '<a:LoginStafPosID>b9cfbec0-7a56-4506-838b-1b1028c187c4</a:LoginStafPosID><a:RegisterID i:nil="true"/><a:SessionID>c28aac98-d3be-4d42-ad6a-b6d14e9903e1</a:SessionID>' \
                 '<a:Sign i:nil="true"/><a:UniqueID>c28aac98-d3be-4d42-ad6a-b6d14e9903e1</a:UniqueID></session>' \
                 '<contStartAdd xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                 f'<a:AppSpID>b9cfbec0-7a56-4506-838b-1b1028c187c4</a:AppSpID><a:ContID>{contid}</a:ContID><a:ExpectStartTime>{startime}</a:ExpectStartTime>' \
                 f'<a:HouseTypeID>{house_id}</a:HouseTypeID><a:IsUrgent>false</a:IsUrgent><a:Remark/><a:SpaceDesignerSpId i:nil="true"/></contStartAdd></ContStartAdd>' \
                 '</s:Body></s:Envelope>'


# 合同登记
def contactadd(allname):
    areacode = random.randint(100, 9999999)
    for n in allname:
        builds = SQL.budid(n)
        a_time = modifydatetime('date')
        custs = SQL.custcretime(n)
        # discountid = SQL.discountid(builds[2])
        url = f'https://dv.lantingroup.cn:{port}/PC/Contract/ContService.svc'
        c_head = {'Content-Type': 'text/xml; charset=utf-8',
                  'SOAPAction': '"http://tempuri.org/IContract/ContractAdd"',
                  'Host': f'dv.lantingroup.cn:{port}',
                  'Content-Length': '2584',
                  'Expect': '100-continue',
                  'Accept-Encoding': 'gzip, deflate',
                  'Connection': 'Keep-Alive'}
        c_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContractAdd xmlns="http://tempuri.org/">{session}' \
                 '<contractAdd xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                 f'<a:AppSpID>{custs[16]}</a:AppSpID><a:AreaCode>{areacode}</a:AreaCode><a:AreaID>{builds[1]}</a:AreaID>' \
                 f'<a:BldID>{builds[0]}</a:BldID><a:CanWeekendConstruction>true</a:CanWeekendConstruction><a:ChannelID i:nil="true"/>' \
                 f'<a:CoID>{custs[18]}</a:CoID><a:CoTimeLimit>0</a:CoTimeLimit><a:ContractDiscountId i:nil="true"/><a:CustID>{builds[2]}</a:CustID>' \
                 f'<a:CustName>{n}</a:CustName><a:CustTel xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><b:string>{builds[3]}</b:string><b:string/>' \
                 f'<b:string/></a:CustTel><a:CustomeReceivedRatio>2</a:CustomeReceivedRatio><a:CustomerHouseTypeID>{builds[4]}</a:CustomerHouseTypeID><a:DecorStyleID>1eca43f3-6ef3-47b7-aec1-fab1a73a45fa</a:DecorStyleID>' \
                 f'<a:DesnID>8ca150bf-7cea-4d0a-a3c4-b650226c71b1</a:DesnID><a:ExpFrameDiagramDate>{a_time}+08:00</a:ExpFrameDiagramDate>' \
                 f'<a:ExpRenderPicDate>{a_time}+08:00</a:ExpRenderPicDate><a:ExpectGetDate>{a_time}+08:00</a:ExpectGetDate>' \
                 f'<a:ExpectStartDate>{a_time}+08:00</a:ExpectStartDate><a:GetDate>{a_time}+08:00</a:GetDate><a:HouseAddress>{builds[5]}</a:HouseAddress>' \
                 f'<a:HouseArea>{builds[6]}</a:HouseArea><a:HouseBuilding>11</a:HouseBuilding><a:HouseCatg>2</a:HouseCatg><a:HouseFloor>33</a:HouseFloor><a:HouseNumber>44</a:HouseNumber>' \
                 f'<a:HouseStructure>160aab3a-ed6e-455f-8687-1a7c1010f6c0</a:HouseStructure><a:HouseType/><a:HouseTypeID>{builds[7]}</a:HouseTypeID>' \
                 '<a:HouseUnit>22</a:HouseUnit><a:IsLoan>false</a:IsLoan><a:IsReceipt>false</a:IsReceipt><a:ModelRoomNo/>' \
                 '<a:OfferGoodsSetID>57e07cd1-481f-4204-855b-e331cfae3eef</a:OfferGoodsSetID><a:OfferTempID i:nil="true"/><a:PaymentStage>1</a:PaymentStage>' \
                 f'<a:ProCatg>0</a:ProCatg><a:Remark/><a:SignAmount>100000</a:SignAmount><a:SignDate>{a_time}+08:00</a:SignDate>' \
                 '<a:TimeLimit>3</a:TimeLimit></contractAdd></ContractAdd></s:Body></s:Envelope>'

        r = requests.post(url, headers=c_head, data=c_body.encode('utf-8'))

        if re.search("<a:IsSuccess>true</a:IsSuccess>", r.text, re.S):
            print(f"客户{n}合同登记成功")
            relateID = re.search("<a:ReturnData>(.*?)</a:ReturnData>", r.text, re.S).group(1)
        else:
            pprint.pprint(r.text)
            raise Exception("合同登记失败！")
        time.sleep(2)
        # 传递1
        url1 = f'https://dv.lantingroup.cn:{port}/PC/Workflow/WorkflowService.svc'
        head1 = {'Content-Type': 'text/xml; charset=utf-8',
                 'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                 'Host': f'dv.lantingroup.cn:{port}',
                 'Content-Length': '1344',
                 'Expect': '100-continue',
                 'Accept-Encoding': 'gzip, deflate',
                 'Connection': 'Keep-Alive'}
        body1 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
                '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                '<a:BackNodeId i:nil="true"/><a:Catg>2</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID i:nil="true"/>' \
                '<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID i:nil="true"/>' \
                f'<a:OperResult>2</a:OperResult><a:RelateID>{relateID}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
        r1 = requests.post(url1, headers=head1, data=body1.encode('utf-8'))
        logid = re.search("<a:ReturnData>(.*?)</a:ReturnData>", r1.text, re.S).group(1)
        head12 = {'Content-Type': 'text/xml; charset=utf-8',
                  'SOAPAction': '"http://tempuri.org/IWorkflow/SelectFlowLogDetail"',
                  'Host': f'dv.lantingroup.cn:{port}',
                  'Content-Length': '632',
                  'Expect': '100-continue',
                  'Accept-Encoding': 'gzip, deflate'}
        body12 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectFlowLogDetail xmlns="http://tempuri.org/">{session}' \
                 f'<flowCatg>2</flowCatg><relateID>{relateID}</relateID></SelectFlowLogDetail></s:Body></s:Envelope>'
        r12 = requests.post(url1, headers=head12, data=body12.encode('utf-8'))
        nodelogid = re.search("<a:NodeLogs>.*?<a:ID>(.*?)</a:ID>", r12.text, re.S).group(1)
        # 新建优惠单
        adddiscount(n)
        # 传递2
        head2 = {'Content-Type': 'text/xml; charset=utf-8',
                 'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                 'Host': f'dv.lantingroup.cn:{port}',
                 'Content-Length': '1412',
                 'Expect': '100-continue',
                 'Accept-Encoding': 'gzip, deflate',
                 'Connection': 'Keep-Alive'}
        body2 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
                '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                '<a:BackNodeId i:nil="true"/><a:Catg>2</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
                f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodelogid}</a:NodeLogID>' \
                f'<a:OperResult>4</a:OperResult><a:RelateID>{relateID}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
        requests.post(url1, headers=head2, data=body2.encode('utf-8'))
        r22 = requests.post(url1, headers=head12, data=body12.encode('utf-8'))
        nodelogid2 = re.search("<a:NodeLogs>.*?<a:ID>(.*?)</a:ID>", r22.text, re.S).group(1)
        # 传递3
        body3 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
                '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                '<a:BackNodeId i:nil="true"/><a:Catg>2</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
                f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodelogid2}</a:NodeLogID>' \
                f'<a:OperResult>4</a:OperResult><a:RelateID>{relateID}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
        requests.post(url1, headers=head2, data=body3.encode('utf-8'))


# 合同优惠登记
def adddiscount(na):
    cretime = modifydatetime('now')
    cretime2 = modifydatetime(minutes=2)
    contid = SQL.selectcontid(na)
    # try:
    #     contid = SQL.selectcontid(n)
    #     contword = f'<a:ContID>{contid}</a:ContID>'
    # except NameError as e:
    #     contword = '<a:ContID i:nil="true"/>'
    appspname = SQL.custfullname(LoginStafPosID)
    custid = SQL.customerid(na)
    if str(custid[1]) == '09a055c1-4885-47e7-a5ca-7066f16c4537':  # 岚庭家居
        discoutlist = '9566b79b-af4e-4865-a8cf-f64330a78a4f'
    elif str(custid[1]) == '8D92D6FB-C865-4A1F-B375-C0C24CD2DCF5':  # 湖北武汉岚庭
        discoutlist = 'e4dd23c9-bde3-4416-827b-e33d065f54c2'
    elif str(custid[1]) == 'c7cc5de4-efdd-4aa7-9615-7a748785be12':  # 幸福魔方
        discoutlist = 'c1f5447d-f35e-4ee7-b3ff-1460dcec55b5'
    else:
        print(str(custid[1]))
        raise Exception("这是啥公司的客户？")
    discs = SQL.discounts(discoutlist)
    prodname = SQL.prodname(discoutlist)
    company = SQL.logincompany(LoginStafPosID)
    # Amount = count*price chkamount = count*chkprice
    url = f'https://dv.lantingroup.cn:{port}/PC/DisCount/DisCountService.svc'
    d_data = {'Content-Type': 'text/xml; charset=utf-8',
              'SOAPAction': '"http://tempuri.org/IDiscount/AddDiscount"',
              'Host': f'dv.lantingroup.cn:{port}',
              'Content-Length': '4155',
              'Expect': '100-continue',
              'Accept-Encoding': 'gzip, deflate',
              'Connection': 'Keep-Alive'}
    d_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><AddDiscount xmlns="http://tempuri.org/">{session}<discount xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:CoID>{custid[1]}</a:CoID><a:CoName>{company}</a:CoName><a:CreTime>{cretime}+08:00</a:CreTime><a:ID i:nil="true"/><a:Oper i:nil="true"/><a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/><a:UpdtTime>{cretime}+08:00</a:UpdtTime><a:AppSpID>{LoginStafPosID}</a:AppSpID><a:AppSpName>{appspname[0]}</a:AppSpName><a:Attach i:nil="true"/><a:BudgetID i:nil="true"/><a:BudgetName i:nil="true"/><a:FinishTime i:nil="true"/><a:FlowState>1</a:FlowState><a:FlowStateTxt>待提交</a:FlowStateTxt><a:IsChkBefore>false</a:IsChkBefore><a:No i:nil="true"/><a:Remark/><a:State>1</a:State><a:StateTxt i:nil="true"/><a:SubmitTime i:nil="true"/><a:ApplyDiscDetls i:nil="true"/><a:BldName i:nil="true"/><a:ChkAmount>{discs[3] * discs[4]}</a:ChkAmount><a:ChkRemark i:nil="true"/><a:CoDiscDetls i:nil="true"/><a:ContAddr i:nil="true"/><a:ContAmt i:nil="true"/><a:ContDept i:nil="true"/><a:ContID>{contid}</a:ContID><a:ContInfo i:nil="true"/><a:ContNo i:nil="true"/><a:CouponDiscDetls i:nil="true"/><a:CustName i:nil="true"/><a:CustNo i:nil="true"/><a:CustSource i:nil="true"/><a:CustState>0</a:CustState><a:CustTel i:nil="true"/><a:CustTels i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:CustTelsList i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:DesnName i:nil="true"/><a:DiscAmount>1.00</a:DiscAmount><a:DiscDetls><a:SvcDiscDetl><a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{cretime2}+08:00</a:CreTime><a:ID i:nil="true"/><a:Oper i:nil="true"/><a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/><a:UpdtTime>{cretime2}+08:00</a:UpdtTime><a:Amount>{discs[2] * discs[4]}</a:Amount><a:BackCount>0</a:BackCount><a:ChkAmount>{discs[3] * discs[4]}</a:ChkAmount><a:ChkPrice>{discs[3]}</a:ChkPrice><a:ChkRemark i:nil="true"/><a:Content>{discs[1]}</a:Content><a:Count>{discs[4]}</a:Count><a:Counted>0</a:Counted><a:CustAreaName i:nil="true"/><a:CustBldName i:nil="true"/><a:CustID i:nil="true"/><a:CustName i:nil="true"/><a:CustNo i:nil="true"/><a:CustSource i:nil="true"/><a:CustState>0</a:CustState><a:CustTel i:nil="true"/><a:DiscId i:nil="true"/><a:DiscItemID>9566b79b-af4e-4865-a8cf-f64330a78a4f</a:DiscItemID><a:DiscNo i:nil="true"/><a:DiscType>1</a:DiscType><a:FactCount>0</a:FactCount><a:IsChange>false</a:IsChange><a:IsEnjoy>true</a:IsEnjoy><a:IsOut>false</a:IsOut><a:Name>{discs[0]}</a:Name><a:Price>{discs[2]}</a:Price><a:ProdCatg>{prodname[1]}</a:ProdCatg><a:ProdDesc i:nil="true"/><a:ProdID i:nil="true"/><a:ProdModel i:nil="true"/><a:ProdName>{prodname[0]}</a:ProdName><a:ProdNo i:nil="true"/><a:ProdSpec i:nil="true"/><a:ProdUnit i:nil="true"/><a:Remark i:nil="true"/><a:State>0</a:State><a:StockCount>0</a:StockCount><a:StockID i:nil="true"/><a:StockName i:nil="true"/><a:StockStateName i:nil="true"/><a:Subject i:nil="true"/><a:TheoryChkAmount>0</a:TheoryChkAmount></a:SvcDiscDetl></a:DiscDetls><a:DiscSetID>{discs[5]}</a:DiscSetID><a:DiscSetName i:nil="true"/><a:IsAlterSignTxt i:nil="true"/><a:IsCheck i:nil="true"/><a:LiveDiscDetls i:nil="true"/><a:MeetCustID>{custid[0]}</a:MeetCustID><a:OfferAmt>0</a:OfferAmt><a:ProductType>0</a:ProductType><a:SignDate i:nil="true"/></discount></AddDiscount></s:Body></s:Envelope>'
    r = requests.post(url, headers=d_data, data=d_body.encode('utf-8'))

    if re.search("<IsSuccess.*?true</IsSuccess>", r.text, re.S):
        print(f"客户{na}优惠登记成功")
        relateid = re.search("<a:ID>(.*?)</a:ID>", r.text, re.S).group(1)
    elif re.search(".*?已被其它优惠单", r.text, re.S):
        pass
    else:
        pprint.pprint(r.text)
        raise Exception("合同优惠登记失败！")
    # 传递1
    c_url = 'https://dv.lantingroup.cn:8075/PC/Workflow/WorkflowService.svc'
    c_head = {'Content-Type': 'text/xml; charset=utf-8',
              'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
              'Host': f'dv.lantingroup.cn:{port}',
              'Content-Length': '1345',
              'Expect': '100-continue',
              'Accept-Encoding': 'gzip, deflate',
              'Connection': 'Keep-Alive'}
    c_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
             '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
             '<a:BackNodeId i:nil="true"/><a:Catg>54</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
             '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID i:nil="true"/>' \
             '<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID i:nil="true"/><a:OperResult>2</a:OperResult>' \
             f'<a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
             '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
    r1 = requests.post(c_url, headers=c_head, data=c_body.encode('utf-8'))
    logid = re.search("<a:ReturnData>(.*?)</a:ReturnData>", r1.text, re.S).group(1)
    c_head1 = {'Content-Type': 'text/xml; charset=utf-8',
               'SOAPAction': '"http://tempuri.org/IWorkflow/SelectFlowLogDetail"',
               'Host': 'dv.lantingroup.cn:8075',
               'Content-Length': '633',
               'Expect': '100-continue',
               'Accept-Encoding': 'gzip, deflate'}
    c_body1 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectFlowLogDetail xmlns="http://tempuri.org/">{session}' \
              f'<flowCatg>54</flowCatg><relateID>{relateid}</relateID></SelectFlowLogDetail></s:Body></s:Envelope>'
    r2 = requests.post(c_url, headers=c_head1, data=c_body1.encode('utf-8'))
    nodelogid = re.search("<a:NodeLogs>.*?<a:ID>(.*?)</a:ID>", r2.text, re.S).group(1)
    # 传递2
    c_head2 = {'Content-Type': 'text/xml; charset=utf-8',
               'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
               'Host': f'dv.lantingroup.cn:{port}',
               'Content-Length': '1413',
               'Expect': '100-continue',
               'Accept-Encoding': 'gzip, deflate',
               'Connection': 'Keep-Alive'}
    c_body2 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
              '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
              '<a:BackNodeId i:nil="true"/><a:Catg>54</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
              f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
              f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodelogid}</a:NodeLogID>' \
              f'<a:OperResult>4</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
              '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
    requests.post(c_url, headers=c_head2, data=c_body2.encode('utf-8'))


# 开工预案申请
def contstartplanadd(names):
    for n in names:
        contid = SQL.selectcontid(n)
        handtime = modifydatetime(minutes=60)
        opers = SQL.getopers(LoginStafPosID)
        session1 = '<request xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:CustomParas i:nil="true"/>' \
                   '<a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight">' \
                   f'<b:LoginStafPosID>{LoginStafPosID}</b:LoginStafPosID><b:RegisterID i:nil="true"/><b:SessionID>{SessionID}</b:SessionID>' \
                   f'<b:Sign i:nil="true"/><b:UniqueID>{UniqueID}</b:UniqueID></a:Session>'
        url = f'https://dv.lantingroup.cn:{port}/PC/ContStart/ContStartService.svc'
        head = {'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': '"http://tempuri.org/IContStartPlan/ContStartPlanAdd"',
                'Host': f'dv.lantingroup.cn:{port}',
                'Content-Length': '1188',
                'Expect': '100-continue',
                'Accept-Encoding': 'gzip, deflate'}
        body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartPlanAdd xmlns="http://tempuri.org/">' \
               f'{session1}<a:Data><a:AppSpID>{LoginStafPosID}</a:AppSpID>' \
               f'<a:BudgeterId i:nil="true"/><a:ContID>{contid}</a:ContID><a:FloorNum>0</a:FloorNum><a:HandoverOfficerID i:nil="true"/>' \
               f'<a:HandoverTime>{handtime}+08:00</a:HandoverTime><a:HouseTypeID i:nil="true"/><a:IsSubCont i:nil="true"/><a:PMDptMgrID i:nil="true"/><a:PMID i:nil="true"/>' \
               '<a:PlanRemark/><a:SpaceDesignerSpId i:nil="true"/><a:SupervisorID i:nil="true"/></a:Data></request></ContStartPlanAdd></s:Body></s:Envelope>'
        r = requests.post(url, headers=head, data=body.encode('utf-8'))
        if re.search("<IsSuccess.*?true</IsSuccess>", r.text, re.S):
            print(f"客户{n}开工预案申请保存成功")
            idd = re.search("<ReturnData.*?>(.*?)</ReturnData>", r.text, re.S).group(1)
        else:
            pprint.pprint(r.text)
            continue
        head2 = {'Content-Type': 'text/xml; charset=utf-8',
                 'SOAPAction': '"http://tempuri.org/IContStartPlan/ContStartPlanSelectSingle"',
                 'Host': f'dv.lantingroup.cn:{port}',
                 'Content-Length': '831',
                 'Expect': '100-continue',
                 'Accept-Encoding': 'gzip, deflate'}
        body2 = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartPlanSelectSingle xmlns="http://tempuri.org/">' \
                '<input xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                '<a:CustomParas i:nil="true"/><a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight">' \
                f'<b:LoginStafPosID>{LoginStafPosID}</b:LoginStafPosID><b:RegisterID i:nil="true"/>' \
                f'<b:SessionID>{SessionID}</b:SessionID><b:Sign i:nil="true"/><b:UniqueID>{UniqueID}</b:UniqueID></a:Session>' \
                f'<a:ID i:nil="true"/><a:ContStartPlanId>{idd}</a:ContStartPlanId></input></ContStartPlanSelectSingle></s:Body></s:Envelope>'
        # BudgeterId 预算员 7d64e453-eb73-4d17-871e-b62c0091992c（岚庭家居）
        r = requests.post(url, headers=head2, data=body2.encode('utf-8'))

        ids = re.search(
            "<a:ContStartPlanFattaList>.*?<a:ID>(.*?)</a:ID>.*?<a:ID>(.*?)</a:ID>.*?</a:ContStartPlanFattaList>",
            r.text, re.S)
        id1 = ids.group(1)
        id2 = ids.group(2)
        updatetime = modifydatetime('now')
        # 传递1
        c_head1 = {'Content-Type': 'text/xml; charset=utf-8',
                   'SOAPAction': '"http://tempuri.org/IContStartPlan/ContStartPlanEdit"',
                   'Host': f'dv.lantingroup.cn:{port}',
                   'Content-Length': '2718',
                   'Expect': '100-continue',
                   'Accept-Encoding': 'gzip, deflate'}
        c_body1 = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartPlanEdit xmlns="http://tempuri.org/">' \
                  f'{session1}<a:Data><a:AppSpID>{LoginStafPosID}</a:AppSpID>' \
                  f'<a:BudgeterId i:nil="true"/><a:ContID>{contid}</a:ContID><a:FloorNum>3</a:FloorNum><a:HandoverOfficerID i:nil="true"/>' \
                  f'<a:HandoverTime>{handtime}</a:HandoverTime><a:HouseTypeID>60d4f93b-82fb-4d76-afdb-f514c46899f1</a:HouseTypeID><a:IsSubCont i:nil="true"/>' \
                  '<a:PMDptMgrID i:nil="true"/><a:PMID i:nil="true"/><a:PlanRemark/><a:SpaceDesignerSpId i:nil="true"/><a:SupervisorID i:nil="true"/><a:ContStartPlanFattaList>' \
                  f'<a:SvcContStartPlanFatta><a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{updatetime}</a:CreTime><a:ID>{id1}</a:ID>' \
                  f'<a:Oper>{opers[1]}</a:Oper><a:OperID>{LoginStafPosID}</a:OperID><a:UniqueID>{id1}</a:UniqueID><a:UpdtOper/>' \
                  f'<a:UpdtOperId i:nil="true"/><a:UpdtTime>{updatetime}</a:UpdtTime><a:ContStartPlanID i:nil="true"/><a:DownLoadText>下载</a:DownLoadText><a:FattaNum>0</a:FattaNum>' \
                  '<a:FattaType>2</a:FattaType><a:FattaTypeName>CAD图纸</a:FattaTypeName><a:Images i:nil="true"/><a:Remark i:nil="true"/><a:UpdtTimeTxt/>' \
                  '<a:UploadText>上传</a:UploadText></a:SvcContStartPlanFatta><a:SvcContStartPlanFatta><a:CoID i:nil="true"/><a:CoName i:nil="true"/>' \
                  f'<a:CreTime>{updatetime}</a:CreTime><a:ID>{id2}</a:ID><a:Oper>{opers[1]}</a:Oper>' \
                  f'<a:OperID>{LoginStafPosID}</a:OperID><a:UniqueID>{id2}</a:UniqueID><a:UpdtOper/><a:UpdtOperId i:nil="true"/>' \
                  f'<a:UpdtTime>{updatetime}</a:UpdtTime><a:ContStartPlanID i:nil="true"/><a:DownLoadText>下载</a:DownLoadText><a:FattaNum>0</a:FattaNum><a:FattaType>1</a:FattaType>' \
                  '<a:FattaTypeName>开工交底单</a:FattaTypeName><a:Images i:nil="true"/><a:Remark i:nil="true"/><a:UpdtTimeTxt/><a:UploadText>上传</a:UploadText></a:SvcContStartPlanFatta>' \
                  f'</a:ContStartPlanFattaList><a:ID>{idd}</a:ID></a:Data></request></ContStartPlanEdit></s:Body></s:Envelope>'
        requests.post(url, headers=c_head1, data=c_body1.encode('utf-8'))
        flow_url = f'https://dv.lantingroup.cn:{port}/PC/Workflow/WorkflowService.svc'
        c_head12 = {'Content-Type': 'text/xml; charset=utf-8',
                    'SOAPAction': '"http://tempuri.org/IWorkflow/SelectFlowLogDetail"',
                    'Host': f'dv.lantingroup.cn:{port}',
                    'Content-Length': '634',
                    'Expect': '100-continue',
                    'Accept-Encoding': 'gzip, deflate'
                    }
        c_body12 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectFlowLogDetail xmlns="http://tempuri.org/">{session}' \
                   f'<flowCatg>406</flowCatg><relateID>{idd}</relateID></SelectFlowLogDetail></s:Body></s:Envelope>'
        requests.post(flow_url, headers=c_head12, data=c_body12.encode('utf-8'))
        c_head13 = c_head12.copy()
        c_head13['SOAPAction'] = '"http://tempuri.org/IWorkflowBase/FlowOper"'
        c_head13['Content-Length'] = '1346'
        c_body13 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
                   '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                   '<a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                   '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID i:nil="true"/>' \
                   '<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID i:nil="true"/><a:OperResult>2</a:OperResult>' \
                   f'<a:RelateID>{idd}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                   '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
        requests.post(flow_url, headers=c_head13, data=c_body13.encode('utf-8'))
        r1 = requests.post(flow_url, headers=c_head12, data=c_body12.encode('utf-8'))
        logids = re.search("<a:FlowLog>.*?<a:ID>(.*?)</a:ID>.*?<a:NodeLogs>.*?<a:ID>(.*?)</a:ID>", r1.text, re.S)
        logid = logids.group(1)
        nodeid = logids.group(2)
        ht = int(time.mktime(time.strptime(handtime.replace("T", ' ')[:-7], "%Y-%m-%d %H:%M:%S"))) * 1000
        ht2 = int(time.mktime(time.strptime(updatetime.replace("T", ' ')[:-7], "%Y-%m-%d %H:%M:%S"))) * 1000
        # 传递2 HandoverOfficerID:工地交接员
        taskdata = '{'+f'"AppSpID":"{LoginStafPosID}","BudgeterId":null,"ContID":"{contid}","FloorNum":3,"HandoverOfficerID":"19e04347-872b-46c4-b3ba-338f71c51c67",' \
                   f'"HandoverTime":"\/Date({ht}+0800)\/","HouseTypeID":"60d4f93b-82fb-4d76-afdb-f514c46899f1","IsSubCont":true,"PMDptMgrID":null,"PMID":null,' \
                   f'"PlanRemark":"","SpaceDesignerSpId":null,"SupervisorID":null,"ContStartPlanFattaList":['+'{'+f'"CoID":null,"CoName":null,"CreTime":"\/Date({ht2}+0800)\/",' \
                   f'"ID":"{id1}","Oper":"{opers[1]}","OperID":"{LoginStafPosID}","UniqueID":"{id1}","UpdtOper":"","UpdtOperId":null,"UpdtTime":"\/Date({ht2}+0800)\/",' \
                   f'"ContStartPlanID":null,"DownLoadText":"下载","FattaNum":0,"FattaType":2,"FattaTypeName":"CAD图纸","Images":null,"Remark":null,"UpdtTimeTxt":"",' \
                   f'"UploadText":"上传"'+'},{'+f'"CoID":null,"CoName":null,"CreTime":"\/Date({ht2}+0800)\/","ID":"{id2}","Oper":"{opers[1]}","OperID":"{LoginStafPosID}",' \
                   f'"UniqueID":"{id2}","UpdtOper":"","UpdtOperId":null,"UpdtTime":"\/Date({ht2}+0800)\/","ContStartPlanID":null,"DownLoadText":"下载","FattaNum":0,' \
                   f'"FattaType":1,"FattaTypeName":"开工交底单","Images":null,"Remark":null,"UpdtTimeTxt":"","UploadText":"上传"'+'}'+f'],"ID":"{idd}"'+'}'
        c_head2 = {'Content-Type': 'text/xml;charset=utf-8',
                   'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                   'Host': f'dv.lantingroup.cn:{port}',
                   'Content-Length': '2847',
                   'Expect': '100-continue',
                   'Accept-Encoding': 'gzip, deflate'
                   }
        c_body2 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
                  '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                  '<a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                  '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc i:nil="true"/>' \
                  f'<a:LogID>{logid}</a:LogID><a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/>' \
                  f'<a:NodeLogID>{nodeid}</a:NodeLogID><a:OperResult>0</a:OperResult><a:RelateID>{idd}</a:RelateID>' \
                  f'<a:Summary i:nil="true"/><a:TaskDataStr>{taskdata}</a:TaskDataStr><a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                  '<a:Urgency>0</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
        requests.post(flow_url, headers=c_head2, data=c_body2.encode('utf-8'))
        c_head13['Content-Length'] = '1414' # 借用c_head13
        c_body21 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
                   '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                   '<a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                   f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
                   f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodeid}</a:NodeLogID>' \
                   f'<a:OperResult>4</a:OperResult><a:RelateID>{idd}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                   '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'

        requests.post(flow_url, headers=c_head13, data=c_body21.encode('utf-8'))
        # 传递3 分配质检员
        taskdata = '{' + f'"AppSpID":"{LoginStafPosID}","BudgeterId":null,"ContID":"{contid}","FloorNum":3,"HandoverOfficerID":"19e04347-872b-46c4-b3ba-338f71c51c67",' \
                    f'"HandoverTime":"\/Date({ht}+0800)\/","HouseTypeID":"60d4f93b-82fb-4d76-afdb-f514c46899f1","IsSubCont":true,"PMDptMgrID":null,"PMID":null,' \
                    f'"PlanRemark":"","SpaceDesignerSpId":null,"SupervisorID":"2919193d-e6e0-4c06-8789-5070b2040d9c","ContStartPlanFattaList":[' + '{' + f'"CoID":null,"CoName":null,"CreTime":"\/Date({ht2}+0800)\/",' \
                    f'"ID":"{id1}","Oper":"{opers[1]}","OperID":"{LoginStafPosID}","UniqueID":"{id1}","UpdtOper":"","UpdtOperId":null,"UpdtTime":"\/Date({ht2}+0800)\/",' \
                    f'"ContStartPlanID":null,"DownLoadText":"下载","FattaNum":0,"FattaType":2,"FattaTypeName":"CAD图纸","Images":null,"Remark":null,"UpdtTimeTxt":"",' \
                    f'"UploadText":"上传"' + '},{' + f'"CoID":null,"CoName":null,"CreTime":"\/Date({ht2}+0800)\/","ID":"{id2}","Oper":"{opers[1]}","OperID":"{LoginStafPosID}",' \
                    f'"UniqueID":"{id2}","UpdtOper":"","UpdtOperId":null,"UpdtTime":"\/Date({ht2}+0800)\/","ContStartPlanID":null,"DownLoadText":"下载","FattaNum":0,' \
                    f'"FattaType":1,"FattaTypeName":"开工交底单","Images":null,"Remark":null,"UpdtTimeTxt":"","UploadText":"上传"' + '}' + f'],"ID":"{idd}"' + '}'
        c_head3 = {'Content-Type': 'text/xml;charset=utf-8',
                   'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                   'Host': f'dv.lantingroup.cn:{port}',
                   'Content-Length': '2881',
                   'Expect': '100-continue',
                   'Accept-Encoding': 'gzip, deflate',
                   'Connection': 'Keep-Alive'
                   }
        c_body3 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
                  '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                  '<a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                  '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc i:nil="true"/>' \
                  f'<a:LogID>{logid}</a:LogID><a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/>' \
                  f'<a:NodeLogID>{nodeid}</a:NodeLogID><a:OperResult>0</a:OperResult><a:RelateID>{idd}</a:RelateID>' \
                  f'<a:Summary i:nil="true"/><a:TaskDataStr>{taskdata}</a:TaskDataStr><a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                  '<a:Urgency>0</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
        # 保存
        requests.post(flow_url, headers=c_head3, data=c_body3.encode('utf-8'))
        # 传递（同传递2）
        requests.post(flow_url, headers=c_head13, data=c_body21.encode('utf-8'))
        # 传递4（上传文件）


        # if re.search("<IsSuccess.*?true</IsSuccess>", r.text, re.S):
        #     print(f"客户{n}开工预案保存成功")
        # else:
        #     pprint.pprint(r.text)


# 登录
def login():
    login_url = f'https://dv.lantingroup.cn:{port}/PC/General/GeneralService.svc'
    login_head = {'Content-Type': 'text/xml; charset=utf-8',
                  'SOAPAction': '"http://tempuri.org/IGeneral/GeneralLogin"',
                  'Host': f'dv.lantingroup.cn:{port}',
                  'Content-Length': '921',
                  'Expect': '100-continue',
                  'Accept-Encoding': 'gzip, deflate'}
    login_body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><GeneralLogin xmlns="http://tempuri.org/">' \
                 '<request xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                 '<a:CustomParas i:nil="true"/><a:CustomParasDataFormat>0</a:CustomParasDataFormat>' \
                 '<a:Session i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight"/><a:ClientInfo xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data">' \
                 '<b:DeviceName>DESKTOP-74B6VCF</b:DeviceName><b:DeviceTag>BFEBFBFF000506E3</b:DeviceTag><b:IP>10.10.55.82</b:IP><b:Mac>70:4D:7B:64:69:33</b:Mac>' \
                 '<b:OS>Microsoft Windows NT 6.2.9200.0</b:OS></a:ClientInfo><a:Password>e68fea592aa34f5901b4ffeeac07ea53</a:Password><a:PhoneCode i:nil="true"/><a:PhoneNum i:nil="true"/>' \
                 '<a:UserName>01210281</a:UserName><a:VersionCode>16</a:VersionCode></request></GeneralLogin></s:Body></s:Envelope>'
    response = requests.post(login_url, headers=login_head, data=login_body.encode('utf-8'))
    context = re.search("<b:SessionID>(.*?)</b:SessionID>.*?<b:UserPos>.*?<b:ID>(.*?)</b:ID>", response.text, re.S)
    sessionid = context.group(1)
    loginid = context.group(2)
    print(sessionid, loginid)
    role_url = f'https://dv.lantingroup.cn:{port}/PC/General/GeneralService.svc'
    role_head = {'Content-Type': 'text/xml; charset=utf-8',
                 'SOAPAction': '"http://tempuri.org/IGeneral/GetUserRole"',
                 'Host': f'dv.lantingroup.cn:{port}',
                 'Content-Length': '712',
                 'Expect': '100-continue',
                 'Accept-Encoding': 'gzip, deflate'}
    role_body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><GetUserRole xmlns="http://tempuri.org/">' \
                '<request xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                '<a:CustomParas i:nil="true"/><a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight">' \
                f'<b:LoginStafPosID>{LoginStafPosID}</b:LoginStafPosID><b:RegisterID i:nil="true"/><b:SessionID>{sessionid}</b:SessionID>' \
                f'<b:Sign i:nil="true"/><b:UniqueID>{sessionid}</b:UniqueID></a:Session></request></GetUserRole></s:Body></s:Envelope>'
    requests.post(role_url, headers=role_head, data=role_body.encode('utf-8'))
    return sessionid


# 设计积分取消
def designintegralcancel(jfd, session, LoginStafPosID, SessionID, port):
    dsgnintegralid = SQL.degnintegralid(jfd)
    cretime = modifydatetime('now')
    url = f'https://dv.lantingroup.cn:{port}/PC/DsgnManagement/DsgnManagementService.svc'
    head = {'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': '"http://tempuri.org/IDesignIntegralCanel/AddDesignIntegralCanel"',
            'Host': f'dv.lantingroup.cn:{port}',
            'Content-Length': '1818',
            'Expect': '100-continue',
            'Accept-Encoding': 'gzip, deflate'}
    body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><AddDesignIntegralCanel xmlns="http://tempuri.org/">' \
           '<request xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
           '<a:CustomParas i:nil="true"/><a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight">' \
           f'<b:LoginStafPosID>{LoginStafPosID}</b:LoginStafPosID><b:RegisterID i:nil="true"/><b:SessionID>{SessionID}</b:SessionID>' \
           f'<b:Sign i:nil="true"/><b:UniqueID>{SessionID}</b:UniqueID></a:Session>' \
           f'<a:Data><a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{cretime}+08:00</a:CreTime><a:ID i:nil="true"/><a:Oper i:nil="true"/>' \
           f'<a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/><a:UpdtTime>{cretime}+08:00</a:UpdtTime>' \
           '<a:AppSpID i:nil="true"/><a:AppSpName i:nil="true"/><a:Attach i:nil="true"/><a:BudgetID i:nil="true"/><a:BudgetName i:nil="true"/><a:FinishTime i:nil="true"/>' \
           '<a:FlowState>1</a:FlowState><a:FlowStateTxt>待提交</a:FlowStateTxt><a:No i:nil="true"/><a:Remark i:nil="true"/><a:State>0</a:State><a:StateTxt i:nil="true"/>' \
           f'<a:SubmitTime i:nil="true"/><a:CanelReason>积分取消原因</a:CanelReason><a:Company i:nil="true"/><a:Department i:nil="true"/><a:DsgnBillNo>{jfd}</a:DsgnBillNo>' \
           f'<a:DsgnIntegralID>{dsgnintegralid}</a:DsgnIntegralID><a:IntegralTypeTxt i:nil="true"/><a:IntegralVal>0</a:IntegralVal><a:Postion i:nil="true"/>' \
           '<a:StaffName i:nil="true"/><a:StaffNo i:nil="true"/><a:Staffstate>0</a:Staffstate><a:TypeID i:nil="true"/></a:Data></request></AddDesignIntegralCanel></s:Body></s:Envelope>'
    r = requests.post(url, headers=head, data=body.encode('utf-8'))

    if re.search("<IsSuccess.*?true</IsSuccess>", r.text, re.S):
        print(f"客户{jfd}设计积分取消保存成功")
        relateid = re.search("<ReturnData.*?>(.*?)</ReturnData>", r.text, re.S).group(1)
    else:
        pprint.pprint(r.text)
        raise Exception("设计积分取消保存失败！")
    # 保存后第一次传递
    c_url = f'https://dv.lantingroup.cn:{port}/PC/Workflow/WorkflowService.svc'
    c_head = {'Content-Type': 'text/xml; charset=utf-8',
              'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
              'Host': 'dv.lantingroup.cn:8075',
              'Content-Length': '1346',
              'Expect': '100-continue',
              'Accept-Encoding': 'gzip, deflate',
              'Connection': 'Keep-Alive'}
    c_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
             '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
             '<a:BackNodeId i:nil="true"/><a:Catg>317</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
             '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID i:nil="true"/>' \
             '<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID i:nil="true"/><a:OperResult>2</a:OperResult>' \
             f'<a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
             '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
    r1 = requests.post(c_url, headers=c_head, data=c_body.encode('utf-8'))
    logid = re.search("<a:ReturnData>(.*?)</a:ReturnData>", r1.text, re.S).group(1)
    # 获取第二次传递所需要的一些ID
    c_head1 = {'Content-Type': 'text/xml; charset=utf-8',
               'SOAPAction': '"http://tempuri.org/IWorkflow/SelectFlowLogDetail"',
               'Host': 'dv.lantingroup.cn:8075',
               'Content-Length': '634',
               'Expect': '100-continue',
               'Accept-Encoding': 'gzip, deflate'}
    c_body1 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectFlowLogDetail xmlns="http://tempuri.org/">{session}' \
              f'<flowCatg>317</flowCatg><relateID>{relateid}</relateID></SelectFlowLogDetail></s:Body></s:Envelope>'

    r2 = requests.post(c_url, headers=c_head1, data=c_body1.encode('utf-8'))
    nodelogid = re.search("<a:NodeLogs>.*?<a:ID>(.*?)</a:ID>", r2.text, re.S).group(1)
    # 第二次传递
    c2_head = {'Content-Type': 'text/xml; charset=utf-8',
               'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
               'Host': f'dv.lantingroup.cn:{port}',
               'Content-Length': '1414',
               'Expect': '100-continue',
               'Accept-Encoding': 'gzip, deflate',
               'Connection': 'Keep-Alive'}
    c2_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
              '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
              '<a:BackNodeId i:nil="true"/><a:Catg>317</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
              f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
              f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodelogid}</a:NodeLogID>' \
              f'<a:OperResult>4</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
              '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
    requests.post(c_url, headers=c2_head, data=c2_body.encode('utf-8'))
    # 获取第三次传递需要的一些ID
    c2_body2 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectFlowLogDetail xmlns="http://tempuri.org/">{session}' \
               f'<flowCatg>317</flowCatg><relateID>{relateid}</relateID></SelectFlowLogDetail></s:Body></s:Envelope>'
    r3 = requests.post(c_url, headers=c_head1, data=c2_body2.encode('utf-8'))
    nodelogid2 = re.search("<a:NodeLogs>.*?<a:ID>(.*?)</a:ID>", r3.text, re.S).group(1)
    # 第三次传递
    c3_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}' \
              '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
              '<a:BackNodeId i:nil="true"/><a:Catg>317</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
              f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
              f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodelogid2}</a:NodeLogID>' \
              f'<a:OperResult>4</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
              '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
    requests.post(c_url, headers=c2_head, data=c3_body.encode('utf-8'))


# 新建工作联络单
def creatliaison():
    cretime = modifydatetime('now')
    requirdate = modifydatetime('date')
    posid = "8ca150bf-7cea-4d0a-a3c4-b650226c71b1"  # SQL.liaisondsgnid()
    liaisontype = SQL.liaisontype()
    appspname = SQL.getopers(LoginStafPosID)
    try:
        conts = SQL.getdsgncont(posid)
        contid = '>' + str(conts[1]) + '</a:ContID>'
        contno = '>' + conts[0] + '</a:ContNo>'
    except NameError:
        contid = ' i:nil="true"/>'
        contno = ' i:nil="true"/>'

    url = 'https://dv.lantingroup.cn:8075/PC/MyWork/Liaison/LiaisonService.svc'
    head = {'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': '"http://tempuri.org/ILiaison/AddLiaison"',
            'Host': 'dv.lantingroup.cn:8075',
            'Content-Length': '1918',
            'Expect': '100-continue',
            'Accept-Encoding': 'gzip, deflate'}
    body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><AddLiaison xmlns="http://tempuri.org/">{session}' \
           '<liaison xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
           f'<a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{cretime}+08:00</a:CreTime><a:ID i:nil="true"/><a:Oper i:nil="true"/>' \
           f'<a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/><a:UpdtTime>{cretime}+08:00</a:UpdtTime>' \
           f'<a:ActualDate i:nil="true"/><a:AppSpID>{LoginStafPosID}</a:AppSpID><a:AppSpName>{appspname[1]}</a:AppSpName><a:Attach/><a:ContAddr i:nil="true"/>' \
           f'<a:ContID{contid}<a:ContNo{contno}<a:ContStartDate i:nil="true"/><a:ContState>0</a:ContState><a:Content>联络原因</a:Content><a:Customer i:nil="true"/>' \
           '<a:CustomerTel i:nil="true"/><a:Dsgner i:nil="true"/><a:DsgnerID i:nil="true"/><a:FlowState>1</a:FlowState><a:IsPenalty>false</a:IsPenalty>' \
           f'<a:IsTimeout>false</a:IsTimeout><a:LiaisonSpID>{posid}</a:LiaisonSpID><a:LiaisonSpName i:nil="true"/><a:No i:nil="true"/>' \
           '<a:OverTimeDays>0</a:OverTimeDays><a:OverTimeStateTxt i:nil="true"/><a:PM i:nil="true"/><a:PMID i:nil="true"/><a:ReplyContent i:nil="true"/><a:ReplyTime i:nil="true"/>' \
           f'<a:RequiredDate>{requirdate}</a:RequiredDate><a:State>1</a:State><a:TypeID>{liaisontype}</a:TypeID><a:TypeName i:nil="true"/>' \
           '</liaison></AddLiaison></s:Body></s:Envelope>'
    r = requests.post(url, headers=head, data=body.encode('utf-8'))
    if re.search("<a:IsSuccess>true</a:IsSuccess>", r.text, re.S):
        print(f"工作联络单保存成功")
    else:
        pprint.pprint(r.text)
        raise Exception("工作联络单保存失败！")


def cailiao():
    IMS_data = []
    for i in range(4):
        url = "https://dv.lantingroup.cn:7079/PC/Contract/ContService.svc"
        head = {'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': '"http://tempuri.org/IQuestionFeedback/SelectContForMemorandum"',
                'Host': 'dv.lantingroup.cn:7079',
                'Content-Length': '3660',
                'Expect': '100-continue',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'Keep-Alive'}
        body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectContForMemorandum xmlns="http://tempuri.org/">' \
               '<request xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:CustomParas i:nil="true"/>' \
               '<a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight">' \
               '<b:LoginStafPosID>988a5622-980d-488b-a52f-35d9180c0c32</b:LoginStafPosID><b:RegisterID i:nil="true"/><b:SessionID>fb2fdc83-8b57-4cd8-9e4e-b4936f137e56</b:SessionID>' \
               '<b:Sign i:nil="true"/><b:UniqueID>fb2fdc83-8b57-4cd8-9e4e-b4936f137e56</b:UniqueID></a:Session>' \
               '<a:ApperRange i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/>' \
               '<a:ApplierRange i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:BeginCreateTime i:nil="true"/><a:BeginFinishTime i:nil="true"/>' \
               '<a:BeginSettleTime i:nil="true"/><a:BeginSubmitTime i:nil="true"/><a:CoId i:nil="true"/><a:ContClashType i:nil="true"/>' \
               '<a:CreatorRange i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:EndCreateTime i:nil="true"/><a:EndFinishTime i:nil="true"/>' \
               '<a:EndSettleTime i:nil="true"/><a:EndSubmitTime i:nil="true"/><a:FlowStates i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
               '<a:MainBillNo i:nil="true"/><a:QueryMode>List</a:QueryMode><a:QueryPara xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data"><b:DataTotal>0</b:DataTotal>' \
               '<b:IsPaging>false</b:IsPaging><b:LastTime i:nil="true"/><b:OrderFields xmlns:c="http://schemas.datacontract.org/2004/07/Base.Data.DbAccess"/><b:PageCount>1</b:PageCount>' \
               '<b:PageSize>50</b:PageSize><b:QueryKey i:nil="true"/><b:StartIndex>0</b:StartIndex></a:QueryPara>' \
               '<a:Cond><DataTotal xmlns="http://schemas.datacontract.org/2004/07/Base.Data">0</DataTotal><IsPaging xmlns="http://schemas.datacontract.org/2004/07/Base.Data">true</IsPaging>' \
               '<LastTime i:nil="true" xmlns="http://schemas.datacontract.org/2004/07/Base.Data"/>' \
               '<OrderFields xmlns="http://schemas.datacontract.org/2004/07/Base.Data" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.DbAccess"/>' \
               '<PageCount xmlns="http://schemas.datacontract.org/2004/07/Base.Data">1</PageCount><PageSize xmlns="http://schemas.datacontract.org/2004/07/Base.Data">50</PageSize>' \
               f'<QueryKey i:nil="true" xmlns="http://schemas.datacontract.org/2004/07/Base.Data"/><StartIndex xmlns="http://schemas.datacontract.org/2004/07/Base.Data">{i}</StartIndex>' \
               '<a:ApperRange i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:BeginCreateTime i:nil="true"/><a:BeginFinishTime i:nil="true"/>' \
               '<a:BeginSettleTime i:nil="true"/><a:BeginSubmitTime i:nil="true"/><a:EndCreateTime i:nil="true"/><a:EndFinishTime i:nil="true"/><a:EndSettleTime i:nil="true"/>' \
               '<a:EndSubmitTime i:nil="true"/><a:IsSelectForUse>false</a:IsSelectForUse><a:CoID i:nil="true"/><a:ContNo i:nil="true"/><a:ContPurState>0</a:ContPurState>' \
               '<a:CustID i:nil="true"/><a:CustName i:nil="true"/><a:CustTel i:nil="true"/><a:HouseAddress i:nil="true"/><a:IsValidAchv i:nil="true"/><a:IsVisitEvaluate i:nil="true"/>' \
               '<a:MatlPurCatg i:nil="true"/><a:PMID i:nil="true"/><a:SecondStartState i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
               '<a:SignDateBegin i:nil="true"/><a:SignDateEnd i:nil="true"/><a:SignPerson i:nil="true"/><a:StartDateBegin i:nil="true"/><a:StartDateEnd i:nil="true"/>' \
               '<a:State xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><b:int>4</b:int></a:State></a:Cond></request></SelectContForMemorandum></s:Body></s:Envelope>'
        r = requests.post(url, headers=head, data=body.encode('utf-8'))
        IMS_data.extend(re.findall('<a:No>(.*?)</a:No>', r.text))
    print(f"IMS数据量：{len(IMS_data)}")
    sql_data = set(SQL.getcailiao())
    print(f"数据库数据量：{len(sql_data)}")
    IMS_data_set = set(IMS_data)

    IMS_sql = IMS_data_set - sql_data
    sql_IMS = sql_data - IMS_data_set

    print(f"IMS比SQL多的数据为：{IMS_sql}")
    print(f"SQL比IMS多的数据为：{sql_IMS}")


# 新建完工登记
def sitecompl(n):
    oper = SQL.getopers(LoginStafPosID)
    cretime = modifydatetime('now')
    contid = SQL.selectcontid(n)
    budgeter = SQL.contperson(contid, 'budgeterspid')
    cmpldate = datetime.date.today() + datetime.timedelta(days=1)
    address = SQL.budid(n)
    personname = SQL.person_name(budgeter)
    custcret = SQL.custcretime(n)
    bldname = SQL.custbldname(custcret[5])
    contno = SQL.contno(n)
    dsgner, dsgnid = SQL.deptstaff('设计师', contno)
    manager, managerid = SQL.deptstaff('管家', contno)
    limittime, startdate, ecmpldate, esdate = SQL.contmsg(contno)
    url = 'https://dv.lantingroup.cn:7079/PC/Site/SiteService.svc'
    header = {'Content-Type': 'text/xml; charset=utf-8',
              'SOAPAction': '"http://tempuri.org/ISiteCmpl/AddPCSiteCmpl"',
              'Host': 'dv.lantingroup.cn:7079',
              'Content-Length': '3196',
              'Expect': '100-continue',
              'Accept-Encoding': 'gzip, deflate'}
    body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><AddPCSiteCmpl xmlns="http://tempuri.org/">{session}' \
           '<siteCmpl xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
           f'<a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{cretime}+08:00</a:CreTime><a:ID i:nil="true"/><a:Oper>{oper}</a:Oper>' \
           f'<a:OperID>{LoginStafPosID}</a:OperID><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/>' \
           f'<a:UpdtTime>{cretime}+08:00</a:UpdtTime><a:AppSpID i:nil="true"/><a:AppSpName/><a:Attach i:nil="true"/><a:BudgetID i:nil="true"/>' \
           '<a:BudgetName i:nil="true"/><a:FinishTime i:nil="true"/><a:FlowState>1</a:FlowState><a:FlowStateTxt>待提交</a:FlowStateTxt><a:IsChkBefore>false</a:IsChkBefore>' \
           f'<a:No i:nil="true"/><a:Remark i:nil="true"/><a:State>1</a:State><a:StateTxt i:nil="true"/><a:SubmitTime i:nil="true"/><a:Budgeter>{personname}</a:Budgeter>' \
           f'<a:BudgeterSpId>{budgeter}</a:BudgeterSpId><a:CmplDate>{cmpldate}</a:CmplDate><a:ContAddr>{address[5]}</a:ContAddr>' \
           f'<a:ContID>{contid}</a:ContID><a:ContPayStage>0</a:ContPayStage><a:ContPayStageTxt/><a:FactDays>0</a:FactDays><a:FinalBudgeter i:nil="true"/>' \
           f'<a:FinalBudgeterSpId i:nil="true"/><a:IsDelay>false</a:IsDelay><a:IsVisit>false</a:IsVisit><a:SiteCmplRankState>0</a:SiteCmplRankState><a:BldName>{bldname}</a:BldName>' \
           '<a:CmplDesc>as等分色弱</a:CmplDesc><a:CoCmplDate i:nil="true"/><a:ContAddrLat>30.6888994627706</a:ContAddrLat><a:ContAddrLon>104.0537440034100</a:ContAddrLon>' \
           f'<a:ContCustName>{n}</a:ContCustName><a:ContCustNo i:nil="true"/><a:ContCustTel>{custcret[6]}</a:ContCustTel>' \
           f'<a:ContCustTels xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><b:string>{custcret[6]}</b:string></a:ContCustTels><a:ContLastPayTime i:nil="true"/>' \
           f'<a:ContNo>{contno}</a:ContNo><a:ContState>4</a:ContState><a:CustTelsList xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays">' \
           f'<b:string>{custcret[6]}</b:string></a:CustTelsList><a:Dsgner>{dsgner}</a:Dsgner><a:DsgnerID>{dsgnid}</a:DsgnerID>' \
           f'<a:ExpectCmplDate>{ecmpldate}</a:ExpectCmplDate><a:ExpectStartDate>{esdate}</a:ExpectStartDate><a:IsAfterSale>false</a:IsAfterSale>' \
           f'<a:IsSubcont>false</a:IsSubcont><a:LimitDays>{limittime}</a:LimitDays><a:Manager>{manager}</a:Manager><a:ManagerID>{managerid}</a:ManagerID>' \
           '<a:PreAcptDate i:nil="true"/><a:PreAcptState>1</a:PreAcptState><a:ProCatg>0</a:ProCatg><a:QualityApprovalTime i:nil="true"/><a:ReceivedRate>0</a:ReceivedRate>' \
           f'<a:StartDate>{startdate}</a:StartDate></siteCmpl></AddPCSiteCmpl></s:Body></s:Envelope>'
    cmpl = requests.post(url, headers=header, data=body.encode('utf-8'))
    pprint.pprint(cmpl.text)


if __name__ == "__main__":
    LoginStafPosID = 'af160a27-5998-4263-aa10-e49a5035082d'
    port = '7079'
    UniqueID = SessionID = 'eb8aed7e-f3b7-42c3-9c0e-23659087187b'
    LoginStafPosID2 = '7592d52d-020c-42e6-bff8-5e051b2ae9de'
    UniqueID2 = SessionID2 = 'e7d68d42-2a80-47ab-8947-61db828c8c4d'
    nowtime = datetime.datetime.now()
    # try:
    #     with open("Loginuser.yaml", "r+") as f:
    #         result = yaml.safe_load(f.read())
    #         old = result['time']
    #         if (nowtime - old) > datetime.timedelta(seconds=7200):
    #             with open("Loginuser.yaml", "w+") as f1:
    #                 result['time'] = nowtime
    #                 UniqueID = SessionID = login()
    #                 result['session'] = SessionID
    #                 yaml.safe_dump(result, f1)
    #         else:
    #             UniqueID = SessionID = result['session']
    # except FileNotFoundError as e:
    #     UniqueID = SessionID = login()
    #     content = {'time': nowtime, 'session': SessionID}
    #     with open("Loginuser.yaml", "w+") as f2:
    #         yaml.safe_dump(content, f2)

    session = f'''<session xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.UserRight" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
        <a:LoginStafPosID>{LoginStafPosID}</a:LoginStafPosID><a:RegisterID i:nil="true"/><a:SessionID>{SessionID}</a:SessionID>
        <a:Sign i:nil="true"/><a:UniqueID>{UniqueID}</a:UniqueID></session>'''
    session2 = f'''<session xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.UserRight" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <a:LoginStafPosID>{LoginStafPosID2}</a:LoginStafPosID><a:RegisterID i:nil="true"/><a:SessionID>{SessionID2}</a:SessionID>
            <a:Sign i:nil="true"/><a:UniqueID>{UniqueID2}</a:UniqueID></session>'''
    all_names = ['东澹之', '台澹眉', '别一席', '天来流', '嗟涛谢', '折心忽', '兮扉兮', '能灭照', '见闻此', '即语水']
    while True:
        k = int(input("执行哪个动作？(1.客户登记 2.合同登记 3.合同优惠单登记 4.开工预案申请 5.设计见面 6.积分取消单并发 7.新建工作联络单 0.quit)"))
        #     add_aftersalerecord()
        #     time.sleep(5)
        #     completerecord()
        #     time.sleep(5)
        if k == 1:
            # 客户登记
            namelist = []
            for _ in range(10):
                name = get_name()
                namelist.append(name)
                customersave(name)
                time.sleep(2)
            print(namelist)
        elif k == 2:
            # 合同登记
            contactadd(all_names)
        elif k == 3:
            # 合同优惠登记
            adddiscount('而历钩')
        elif k == 4:
            # 开工预案申请
            contstartplanadd(all_names)
        elif k == 5:
            # 设计见面
            for n in all_names:
                custmeet(n)
        elif k == 6:
            # 并发设计积分取消单
            # p1 = multiprocessing.Process(target=designintegralcancel, args=('JF2109170000017', session, LoginStafPosID, SessionID, port))
            # p2 = multiprocessing.Process(target=designintegralcancel, args=('JF2109170000017', session2, LoginStafPosID2, SessionID2,port))
            # p1.start()
            # p2.start()
            designintegralcancel('JF2109170000005', session, LoginStafPosID, SessionID, port)
            # time.sleep(0.5)
            designintegralcancel('JF2109170000005', session2, LoginStafPosID2, SessionID2, port)
        elif k == 7:
            # 新建工作联络单
            for _ in range(15):
                creatliaison()
        elif k == 0:
            break
        elif k == 8:
            cailiao()
        elif k == 9:
            sitecompl('峦巅黄')
        else:
            print('输入错误，请重新输入！q退出')
            continue

        break
