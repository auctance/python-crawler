import requests
import re
import time #使用

# the head url
head_url='http://www.cjcyw.com/plus/list.php?tid=3&TotalResult=32109&PageNo='

head={}
head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'

# all have 1784 pages
home_pages=[]
for ii in range(1,1784):
    temp=head_url+str(ii)
    home_pages.append(temp)

# convert ms to datetime
def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime
# timeStamp(1614920400000)

# save to file
def to_csv(filename,sta,tm,dis,level):
    ff=open(filename,'a+',encoding='gb2312') #防止中文乱码
#    ff=open(filename,'a+',encoding='utf-8') #防止中文乱码

    for ii in range(len(sta)):
        ff.write(str(sta[ii])+','+str(tm[ii])+','+str(dis[ii])+','+str(level[ii])+'\n')
    ff.close()


# from every page get all "水情信息" urls
def target_url(one_page_url):
    onepage_url=[]
    r=requests.get(one_page_url,headers=head)
    rr=r.text
    # 获取 '水情信息' 的url   使用正则匹配
    pattern=re.compile('<li><a class="a1" href="/a/(.*?).html" target="_blank"><span class="list_title"><span style="color:"><b>航道公告:</b>(.*?)水情信息</span>')
    target=pattern.findall(rr)
    # get the num and convert to url
    for ii in range(len(target)):
        # print(target[ii][0])
        # print(target[ii][1])
        new_url=r'http://www.cjcyw.com/a/'+str(target[ii][0])+'.html'
        print(new_url)
        onepage_url.append(new_url)
    return onepage_url

# get   站名	时间	水位(m)	流量(m3/s)
def get_info(one_url):
    station=[]
    time=[]
    level=[]
    discharge=[]
    r1=requests.get(one_url,headers=head)
    r1.encoding='utf-8'
    r2=r1.text
    pattern2=re.compile('var sssq = (.*?);')
    target2=pattern2.findall(r2)
    # target2 is a list  and remove [{}]
    tt=target2[0][2:-2]
    tt2=tt.split('},{') # for all stations
    # match and get the station and ...
    for ii in range(len(tt2)): # for all stations
        one_str=tt2[ii]
        templist=one_str.split(',')
        for jj in range(len(templist)): # for one station
            if templist[jj][:3]=='"q"': #discharge
                tmp_dis=templist[jj].split(':"')[1][:-1]
                discharge.append(tmp_dis)
            if templist[jj][:6]=='"stnm"': #station
                tmp_sta=templist[jj].split(':"')[1][:-1]
                station.append(tmp_sta)
            if templist[jj][:4]=='"tm"': #time
                tmp_tm=templist[jj].split(':')[1]
                tmp_tm2=timeStamp(float(tmp_tm))
                time.append(tmp_tm2)
            if templist[jj][:3]=='"z"': #level
                tmp_level=templist[jj].split(':"')[1][:-1]
                level.append(tmp_level)
    print(station)
    print(time)
    print(discharge)
    print(level)
    return station,time,discharge,level

for ii in range(len(home_pages)):
    test1=target_url(home_pages[ii])
    for jj in range(len(test1)):
        sta1, tm1, dis1, level1 = get_info(test1[ii])
        print("************")
        to_csv('test.csv', sta1, tm1, dis1, level1)
# test1=target_url(home_pages[600]) # one page   test1=['url1','url2','url3']
# for ii in range(len(test1)):  # for all useful urls in one page
#     sta1,tm1,dis1,level1=get_info(test1[ii])
#     print("************")
#     to_csv('test.csv',sta1,tm1,dis1,level1)



# json, pandas-dataframe, ip-pool