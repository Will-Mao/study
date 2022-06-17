# encoding=utf-8
import base64
import gzip
import json
import os
import uuid

import requests, pprint
import random, time
import sqlserver_act as SQL
import datetime
import re
import uiautomation as ui
# import multiprocessing, yaml
import subprocess
import pyautogui
from threading import Thread


class ImsData:

    def __init__(self, login_user, port):
        self.port = port
        self.kehu = []
        self.posinfo = SQL.get_session(login_user)
        if self.posinfo:
            self.SessionID = self.UniqueID = str(self.posinfo[0]).lower()
            self.LoginStafPosID = str(self.posinfo[1]).lower()
        else:
            print("用户未登录，将自动登录")
            # os.system("pause")
            self.SessionID = self.UniqueID, self.LoginStafPosID = login()
        self.opers = SQL.getopers(self.LoginStafPosID)
        self.coid = str(SQL.getcoid(self.LoginStafPosID)).lower()
        self.contID = SQL.contid()
        self.session = '<session xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.UserRight" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                       f'<a:LoginStafPosID>{self.LoginStafPosID}</a:LoginStafPosID><a:RegisterID i:nil="true"/><a:SessionID>{self.SessionID}</a:SessionID>' \
                       f'<a:Sign i:nil="true"/><a:UniqueID>{self.UniqueID}</a:UniqueID></session>'

    def collect_name(self, func, num):
        name_list = []
        for _ in range(num):
            n = func()
            name_list.append(n)
        return name_list

    # 日期生成
    def modifydatetime(*args, **kwargs):
        now_time = datetime.datetime.now()
        if 'minutes' in kwargs:
            dt = now_time + datetime.timedelta(minutes=kwargs['minutes'])
        elif 'days' in kwargs:
            dt = now_time + datetime.timedelta(days=kwargs['days'])
        elif args[1] == 'date':
            dt = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")
        elif args[1] == 'now':
            dt = now_time
        else:
            if '.' in str(args[1]):
                tt = datetime.datetime.strptime(str(args[1]), "%Y-%m-%d %H:%M:%S.%f")
                dt = str(tt)[:-3]
            else:
                dt = args[1]

        return str(dt).replace(' ', 'T')

    # 随机生成一个名字
    @staticmethod
    def get_name():
        name_word = "海客谈瀛洲烟涛微茫信难求越人语天姥云霞明灭或可睹天姥连天向天横势拔五岳掩赤城天台四万八千丈对此欲倒东南倾我欲因之梦吴越一夜飞度" \
                    "镜湖月湖月照我影送我至剡溪谢公宿处今尚在渌水荡漾清猿啼脚著谢公屐身登青云梯半壁见海日空中闻天鸡千岩万转路不定迷花倚石忽已暝熊咆" \
                    "龙吟殷岩泉栗深林兮惊层巅云青青兮欲雨水澹澹兮生烟列缺霹雳丘峦崩摧洞天石扉訇然中开青冥浩荡不见底日月照耀金银台霓为衣兮风为马云之" \
                    "君兮纷纷而来下虎鼓瑟兮鸾回车仙之人兮列如麻忽魂悸以魄动恍惊起而长嗟惟觉时之枕席失向来之烟霞世间行乐亦如此古来万事东流水别君去兮" \
                    "何时还且放白鹿青崖间须行即骑访名山安能摧眉折腰事权贵使我不得开心颜"
        nn = random.sample(name_word, 3)
        custname = ''.join(nn)
        return '毛'+custname

    # 添加售后登记
    def add_aftersalerecord(self):
        cretime = self.modifydatetime('now')
        num = random.randint(1, 5)
        p_id, p_name = SQL.get_problem(num)
        url = f"https://dv.lantingroup.cn:{self.port}/PC/AfaterSale/AfterSaleService.svc"
        header = {'Content-Type': 'text/xml; charset=utf-8',
                  'Host': f'dv.lantingroup.cn:{self.port}',
                  'Expect': '100-continue',
                  'Accept-Encoding': 'gzip,deflate',
                  'SOAPAction': '"http://tempuri.org/IAfterSaleRecord/AddAfterSaleRecord"'}
        body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><AddAfterSaleRecord xmlns="http://tempuri.org/">{self.session}\
        <afterSaleRecord xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">\
                <a:CoID>{self.coid}</a:CoID><a:CoName i:nil="true"/><a:CreTime>{cretime}+08:00</a:CreTime>\
                <a:ID i:nil="true"/><a:Oper i:nil="true"/><a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/>\
                <a:UpdtOperId i:nil="true"/><a:UpdtTime>{cretime}+08:00</a:UpdtTime><a:AfterSaleCharges i:nil="true"/>\
                <a:AfterSaleComplains i:nil="true"/><a:AfterSaleCosts i:nil="true"/><a:AfterSaleFollows i:nil="true"/><a:AfterSalePersons i:nil="true"/>\
                <a:Attach/><a:CommunicateTime>111222333</a:CommunicateTime><a:ContAmt i:nil="true"/><a:ContBldName i:nil="true"/><a:ContCustName i:nil="true"/>\
                <a:ContCustPhone i:nil="true"/><a:ContDesnName i:nil="true"/><a:ContGuWenName i:nil="true"/><a:ContID>{self.contID[0]}</a:ContID>\
                <a:ContNo i:nil="true"/><a:ContPersonList i:nil="true"/><a:ContPjtAddr i:nil="true"/><a:ContPmName i:nil="true"/><a:ContState>0</a:ContState>\
                <a:Content>121212232323</a:Content><a:Contract i:nil="true"/><a:CustName>{self.contID[1]}</a:CustName><a:CustPhone></a:CustPhone>\
                <a:Defendant i:nil="true"/><a:FinishTime i:nil="true"/><a:IsExistComplain>false</a:IsExistComplain><a:IsSubcont>false</a:IsSubcont><a:No i:nil="true"/>\
                <a:ProblemID>{p_id}</a:ProblemID><a:ProblemName>{p_name}</a:ProblemName>\
                <a:Responsibility i:nil="true"/><a:ShuiDianAmt i:nil="true"/><a:SourceID>550a90b3-8305-41e7-a5a0-5813b9499b9c</a:SourceID><a:State>0</a:State>\
                <a:SupplierIDList i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:WarrantyCardID i:nil="true"/>\
                <a:WarrantyCardInfo i:nil="true"/></afterSaleRecord></AddAfterSaleRecord></s:Body></s:Envelope>'

        r = requests.post(url, headers=header, data=body.encode('utf-8'))
        # r.encoding = 'gb2312'
        if self.contID[1] in r.text:
            print('add_aftersale Pass \n')
        else:
            print(r.text)
            raise NameError(f"{self.contID[1]} 没有完成")
        # print(r.text)

    # 完成售后登记
    def completerecord(self):
        record_id = SQL.get_recordid(self.contID[1])
        url = f"https://dv.lantingroup.cn:{self.port}/PC/AfaterSale/AfterSaleService.svc"
        c_header = {'Content-Type': 'text/xml; charset=utf-8',
                    'SOAPAction': '"http://tempuri.org/IAfterSaleRecord/FinishAfterSaleRecord"',
                    'Host': f'dv.lantingroup.cn:{self.port}',
                    'Content-Length': '632',
                    'Expect': '100-continue',
                    'Accept-Encoding': 'gzip, deflate'}

        c_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body>\
            <FinishAfterSaleRecord xmlns="http://tempuri.org/">{self.session}\
            <afterSaleRecordID>{record_id}</afterSaleRecordID></FinishAfterSaleRecord></s:Body></s:Envelope>'
        r = requests.post(url, headers=c_header, data=c_body.encode('utf-8'))
        if self.contID[1] in r.text:
            print('complete Pass \n')
        else:
            print(r.text)
            raise NameError(f"{self.contID[1]} 没有完成")

    # 新增客户
    def customersave(self, num):
        while num > 0:
            kehu_name = self.get_name()
            c_phone = random.randint(10000000000, 20000000000)
            cre_time = self.modifydatetime('now')
            cont_time = self.modifydatetime(minutes=5)
            follow_time = self.modifydatetime(days=1)
            address = SQL.get_building()
            source = SQL.custsource()
            housetype = SQL.housetype()
            custhouse = SQL.custhousetype()
            age = SQL.custages()
            channelid = SQL.custchannel()
            follow_way = SQL.custfollowway()
            custlevel = SQL.custlevelid()
            customindent = SQL.customerindent()
            coid = SQL.getcoid(self.LoginStafPosID)
            if str(coid) == '09a055c1-4885-47e7-a5ca-7066f16c4537':  # 岚庭家居
                market = '1dc04ef2-7e83-4c61-8162-a07b7f3c46f9'
            # elif str(custid[1]) == '8D92D6FB-C865-4A1F-B375-C0C24CD2DCF5':  # 湖北武汉岚庭
            #     discoutlist = 'e4dd23c9-bde3-4416-827b-e33d065f54c2'
            elif str(coid) == 'c7cc5de4-efdd-4aa7-9615-7a748785be12':  # 幸福魔方
                market = '780c0b91-b12e-4b7e-a2d7-d0db6ce8439e'
            else:
                print(str(coid))
                raise Exception("这是啥公司的客户？")
            url = f'https://dv.lantingroup.cn:{self.port}/PC/Customer/CustomerService.svc'
            cs_header = {'Content-Type': 'text/xml; charset=utf-8',
                         'SOAPAction': '"http://tempuri.org/ICustomer/CustomerSave"',
                         'Host': f'dv.lantingroup.cn:{self.port}',
                         'Content-Length': '4779',
                         'Expect': '100-continue',
                         'Accept-Encoding': 'gzip, deflate'}

            cs_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><CustomerSave xmlns="http://tempuri.org/">{self.session}' \
                      f'<customer xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                      f'<a:CoID>{self.coid}</a:CoID><a:CoName i:nil="true"/><a:CreTime>{cre_time}+08:00</a:CreTime><a:ID i:nil="true"/>' \
                      f'<a:Oper>{self.opers[1]}</a:Oper><a:OperID>{self.opers[0]}</a:OperID><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/>' \
                      f'<a:UpdtOperId i:nil="true"/><a:UpdtTime>{cre_time}+08:00</a:UpdtTime><a:Address>{address[0]}11栋22单元33层44号</a:Address><a:AppSpID i:nil="true"/>' \
                      f'<a:Apper i:nil="true"/><a:AreaID>{address[1]}</a:AreaID><a:AreaName i:nil="true"/><a:Catg>0</a:Catg>' \
                      f'<a:CustBldID>{address[2]}</a:CustBldID><a:CustBldName i:nil="true"/><a:CustContactWay i:nil="true"/>' \
                      f'<a:CustContactWays><a:SvcCustContactWay><a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{cont_time}+08:00</a:CreTime>' \
                      f'<a:ID i:nil="true"/><a:Oper i:nil="true"/><a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/>' \
                      f'<a:UpdtTime>{cont_time}+08:00</a:UpdtTime><a:Catg>1</a:Catg><a:CustID i:nil="true"/><a:Sort>0</a:Sort><a:Way>{c_phone}</a:Way></a:SvcCustContactWay>' \
                      f'</a:CustContactWays><a:CustDsgnID i:nil="true"/><a:CustDsgner i:nil="true"/><a:CustIntentID>{customindent}</a:CustIntentID>' \
                      f'<a:CustIntentName i:nil="true"/><a:CustLevelID>{custlevel}</a:CustLevelID>' \
                      f'<a:CustLevelName i:nil="true"/><a:CustName>{kehu_name}</a:CustName><a:CustPersons/><a:CustSourceID>{source}</a:CustSourceID>' \
                      f'<a:CustSourceName i:nil="true"/><a:CustTels i:nil="true"/><a:CustTelsAllStr i:nil="true"/>' \
                      f'<a:CustTelsList i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:CustTelsStr i:nil="true"/>' \
                      f'<a:CustomerHouseTypeID>{custhouse}</a:CustomerHouseTypeID><a:CustomerHouseTypeName i:nil="true"/><a:DeptName i:nil="true"/>' \
                      f'<a:HandInDate>{cre_time}+08:00</a:HandInDate><a:HouseArea>130</a:HouseArea><a:HouseBuilding>11</a:HouseBuilding><a:HouseFloor>33</a:HouseFloor>' \
                      f'<a:HouseNumber>44</a:HouseNumber><a:HouseType/><a:HouseTypeID>{housetype}</a:HouseTypeID><a:HouseTypeName i:nil="true"/>' \
                      f'<a:HouseUnit>22</a:HouseUnit><a:IsAreaRepeat i:nil="true"/><a:NextFlwTime i:nil="true"/><a:NextFlwWayID i:nil="true"/><a:NextFlwWayName i:nil="true"/>' \
                      f'<a:No i:nil="true"/><a:Remark>客户说明内容</a:Remark><a:RepeatCatg>0</a:RepeatCatg><a:AgeGroupID>{age}</a:AgeGroupID>' \
                      f'<a:AssState>3</a:AssState><a:ChannelID>{channelid}</a:ChannelID><a:ChannelName i:nil="true"/><a:ConsultWayID i:nil="true"/>' \
                      f'<a:ConsultWayName i:nil="true"/><a:ContAddr i:nil="true"/><a:ContAmt i:nil="true"/><a:ContID i:nil="true"/><a:ContNo i:nil="true"/>' \
                      f'<a:ContNoList i:nil="true"/><a:ContProCatg>0</a:ContProCatg>' \
                      f'<a:ContState>0</a:ContState><a:DesignMode i:nil="true"/><a:DesignModeTxt i:nil="true"/><a:DesnID i:nil="true"/><a:DesnName i:nil="true"/>' \
                      f'<a:ExtensionManDirectorName i:nil="true"/><a:FlwData><a:AppSpID i:nil="true"/><a:Attachment/><a:Catg>1</a:Catg><a:CustID i:nil="true"/>' \
                      f'<a:CustIntention>{customindent}</a:CustIntention><a:CustState>0</a:CustState><a:FollowContent>本次跟进内容</a:FollowContent>' \
                      f'<a:FollowType>c056bd76-5016-4dda-8c94-5f0a55a3003d</a:FollowType><a:FollowWay>{follow_way}</a:FollowWay><a:IsCanProtectCustomer>false</a:IsCanProtectCustomer>' \
                      f'<a:NextFlowContent>下次跟进内容</a:NextFlowContent><a:NextFollowTime>{follow_time}+08:00</a:NextFollowTime>' \
                      f'<a:NextFollowWay>{follow_way}</a:NextFollowWay></a:FlwData>' \
                      f'<a:IntentDate i:nil="true"/><a:IsPayCust>false</a:IsPayCust><a:IsReceipt>true</a:IsReceipt><a:IsRepeat>false</a:IsRepeat>' \
                      f'<a:KeyWord i:nil="true"/><a:MarketerID>{market}</a:MarketerID><a:MatketerName i:nil="true"/><a:OperationManagerName i:nil="true"/>' \
                      f'<a:PMID i:nil="true"/><a:PMName i:nil="true"/><a:PromID i:nil="true"/><a:PromName i:nil="true"/><a:PullDeadReason i:nil="true"/>' \
                      f'<a:ServiceDirectorName i:nil="true"/><a:ServiceName i:nil="true"/>' \
                      f'<a:SiteID i:nil="true"/><a:SiteName i:nil="true"/><a:SitePromName i:nil="true"/>' \
                      f'<a:SiteUrl i:nil="true"/><a:State>0</a:State></customer></CustomerSave></s:Body></s:Envelope>'
            # 耳A区 marketID：1dc04ef2-7e83-4c61-8162-a07b7f3c46f9 ，C区marketID：5a70e19f-57f3-4d42-84b7-124c96e67806， 湖北marketID：9004b1f3-ef27-4791-9219-eb18a3bae284
            r = requests.post(url, headers=cs_header, data=cs_body.encode('utf-8'))
            if re.search("<IsSuccess.*?true</IsSuccess>", r.text, re.S):
                print(f"客户{kehu_name}新增成功")
                self.kehu.append(kehu_name)
                custid = re.search("ReturnData.+?>(.*?)</ReturnData>", r.text).group(1)
                time.sleep(2)
                self.tointent(custid)
                time.sleep(1)
                self.custmeet(kehu_name)
                # return kehu_name
            else:
                print(r.text)
            num -= 1
        return self.kehu

    # 转意向客户
    def tointent(self, custid):
        url = f'https://dv.lantingroup.cn:{self.port}/PC/Customer/CustomerService.svc'
        intent_head = {'Content-Type': 'text/xml; charset=utf-8',
                       'SOAPAction': '"http://tempuri.org/ICustomer/CustomerToIntent"',
                       'Host': f'dv.lantingroup.cn:{self.port}',
                       'Content-Length': '609',
                       'Expect': '100-continue',
                       'Accept-Encoding': 'gzip, deflate',
                       'Connection': 'Keep-Alive'}

        intent_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><CustomerToIntent xmlns="http://tempuri.org/">{self.session} \
                      <custID>{custid}</custID><remark/></CustomerToIntent></s:Body></s:Envelope>'
        requests.post(url, headers=intent_head, data=intent_body.encode('utf-8'))

    # 设计见面
    def custmeet(self, custname):
        opers = SQL.getopers(self.LoginStafPosID)
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
        cretime = self.modifydatetime('now')
        if str(custcret[18]) == '09a055c1-4885-47e7-a5ca-7066f16c4537':  # 岚庭家居
            deepdsgn = '设三3组/杜甫'
            deepid = 'f9080334-f038-496f-bf2e-c258f925d494'
            schdsgn = '设三3组/苏轼'
            schid = '999c0ab5-bb08-418e-8c01-cad99377cdd7'
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
        url = f'https://dv.lantingroup.cn:{self.port}/PC/Customer/CustomerService.svc'
        head = {'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': '"http://tempuri.org/ICustMeet/SaveCustMeet"',
                'Host': f'dv.lantingroup.cn:{self.port}',
                'Content-Length': '6570',
                'Expect': '100-continue',
                'Accept-Encoding': 'gzip, deflate'}
        body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SaveCustMeet xmlns="http://tempuri.org/">{self.session}' \
               '<custMeet xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
               f'<a:CoID>{custcret[18]}</a:CoID><a:CoName i:nil="true"/><a:CreTime>{cretime}+08:00</a:CreTime><a:ID i:nil="true"/>' \
               f'<a:Oper>{opers[1]}</a:Oper><a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/>' \
               f'<a:UpdtTime>{cretime}+08:00</a:UpdtTime><a:AppSpID>{custcret[16]}</a:AppSpID><a:Apper i:nil="true"/>' \
               f'<a:Cust><a:CoID>{custcret[18]}</a:CoID><a:CoName>{coname}</a:CoName><a:CreTime>{self.modifydatetime(custcret[0])}</a:CreTime>' \
               f'<a:ID>{custcret[1]}</a:ID><a:Oper>{oper}</a:Oper><a:OperID>{self.LoginStafPosID}</a:OperID>' \
               f'<a:UniqueID>{custcret[1]}</a:UniqueID><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/>' \
               f'<a:UpdtTime>{self.modifydatetime(custcret[2])}</a:UpdtTime><a:Address>{custcret[3]}</a:Address><a:AppSpID>{custcret[16]}</a:AppSpID>' \
               f'<a:Apper>{fullname}</a:Apper><a:AreaID>{custcret[4]}</a:AreaID><a:AreaName>{areaname}</a:AreaName>' \
               f'<a:Catg>2</a:Catg><a:CustBldID>{custcret[5]}</a:CustBldID><a:CustBldName>{bldname}</a:CustBldName><a:CustContactWay>{custcret[6]}</a:CustContactWay>' \
               f'<a:CustContactWays><a:SvcCustContactWay><a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{self.modifydatetime(contacts[0])}</a:CreTime><a:ID i:nil="true"/>' \
               f'<a:Oper i:nil="true"/><a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/>' \
               f'<a:UpdtTime>{self.modifydatetime(contacts[1])}</a:UpdtTime><a:Catg>1</a:Catg><a:CustID>{custcret[1]}</a:CustID><a:Sort>0</a:Sort>' \
               f'<a:Way>{custcret[6]}</a:Way></a:SvcCustContactWay></a:CustContactWays><a:CustDsgnID i:nil="true"/><a:CustDsgner/>' \
               f'<a:CustIntentID>{custcret[7]}</a:CustIntentID><a:CustIntentName>{indentname}</a:CustIntentName><a:CustLevelID>{custcret[8]}</a:CustLevelID>' \
               f'<a:CustLevelName>{levelname}</a:CustLevelName><a:CustName>{custname}</a:CustName><a:CustPersons><a:SvcCustPerson><a:CoID i:nil="true"/><a:CoName i:nil="true"/>' \
               f'<a:CreTime>{self.modifydatetime(custpers[4])}</a:CreTime><a:ID>{custpers[2]}</a:ID><a:Oper i:nil="true"/><a:OperID>{custpers[3]}</a:OperID>' \
               f'<a:UniqueID>{custpers[2]}</a:UniqueID><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/><a:UpdtTime>{self.modifydatetime(custpers[5])}</a:UpdtTime>' \
               f'<a:CustID>{custcret[1]}</a:CustID><a:DeptName i:nil="true"/><a:PersonCatg>7</a:PersonCatg><a:Ramark i:nil="true"/>' \
               f'<a:UserID>{custpers[0]}</a:UserID><a:UserName>{username}</a:UserName>' \
               f'<a:UserSpID>{custpers[1]}</a:UserSpID></a:SvcCustPerson></a:CustPersons><a:CustSourceID>{custcret[9]}</a:CustSourceID>' \
               f'<a:CustSourceName>{sourcename}</a:CustSourceName><a:CustTels i:nil="true"/><a:CustTelsAllStr>{custcret[6]}</a:CustTelsAllStr>' \
               f'<a:CustTelsList xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><b:string>{custcret[6]}</b:string></a:CustTelsList><a:CustTelsStr>{custcret[6]}</a:CustTelsStr>' \
               f'<a:CustomerHouseTypeID>{custcret[10]}</a:CustomerHouseTypeID><a:CustomerHouseTypeName>{housetypename}</a:CustomerHouseTypeName><a:DeptName i:nil="true"/>' \
               f'<a:HandInDate>{self.modifydatetime(custcret[11])}</a:HandInDate><a:HouseArea>130.00</a:HouseArea><a:HouseBuilding>11</a:HouseBuilding><a:HouseFloor>33</a:HouseFloor>' \
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
               f'<a:MeetDate>{self.modifydatetime("date")}+08:00</a:MeetDate><a:MeetingTypeID>d966474e-cba6-405b-85d8-a0ae064ff10f</a:MeetingTypeID><a:No i:nil="true"/><a:Remark/>' \
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
        chuandi_url = f'https://dv.lantingroup.cn:{self.port}/PC/Workflow/WorkflowService.svc'
        chuandi_head = {'Content-Type': 'text/xml; charset=utf-8',
                        'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                        'Host': f'dv.lantingroup.cn:{self.port}',
                        'Content-Length': '1344',
                        'Expect': '100-continue',
                        'Accept-Encoding': 'gzip, deflate'}
        chuandi_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
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
                         'Host': f'dv.lantingroup.cn:{self.port}',
                         'Content-Length': '632',
                         'Expect': '100-continue',
                         'Accept-Encoding': 'gzip, deflate'}
        chuandi_body2 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectFlowLogDetail xmlns="http://tempuri.org/">{self.session}' \
                        f'<flowCatg>1</flowCatg><relateID>{relateid}</relateID></SelectFlowLogDetail></s:Body></s:Envelope>'
        r1 = requests.post(chuandi_url, headers=chuandi_head2, data=chuandi_body2.encode('utf-8'))
        nodelogid = re.search("<a:NodeLogs>.*?<a:ID>(.*?)</a:ID>", r1.text, re.S).group(1)
        time.sleep(1)
        # 传递2
        chuandi_head3 = {'Content-Type': 'text/xml; charset=utf-8',
                         'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                         'Host': f'dv.lantingroup.cn:{self.port}',
                         'Content-Length': '1412',
                         'Expect': '100-continue',
                         'Accept-Encoding': 'gzip, deflate',
                         'Connection': 'Keep-Alive'}
        chuandi_body3 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                        '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                        '<a:BackNodeId i:nil="true"/><a:Catg>1</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                        f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
                        f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodelogid}</a:NodeLogID>' \
                        f'<a:OperResult>4</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                        '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
        requests.post(chuandi_url, headers=chuandi_head3, data=chuandi_body3.encode('utf-8'))

    # 开工申请
    def contstart(self, names):
        if type(names) == int:
            self.contactadd(names)
        else:
            self.kehu = names
        for n in self.kehu:
            custs = SQL.custcretime(n)
            contid = SQL.selectcontid(n)
            startime = self.modifydatetime(days=2)
            house_id = SQL.housetypeid(contid)
            factstart = self.modifydatetime("now")
            url = f'https://dv.lantingroup.cn:{self.port}/PC/ContStart/ContStartService.svc'
            conts_head = {'Content-Type': 'text/xml; charset=utf-8',
                          'SOAPAction': '"http://tempuri.org/IContStart/ContStartAdd"',
                          'Host': f'dv.lantingroup.cn:{self.port}',
                          'Content-Length': '1189',
                          'Expect': '100-continue',
                          'Accept-Encoding': 'gzip, deflate',
                          'Connection': 'Keep-Alive'}

            conts_body2 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartAdd xmlns="http://tempuri.org/">{self.session}' \
                          '<contStartAdd xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                          f'<a:AppSpID>{custs[16]}</a:AppSpID><a:BudgeterID i:nil="true"/><a:CoTimeLimit>23</a:CoTimeLimit>' \
                          f'<a:ContID>{contid}</a:ContID><a:ExpectStartTime>{startime}</a:ExpectStartTime><a:FloorNum>12</a:FloorNum>' \
                          f'<a:HouseTypeID>{house_id}</a:HouseTypeID><a:IsOrderGrabbing i:nil="true"/><a:IsSubCont>false</a:IsSubCont>' \
                          '<a:IsUrgent>false</a:IsUrgent><a:Remark/><a:SpaceDesignerSpId>8ff8c7df-92b8-4288-853b-e986f0ebb26e</a:SpaceDesignerSpId>' \
                          '<a:SupervisorID i:nil="true"/></contStartAdd></ContStartAdd></s:Body></s:Envelope>'
            # <a:SpaceDesignerSpId i:nil="true"/>
            r = requests.post(url, headers=conts_head, data=conts_body2.encode('utf-8'))
            if re.search("<a:IsSuccess>true</a:IsSuccess>", r.text, re.S):
                print(f"客户{n}开工申请保存成功")
                relateid = re.search("<a:ReturnData>(.*?)</a:ReturnData>", r.text, re.S).group(
                    1)  # 885de8e7-603c-4ecf-909f-5f5c6498a057
            else:
                print(r.text)
                raise Exception("开工申请保存失败！")

            # # 流程任务，设置房屋层数
            # conts_head['Content-Length'] = '822'
            # conts_head['SOAPAction'] = '"http://tempuri.org/IContStart/ContStartSetFloorNum"'
            # c_body03 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartSetFloorNum xmlns="http://tempuri.org/">' \
            #            f'<seeSession xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.UserRight" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:LoginStafPosID>{self.LoginStafPosID}</a:LoginStafPosID>' \
            #            f'<a:RegisterID i:nil="true"/><a:SessionID>{self.SessionID}</a:SessionID><a:Sign i:nil="true"/><a:UniqueID>{self.UniqueID}</a:UniqueID></seeSession>' \
            #            '<contStartSetFloorNum xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
            #            f'<a:ContStartID>{relateid}</a:ContStartID><a:FloorNum>5</a:FloorNum></contStartSetFloorNum></ContStartSetFloorNum></s:Body></s:Envelope>'
            # s2 = requests.post(url, headers=conts_head, data=c_body03.encode('utf-8'))
            # print('s2: ' + s2.text)
            # # 流程任务，设置施工天数
            # conts_head['Content-Length'] = '841'
            # conts_head['SOAPAction'] = '"http://tempuri.org/IContStart/ContStartSetCoTimeLimit"'
            # # c_body04 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartSetFloorNum xmlns="http://tempuri.org/"><seeSession xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.UserRight" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:LoginStafPosID>{self.LoginStafPosID}</a:LoginStafPosID>' \
            # #            f'<a:RegisterID i:nil="true"/><a:SessionID>{self.SessionID}</a:SessionID><a:Sign i:nil="true"/><a:UniqueID>{self.UniqueID}</a:UniqueID></seeSession>' \
            # #            '<contStartSetCoTimeLimit xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
            # #            f'<a:CoTimeLimit>51</a:CoTimeLimit><a:ContStartID>{relateid}</a:ContStartID></contStartSetCoTimeLimit></ContStartSetCoTimeLimit></s:Body></s:Envelope>'
            # c = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartSetCoTimeLimit xmlns="http://tempuri.org/">' \
            #     '<seeSession xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.UserRight" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
            #     f'<a:LoginStafPosID>{self.LoginStafPosID}</a:LoginStafPosID><a:RegisterID i:nil="true"/><a:SessionID>{self.SessionID}</a:SessionID>' \
            #     f'<a:Sign i:nil="true"/><a:UniqueID>{self.SessionID}</a:UniqueID></seeSession>' \
            #     '<contStartSetCoTimeLimit xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
            #     f'<a:CoTimeLimit>55</a:CoTimeLimit><a:ContStartID>{relateid}</a:ContStartID></contStartSetCoTimeLimit></ContStartSetCoTimeLimit>' \
            #     '</s:Body></s:Envelope>'
            # s3 = requests.post(url, headers=conts_head, data=c.encode('utf-8'))
            # print('s3: ' + s3.text)
            # 传递1，进入财务部审核节点
            with open("bodydata.json", "r", encoding='utf-8') as f:
                d = json.load(f)
            d['kaigong']['HouseTypeID'] = str(custs[12])
            # timestamp = startime.split('.')[0]
            # t2 = datetime.datetime.strptime(timestamp,"%Y-%m-%d %H:%M:%S").timestamp()
            # t3 = str(t2).split('.')[0]
            # d['kaigong']['ExpectStartTime'] = f"/Date({t3}000+0800)/",
            t3 = int(time.mktime(time.strptime(startime.replace("T", ' ')[:-7], "%Y-%m-%d %H:%M:%S"))) * 1000
            d['kaigong']['ExpectStartTime'] = f"/Date({t3}+0800)/"
            taskdata = json.dumps(d["kaigong"])
            flow_url = f'https://dv.lantingroup.cn:{self.port}/PC/Workflow/WorkflowService.svc'
            c_head = {
                'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                'Host': f'dv.lantingroup.cn:{self.port}',
                'Content-Length': '1780',
                'Expect': '100-continue',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'Keep-Alive'
            }
            c_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                     '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                     '<a:BackNodeId i:nil="true"/><a:Catg>5</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                     '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc i:nil="true"/><a:LogID i:nil="true"/>' \
                     '<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID i:nil="true"/>' \
                     f'<a:OperResult>0</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/>' \
                     f'<a:TaskDataStr>{taskdata}</a:TaskDataStr>' \
                     '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>0</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            requests.post(flow_url, headers=c_head, data=c_body.encode('utf-8'))
            # 传递1，进入财务部审核
            c_head['Content-Length'] = '1412'
            c_body03 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                       '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                       '<a:BackNodeId i:nil="true"/><a:Catg>5</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                       '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID i:nil="true"/>' \
                       '<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID i:nil="true"/>' \
                       f'<a:OperResult>2</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                       '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            requests.post(flow_url, headers=c_head, data=c_body03.encode('utf-8'))
            # 传递2，进入质检文员确定
            nodeids = SQL.get_flow('财务部审核')
            logid = nodeids[0]
            nodeid = nodeids[1]
            node_body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{session}
            <flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <a:BackNodeId i:nil="true"/><a:Catg>5</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>
            <a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{LogID}</a:LogID>
            <a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{NodelogID}</a:NodeLogID>
            <a:OperResult>4</a:OperResult><a:RelateID>{RelateID}</a:RelateID><a:Summary i:nil="true"/>
            <a:TaskDataStr i:nil="true"/><a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>"""

            c_body1 = node_body.format(session=self.session, LogID=logid, NodelogID=nodeid, RelateID=relateid)
            requests.post(flow_url, headers=c_head, data=c_body1.encode('utf-8'))
            # 流程任务，分配质检员,SupervisorID 质检员ID
            conts_head['Content-Length'] = '964'
            conts_head['SOAPAction'] = '"http://tempuri.org/IContStart/ContStartDistSupervisor"'
            c_body12 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartDistSupervisor xmlns="http://tempuri.org/">{self.session}' \
                       '<contStartDistSupervisor xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:AreaCode>12121212</a:AreaCode>' \
                       f'<a:ContStartID>{relateid}</a:ContStartID><a:FactStartDate>{factstart}+08:00</a:FactStartDate>' \
                       '<a:SupervisorID>bc1f55e6-a3e9-42f6-9ac3-674c9ccec2ce</a:SupervisorID></contStartDistSupervisor></ContStartDistSupervisor></s:Body></s:Envelope>'
            requests.post(url, headers=conts_head, data=c_body12.encode('utf-8'))
            # 传递3，进入工程部确认管家节点
            nodeids = SQL.get_flow('质检文员确认')
            nodeid2 = nodeids[1]
            c_body2 = node_body.format(session=self.session, LogID=logid, NodelogID=nodeid2, RelateID=relateid)

            requests.post(flow_url, headers=c_head, data=c_body2.encode('utf-8'))
            # 流程任务，分配工程部门
            conts_head['Content-Length'] = '906'
            conts_head['SOAPAction'] = '"http://tempuri.org/IContStart/ContStartDistPMDpt"'
            c_body21 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartDistPMDpt xmlns="http://tempuri.org/">{self.session}' \
                       '<contStartDistPMDpt xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                       f'<a:ContStartID>{relateid}</a:ContStartID><a:PMDptID>17beb2c0-d077-4073-9e94-c7b4de7f9ec7</a:PMDptID>' \
                       '<a:PMDptMgrID>b7f5063e-50a3-46d7-a42d-bd8916b83b7c</a:PMDptMgrID></contStartDistPMDpt></ContStartDistPMDpt></s:Body></s:Envelope>'
            requests.post(url, headers=conts_head, data=c_body21.encode('utf-8'))
            # 流程任务，是否分包
            conts_head['Content-Length'] = '823'
            conts_head['SOAPAction'] = '"http://tempuri.org/IContStart/ContStartSetSubCont"'
            c_body22 = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartSetSubCont xmlns="http://tempuri.org/">' \
                       '<seeSession xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.UserRight" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                       f'<a:LoginStafPosID>{self.LoginStafPosID}</a:LoginStafPosID><a:RegisterID i:nil="true"/><a:SessionID>{self.SessionID}</a:SessionID>' \
                       f'<a:Sign i:nil="true"/><a:UniqueID>{self.SessionID}</a:UniqueID></seeSession>' \
                       '<contStartSetSubCont xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                       f'<a:ContStartID>{relateid}</a:ContStartID><a:IsSubCont>true</a:IsSubCont></contStartSetSubCont></ContStartSetSubCont></s:Body></s:Envelope>'
            requests.post(url, headers=conts_head, data=c_body22.encode('utf-8'))
            # 流程任务，分配管家
            conts_head['Content-Length'] = '823'
            conts_head['SOAPAction'] = '"http://tempuri.org/IContStart/ContStartDistPM"'
            c_body23 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartDistPM xmlns="http://tempuri.org/">{self.session}' \
                       '<contStartDistPM xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                       f'<a:ContStartID>{relateid}</a:ContStartID><a:PMID>7884c302-48f3-4aa0-a44e-96aae2874b85</a:PMID></contStartDistPM></ContStartDistPM></s:Body></s:Envelope>'
            requests.post(url, headers=conts_head, data=c_body23.encode('utf-8'))
            # 传递4，进入行政人力部审核
            nodeids = SQL.get_flow('工程部确认管家')
            nodeid3 = nodeids[1]
            with open("bodydata.json", "r", encoding='utf-8') as f:
                d1 = json.load(f)
            d1['kaigong']['IsOrderGrabbing'] = True
            taskdata = json.dumps(d1["kaigong"])
            c_head['Content-Length'] = '1694'
            c_body3 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                      '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                      '<a:BackNodeId i:nil="true"/><a:Catg>5</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc i:nil="true"/><a:LogID>{logid}</a:LogID>' \
                      f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodeid3}</a:NodeLogID>' \
                      f'<a:OperResult>0</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/>' \
                      f'<a:TaskDataStr>{taskdata}</a:TaskDataStr><a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      f'<a:Urgency>0</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            requests.post(flow_url, headers=c_head, data=c_body3.encode('utf-8'))
            c_body31 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                       '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                       '<a:BackNodeId i:nil="true"/><a:Catg>5</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                       f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
                       f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodeid3}</a:NodeLogID>' \
                       f'<a:OperResult>4</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                       '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            requests.post(flow_url, headers=c_head, data=c_body31.encode('utf-8'))
            # 传递5，进入成控部审核
            nodeids = SQL.get_flow('行政人力部审核')
            nodeid4 = nodeids[1]
            c_head['Content-Length'] = '1694'
            c_body4 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                      '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                      '<a:BackNodeId i:nil="true"/><a:Catg>5</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc i:nil="true"/><a:LogID>{logid}</a:LogID>' \
                      f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodeid4}</a:NodeLogID>' \
                      f'<a:OperResult>0</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/>' \
                      f'<a:TaskDataStr>{taskdata}</a:TaskDataStr><a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      f'<a:Urgency>0</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            requests.post(flow_url, headers=c_head, data=c_body4.encode('utf-8'))
            c_body42 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                       '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                       '<a:BackNodeId i:nil="true"/><a:Catg>5</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                       f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
                       f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodeid4}</a:NodeLogID>' \
                       f'<a:OperResult>4</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                       '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            requests.post(flow_url, headers=c_head, data=c_body42.encode('utf-8'))
            # 流程任务，分配预算员
            conts_head['Content-Length'] = '942'
            conts_head['SOAPAction'] = '"http://tempuri.org/IContStart/ContStartDistBudgeteer"'
            c_body41 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartDistBudgeteer xmlns="http://tempuri.org/">{self.session}' \
                       '<contStartDistBudgeteer xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                       f'<a:BugeteerID>20a23695-b288-4b52-9b4f-4660dfecdede</a:BugeteerID><a:ContStartID>{relateid}</a:ContStartID>' \
                       '<a:LibID>7592d52d-020c-42e6-bff8-5e051b2ae9de</a:LibID><a:Remark i:nil="true"/></contStartDistBudgeteer></ContStartDistBudgeteer></s:Body></s:Envelope>'
            requests.post(url, headers=conts_head, data=c_body41.encode('utf-8'))
            # 传递6，完成流程
            nodeids = SQL.get_flow('成控部审核')
            nodeid5 = nodeids[1]
            c_head['Content-Length'] = '1412'
            c_body5 = node_body.format(session=self.session, LogID=logid, NodelogID=nodeid5, RelateID=relateid)
            requests.post(flow_url, headers=c_head, data=c_body5.encode('utf-8'))
            SQL.update_flow(logid)


    # 合同登记
    def contactadd(self, custlist):
        if type(custlist) == int:
            custlist = self.customersave(custlist)
        for n in custlist:
            areacode = random.randint(100, 9999999)
            builds = SQL.budid(n)
            a_time = self.modifydatetime('date')
            custs = SQL.custcretime(n)
            desnid = SQL.get_meettime(n)
            if desnid[1] is None:
                desnid[1] = desnid[2]
            # discountid = SQL.discountid(builds[2])
            url = f'https://dv.lantingroup.cn:{self.port}/PC/Contract/ContService.svc'
            c_head = {'Content-Type': 'text/xml; charset=utf-8',
                      'SOAPAction': '"http://tempuri.org/IContract/ContractAdd"',
                      'Host': f'dv.lantingroup.cn:{self.port}',
                      'Content-Length': '2584',
                      'Expect': '100-continue',
                      'Accept-Encoding': 'gzip, deflate',
                      'Connection': 'Keep-Alive'}
            c_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContractAdd xmlns="http://tempuri.org/">{self.session}' \
                     '<contractAdd xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                     f'<a:AppSpID>{custs[16]}</a:AppSpID><a:AreaCode i:nil="true"/><a:AreaID>{builds[1]}</a:AreaID>' \
                     f'<a:BldID>{builds[0]}</a:BldID><a:CanWeekendConstruction>true</a:CanWeekendConstruction><a:ChannelID i:nil="true"/>' \
                     f'<a:CoID>{custs[18]}</a:CoID><a:CoTimeLimit>0</a:CoTimeLimit><a:ContractDiscountId i:nil="true"/><a:CustID>{builds[2]}</a:CustID>' \
                     f'<a:CustName>{n}</a:CustName><a:CustTel xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><b:string>{builds[3]}</b:string><b:string/>' \
                     f'<b:string/></a:CustTel><a:CustomeReceivedRatio>2</a:CustomeReceivedRatio><a:CustomerHouseTypeID>{builds[4]}</a:CustomerHouseTypeID><a:DecorStyleID>1eca43f3-6ef3-47b7-aec1-fab1a73a45fa</a:DecorStyleID>' \
                     f'<a:DesnID>{desnid[1]}</a:DesnID><a:ExpFrameDiagramDate>{a_time}+08:00</a:ExpFrameDiagramDate>' \
                     f'<a:ExpRenderPicDate>{a_time}+08:00</a:ExpRenderPicDate><a:ExpectGetDate>{a_time}+08:00</a:ExpectGetDate>' \
                     f'<a:ExpectStartDate>{a_time}+08:00</a:ExpectStartDate><a:GetDate i:nil="true"/><a:HouseAddress>{builds[5]}</a:HouseAddress>' \
                     f'<a:HouseArea>{builds[6]}</a:HouseArea><a:HouseBuilding>11</a:HouseBuilding><a:HouseCatg>2</a:HouseCatg><a:HouseFloor>33</a:HouseFloor><a:HouseNumber>44</a:HouseNumber>' \
                     f'<a:HouseStructure>160aab3a-ed6e-455f-8687-1a7c1010f6c0</a:HouseStructure><a:HouseType/><a:HouseTypeID>{builds[7]}</a:HouseTypeID>' \
                     f'<a:HouseUnit>22</a:HouseUnit><a:IsLoan>false</a:IsLoan><a:IsReceipt>false</a:IsReceipt><a:ModelRoomNo>{areacode}</a:ModelRoomNo>' \
                     '<a:OfferGoodsSetID>57e07cd1-481f-4204-855b-e331cfae3eef</a:OfferGoodsSetID><a:OfferTempID i:nil="true"/><a:PaymentStage>1</a:PaymentStage>' \
                     f'<a:ProCatg>0</a:ProCatg><a:Remark/><a:SignAmount>100000</a:SignAmount><a:SignDate>{a_time}+08:00</a:SignDate>' \
                     '<a:TimeLimit>3</a:TimeLimit></contractAdd></ContractAdd></s:Body></s:Envelope>'
            r = requests.post(url, headers=c_head, data=c_body.encode('utf-8'))

            if re.search("<a:IsSuccess>true</a:IsSuccess>", r.text, re.S):
                print(f"客户{n}合同登记成功")
                relateID = re.search("<a:ReturnData>(.*?)</a:ReturnData>", r.text, re.S).group(1)
            else:
                print(r.text)
                raise Exception("合同登记失败！")
            time.sleep(1)
            # 传递1
            url1 = f'https://dv.lantingroup.cn:{self.port}/PC/Workflow/WorkflowService.svc'
            head1 = {'Content-Type': 'text/xml; charset=utf-8',
                     'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                     'Host': f'dv.lantingroup.cn:{self.port}',
                     'Content-Length': '1344',
                     'Expect': '100-continue',
                     'Accept-Encoding': 'gzip, deflate',
                     'Connection': 'Keep-Alive'}
            body1 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
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
                      'Host': f'dv.lantingroup.cn:{self.port}',
                      'Content-Length': '632',
                      'Expect': '100-continue',
                      'Accept-Encoding': 'gzip, deflate'}
            body12 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectFlowLogDetail xmlns="http://tempuri.org/">{self.session}' \
                     f'<flowCatg>2</flowCatg><relateID>{relateID}</relateID></SelectFlowLogDetail></s:Body></s:Envelope>'
            r12 = requests.post(url1, headers=head12, data=body12.encode('utf-8'))
            nodelogid = re.search("<a:NodeLogs>.*?<a:ID>(.*?)</a:ID>", r12.text, re.S).group(1)
            # 新建优惠单
            self.adddiscount(n)
            # 传递2
            head2 = {'Content-Type': 'text/xml; charset=utf-8',
                     'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                     'Host': f'dv.lantingroup.cn:{self.port}',
                     'Content-Length': '1412',
                     'Expect': '100-continue',
                     'Accept-Encoding': 'gzip, deflate',
                     'Connection': 'Keep-Alive'}
            body2 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
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
            body3 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                    '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                    '<a:BackNodeId i:nil="true"/><a:Catg>2</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                    f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
                    f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodelogid2}</a:NodeLogID>' \
                    f'<a:OperResult>4</a:OperResult><a:RelateID>{relateID}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                    '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            requests.post(url1, headers=head2, data=body3.encode('utf-8'))
            # return n,builds[0],relateID,builds[2],desnid,builds[7]
            self.creatoffer(n, builds[0], relateID, builds[2], desnid, builds[7])

    # 合同优惠登记
    def adddiscount(self, na):
        cretime = self.modifydatetime('now')
        cretime2 = self.modifydatetime(minutes=2)
        contid = SQL.selectcontid(na)
        # try:
        #     contid = SQL.selectcontid(n)
        #     contword = f'<a:ContID>{contid}</a:ContID>'
        # except NameError as e:
        #     contword = '<a:ContID i:nil="true"/>'
        appspname = SQL.custfullname(self.LoginStafPosID)
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
        company = SQL.logincompany(self.LoginStafPosID)
        # Amount = count*price chkamount = count*chkprice
        url = f'https://dv.lantingroup.cn:{self.port}/PC/DisCount/DisCountService.svc'
        d_data = {'Content-Type': 'text/xml; charset=utf-8',
                  'SOAPAction': '"http://tempuri.org/IDiscount/AddDiscount"',
                  'Host': f'dv.lantingroup.cn:{self.port}',
                  'Content-Length': '4155',
                  'Expect': '100-continue',
                  'Accept-Encoding': 'gzip, deflate',
                  'Connection': 'Keep-Alive'}
        d_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><AddDiscount xmlns="http://tempuri.org/">{self.session}' \
                 f'<discount xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                 f'<a:CoID>{custid[1]}</a:CoID><a:CoName>{company}</a:CoName><a:CreTime>{cretime}+08:00</a:CreTime><a:ID i:nil="true"/><a:Oper i:nil="true"/>' \
                 f'<a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/><a:UpdtTime>{cretime}+08:00</a:UpdtTime>' \
                 f'<a:AppSpID>{self.LoginStafPosID}</a:AppSpID><a:AppSpName>{appspname[0]}</a:AppSpName><a:Attach i:nil="true"/><a:BudgetID i:nil="true"/>' \
                 f'<a:BudgetName i:nil="true"/><a:FinishTime i:nil="true"/><a:FlowState>1</a:FlowState><a:FlowStateTxt>待提交</a:FlowStateTxt>' \
                 f'<a:IsChkBefore>false</a:IsChkBefore><a:No i:nil="true"/><a:Remark/><a:State>1</a:State><a:StateTxt i:nil="true"/><a:SubmitTime i:nil="true"/>' \
                 f'<a:ApplyDiscDetls i:nil="true"/><a:BldName i:nil="true"/><a:ChkAmount>{discs[3] * discs[4]}</a:ChkAmount><a:ChkRemark i:nil="true"/>' \
                 f'<a:CoDiscDetls i:nil="true"/><a:ContAddr i:nil="true"/><a:ContAmt i:nil="true"/><a:ContDept i:nil="true"/><a:ContID>{contid}</a:ContID>' \
                 f'<a:ContInfo i:nil="true"/><a:ContNo i:nil="true"/><a:CouponDiscDetls i:nil="true"/><a:CustName i:nil="true"/><a:CustNo i:nil="true"/>' \
                 f'<a:CustSource i:nil="true"/><a:CustState>0</a:CustState><a:CustTel i:nil="true"/><a:CustTels i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                 f'<a:CustTelsList i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:DesnName i:nil="true"/><a:DiscAmount>1.00</a:DiscAmount>' \
                 f'<a:DiscDetls><a:SvcDiscDetl><a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{cretime2}+08:00</a:CreTime><a:ID i:nil="true"/><a:Oper i:nil="true"/>' \
                 f'<a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/><a:UpdtTime>{cretime2}+08:00</a:UpdtTime>' \
                 f'<a:Amount>{discs[2] * discs[4]}</a:Amount><a:BackCount>0</a:BackCount><a:ChkAmount>{discs[3] * discs[4]}</a:ChkAmount><a:ChkPrice>{discs[3]}</a:ChkPrice>' \
                 f'<a:ChkRemark i:nil="true"/><a:Content>{discs[1]}</a:Content><a:Count>{discs[4]}</a:Count><a:Counted>0</a:Counted><a:CustAreaName i:nil="true"/>' \
                 f'<a:CustBldName i:nil="true"/><a:CustID i:nil="true"/><a:CustName i:nil="true"/><a:CustNo i:nil="true"/><a:CustSource i:nil="true"/>' \
                 f'<a:CustState>0</a:CustState><a:CustTel i:nil="true"/><a:DiscId i:nil="true"/><a:DiscItemID>9566b79b-af4e-4865-a8cf-f64330a78a4f</a:DiscItemID>' \
                 f'<a:DiscNo i:nil="true"/><a:DiscType>1</a:DiscType><a:FactCount>0</a:FactCount><a:IsChange>false</a:IsChange><a:IsEnjoy>true</a:IsEnjoy>' \
                 f'<a:IsOut>false</a:IsOut><a:Name>{discs[0]}</a:Name><a:Price>{discs[2]}</a:Price><a:ProdCatg>{prodname[1]}</a:ProdCatg><a:ProdDesc i:nil="true"/>' \
                 f'<a:ProdID i:nil="true"/><a:ProdModel i:nil="true"/><a:ProdName>{prodname[0]}</a:ProdName><a:ProdNo i:nil="true"/><a:ProdSpec i:nil="true"/>' \
                 f'<a:ProdUnit i:nil="true"/><a:Remark i:nil="true"/><a:State>0</a:State><a:StockCount>0</a:StockCount><a:StockID i:nil="true"/><a:StockName i:nil="true"/>' \
                 f'<a:StockStateName i:nil="true"/><a:Subject i:nil="true"/><a:TheoryChkAmount>0</a:TheoryChkAmount></a:SvcDiscDetl></a:DiscDetls><a:DiscSetID>{discs[5]}</a:DiscSetID>' \
                 f'<a:DiscSetName i:nil="true"/><a:IsAlterSignTxt i:nil="true"/><a:IsCheck i:nil="true"/><a:LiveDiscDetls i:nil="true"/><a:MeetCustID>{custid[0]}</a:MeetCustID>' \
                 f'<a:OfferAmt>0</a:OfferAmt><a:ProductType>0</a:ProductType><a:SignDate i:nil="true"/></discount></AddDiscount></s:Body></s:Envelope>'
        r = requests.post(url, headers=d_data, data=d_body.encode('utf-8'))

        if re.search("<IsSuccess.*?true</IsSuccess>", r.text, re.S):
            print(f"客户{na}优惠登记成功")
            relateid = re.search("<a:ID>(.*?)</a:ID>", r.text, re.S).group(1)
        elif re.search(".*?已被其它优惠单", r.text, re.S):
            return
        else:
            pprint.pprint(r.text)
            raise Exception("合同优惠登记失败！")
        # 传递1
        c_url = f'https://dv.lantingroup.cn:{self.port}/PC/Workflow/WorkflowService.svc'
        c_head = {'Content-Type': 'text/xml; charset=utf-8',
                  'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                  'Host': f'dv.lantingroup.cn:{self.port}',
                  'Content-Length': '1345',
                  'Expect': '100-continue',
                  'Accept-Encoding': 'gzip, deflate',
                  'Connection': 'Keep-Alive'}
        c_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
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
        c_body1 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectFlowLogDetail xmlns="http://tempuri.org/">{self.session}' \
                  f'<flowCatg>54</flowCatg><relateID>{relateid}</relateID></SelectFlowLogDetail></s:Body></s:Envelope>'
        r2 = requests.post(c_url, headers=c_head1, data=c_body1.encode('utf-8'))
        nodelogid = re.search("<a:NodeLogs>.*?<a:ID>(.*?)</a:ID>", r2.text, re.S).group(1)
        # 传递2
        c_head2 = {'Content-Type': 'text/xml; charset=utf-8',
                   'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                   'Host': f'dv.lantingroup.cn:{self.port}',
                   'Content-Length': '1413',
                   'Expect': '100-continue',
                   'Accept-Encoding': 'gzip, deflate',
                   'Connection': 'Keep-Alive'}
        c_body2 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                  '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                  '<a:BackNodeId i:nil="true"/><a:Catg>54</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                  f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
                  f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodelogid}</a:NodeLogID>' \
                  f'<a:OperResult>4</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                  '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
        requests.post(c_url, headers=c_head2, data=c_body2.encode('utf-8'))

    # 开工预案申请
    def contstartplanadd(self, names):
        if type(names) == int:
            self.contactadd(names)
        else:
            self.kehu = names
        for n in self.kehu:
            contid = SQL.selectcontid(n)
            handtime = self.modifydatetime(days=3)
            opers = SQL.getopers(self.LoginStafPosID)
            session1 = '<request xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:CustomParas i:nil="true"/>' \
                       '<a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight">' \
                       f'<b:LoginStafPosID>{self.LoginStafPosID}</b:LoginStafPosID><b:RegisterID i:nil="true"/><b:SessionID>{self.SessionID}</b:SessionID>' \
                       f'<b:Sign i:nil="true"/><b:UniqueID>{self.UniqueID}</b:UniqueID></a:Session>'
            # 新建保存
            url = f'https://dv.lantingroup.cn:{self.port}/PC/ContStart/ContStartService.svc'
            head = {'Content-Type': 'text/xml; charset=utf-8',
                    'SOAPAction': '"http://tempuri.org/IContStartPlan/ContStartPlanAdd"',
                    'Host': f'dv.lantingroup.cn:{self.port}',
                    'Content-Length': '1268',
                    'Expect': '100-continue',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'Keep-Alive'}
            body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartPlanAdd xmlns="http://tempuri.org/">' \
                   f'{session1}<a:Data><a:AppSpID>{self.LoginStafPosID}</a:AppSpID>' \
                   f'<a:BudgeterId i:nil="true"/><a:ContID>{contid}</a:ContID><a:FloorNum>0</a:FloorNum><a:HandoverOfficerID i:nil="true"/>' \
                   f'<a:HandoverTime>{handtime}</a:HandoverTime><a:HouseTypeID i:nil="true"/><a:IsSubCont i:nil="true"/><a:PMDptMgrID i:nil="true"/><a:PMID i:nil="true"/>' \
                   '<a:PlanRemark/><a:SpaceDesignerSpId i:nil="true"/><a:SupervisorID i:nil="true"/></a:Data></request></ContStartPlanAdd></s:Body></s:Envelope>'
            r = requests.post(url, headers=head, data=body.encode('utf-8'))
            if re.search("<IsSuccess.*?true</IsSuccess>", r.text, re.S):
                print(f"客户{n}开工预案申请保存成功")
                idd = re.search("<ReturnData.*?>(.*?)</ReturnData>", r.text, re.S).group(1)
            else:
                pprint.pprint(r.text)
                continue
            # 附件保存传递
            head2 = {'Content-Type': 'text/xml; charset=utf-8',
                     'SOAPAction': '"http://tempuri.org/IContStartPlan/ContStartPlanSelectSingle"',
                     'Host': f'dv.lantingroup.cn:{self.port}',
                     'Content-Length': '831',
                     'Expect': '100-continue',
                     'Accept-Encoding': 'gzip, deflate'}
            body2 = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartPlanSelectSingle xmlns="http://tempuri.org/">' \
                    '<input xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                    '<a:CustomParas i:nil="true"/><a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight">' \
                    f'<b:LoginStafPosID>{self.LoginStafPosID}</b:LoginStafPosID><b:RegisterID i:nil="true"/>' \
                    f'<b:SessionID>{self.SessionID}</b:SessionID><b:Sign i:nil="true"/><b:UniqueID>{self.UniqueID}</b:UniqueID></a:Session>' \
                    f'<a:ID i:nil="true"/><a:ContStartPlanId>{idd}</a:ContStartPlanId></input></ContStartPlanSelectSingle></s:Body></s:Envelope>'
            # BudgeterId 预算员 7d64e453-eb73-4d17-871e-b62c0091992c（岚庭家居）
            r = requests.post(url, headers=head2, data=body2.encode('utf-8'))
            ids = re.search(
                "<a:ContStartPlanFattaList>.*?<a:ID>(.*?)</a:ID>.*?<a:ID>(.*?)</a:ID>.*?</a:ContStartPlanFattaList>",
                r.text, re.S)
            id1 = ids.group(1)
            id2 = ids.group(2)
            updatetime = self.modifydatetime('now')  # 1111
            # 第一个流程节点，写入流程任务，房屋层数，房屋类型，保存
            c_head1 = {'Content-Type': 'text/xml; charset=utf-8',
                       'SOAPAction': '"http://tempuri.org/IContStartPlan/ContStartPlanEdit"',
                       'Host': f'dv.lantingroup.cn:{self.port}',
                       'Content-Length': '2912',
                       'Expect': '100-continue',
                       'Accept-Encoding': 'gzip, deflate',
                       'Connection': 'Keep-Alive'}
            c_body1 = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ContStartPlanEdit xmlns="http://tempuri.org/">' \
                      f'{session1}<a:Data><a:AppSpID>{self.LoginStafPosID}</a:AppSpID>' \
                      f'<a:BudgeterId i:nil="true"/><a:ContID>{contid}</a:ContID><a:FloorNum>3</a:FloorNum><a:HandoverOfficerID i:nil="true"/>' \
                      f'<a:HandoverTime>{handtime}</a:HandoverTime><a:HouseTypeID>60d4f93b-82fb-4d76-afdb-f514c46899f1</a:HouseTypeID><a:IsSubCont i:nil="true"/>' \
                      '<a:PMDptMgrID i:nil="true"/><a:PMID i:nil="true"/><a:PlanRemark/><a:SpaceDesignerSpId i:nil="true"/><a:SupervisorID i:nil="true"/><a:ContStartPlanFattaList>' \
                      f'<a:SvcContStartPlanFatta><a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{updatetime}</a:CreTime><a:ID>{id1}</a:ID>' \
                      f'<a:Oper>{opers[1]}</a:Oper><a:OperID>{self.LoginStafPosID}</a:OperID><a:UniqueID>{id1}</a:UniqueID><a:UpdtOper/>' \
                      f'<a:UpdtOperId i:nil="true"/><a:UpdtTime>{updatetime}</a:UpdtTime><a:ContStartPlanID i:nil="true"/><a:DownLoadText>下载</a:DownLoadText><a:FattaNum>0</a:FattaNum>' \
                      '<a:FattaType>2</a:FattaType><a:FattaTypeName>CAD图纸</a:FattaTypeName><a:Images i:nil="true"/><a:Remark i:nil="true"/><a:UpdtTimeTxt/>' \
                      '<a:UploadText>上传</a:UploadText></a:SvcContStartPlanFatta><a:SvcContStartPlanFatta><a:CoID i:nil="true"/><a:CoName i:nil="true"/>' \
                      f'<a:CreTime>{updatetime}</a:CreTime><a:ID>{id2}</a:ID><a:Oper>{opers[1]}</a:Oper>' \
                      f'<a:OperID>{self.LoginStafPosID}</a:OperID><a:UniqueID>{id2}</a:UniqueID><a:UpdtOper/><a:UpdtOperId i:nil="true"/>' \
                      f'<a:UpdtTime>{updatetime}</a:UpdtTime><a:ContStartPlanID i:nil="true"/><a:DownLoadText>下载</a:DownLoadText><a:FattaNum>0</a:FattaNum><a:FattaType>1</a:FattaType>' \
                      '<a:FattaTypeName>开工交底单</a:FattaTypeName><a:Images i:nil="true"/><a:Remark i:nil="true"/><a:UpdtTimeTxt/><a:UploadText>上传</a:UploadText></a:SvcContStartPlanFatta>' \
                      f'</a:ContStartPlanFattaList><a:ID>{idd}</a:ID></a:Data></request></ContStartPlanEdit></s:Body></s:Envelope>'
            c1 = requests.post(url, headers=c_head1, data=c_body1.encode('utf-8'))
            print('C1:' + c1.text)
            flow_url = f'https://dv.lantingroup.cn:{self.port}/PC/Workflow/WorkflowService.svc'
            c_head12 = {'Content-Type': 'text/xml; charset=utf-8',
                        'SOAPAction': '"http://tempuri.org/IWorkflow/SelectFlowLogDetail"',
                        'Host': f'dv.lantingroup.cn:{self.port}',
                        'Content-Length': '634',
                        'Expect': '100-continue',
                        'Accept-Encoding': 'gzip, deflate'
                        }
            c_head13 = c_head12.copy()
            c_head13['SOAPAction'] = '"http://tempuri.org/IWorkflowBase/FlowOper"'
            c_head13['Content-Length'] = '1346'
            c_body13 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                       '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                       '<a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                       '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID i:nil="true"/>' \
                       '<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID i:nil="true"/><a:OperResult>2</a:OperResult>' \
                       f'<a:RelateID>{idd}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                       '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            # 传递1，进入第二个节点，质检部确认质检员
            c13 = requests.post(flow_url, headers=c_head13, data=c_body13.encode('utf-8'))
            print('C13:' + c13.text)
            nodeids = SQL.get_flow('质检部确定质检员')
            logid = nodeids[0]
            nodeid = nodeids[1]
            ht = int(time.mktime(time.strptime(handtime.replace("T", ' ')[:-7], "%Y-%m-%d %H:%M:%S"))) * 1000
            ht2 = int(time.mktime(time.strptime(updatetime.replace("T", ' ')[:-7], "%Y-%m-%d %H:%M:%S"))) * 1000
            # HandoverOfficerID:工地交接员
            with open("bodydata.json", "r", encoding='utf-8') as f:
                d = json.load(f)
                d["yuan"]['AppSpID'] = str(self.LoginStafPosID)
                d["yuan"]['ContID'] = str(contid)
                d["yuan"]['HandoverTime'] = rf"/Date({ht}+0800)/"
                d["yuan"]['ContStartPlanFattaList'][0]["CreTime"] = rf"/Date({ht2}+0800)/"
                d["yuan"]['ContStartPlanFattaList'][0]["ID"] = str(id1)
                d["yuan"]['ContStartPlanFattaList'][0]["Oper"] = str(opers[1])
                d["yuan"]['ContStartPlanFattaList'][0]["OperID"] = self.LoginStafPosID
                d["yuan"]['ContStartPlanFattaList'][0]["UniqueID"] = str(id1)
                d["yuan"]['ContStartPlanFattaList'][0]["UpdtTime"] = rf"/Date({ht2}+0800)/"
                d["yuan"]['ContStartPlanFattaList'][1]["CreTime"] = rf"/Date({ht2}+0800)/"
                d["yuan"]['ContStartPlanFattaList'][1]["ID"] = str(id2)
                d["yuan"]['ContStartPlanFattaList'][1]["Oper"] = str(opers[1])
                d["yuan"]['ContStartPlanFattaList'][1]["OperID"] = str(self.LoginStafPosID)
                d["yuan"]['ContStartPlanFattaList'][1]["UniqueID"] = str(id2)
                d["yuan"]['ContStartPlanFattaList'][1]["UpdtTime"] = rf"/Date({ht2}+0800)/"
                d["yuan"]['ID'] = idd
                task = json.dumps(d["yuan"])
                taskdata = task.replace('/', '\/')
            c_head2 = {'Content-Type': 'text/xml;charset=utf-8',
                       'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                       'Host': f'dv.lantingroup.cn:{self.port}',
                       'Content-Length': '3014',
                       'Expect': '100-continue',
                       'Accept-Encoding': 'gzip, deflate',
                       'Connection': 'Keep-Alive'
                       }
            c_body2 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                      '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                      '<a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc i:nil="true"/>' \
                      f'<a:LogID>{logid}</a:LogID><a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/>' \
                      f'<a:NodeLogID>{nodeid}</a:NodeLogID><a:OperResult>0</a:OperResult><a:RelateID>{idd}</a:RelateID>' \
                      f'<a:Summary i:nil="true"/><a:TaskDataStr>{taskdata}</a:TaskDataStr><a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      '<a:Urgency>0</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            # 第二个节点完成流程任务，保存
            requests.post(flow_url, headers=c_head2, data=c_body2.encode('utf-8'))
            # 传递2,进入第三个节点工程部确认装修管家
            c_head13['Content-Length'] = '1414'  # 借用c_head13
            c_body = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{Session}
            <flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>
            <a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{LogID}</a:LogID>
            <a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{NodeID}</a:NodeLogID>
            <a:OperResult>4</a:OperResult><a:RelateID>{RelateID}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>
            <a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>"""

            c_body21 = c_body.format(Session=self.session, LogID=logid, NodeID=nodeid, RelateID=idd)
            c2 = requests.post(flow_url, headers=c_head13, data=c_body21.encode('utf-8'))
            print('C2:' + c2.text)
            # 第三个节点工程部确认装修管家内，写入流程任务
            d["yuan"]['HandoverOfficerID'] = "ffc42188-8bff-4820-bd1d-3a78d13dc948"
            d["yuan"]['IsSubCont'] = True
            task = json.dumps(d["yuan"])
            taskdata = task.replace('/', '\/')
            nodeids = SQL.get_flow('工程部确定装修管家')
            nodeid2 = nodeids[1]
            c_head3 = {'Content-Type': 'text/xml;charset=utf-8',
                       'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                       'Host': f'dv.lantingroup.cn:{self.port}',
                       'Content-Length': '3014',
                       'Expect': '100-continue',
                       'Accept-Encoding': 'gzip, deflate',
                       'Connection': 'Keep-Alive'
                       }
            c_body3 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                      '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                      '<a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc i:nil="true"/>' \
                      f'<a:LogID>{logid}</a:LogID><a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/>' \
                      f'<a:NodeLogID>{nodeid2}</a:NodeLogID><a:OperResult>0</a:OperResult><a:RelateID>{idd}</a:RelateID>' \
                      f'<a:Summary i:nil="true"/><a:TaskDataStr>{taskdata}</a:TaskDataStr><a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      '<a:Urgency>0</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            # 保存，流程任务,输入分包，装修管家
            c3 = requests.post(flow_url, headers=c_head3, data=c_body3.encode('utf-8'))
            print('C3:' + c3.text)
            # 传递3，进入设计师上传附件节点
            c_body31 = c_body.format(Session=self.session, LogID=logid, NodeID=nodeid2, RelateID=idd)
            c31 = requests.post(flow_url, headers=c_head13, data=c_body31.encode('utf-8'))
            print('C31:' + c31.text)
            # 第四个节点设计师上传附件内，上传图片
            url1 = f"https://dv.lantingroup.cn:{port}/PC/General/GeneralService.svc"
            header1 = {
                'Content-Type': 'text/xml;charset=utf-8',
                'SOAPAction': '"http://tempuri.org/IFileRecord/AddFileRecord"',
                'Host': f'dv.lantingroup.cn:{self.port}',
                'Content-Length': '1080',
                'Expect': '100-continue',
                'Accept-Encoding': 'gzip, deflate'
            }
            uptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for pic_type, pic_name, suffixname in ([1, '1623048597(1) - 副本', 'jpg'], [2, '1623048597副本', 'dwg']):
                relateid = SQL.pic_relateid(contid, pic_type)
                body1 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><AddFileRecord xmlns="http://tempuri.org/">{self.session}' \
                        '<fileRecord xmlns:a="http://schemas.datacontract.org/2004/07/Base.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                        f'<a:Catg>50</a:Catg><a:Desc>{pic_name}</a:Desc><a:Height>640</a:Height><a:ID i:nil="true"/><a:Name>{pic_name}</a:Name><a:OperID i:nil="true"/>' \
                        f'<a:OperTime i:nil="true"/><a:Path i:nil="true"/><a:RelateID>{relateid}</a:RelateID><a:Size>61239</a:Size><a:SuffixName>{suffixname}</a:SuffixName>' \
                        '<a:Type>2</a:Type><a:UniqueID i:nil="true"/><a:Width>958</a:Width></fileRecord></AddFileRecord></s:Body></s:Envelope>'
                requests.post(url1, headers=header1, data=body1.encode('utf-8'))
            nodeids = SQL.get_flow('设计师上传附件')
            nodeid3 = nodeids[1]
            d["yuan"]['IsOrderGrabbing'] = True
            d["yuan"]['ContStartPlanFattaList'][0]["UpdtOper"] = str(opers[1])
            d["yuan"]['ContStartPlanFattaList'][0]["UpdtOperId"] = self.LoginStafPosID
            d["yuan"]['ContStartPlanFattaList'][0]["FattaNum"] = 1
            d["yuan"]['ContStartPlanFattaList'][0]["UpdtTimeTxt"] = str(uptime)
            d["yuan"]['ContStartPlanFattaList'][1]["UpdtOper"] = str(opers[1])
            d["yuan"]['ContStartPlanFattaList'][1]["UpdtOperId"] = self.LoginStafPosID
            d["yuan"]['ContStartPlanFattaList'][1]["FattaNum"] = 1
            d["yuan"]['ContStartPlanFattaList'][1]["UpdtTimeTxt"] = str(uptime)
            task = json.dumps(d["yuan"])
            taskdata = task.replace('/', '\/')
            c_head4 = {
                'Content-Type': 'text/xml;charset=utf-8',
                'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                'Host': f'dv.lantingroup.cn:{self.port}',
                'Content-Length': '3138',
                'Expect': '100-continue',
                'Accept-Encoding': 'gzip, deflate'
            }
            c_body4 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                      '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                      '<a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc i:nil="true"/>' \
                      f'<a:LogID>{logid}</a:LogID><a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/>' \
                      f'<a:NodeLogID>{nodeid3}</a:NodeLogID><a:OperResult>0</a:OperResult><a:RelateID>{idd}</a:RelateID><a:Summary i:nil="true"/>' \
                      f'<a:TaskDataStr>{taskdata}</a:TaskDataStr><a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      '<a:Urgency>0</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            # 写入流程任务，保存
            c4 = requests.post(flow_url, headers=c_head4, data=c_body4.encode('utf-8'))
            print('C4:' + c4.text)
            # 传递4进入成控部审核
            c_head4['Content-Length'] = '1414'
            # c_body41 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
            #            '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
            #            '<a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
            #            f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
            #            f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodeid2}</a:NodeLogID>' \
            #            f'<a:OperResult>4</a:OperResult><a:RelateID>{idd}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
            #            '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            c_body41 = c_body.format(Session=self.session, LogID=logid, NodeID=nodeid3, RelateID=idd)
            c41 = requests.post(flow_url, headers=c_head4, data=c_body41.encode('utf-8'))
            print('C41:' + c41.text)
            # 传递5（成控部审核节点内进行），进入分配预算员节点（成控部审核节点无流程任务，直接传递）
            nodeids = SQL.get_flow('成控部审核')
            nodeid4 = nodeids[1]
            c_body5 = c_body.format(Session=self.session, LogID=logid, NodeID=nodeid4, RelateID=idd)
            w = requests.post(flow_url, headers=c_head4, data=c_body5.encode('utf-8'))
            print(w.text)
            # 第六个节点，成控部分配预算员内，执行流程任务分配预算员
            nodeids = SQL.get_flow('成控部分配预算员')
            nodeid5 = nodeids[1]
            d['yuan']['BudgeterId'] = "3617f2fd-a87b-4a0a-ae0e-4dc3697f8578"
            task = json.dumps(d["yuan"])
            taskdata = task.replace('/', '\/')
            c_head6 = {
                'Content-Type': 'text/xml;charset=utf-8',
                'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                'Host': f'dv.lantingroup.cn:{self.port}',
                'Content-Length': '3138',
                'Expect': '100-continue',
                'Accept-Encoding': 'gzip, deflate'
            }
            c_body6 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                      '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                      '<a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc i:nil="true"/>' \
                      f'<a:LogID>{logid}</a:LogID><a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/>' \
                      f'<a:NodeLogID>{nodeid5}</a:NodeLogID><a:OperResult>0</a:OperResult><a:RelateID>{idd}</a:RelateID><a:Summary i:nil="true"/>' \
                      f'<a:TaskDataStr>{taskdata}</a:TaskDataStr><a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      '<a:Urgency>0</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            requests.post(flow_url, headers=c_head6, data=c_body6.encode('utf-8'))
            c_body51 = c_body.format(Session=self.session, LogID=logid, NodeID=nodeid5, RelateID=idd)
            # 传递6，进入内部工期节点
            c51 = requests.post(flow_url, headers=c_head4, data=c_body51.encode('utf-8'))
            print('C51:' + c51.text)
            # 传递7，完成流程
            nodeids = SQL.get_flow('内部工期')
            nodeid6 = nodeids[1]
            d['yuan']['InsideTimeLimit'] = 12
            task = json.dumps(d["yuan"])
            taskdata = task.replace('/', '\/')
            c_head6['Content-Length'] = '3007'
            c_body7 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                      '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                      '<a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      '<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc i:nil="true"/>' \
                      f'<a:LogID>{logid}</a:LogID><a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/>' \
                      f'<a:NodeLogID>{nodeid6}</a:NodeLogID><a:OperResult>0</a:OperResult><a:RelateID>{idd}</a:RelateID><a:Summary i:nil="true"/>' \
                      f'<a:TaskDataStr>{taskdata}</a:TaskDataStr><a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                      '<a:Urgency>0</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
            requests.post(flow_url, headers=c_head6, data=c_body7.encode('utf-8'))
            c_body51 = c_body.format(Session=self.session, LogID=logid, NodeID=nodeid6, RelateID=idd)
            c51 = requests.post(flow_url, headers=c_head4, data=c_body51.encode('utf-8'))
            print('C51:' + c51.text)
            # 流程通知
            nodeids = SQL.get_flow('工程部确定装修管家')
            nodeid7 = nodeids[1]
            tbody = f"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}
                        <flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
                        <a:BackNodeId i:nil="true"/><a:Catg>406</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>
                        <a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>
                        <a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodeid7}</a:NodeLogID>
                        <a:OperResult>7</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>
                        <a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>0</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>"""
            t = requests.post(flow_url, headers=c_head13, data=tbody.encode('utf-8'))
            print('t:' + t.text)
            t2_head = {
                'Content-Type': 'text/xml;charset=utf-8',
                'SOAPAction': '"http://tempuri.org/IWorkflow/SelectFlowLogDetail"',
                'Host': f'dv.lantingroup.cn:{self.port}',
                'Content-Length': '634',
                'Expect': '100-continue',
                'Accept-Encoding': 'gzip, deflate'
            }
            t2_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectFlowLogDetail xmlns="http://tempuri.org/">{self.session}' \
                      f'<flowCatg>406</flowCatg><relateID>{relateid}</relateID></SelectFlowLogDetail></s:Body></s:Envelope>'
            t2 = requests.post(flow_url, headers=t2_head, data=t2_body.encode('utf-8'))

    # 设计积分取消
    def designintegralcancel(self, jfd):
        dsgnintegralid = SQL.degnintegralid(jfd)
        cretime = self.modifydatetime('now')
        url = f'https://dv.lantingroup.cn:{self.port}/PC/DsgnManagement/DsgnManagementService.svc'
        head = {'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': '"http://tempuri.org/IDesignIntegralCanel/AddDesignIntegralCanel"',
                'Host': f'dv.lantingroup.cn:{self.port}',
                'Content-Length': '1818',
                'Expect': '100-continue',
                'Accept-Encoding': 'gzip, deflate'}
        body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><AddDesignIntegralCanel xmlns="http://tempuri.org/">' \
               '<request xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
               '<a:CustomParas i:nil="true"/><a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight">' \
               f'<b:LoginStafPosID>{self.LoginStafPosID}</b:LoginStafPosID><b:RegisterID i:nil="true"/><b:SessionID>{self.SessionID}</b:SessionID>' \
               f'<b:Sign i:nil="true"/><b:UniqueID>{self.SessionID}</b:UniqueID></a:Session>' \
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
        c_url = f'https://dv.lantingroup.cn:{self.port}/PC/Workflow/WorkflowService.svc'
        c_head = {'Content-Type': 'text/xml; charset=utf-8',
                  'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                  'Host': 'dv.lantingroup.cn:8075',
                  'Content-Length': '1346',
                  'Expect': '100-continue',
                  'Accept-Encoding': 'gzip, deflate',
                  'Connection': 'Keep-Alive'}
        c_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
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
        c_body1 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectFlowLogDetail xmlns="http://tempuri.org/">{self.session}' \
                  f'<flowCatg>317</flowCatg><relateID>{relateid}</relateID></SelectFlowLogDetail></s:Body></s:Envelope>'

        r2 = requests.post(c_url, headers=c_head1, data=c_body1.encode('utf-8'))
        nodelogid = re.search("<a:NodeLogs>.*?<a:ID>(.*?)</a:ID>", r2.text, re.S).group(1)
        # 第二次传递
        c2_head = {'Content-Type': 'text/xml; charset=utf-8',
                   'SOAPAction': '"http://tempuri.org/IWorkflowBase/FlowOper"',
                   'Host': f'dv.lantingroup.cn:{self.port}',
                   'Content-Length': '1414',
                   'Expect': '100-continue',
                   'Accept-Encoding': 'gzip, deflate',
                   'Connection': 'Keep-Alive'}
        c2_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                  '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                  '<a:BackNodeId i:nil="true"/><a:Catg>317</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                  f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
                  f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodelogid}</a:NodeLogID>' \
                  f'<a:OperResult>4</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                  '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
        requests.post(c_url, headers=c2_head, data=c2_body.encode('utf-8'))
        # 获取第三次传递需要的一些ID
        c2_body2 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><SelectFlowLogDetail xmlns="http://tempuri.org/">{self.session}' \
                   f'<flowCatg>317</flowCatg><relateID>{relateid}</relateID></SelectFlowLogDetail></s:Body></s:Envelope>'
        r3 = requests.post(c_url, headers=c_head1, data=c2_body2.encode('utf-8'))
        nodelogid2 = re.search("<a:NodeLogs>.*?<a:ID>(.*?)</a:ID>", r3.text, re.S).group(1)
        # 第三次传递
        c3_body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><FlowOper xmlns="http://tempuri.org/">{self.session}' \
                  '<flowOperPara xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.Workflow" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
                  '<a:BackNodeId i:nil="true"/><a:Catg>317</a:Catg><a:CopyLogIDs i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/>' \
                  f'<a:Copyers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:Desc/><a:LogID>{logid}</a:LogID>' \
                  f'<a:NewHandlers i:nil="true" xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.Organization"/><a:NodeLogID>{nodelogid2}</a:NodeLogID>' \
                  f'<a:OperResult>4</a:OperResult><a:RelateID>{relateid}</a:RelateID><a:Summary i:nil="true"/><a:TaskDataStr i:nil="true"/>' \
                  '<a:TaskIds i:nil="true" xmlns:b="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><a:Urgency>1</a:Urgency></flowOperPara></FlowOper></s:Body></s:Envelope>'
        requests.post(c_url, headers=c2_head, data=c3_body.encode('utf-8'))

    # 新建工作联络单
    def creatliaison(self):
        cretime = self.modifydatetime('now')
        requirdate = self.modifydatetime('date')
        posid = "8ca150bf-7cea-4d0a-a3c4-b650226c71b1"  # SQL.liaisondsgnid()
        liaisontype = SQL.liaisontype()
        appspname = SQL.getopers(self.LoginStafPosID)
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
        body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><AddLiaison xmlns="http://tempuri.org/">{self.session}' \
               '<liaison xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
               f'<a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{cretime}+08:00</a:CreTime><a:ID i:nil="true"/><a:Oper i:nil="true"/>' \
               f'<a:OperID i:nil="true"/><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/><a:UpdtTime>{cretime}+08:00</a:UpdtTime>' \
               f'<a:ActualDate i:nil="true"/><a:AppSpID>{self.LoginStafPosID}</a:AppSpID><a:AppSpName>{appspname[1]}</a:AppSpName><a:Attach/><a:ContAddr i:nil="true"/>' \
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

    def cailiao(self):
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
    def sitecompl(self, n):
        oper = SQL.getopers(self.LoginStafPosID)
        cretime = self.modifydatetime('now')
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
        body = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><AddPCSiteCmpl xmlns="http://tempuri.org/">{self.session}' \
               '<siteCmpl xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
               f'<a:CoID i:nil="true"/><a:CoName i:nil="true"/><a:CreTime>{cretime}+08:00</a:CreTime><a:ID i:nil="true"/><a:Oper>{oper}</a:Oper>' \
               f'<a:OperID>{self.LoginStafPosID}</a:OperID><a:UniqueID i:nil="true"/><a:UpdtOper i:nil="true"/><a:UpdtOperId i:nil="true"/>' \
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

    # 关闭窗口
    def gui_close(self, img):
        i = 0
        key = False
        while True:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if location is not None:
                key = True
                pyautogui.click(location.x, location.y, clicks=1, interval=0.2, duration=0.2, button="left")
                # time.sleep(1)
                continue
            if key:
                break
            print(f"未找到匹配图片 {img},1秒后重试")
            i += 1
            if i > 8:
                os.system("pause")
            time.sleep(1)

    # 上传图片
    def upload_pic(self, IMSwindow, page, loc, pic_name):
        page.DataItemControl(Depth=2, Name=loc).Click(simulateMove=False)
        pics_add = IMSwindow.WindowControl(searchDepth=1, Name='添加文件').ToolBarControl(Depth=7,
                                                                                      Name='Custom 2').ButtonControl(
            searchDepth=1, Name='添加')
        pics_add.Click(simulateMove=False)
        IMSwindow.WindowControl(searchDepth=1, Name='添加文件').EditControl(Depth=4, Name='文件名(N):').SendKeys(
            pic_name)
        IMSwindow.WindowControl(searchDepth=1, Name='添加文件').WindowControl(searchDepth=1, Name='打开').ButtonControl(
            searchDepth=1, Name='打开(O)').Click(simulateMove=False)
        IMSwindow.WindowControl(searchDepth=1, Name='添加文件').ButtonControl(Depth=4, Name='保存').Click(
            simulateMove=False)

    # 使用uiautomation新建开工预案单
    def contstartplanadd_ui(self, names):
        ui.uiautomation.SetGlobalSearchTimeout(10)
        now_time = datetime.datetime.now()
        tom = now_time + datetime.timedelta(days=3)
        toms = tom.strftime("%Y-%m-%d %H:%M:%S")
        IMSwindow = ui.WindowControl(searchDepth=1, Name="毛伟人 岚庭ERP ")

        if first:
            self.check_ims_exists()
            # time.sleep(3)
            if IMSwindow.TextControl(Depth=3, SubName='你有').Exists(maxSearchSeconds=3):
                IMSwindow.ButtonControl(Depth=3, Name='马上处理').Click(simulateMove=False)
            IMSwindow.SetActive()
            IMSwindow.EditControl(Depth=6, AutomationId="teSearch").GetValuePattern().SetValue("开工预案申请")
            IMSwindow.Click(50, 130, simulateMove=False)
            # time.sleep(3)
        yuanliebiao = IMSwindow.PaneControl(Depth=3, AutomationId='UCContStartPlan')
        yuanliebiao.ButtonControl(Depth=7, Name="新建").Click(simulateMove=False)
        time.sleep(3)

        kaigong = IMSwindow.PaneControl(Depth=3, AutomationId="UCContStartPlanDetail")

        hetong = kaigong.EditControl(Depth=4, AutomationId="hlinkCont")

        hetong.Click(simulateMove=False)
        IMSwindow.EditControl(Depth=3, AutomationId='tbxCustName').SendKeys(names)
        ui.SendKeys('{Enter}')
        IMSwindow.WindowControl(searchDepth=1, Name='合同选择').ButtonControl(Depth=5, Name='选择').Click(simulateMove=False)
        kaigong.PaneControl(Depth=4, AutomationId='myTime').SendKeys(toms)
        save = kaigong.ButtonControl(Depth=5, Name='保存')
        save.Click(simulateMove=False)
        if IMSwindow.WindowControl(searchDepth=1, Name='提示框').TextControl(searchDepth=1,
                                                                          SubName='该合同已存在有效的开工预案申请').Exists(
                maxSearchSeconds=1):
            print(f"合同{names}已存在有效的开工预案申请")
            ui.SendKeys("{Space}")
            self.gui_close('img.png')
            ui.SendKeys("{Space}")
            return
        # IMSwindow.WindowControl(searchDepth=1, Name='提示框').ButtonControl(searchDepth=1, Name='确定').Click()
        ui.SendKeys("{Space}")

        detail = kaigong.PaneControl(Depth=3, Name='The XtraLayoutControl')
        # 输入房屋层数
        detail.EditControl(searchDepth=1, AutomationId='tbxFloorNum').SendKeys('3')
        detail.EditControl(searchDepth=1, AutomationId='hlinkHouseType').Click(simulateMove=False)
        # 输入房屋类型
        IMSwindow.WindowControl(searchDepth=1, Name='请选择').EditControl(Depth=6, AutomationId='txtKeywords').SendKeys(
            '精装房')
        IMSwindow.TreeItemControl(Depth=10, Name='Node0').DataItemControl(searchDepth=1, SubName='名称').Click(-172, -9,
                                                                                                             simulateMove=False)
        IMSwindow.ButtonControl(Depth=6, Name='确定').Click(simulateMove=False)

        chuandi = kaigong.ButtonControl(Depth=5, Name='传递')

        chuandi.Click(simulateMove=False)
        ui.SendKeys("{Space}")
        ui.SendKeys("{Space}")
        # 输入质检员
        detail.EditControl(searchDepth=1, AutomationId='hlinkSupervisor').Click(simulateMove=False)
        tank = IMSwindow.PaneControl(Depth=2, Name='The XtraLayoutControl')
        tank.EditControl(searchDepth=1, AutomationId='myKey').SendKeys('刘映新')
        ui.SendKeys("{Enter}")
        tank.ButtonControl(searchDepth=1, AutomationId='myConfirm').Click(simulateMove=False)
        # 输入区域代码
        detail.EditControl(searchDepth=1, AutomationId='tbxAreaCode').SendKeys('435322')
        chuandi.Click(simulateMove=False)
        ui.SendKeys("{Space}")
        ui.SendKeys("{Space}")
        # 是否分包
        detail.EditControl(searchDepth=1, AutomationId='isSubCont').SendKeys('否')
        # 点击输入装修管家 小陈装修管家
        detail.EditControl(searchDepth=1, AutomationId='hlinkHandoverOfficer').Click(simulateMove=False)
        a = IMSwindow.WindowControl(searchDepth=1, AutomationId='FrmUserControlContainer').PaneControl(searchDepth=1,
                                                                                                       AutomationId='pnlContainer')
        a.PaneControl(Depth=2, AutomationId='layoutControl1').EditControl(searchDepth=1,
                                                                          AutomationId='myStfName').SendKeys('王金贵')
        ui.SendKeys("{Enter}")
        staffpos = a.PaneControl(Depth=2, AutomationId='myStaffTablePanel').CustomControl(Depth=2, Name='Data Panel')
        for s in staffpos.GetChildren():
            pos_name = s.DataItemControl(searchDepth=1, SubName='员工姓名').GetValuePattern().Value
            pos_status = s.DataItemControl(searchDepth=1, SubName='职位状态').GetValuePattern().Value
            if pos_name.startswith("【岚庭家居】") and pos_status == "正式":
                s.Click(simulateMove=False)
                a.PaneControl(Depth=2, AutomationId='myStaffToolBarPanel').PaneControl(searchDepth=1,
                                                                                       AutomationId='UCBase').ButtonControl(
                    Depth=3, name='选择').Click(simulateMove=False)
        chuandi.Click(simulateMove=False)
        ui.SendKeys("{Space 2}")
        while True:
            tree = detail.CustomControl(Depth=5, Name='Data Panel')
            dp = detail.TabControl(searchDepth=1, AutomationId='xtraTabControl1').CustomControl(Depth=4,
                                                                                                Name='Data Panel')
            if dp.Exists():
                break
        for r, depth in ui.WalkControl(tree, includeTop=False, maxDepth=1):
            # if not isinstance(r, ui.CustomControl):
            #     continue
            item = r.GetFirstChildControl().GetValuePattern().Value
            if item == 'CAD图纸':
                self.upload_pic(IMSwindow, dp, '上传图片 row 0', '处理描述 - 副本.dwg')
                self.upload_pic(IMSwindow, dp, '上传图片 row 1', '1122.jpg')
            else:
                self.upload_pic(IMSwindow, dp, '上传图片 row 0', '1122.jpg')
                self.upload_pic(IMSwindow, dp, '上传图片 row 1', '处理描述 - 副本.dwg')
            break
        chuandi.Click(simulateMove=False)
        ui.SendKeys("{Space}")
        ui.SendKeys("{Space}")
        ui.SendKeys("{Space 3}")
        if IMSwindow.WindowControl(searchDepth=1, Name='流程传递操作').TextControl(Depth=2,
                                                                             Name='合同报价单未提交，请先提交报价再进行传递！').Exists(
            maxSearchSeconds=1):
            print("提交报价单")
            self.baojiadan(names, )

        detail.EditControl(searchDepth=1, AutomationId='tbxBudgetor').Click(simulateMove=False)
        IMSwindow.WindowControl(searchDepth=1, Name='预算员选择').ButtonControl(Depth=5, Name='选择').Click(simulateMove=False)
        chuandi.Click(simulateMove=False)
        ui.SendKeys("{Space 2}")
        detail.EditControl(searchDepth=1, AutomationId='insideTimeLimit').SendKeys('3')
        chuandi.Click(simulateMove=False)
        ui.SendKeys("{Space 2}")
        time.sleep(1)

        self.gui_close('img.png')

    # 判断IMS是否已经打开
    @staticmethod
    def check_ims_exists():
        if not ui.WindowControl(searchDepth=1, Name="毛伟人 岚庭ERP ").Exists(2):
            subprocess.Popen(r'F:\test\TestClient\IMS\release_6\LandErp.Client.exe')
            imswindow = ui.WindowControl(searchDepth=1, Name="Land IMS 1.3.2")
            imswindow.EditControl(Name="账号:").SendKeys("01210281")
            imswindow.EditControl(Name="密码:").SendKeys("a1234567890")
            imswindow.ButtonControl(Name="登录").Click(simulateMove=False)

    # 新建报价单(UI)
    def baojiadan(self, name, jiaju=True, *args):
        ui.uiautomation.SetGlobalSearchTimeout(10)
        if jiaju:
            args_list = ["毛伟人 岚庭ERP ", '岚庭家居', '测试报价产品报价模板']
        else:
            args_list = ["幸福毛经理 岚庭ERP ", '幸福魔方', '测试V+整装']
        imswindow = ui.WindowControl(searchDepth=1, Name=args_list[0])
        if first:
            self.check_ims_exists()
            ui.uiautomation.SetGlobalSearchTimeout(5)
            # time.sleep(3)
            if imswindow.TextControl(Depth=3, SubName='你有').Exists(maxSearchSeconds=3):
                imswindow.ButtonControl(Depth=3, Name='马上处理').Click(simulateMove=False)
            imswindow.SetActive()
            imswindow.EditControl(Depth=6, AutomationId="teSearch").GetValuePattern().SetValue("报价单")
            imswindow.Click(50, 130, simulateMove=False)
        bjliebiao = imswindow.PaneControl(Depth=3, AutomationId='UCOffer')
        bjliebiao.ButtonControl(Depth=7, Name="新建").Click(waitTime=0.01)
        imswindow.EditControl(Depth=5, AutomationId='hlinkCoName').Click(simulateMove=False)
        imswindow.EditControl(Depth=4, AutomationId='myKey').SendKeys(args_list[1])
        ui.SendKeys("{Enter}")
        imswindow.ButtonControl(Depth=4, Name='确认选择').Click(simulateMove=False)
        imswindow.EditControl(Depth=5, AutomationId='hlinkCustName').Click(simulateMove=False)
        imswindow.EditControl(Depth=7, AutomationId='myName').SendKeys(name)
        ui.SendKeys("{Enter}")
        imswindow.ButtonControl(Depth=9, Name="选择").Click(simulateMove=False)
        key = True
        c_list = {}
        while key:
            tree = imswindow.CustomControl(Depth=7, Name='Data Panel')
            for item, depth in ui.WalkControl(tree, includeTop=False, maxDepth=1):
                if not isinstance(item, ui.CustomControl):
                    continue

                ming = item.DataItemControl(searchDepth=1, SubName='名称').GetValuePattern().Value
                num = item.Name
                c_list[ming] = num
            if args_list[2] in c_list.keys():  # 测试报价产品报价模板
                imswindow.CustomControl(Depth=7, Name='Data Panel').CustomControl(searchDepth=1,
                                                                                  Name=c_list[args_list[2]]).Click(
                    simulateMove=False)
                imswindow.ButtonControl(Depth=6, Name='确定').Click(simulateMove=False)
                break
            elif imswindow.ButtonControl(Depth=8, Name='Page Down').BoundingRectangle.top == 0:
                key = False
                print("没有找到")
                os.system("pause")
            else:
                imswindow.ScrollBarControl(Depth=7, name="scroll bar").GetNextSiblingControl().WheelDown(wheelTimes=25)
        time.sleep(2)
        w1 = imswindow.PaneControl(searchDepth=3, AutomationId='UCOfferFullVEdit').PaneControl(Depth=3,
                                                                                               Name='The XtraLayoutControl').TabControl(
            searchDepth=1, AutomationId='xtraTabControl1')
        w1.PaneControl(searchDepth=2, Name='pnlToolBarFuncArea').ButtonControl(Depth=4, Name='添加').Click(
            simulateMove=False)
        room = imswindow.WindowControl(searchDepth=1, Name='请选择').DataItemControl(Depth=10, Name='名称 row 1')
        l = room.BoundingRectangle.left
        t = room.BoundingRectangle.bottom
        ui.Click(l - 10, t + 10)
        imswindow.WindowControl(searchDepth=1, Name='请选择').ButtonControl(Depth=5, Name='确定').Click(simulateMove=False)
        w1.DataItemControl(Depth=6, SubName='面积').SendKeys('40')
        button_bar = imswindow.PaneControl(searchDepth=3, AutomationId='UCOfferFullVEdit').PaneControl(Depth=3,
                                                                                                       Name='pnlOperate')
        button_bar.ButtonControl(Depth=2, AutomationId='simpleButton保 存').Click(simulateMove=False)
        ui.SendKeys("{Space 2}")
        button_bar.ButtonControl(Depth=2, Name='提交').Click()
        ui.SendKeys("{Space 2}")
        self.gui_close('baojia.jpg')

    def backruleset(self):
        cre_time = self.modifydatetime("now")
        b_url = f'https://dv.lantingroup.cn:{self.port}/PC//SystemSet/BaseSet/BaseSetService.svc'
        B_header = {
            'Content - Type': 'text / xml;charset = utf - 8',
            'SOAPAction': '"http://tempuri.org/IChargebackRuleSet/ChargebackRuleSetAdd"',
            'Host': 'dv.lantingroup.cn:7078',
            'Content - Length': '2188',
            'Expect': '100 -continue',
            'Accept - Encoding': 'gzip, deflate'
        }
        B_body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><ChargebackRuleSetAdd xmlns="http://tempuri.org/"><requestxmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><a:CustomParas i:nil="true"/><a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight"><b:LoginStafPosID>93f35f7c-9853-473d-84fe-a37a48de2844</b:LoginStafPosID><b:RegisterID i:nil="true"/><b:SessionID>be2a5d13-1ac2-4d21-903a-024a261ba023</b:SessionID><b:Sign i:nil="true"/><b:UniqueID>be2a5d13-1ac2-4d21-903a-024a261ba023</b:UniqueID></a:Session><a:Data><a:CoID>09a055c1-4885-47e7-a5ca-7066f16c4537</a:CoID><a:CoName i:nil="true"/><a:CreTime>' \
                 f'{cre_time}+08:00</a:CreTime><a:Creator>幸福毛经理</a:Creator><a:CreatorId>93f35f7c-9853-473d-84fe-a37a48de2844</a:CreatorId><a:ID i:nil="true"/>' \
                 '<a:Noi:nil="true"/><a:Oper>幸福毛经理</a:Oper><a:OperID>93f35f7c-9853-473d-84fe-a37a48de2844</a:OperID><a:UniqueID i:nil="true"/><a:UpdtTime>2022-03-17T10:21:52.015464+08:00</a:UpdtTime><a:IntervalUnit>4</a:IntervalUnit><a:Intervaltime>0</a:Intervaltime><a:IsBack>false</a:IsBack><a:IsRule>true</a:IsRule><a:Remark>备注备注备注备注</a:Remark><a:RuleRemark>&lt;!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"&gt;&#xD;&lt;html xmlns="http://www.w3.org/1999/xhtml"&gt;&#xD;&lt;head&gt;&#xD;&lt;meta http-equiv="Content-Type" content="text/html; charset=utf-8" /&gt;&lt;title&gt;&#xD;&lt;/title&gt;&#xD;&lt;style type="text/css"&gt;&#xD;.cs95E872D0{text-align:left;text-indent:0pt;margin:0pt 0pt 0pt 0pt}&#xD;.cs743615A1{color:#000000;background-color:transparent;font-family:"Microsoft YaHeiUI" ;font-size:11pt;font-weight:normal;font-style:normal;}&#xD;&lt;/style&gt;&#xD;&lt;/head&gt;&#xD;&lt;body&gt;&#xD;&lt;p class="cs95E872D0"&gt;&lt;span class="cs743615A1"&gt;退单规则说明&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&#xD;&lt;/html&gt;</a:RuleRemark><a:State>1</a:State></a:Data></request></ChargebackRuleSetAdd></s:Body></s:Envelope>'

        cmpl = requests.post(b_url, headers=B_header, data=B_body.encode('utf-8'))

    # 新建开工申请(UI)
    def kaigong(self, n):
        ui.uiautomation.SetGlobalSearchTimeout(10)
        imswindow = ui.WindowControl(searchDepth=1, Name="毛伟人 岚庭ERP ")

        if first:
            self.check_ims_exists()
            ui.uiautomation.SetGlobalSearchTimeout(5)
            # time.sleep(3)
            if imswindow.TextControl(Depth=3, SubName='你有').Exists(maxSearchSeconds=3):
                imswindow.ButtonControl(Depth=3, Name='马上处理').Click(simulateMove=False)
            imswindow.SetActive()
            imswindow.EditControl(Depth=6, AutomationId="teSearch").GetValuePattern().SetValue("开工申请")
            imswindow.Click(50, 130, simulateMove=False)
        kaigonglie = imswindow.PaneControl(Depth=3, AutomationId='UCContStart')
        kaigonglie.ButtonControl(Depth=7, Name="新建").Click()
        time.sleep(3)

        kaigongdetail = imswindow.PaneControl(Depth=3, AutomationId='UCContStartDetail')
        layout = kaigongdetail.PaneControl(Depth=3, AutomationId='layoutControl1')

        layout.EditControl(searchDepth=1, AutomationId='hlinkCont').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='合同选择').PaneControl(searchDepth=1,
                                                                        AutomationId='layoutControl1').EditControl(
            searchDepth=1, AutomationId='tbxCustName').SendKeys(n)
        ui.SendKeys("{Enter}")
        imswindow.WindowControl(searchDepth=1, Name='合同选择').PaneControl(searchDepth=1,
                                                                        AutomationId='pnlToolbar').ButtonControl(
            Depth=4, Name="选择").Click()
        layout.EditControl(searchDepth=1, AutomationId='hyldateExpectStartTime').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='预计交底时间选择').CustomControl(Depth=4, Name='Row 3').DoubleClick()

        tool_button = layout.GetNextSiblingControl().GetFirstChildControl()

        tool_button.ButtonControl(searchDepth=1, Name="保存").Click(simulateMove=False)
        ui.SendKeys("{Space}")
        tool_button.ButtonControl(searchDepth=1, Name='选择空间设计师').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='选择空间设计师').EditControl(Depth=2,
                                                                           AutomationId='hlinkSpaceDesigner').Click(
            simulateMove=False)
        ui.SendKeys('6部4组深化设计师')
        ui.SendKeys("{Enter}")
        imswindow.WindowControl(searchDepth=1, Name='选择空间设计师').ButtonControl(Depth=3, Name='确认选择').Click(
            simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='选择空间设计师').ButtonControl(Depth=3, Name='保存').Click(
            simulateMove=False)
        tool_button.ButtonControl(searchDepth=1, Name='设置房屋层数').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='设置房屋层数').EditControl(Depth=2,
                                                                          AutomationId='tbxFloorNum').SendKeys('3')
        imswindow.WindowControl(searchDepth=1, Name='设置房屋层数').ButtonControl(Depth=3, Name='保存').Click(
            simulateMove=False)
        tool_button.ButtonControl(searchDepth=1, Name='传递').Click(simulateMove=False)
        ui.SendKeys("{Space 2}")
        ui.SendKeys("{Space 3}")

        tool_button.ButtonControl(searchDepth=1, Name='分配质检员').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='开工单分配项目监理').EditControl(Depth=2,
                                                                             AutomationId='hlinkSupervisor').Click(
            simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='开工单分配项目监理').ButtonControl(Depth=3, Name='查询').Click(
            simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='开工单分配项目监理').ButtonControl(Depth=3, Name='确认选择').Click(
            simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='开工单分配项目监理').PaneControl(searchDepth=1,
                                                                             Name='The XtraLayoutControl').PaneControl(
            Depth=1,
            AutomationId='dateFactStartDate').Click(
            simulateMove=False)
        ui.SendKeys("{Space}")

        imswindow.WindowControl(searchDepth=1, Name='开工单分配项目监理').EditControl(Depth=2,
                                                                             AutomationId='tbxAreaCode').SendKeys(
            '13234')
        imswindow.WindowControl(searchDepth=1, Name='开工单分配项目监理').ButtonControl(Depth=3, Name='确定').Click()
        tool_button.ButtonControl(searchDepth=1, Name='传递').Click(simulateMove=False)
        ui.SendKeys("{Space 2}")

        tool_button.ButtonControl(searchDepth=1, Name='分配工程部').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='开工单分配工程部').EditControl(Depth=2,
                                                                            AutomationId='hlinkPMDptMgr').Click(
            simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='开工单分配工程部').WindowControl(searchDepth=1, Name='通讯录').PaneControl(
            Depth=3, Name='The XtraLayoutControl').EditControl(AutomationId='myStfName').SendKeys('zky')
        ui.SendKeys("{Enter}")
        imswindow.WindowControl(searchDepth=1, Name='开工单分配工程部').WindowControl(searchDepth=1, Name='通讯录').PaneControl(
            Depth=3, AutomationId='myStaffToolBarPanel').ButtonControl(Depth=4, Name='选择').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='开工单分配工程部').ButtonControl(Depth=3, Name='保存').Click()
        tool_button.ButtonControl(searchDepth=1, Name='设置分包').Click(simulateMove=False)
        time.sleep(5)
        # imswindow.WindowControl(searchDepth=1, Name='开工单设置分包').ButtonControl(Depth=3, Name='保存').Click()
        tool_button.ButtonControl(searchDepth=1, Name='分配装修管家').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='开工单分配装修管家').EditControl(Depth=2,
                                                                             AutomationId='hlinkPM').Click(
            simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='开工单分配装修管家').WindowControl(searchDepth=1, Name='员工查询').PaneControl(
            Depth=3, Name='The XtraLayoutControl').EditControl(AutomationId='myStfName').SendKeys('幸福小管家')
        ui.SendKeys("{Enter}")
        imswindow.WindowControl(searchDepth=1, Name='开工单分配装修管家').WindowControl(searchDepth=1, Name='员工查询').PaneControl(
            Depth=3, AutomationId='myStaffToolBarPanel').ButtonControl(Depth=4, Name='选择').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='开工单分配装修管家').ButtonControl(Depth=3, Name='保存').Click()
        tool_button.ButtonControl(searchDepth=1, Name='传递').Click(simulateMove=False)
        ui.SendKeys("{Space 2}")
        tool_button.ButtonControl(searchDepth=1, Name='设置内部工期').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='开工单设置内部工期').EditControl(Depth=2,
                                                                             AutomationId='tbxCoTimeLimit').SendKeys(
            '5')
        imswindow.WindowControl(searchDepth=1, Name='开工单设置内部工期').ButtonControl(Depth=3, Name='保存').Click()
        tool_button.ButtonControl(searchDepth=1, Name='传递').Click(simulateMove=False)
        ui.SendKeys("{Space 2}")
        tool_button.ButtonControl(searchDepth=1, Name='分配预算员').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='分配预算员').EditControl(Depth=2,
                                                                         AutomationId='hlinkBudgetor').Click(
            simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='分配预算员').WindowControl(searchDepth=1, Name='预算员选择').ButtonControl(
            Depth=5, Name='选择').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='分配预算员').ButtonControl(Depth=3, Name='保存').Click(simulateMove=False)
        ui.SendKeys("{Space}")
        tool_button.ButtonControl(searchDepth=1, Name='传递').Click(simulateMove=False)
        ui.SendKeys("{Space 2}")
        ui.SendKeys("{Space 3}")
        self.gui_close("kaigong.jpg")

    # 新建核算单(UI)
    def hesuandan(self, n):
        ui.uiautomation.SetGlobalSearchTimeout(10)
        imswindow = ui.WindowControl(searchDepth=1, Name="毛伟人 岚庭ERP ")

        if first:
            self.check_ims_exists()
            ui.uiautomation.SetGlobalSearchTimeout(5)
            # time.sleep(3)
            if imswindow.TextControl(Depth=3, SubName='你有').Exists(maxSearchSeconds=3):
                imswindow.ButtonControl(Depth=3, Name='马上处理').Click(simulateMove=False)
            imswindow.SetActive()
            imswindow.EditControl(Depth=6, AutomationId="teSearch").GetValuePattern().SetValue("核算单")
            imswindow.Click(50, 130, simulateMove=False)
        hesuanlie = imswindow.PaneControl(Depth=3, AutomationId='UCMatlChk')
        hesuanlie.ButtonControl(Depth=7, Name="新建").Click()
        hesuandetail = imswindow.PaneControl(Depth=3, AutomationId='UCMatlChkDetail').PaneControl(Depth=3,
                                                                                                  AutomationId='layoutControl1')
        hesuandetail.EditControl(searchDepth=1, AutomationId='hlinkContNo').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='合同选择').PaneControl(searchDepth=1,
                                                                        AutomationId='layoutControl1').EditControl(
            searchDepth=1, AutomationId='tbxCustName').SendKeys(n)
        ui.SendKeys("{Enter}")
        imswindow.WindowControl(searchDepth=1, Name='合同选择').PaneControl(searchDepth=1,
                                                                        AutomationId='pnlToolbar').ButtonControl(
            Depth=4, Name="选择").Click(simulateMove=False)
        hesuandetail.EditControl(searchDepth=1, AutomationId='tbxJiJiaSize').SendKeys('120')
        hesuandetail.EditControl(searchDepth=1, AutomationId='tbxInnerFrameSize').SendKeys('110')

        tool_bar = hesuandetail.GetNextSiblingControl().PaneControl(searchDepth=1, AutomationId='UCOperateBar')

        tool_bar.ButtonControl(searchDepth=1, Name='保存').Click(simulateMove=False)
        ui.SendKeys("{Space 2}")
        time.sleep(3)

        tool_bar.ButtonControl(searchDepth=1, Name='主材确认单').Click(simulateMove=False)
        time.sleep(3)  # 新建主材确认单
        matlconfirm = imswindow.PaneControl(Depth=3, AutomationId='UCMatlConfirmDetail').PaneControl(Depth=3,
                                                                                                     AutomationId='layoutControl1')
        matl = matlconfirm.TabControl(searchDepth=1, AutomationId='xtraTabControl1').PaneControl(Depth=2,
                                                                                                 AutomationId='pnlMatlConfirmDetlMatl')
        try:
            matl.CustomControl(Depth=2, Name='Data Panel').CustomControl(searchDepth=1, Name='Row 1').DataItemControl(
                searchDepth=1, Name='材料名称 row 0').DoubleClick(simulateMove=False)
            imswindow.WindowControl(searchDepth=1, Name='选择材料产品').PaneControl(Depth=2, Name='pnlTable').CustomControl(
                Depth=3, Name='Row 2').DoubleClick(simulateMove=False)
            matl.CustomControl(Depth=2, Name='Data Panel').CustomControl(searchDepth=1, Name='Row 2').DataItemControl(
                searchDepth=1, Name='材料名称 row 1').DoubleClick(simulateMove=False)
            imswindow.WindowControl(searchDepth=1, Name='选择材料产品').PaneControl(Depth=2, Name='pnlTable').CustomControl(
                Depth=3, Name='Row 1').DoubleClick(simulateMove=False)
            matl_name = matl.CustomControl(Depth=2, Name='Data Panel').CustomControl(searchDepth=1,
                                                                                     Name='Row 2').DataItemControl(
                searchDepth=1, Name='材料名称 row 1').GetValuePattern().Value
            if matl_name == "洁具":
                row = "Row 2"
                matl_row = '产品参数 row 1'
            else:
                row = "Row 1"
                matl_row = '产品参数 row 0'
            matl.CustomControl(Depth=2, Name='Data Panel').CustomControl(searchDepth=1, Name=row).DataItemControl(
                searchDepth=1, Name=matl_row).DoubleClick(simulateMove=False)
            imswindow.WindowControl(searchDepth=1, Name='扩展属性选择').ButtonControl(Depth=5, Name='确定').Click(
                simulateMove=False)
            matlconfirm.TabControl(searchDepth=1, AutomationId='xtraTabControl1').TabItemControl(searchDepth=1,
                                                                                                 Name='基装材料').Click(
                simulateMove=False)
            matlconfirm.TabControl(searchDepth=1, AutomationId='xtraTabControl1').GroupControl(Depth=3,
                                                                                               Name='Data Panel').TreeItemControl(
                searchDepth=1, Name='Node1').DataItemControl(searchDepth=1, Name='产品参数 row 1').DoubleClick(
                simulateMove=False)
            imswindow.WindowControl(searchDepth=1, Name='扩展属性选择').ButtonControl(Depth=5, Name='确定').Click(
                simulateMove=False)
        except LookupError:
            pass
        matlconfirm.GetNextSiblingControl().ButtonControl(Depth=2, Name='保存编辑').Click(simulateMove=False)
        ui.SendKeys("{Space}")
        matlconfirm.GetNextSiblingControl().ButtonControl(Depth=2, Name='传递').Click(simulateMove=False)
        ui.SendKeys("{Space 3}")
        matlconfirm.TabControl(searchDepth=1, AutomationId='xtraTabControl1').TabItemControl(searchDepth=1,
                                                                                             Name='主材材料').Click(
            simulateMove=False)
        dp = matl.CustomControl(Depth=2, Name='Data Panel')
        self.upload_pic(imswindow, dp, '上传图片 row 0', '1122.jpg')
        self.upload_pic(imswindow, dp, '上传图片 row 1', '1122.jpg')
        matlconfirm.GetNextSiblingControl().ButtonControl(Depth=2, Name='传递').Click(simulateMove=False)
        ui.SendKeys("{Space 3}")
        matlconfirm.GetNextSiblingControl().ButtonControl(Depth=2, Name='传递').Click()
        ui.SendKeys("{Space 3}")
        time.sleep(1)
        ui.SendKeys("{Space 4}")
        time.sleep(3)
        self.gui_close('matl.jpg')

        tool_bar.ButtonControl(searchDepth=1, Name='主材通知单').Click(simulateMove=False)  # 新建主材通知单
        time.sleep(2)
        matl_notice = imswindow.PaneControl(Depth=3, AutomationId='UCMatlPurConfirmDetail').PaneControl(Depth=3,
                                                                                                        AutomationId='layoutControl1')
        matlpur_tool = matl_notice.GetNextSiblingControl().PaneControl(searchDepth=1, AutomationId='UCOperateBar')
        matlpur_tool.ButtonControl(searchDepth=1, Name='保存').Click(simulateMove=False)
        ui.SendKeys("{Space}")
        matlpur_tool.ButtonControl(searchDepth=1, Name='传递').Click(simulateMove=False)
        ui.SendKeys("{Space 8}")
        time.sleep(3)
        self.gui_close('matlpur.jpg')
        '''
        time.sleep(2)
        tool_bar.ButtonControl(searchDepth=1, Name='基材通知单').Click(simulateMove=False)  # 新建基材通知单
        time.sleep(1)
        matlbase_notice = imswindow.PaneControl(Depth=3, AutomationId='UCMatlPurBaseConfirm').PaneControl(Depth=2,
                                                                                                          Name='pnlContainer')
        matlbase_notice.PaneControl(searchDepth=1, Name='pnlToolbar').ButtonControl(Depth=4, Name='新建').Click(
            simulateMove=False)
        time.sleep(2)
        matlpur_detail_tool = imswindow.PaneControl(Depth=3, AutomationId='UCMatlPurBaseConfirmDetail').PaneControl(
            Depth=3, AutomationId='pnlOperate').PaneControl(searchDepth=1, AutomationId='UCOperateBar')
        matlpur_detail_tool.ButtonControl(searchDepth=1, Name='保存').Click(simulateMove=False)
        ui.SendKeys("{Space}")
        matlpur_detail_tool.ButtonControl(searchDepth=1, Name='传递').Click(simulateMove=False)
        ui.SendKeys("{Space 6}")
        time.sleep(3)
        self.gui_close('matlbase.jpg')
        # self.gui_close('matlbase.jpg')

        tool_bar.ButtonControl(searchDepth=1, Name='工人发包单').Click(simulateMove=False)  # 新建工人发包单
        time.sleep(2)
        money_work = imswindow.PaneControl(Depth=3, AutomationId='UCBaseMoneyWorker').PaneControl(Depth=3,
                                                                                                  AutomationId='layoutControl1')
        money_work.GetPreviousSiblingControl().ButtonControl(Depth=4, Name='新建').Click(simulateMove=False)
        time.sleep(2)
        money_worker_detail = imswindow.PaneControl(Depth=3, AutomationId='UCBaseMoneyWorkerEdit').PaneControl(Depth=3,
                                                                                                               AutomationId='layoutControl1')
        money_worker_detail.ButtonControl(Depth=5, Name='添加基装项目').Click(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='选择项目').PaneControl(Depth=2, Name='myTable').CustomControl(Depth=5,
                                                                                                               Name='Data Panel').CustomControl(
            searchDepth=1, Name='Row 3').DoubleClick(simulateMove=False)
        imswindow.WindowControl(searchDepth=1, Name='选择项目').PaneControl(searchDepth=1,
                                                                        Name='myOperatePanel').ButtonControl(Depth=2,
                                                                                                             Name='确定').Click(
            simulateMove=False)
        money_worker_detail.PaneControl(searchDepth=1, Name='pnlOperate').ButtonControl(Depth=2, Name='保存').Click(
            simulateMove=False)
        ui.SendKeys("{Space}")
        money_worker_detail.PaneControl(searchDepth=1, Name='pnlOperate').ButtonControl(Depth=2, Name='传递').Click(
            simulateMove=False)
        ui.SendKeys("{Space 2}")
        self.gui_close('workerde.jpg')
        self.gui_close('worker.jpg')

        tool_bar.ButtonControl(searchDepth=1, Name='保存').Click(simulateMove=False)
        ui.SendKeys("{Space 2}")
        tool_bar.ButtonControl(searchDepth=1, Name='核算完成').Click(simulateMove=False)
        ui.SendKeys("{Space 2}")
        '''
        self.gui_close("hesuan.jpg")

    # 新建核算单
    def matlchk(self):
        matlurl = f'https://dv.lantingroup.cn:{self.port}/PC/Check/MatlChkService.svc'
        header = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': '"http://tempuri.org/IMatlChk/MatlChklEdit"',
            'Host': f'dv.lantingroup.cn:{self.port}',
            'Content-Length': '1899',
            'Expect': '100-continue',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'Keep-Alive'
        }

    # 工种经理抢单
    def ordergrab(self, posid, sessionid):
        url = f'https://dv.lantingroup.cn:{self.port}/PC/Site/SiteService.svc'
        head = {'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': '"http://tempuri.org/IOrderGrabbingPool/OrderGrabbingOper"',
                'Host': 'dv.lantingroup.cn:7078',
                'Content-Length': '773',
                'Expect': '100-continue',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'Keep-Alive'
                }
        body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><OrderGrabbingOper xmlns="http://tempuri.org/">' \
               '<request xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
               '<a:CustomParas i:nil="true"/><a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight">' \
               f'<b:LoginStafPosID>{posid}</b:LoginStafPosID><b:RegisterID i:nil="true"/><b:SessionID>{sessionid}</b:SessionID>' \
               f'<b:Sign i:nil="true"/><b:UniqueID>{sessionid}</b:UniqueID></a:Session>' \
               '<a:ID>1e039a02-03e3-44d1-9808-b50f71c3f012</a:ID></request></OrderGrabbingOper></s:Body></s:Envelope>'
        cmpl = requests.post(url, headers=head, data=body.encode('utf-8'))
        print(cmpl.text)

    # 分配角色
    def select_role(self):
        url = f"https://dv.lantingroup.cn:{self.port}/PC/RightManage/RightManageService.svc"
        header = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': '""http://tempuri.org/IRightManageErp/StaffPosRoleModify"',
            'Host': f'dv.lantingroup.cn:{self.port}',
            'Content-Length': '872',
            'Expect': '100-continue',
            'Accept-Encoding': 'gzip, deflate'
        }
        body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><StaffPosRoleModify xmlns="http://tempuri.org/">' \
               '<staffPosRoleForchange xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
               '<a:CustomParas i:nil="true"/><a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight">' \
               f'<b:LoginStafPosID>{self.LoginStafPosID}</b:LoginStafPosID><b:RegisterID i:nil="true"/><b:SessionID>{self.SessionID}</b:SessionID>' \
               f'<b:Sign i:nil="true"/><b:UniqueID>{self.UniqueID}</b:UniqueID></a:Session><a:RoleID>e1da41b9-5785-4e39-983f-a17675a2885a</a:RoleID>' \
               '<a:StfPosID>f07ec952-b402-46af-a40f-2946d0a2e237</a:StfPosID></staffPosRoleForchange></StaffPosRoleModify></s:Body></s:Envelope>'
        cmpl = requests.post(url, headers=header, data=body.encode('utf-8'))
        if re.search("<a:IsSuccess>true</a:IsSuccess>", cmpl.text, re.S):
            print("修改角色成功")

    def test_show(self):
        for i in range(5):
            print(i)
            time.sleep(1)

    # 分派工人
    def choice_worker(self, posid, sessionid, order_id):
        url = "https://dv.lantingroup.cn:7078/PC/Site/SiteService.svc"
        header = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': '"http://tempuri.org/IAssignPool/AssignPerson"',
            'Host': 'dv.lantingroup.cn:7078',
            'Content-Length': '836',
            'Expect': '100-continue',
            'Accept-Encoding': 'gzip, deflate'
        }
        body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><AssignPerson xmlns="http://tempuri.org/">' \
               '<request xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
               '<a:CustomParas i:nil="true"/><a:CustomParasDataFormat>0</a:CustomParasDataFormat><a:Session xmlns:b="http://schemas.datacontract.org/2004/07/Base.Data.UserRight">' \
               f'<b:LoginStafPosID>{posid}</b:LoginStafPosID><b:RegisterID i:nil="true"/><b:SessionID>{sessionid}</b:SessionID>' \
               f'<b:Sign i:nil="true"/><b:UniqueID>{sessionid}</b:UniqueID></a:Session><a:ID>{order_id}</a:ID>' \
               '<a:WorkerUserSpId>b6c6ebfb-4e0f-4a31-8a75-2cd005f601a6</a:WorkerUserSpId></request></AssignPerson></s:Body></s:Envelope>'
        result = requests.post(url, headers=header, data=body.encode('utf-8'))
        print(result.text)

    # 新建报价单
    def creatoffer(self, *args):
        # args = self.contactadd(num)
        cre_time = self.modifydatetime('now')
        a_time = self.modifydatetime('date')
        UID = uuid.uuid1()
        uid = uuid.uuid4()
        if type(args[0]) != list:
            bldid = args[1]
            contid = args[2]
            custid = SQL.customerid(args[0])
            meet_time = args[4]
            house_type = args[5]
            self.offer(args[0], cre_time, a_time, UID, uid, bldid, contid, custid, meet_time, house_type)
        elif type(args[0]) == list:
            for c in args[0]:
                bldids = SQL.budid(c)
                bldid = bldids[0]
                contid = SQL.selectcontid(c)
                custid = SQL.customerid(c)
                meet_time = SQL.get_meettime(c)
                house_type = bldids[7]
                self.offer(c, cre_time, a_time, UID, uid, bldid, contid, custid, meet_time, house_type)

    def offer(self, arg0, cre_time, a_time, UID, uid, bldid, contid, custid, meet_time, house_type):
        bldname = SQL.get_bldname(bldid)
        applydate = str(meet_time[0]).replace(' ', 'T')
        if self.coid == '09a055c1-4885-47e7-a5ca-7066f16c4537':
            amount = '11208'
            checkmount = '93340'
            mgtamount = '-660'
            tax = '18723.50'
            diffamount = '-6000.00'
            diffarea = '-6.0'
            scupfound = '1000.0'
            offertemp = 'f3f6bffe-1efc-4067-963f-9586c2ff8bc0'
            matlseries = 'b81d4629-0d8c-4552-ba18-107ae396c5a3'
            price = '1000'
            tempmount = '100000'
            tempsize = '66.00'
        elif self.coid == 'c7cc5de4-efdd-4aa7-9615-7a748785be12':
            amount = '143'
            checkmount = '130'
            mgtamount = '0'
            tax = '13.00'
            diffamount = '0'
            diffarea = '0'
            scupfound = '0'
            offertemp = '29b7e19e-7f05-4b16-aa8c-485505945d38'
            matlseries = 'afbccb1c-792d-450b-b232-e52271d66ca9'
            price = '300'
            tempmount = '130'
            tempsize = '20.00'
        else:
            raise Exception("公司不支持！")
        url = f"https://dv.lantingroup.cn:{self.port}/PC/OfferInfo/Offer/OfferService.svc"
        header = {
            'Content-Type': 'text/xml;charset=utf-8',
            'SOAPAction': '"http://tempuri.org/IOfferFullV/OfferFullVAdd"',
            'Host': f'dv.lantingroup.cn:{self.port}',
            'Content-Length': '3271',
            'Expect': '100-continue',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'Keep-Alive'
        }
        data = f'<OfferFullVAdd xmlns="http://tempuri.org/"><session xmlns:a="http://schemas.datacontract.org/2004/07/Base.Data.UserRight" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
               f'<a:LoginStafPosID>{self.LoginStafPosID}</a:LoginStafPosID><a:RegisterID i:nil="true"></a:RegisterID>' \
               f'<a:SessionID>{self.SessionID}</a:SessionID><a:Sign i:nil="true"></a:Sign><a:UniqueID>{self.UniqueID}</a:UniqueID></session>' \
               '<offerFullVEdit xmlns:a="http://schemas.datacontract.org/2004/07/LandErp.ServiceModel" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">' \
               f'<a:BilsCoID i:nil="true"></a:BilsCoID><a:BilsCoName i:nil="true"></a:BilsCoName><a:CoID>{self.coid}</a:CoID><a:CoName i:nil="true"></a:CoName>' \
               f'<a:CreTime>{cre_time}+08:00</a:CreTime><a:ID>{UID}</a:ID><a:Oper i:nil="true"></a:Oper><a:OperID i:nil="true"></a:OperID>' \
               f'<a:UniqueID>{UID}</a:UniqueID><a:UpdtOper i:nil="true"></a:UpdtOper><a:UpdtOperId i:nil="true"></a:UpdtOperId>' \
               f'<a:UpdtTime>{cre_time}+08:00</a:UpdtTime><a:AppSpID>{self.LoginStafPosID}</a:AppSpID><a:AppSpName i:nil="true"></a:AppSpName>' \
               '<a:Attach i:nil="true"></a:Attach><a:BudgetID i:nil="true"></a:BudgetID><a:BudgetName i:nil="true"></a:BudgetName><a:FinishTime i:nil="true"></a:FinishTime>' \
               '<a:FlowState>0</a:FlowState><a:FlowStateTxt></a:FlowStateTxt><a:IsChkBefore>false</a:IsChkBefore><a:No i:nil="true"></a:No><a:Remark i:nil="true"></a:Remark>' \
               f'<a:State>0</a:State><a:StateTxt i:nil="true"></a:StateTxt><a:SubmitTime i:nil="true"></a:SubmitTime><a:Amount>{amount}</a:Amount>' \
               f'<a:ApplyDate>{applydate}</a:ApplyDate><a:BldID>{bldid}</a:BldID><a:BldName>{bldname}</a:BldName>' \
               f'<a:CheckAmount>{checkmount}</a:CheckAmount><a:ContID>{contid}</a:ContID><a:ContState>0</a:ContState><a:ContSysNo i:nil="true"></a:ContSysNo>' \
               f'<a:CustID>{custid[0]}</a:CustID><a:CustName>{arg0}</a:CustName><a:CustPhone>{custid[2]}</a:CustPhone>' \
               f'<a:DecorStyleID>1eca43f3-6ef3-47b7-aec1-fab1a73a45fa</a:DecorStyleID><a:DesnAmount>0</a:DesnAmount><a:DesnID>{meet_time[1]}</a:DesnID>' \
               '<a:DesnName i:nil="true"></a:DesnName><a:DiscAmount>0</a:DiscAmount><a:DiscID i:nil="true"></a:DiscID><a:DiscSysNo i:nil="true"></a:DiscSysNo>' \
               '<a:FactAmount>100000</a:FactAmount><a:FeesAmount>0</a:FeesAmount><a:FreeMgtAmount>false</a:FreeMgtAmount><a:HouseAddr i:nil="true"></a:HouseAddr>' \
               f'<a:HouseTypeID>{house_type}</a:HouseTypeID><a:IsSubCont>false</a:IsSubCont><a:MeetCustDate>{meet_time[0].date()}T00:00:00</a:MeetCustDate>' \
               f'<a:MeetCustID>{meet_time[3]}</a:MeetCustID><a:MgtAmount>{mgtamount}</a:MgtAmount><a:NeedInvoice>true</a:NeedInvoice>' \
               f'<a:OfferDate>{a_time}+08:00</a:OfferDate><a:OfferTempID>{offertemp}</a:OfferTempID>' \
               '<a:OfferTempName i:nil="true"></a:OfferTempName><a:OfferTempSysNo i:nil="true"></a:OfferTempSysNo><a:OfferType>6</a:OfferType><a:OptAmount>0</a:OptAmount>' \
               f'<a:SignDate i:nil="true"></a:SignDate><a:Tax>{tax}</a:Tax><a:TempRemark></a:TempRemark><a:AreaSize>44</a:AreaSize><a:AreaSizeDiffAmount>{diffamount}</a:AreaSizeDiffAmount>' \
               f'<a:DiffAreaSize>{diffarea}</a:DiffAreaSize><a:FrameAreaSize>64</a:FrameAreaSize><a:FullVType>6</a:FullVType><a:IncludeSculptFund>{scupfound}</a:IncludeSculptFund>' \
               f'<a:MatlSeriesID>{matlseries}</a:MatlSeriesID><a:Price>{price}</a:Price><a:PricingType>0</a:PricingType><a:TempAmount>{tempmount}</a:TempAmount>' \
               f'<a:TempAreaSize>{tempsize}</a:TempAreaSize><a:TempMaxAreaSize>0</a:TempMaxAreaSize><a:TempMinAreaSize>0</a:TempMinAreaSize><a:ToiletAmount>0</a:ToiletAmount>' \
               '<a:ValAreaSize>0</a:ValAreaSize><a:FuncAreaFullVItems><a:SvcFuncAreaFullVItemEdit><a:BilsCoID i:nil="true"></a:BilsCoID><a:BilsCoName i:nil="true"></a:BilsCoName>' \
               f'<a:CoID i:nil="true"></a:CoID><a:CoName i:nil="true"></a:CoName><a:CreTime>{cre_time}+08:00</a:CreTime><a:ID>{uid}</a:ID>' \
               f'<a:Oper i:nil="true"></a:Oper><a:OperID i:nil="true"></a:OperID><a:UniqueID>{uid}</a:UniqueID><a:UpdtOper i:nil="true"></a:UpdtOper>' \
               f'<a:UpdtOperId i:nil="true"></a:UpdtOperId><a:UpdtTime>{cre_time}+08:00</a:UpdtTime><a:FuncAreaOfferItemID i:nil="true"></a:FuncAreaOfferItemID>' \
               '<a:IsTempContain>false</a:IsTempContain><a:LimitSize i:nil="true"></a:LimitSize><a:Price>0</a:Price><a:Remark>此功能区面积未计入计价面积，所有项目需单独列项计费</a:Remark>' \
               '<a:EditState>1</a:EditState><a:FuncAreaItem><a:BilsCoID i:nil="true"></a:BilsCoID><a:BilsCoName i:nil="true"></a:BilsCoName><a:CoID i:nil="true"></a:CoID>' \
               f'<a:CoName i:nil="true"></a:CoName><a:CreTime>{cre_time}+08:00</a:CreTime><a:ID>{uid}</a:ID><a:Oper i:nil="true"></a:Oper>' \
               f'<a:OperID i:nil="true"></a:OperID><a:UniqueID>{uid}</a:UniqueID><a:UpdtOper i:nil="true"></a:UpdtOper><a:UpdtOperId i:nil="true"></a:UpdtOperId>' \
               f'<a:UpdtTime>{cre_time}+08:00</a:UpdtTime><a:AreaSize>44</a:AreaSize><a:CommFuncAreaID>f542cf59-8384-41ab-9cdd-17115e6c9c12</a:CommFuncAreaID>' \
               f'<a:ContID>{contid}</a:ContID><a:FuncAreaTypeID>1abfce2c-30d9-4d54-986c-56a4d57da799</a:FuncAreaTypeID>' \
               '<a:FuncAreaTypeName i:nil="true"></a:FuncAreaTypeName><a:IsCostCtrlAdd>false</a:IsCostCtrlAdd><a:MatlSize>0</a:MatlSize><a:Name>主卧</a:Name>' \
               f'<a:OfferID>{UID}</a:OfferID><a:Remark i:nil="true"></a:Remark><a:State>1</a:State><a:EditState>0</a:EditState></a:FuncAreaItem>' \
               '</a:SvcFuncAreaFullVItemEdit></a:FuncAreaFullVItems><a:OfferItemDetls></a:OfferItemDetls></offerFullVEdit></OfferFullVAdd>'
        # offertemp 报价模板 matlseries 系列
        # 压缩
        t = gzip.compress(data.encode('utf-8'))
        # 转码
        ZIP = str(base64.b64encode(t), 'utf-8')
        body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Header>' \
               '<Compression xmlns="http://www.microsoft.com/compression">algorithm = "GZip"</Compression></s:Header>' \
               f'<s:Body><CompressedBody xmlns="http://www.microsoft.com/compression">{ZIP}</CompressedBody></s:Body></s:Envelope>'
        # print(body)
        # time.sleep(10)
        r = requests.post(url, headers=header, data=body.encode('utf-8'))
        if re.search("<a:IsSuccess>true</a:IsSuccess>", r.text, re.S):
            print(f"客户{arg0}报价新建保存成功")
        else:
            print(data)
            print(r.text)
            raise Exception(f"客户{arg0}报价失败！")

        header3 = {
            'Content-Type': 'text/xml;charset=utf-8',
            'SOAPAction': '"http://tempuri.org/IOfferFullV/OfferFullVSubmit"',
            'Host': f'dv.lantingroup.cn:{self.port}',
            'Content-Length': '602',
            'Expect': '100-continue',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'Keep-Alive'
        }
        body3 = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><OfferFullVSubmit xmlns="http://tempuri.org/">{self.session}' \
                f'<offerID>{UID}</offerID></OfferFullVSubmit></s:Body></s:Envelope>'
        requests.post(url, headers=header3, data=body3.encode('utf-8'))


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
                 '<b:DeviceName>DESKTOP-74B6VCF</b:DeviceName><b:DeviceTag>BFEBFBFF000506E3</b:DeviceTag><b:IP>10.10.55.106</b:IP><b:Mac>70:4D:7B:64:69:33</b:Mac>' \
                 '<b:OS>Microsoft Windows NT 6.2.9200.0</b:OS></a:ClientInfo><a:Password>d82756cbfb2d680e4a249a3ccceb6f62</a:Password><a:PhoneCode i:nil="true"/><a:PhoneNum i:nil="true"/>' \
                 '<a:UserName>01210281</a:UserName><a:VersionCode>540</a:VersionCode></request></GeneralLogin></s:Body></s:Envelope>'
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
                f'<b:LoginStafPosID>{loginid}</b:LoginStafPosID><b:RegisterID i:nil="true"/><b:SessionID>{sessionid}</b:SessionID>' \
                f'<b:Sign i:nil="true"/><b:UniqueID>{sessionid}</b:UniqueID></a:Session></request></GetUserRole></s:Body></s:Envelope>'
    requests.post(role_url, headers=role_head, data=role_body.encode('utf-8'))
    return sessionid, loginid


if __name__ == "__main__":
    # LoginStafPosID = 'a1e929d3-a959-4f7b-b418-a48a60955709'
    port = '7078'
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

    ims = ImsData('16210025', port)
    func = {1: "customersave", 2: "contactadd", 3: "adddiscount", 4: "contstartplanadd_ui", 5: "custmeet",
            6: "baojiadan", 7: "kaigong", 8: "hesuandan"}
    # t1 = Thread(target=ims.choice_worker, args=('7592d52d-020c-42e6-bff8-5e051b2ae9de','ec7e0716-73d7-41b2-bb26-1aa391c8c7c6', '77c80ff9-a31f-444c-8e0d-2679a2c383fd'))
    # t2 = Thread(target=ims.choice_worker, args=('a1e929d3-a959-4f7b-b418-a48a60955709','524c4be5-c1c8-43fb-8c7d-76bf3e7b83dd', 'be70b0a8-d288-40de-ac60-7274ddff4250'))
    # t2.start()
    # t1.start()
    # t1.join()
    # t2.join()
    ims.contstart(['贝乐英(非自动计划)'])
    # ims.contstartplanadd(['兮安水'])
    # ims.contstartplanadd(['事心嗟'])
    while True:
        k = int(input("执行哪个动作？(1.客户登记 2.合同登记 3.合同优惠单登记 4.开工预案申请 5.设计见面 6.报价单 7.开工申请 8.核算单  0.quit)"))
        if k == 1:
            getattr(ims, "customersave")(5)
        elif 0 < k < 9:
            first = True
            getattr(ims, func[k])(1)
            if first:
                first = False
            print(ims.kehu)
            break
        elif k == 0:
            break
        else:
            print('输入错误，请重新输入！0退出')
            continue
