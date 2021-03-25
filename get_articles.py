import requests
from bs4 import BeautifulSoup
from tkinter import *
import os


def get_pdf(url):
    r = requests.get(url,headers=head)
    filename = url.split('/')[-1]
    if not os.path.exists('./pdf_files'):
        os.mkdir('./pdf_files')
    with open('./pdf_files/'+filename, 'wb+') as f:
        print('now saving {}'.format(filename))
        f.write(r.content)

head={}
head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
# https://hk7194.scholar.eu.org/scholar?start=20&q=changjiang+salinity+sediment&hl=zh-CN&as_sdt=0,5

# give keywords and generate pages
def get_pages(keywords_list,scrab_pages):
    # get init url
    url1='https://sc.panda321.com/scholar?start=0&q='
    for ii in range(len(keywords_list)):
        url1=url1+str(keywords_list[ii])+'+'
    url1=url1[:-1]+'&hl=zh-CN&as_sdt=0,5'
    # get more pages
    url_list=[]
    url_list.append(url1)
    for ii in range(1,scrab_pages):
        url_list.append(url1.replace('start=0','start='+str(ii)+'0'))
    for u in url_list:
        print(u)
    return url_list


# get all urls in one page
def get_onepage(url2):
    r1=requests.get(url2,headers=head)
    r1.encoding='utf-8'
    r2=r1.text
    # print(r2)
    soup=BeautifulSoup(r2,'html.parser')
    #print(soup.prettify())
    print("******************** This is a new page *********************")
    tmpa=soup.find_all(name='a')
    for ele in tmpa:
        if ele['href'][:5]=='https' and len(ele['href'])>20 and ele['href'][8:15]!='sci-hub':
            print(ele['href'])
            print("***")
            rr=requests.get(ele['href'],headers=head)
            rr.encoding='utf-8'
            rr2=rr.text
            try:
                pattern=re.compile(r'"citation_doi" content="(.*?)" />')
                target=pattern.findall(rr2)
                # print(target)
                if len(target)!=0:
                    scihub_url='https://www.sci-hub.ren/'+target[0]
                    print(scihub_url)
                    rx=requests.get(scihub_url,headers=head)
                    rx.encoding='utf-8'
                    rx2=rx.text
                    pattern2=re.compile(r'iframe src="(.*?)" id=')
                    target2=pattern2.findall(rx2)
                    target3=target2[0].split('#')[0]
                    print(111111)
                    print(target2)
                    print(target3)
                    print(22222)
                    get_pdf(target3)
            except Exception as e:
                print(e)
                pass

url_list=get_pages(['ensemble','forecast','downscaling'],3)# 这里需要输入关键词和需要爬取的页数,修改完成后运行程序即可
for ii in range(len(url_list)):
    get_onepage(url_list[ii])