import requests,pickle,os
from bs4 import BeautifulSoup
from PIL import Image


captcha_url ='https://hs-cas.hundsun.com/cas/kaptcha.jpg'
urls ='https://hs-cas.hundsun.com/cas/login?service=https://home.hundsun.com/SynLogin.aspx'
geturl ='https://home.hundsun.com/bar/s-68-1.aspx'
connecturl ='https://home.hundsun.com'

headers1 = { "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "Referer":"https://hs-cas.hundsun.com/cas/login?service=https://home.hundsun.com/SynLogin.aspx",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
           }

#拼接传入data数据
data={"username":"XXXXX","password":"XXXXX"}

def getcaptcha():

    r = s.get(captcha_url)
    with open('captcha.jpg','wb') as f:
        f.write(r.content)
    im = Image.open('captcha.jpg')
    im.show()
    im.close()
    captcha=input('请输入验证码：')
    data["captcha"]=captcha

def getdata():
    r = s.get(url=urls)
    soup = BeautifulSoup(r.text,"html.parser")
    lt = soup.find('input',attrs={'name':'lt'})['value']
    execution = soup.find('input',attrs={'name':'execution'})['value']
    _eventId = soup.find('input',attrs={'name':'_eventId'})['value']
    data['_eventId']=_eventId
    data['execution']=execution
    data['lt']=lt


def islogin():
    if int(s.get('https://home.hundsun.com/u/11315.aspx', allow_redirects=False).status_code) == 200:
        return True
    else:
        print('没有登录')
        return False

def login():

    r1 = s.post(url=urls,data=data,headers=headers1)#登陆
    print(r1.status_code)

    with open('cookies', 'wb') as f: #成功登陆保存cookies
        pickle.dump(requests.utils.dict_from_cookiejar(s.cookies), f)
        f.close()

    pages = []
    r2 = s.get(url=geturl)
    #print(r2.text)
    soup = BeautifulSoup(r2.text,"html.parser")
    #pattern =r'href=\"(\S*)\"'
    allpage =[]
    for one in soup.find_all('h5',class_=''):
        #print(one)
        #shortpage = re.findall(pattern,str(one))
        shortpage = one.find('a')['href']
        #print(shortpage)
        allpage.append(connecturl+str(shortpage))

    news =[]
    for onepage in allpage:
        r3 = s.get(url=onepage)
        soup = BeautifulSoup(r3.text,"html.parser")
        headr = soup.find('head')
        title = headr.find('title').string
        description = headr.find('meta',{'name':'description'})['content']
        news.append(title.strip('\n'))
        news.append(description.strip('\n'))
        '''
        results = soup.find('meta',{'name':'description'})['content']
        news.append(results)
        '''
        news.append('---------------------------')

    for onenew in news:
        print(onenew)

s = requests.session()
try:
    if os.path.getsize('cookies') > 0:
        with open('cookies', 'rb') as f2:
            s.cookies = requests.utils.cookiejar_from_dict(pickle.load(f2))
            #print(s.cookies)
            f2.close()
except:
    print('cookies 未能加载')
if not islogin():
    getcaptcha()
    getdata()
login()
