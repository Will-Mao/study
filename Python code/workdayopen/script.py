import time
from RemarkTools import WorkDay
import ding_dailydaper

url = ['https://landit.zentaopm.com/bug-browse-2.html', 'https://landit.zentaopm.com/project-index-no.html','https://cdqlkj.yuque.com/lga3p2/gg73il/vfk8ez','https://cdqlkj.yuque.com/lga3p2/aex4el/aqg510']
app = [r'C:\Program Files (x86)\DingDing\DingtalkLauncher.exe']
# [r'F:\test\TestClient\IMS\master\LandErp.Client.exe',
#                                                                  'LAND IMS 1.3.2', 'Edit2', 'Edit5','01210281',
#                                                                  '1234567890a']
worker = WorkDay()
for u in url:
    worker.openbrowes(u)
for a in app:
    if type(a) is list:
        app = worker.openapp(a[0])
        worker.login(app[a[1]], a[3], a[2], a[4], a[5])
    # else:
    #     worker.openapp(a)
time.sleep(5)
ding_dailydaper.daily_paper_check()
