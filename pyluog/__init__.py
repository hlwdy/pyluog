import requests,io,re,json
import matplotlib.pyplot as plt
from PIL import Image
from urllib.parse import unquote

headers = {
    'Referer': 'https://www.luogu.com.cn/auth/login',
    'Origin': 'https://www.luogu.com.cn',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.421.0 Safari/537.36",
    "Accept": "*/*",
    'Connection': 'keep-alive',
    'x-requested-with': 'XMLHttpRequest',
    'x-csrf-token':'',
}

class User:
    name=''
    password=''
    sess=None
    def __init__(self,name,password):
        self.name=name
        self.password=password
    
    def login(self):
        headers['x-csrf-token']=''
        headers['Content-Type']=''
        s=requests.session()
        r=s.get('https://www.luogu.com.cn/auth/login',headers=headers)
        client_id=r.cookies.get('__client_id')
        csrf_token=re.findall('<meta name="csrf-token" content="(.*?)">',r.text)[0]
        headers['x-csrf-token']=csrf_token
        print('获取验证码...')
        r=s.get('https://www.luogu.com.cn/api/verify/captcha',headers=headers)
        plt.imshow(Image.open(io.BytesIO(r.content)))
        plt.axis('off')
        plt.show()
        captcha=input('请输入验证码: ')
        
        print('正在进行登录...')
        headers['Content-Type']='application/json'
        data = {
            'captcha': captcha,
            'password': self.name,
            'username': self.password,
        }
        r=s.post('https://www.luogu.com.cn/api/auth/userPassLogin',headers=headers,data=json.dumps(data))
        print(r.text)
        if('status' in r.json() and r.json()['status']==403):
            print('出现错误: '+r.json()['errorMessage'])
            print('登录失败!')
            return
        tk=r.json()['syncToken']
        print('Token获取成功!')
        data={'syncToken':tk}
        r=s.post('https://www.luogu.org/api/auth/syncLogin',headers=headers,data=json.dumps(data))
        print(r.cookies)
        self.sess=s
        print('登录成功!')
        print('用户名: '+self.name)
        headers['x-csrf-token']=''
        headers['Content-Type']=''
        
    def getUserData(self):
        s=self.sess
        if(not s):
            print('请先登录!')
            return
        r=s.get('https://www.luogu.com.cn',headers=headers)
        return (json.loads(unquote(re.findall('JSON.parse\(decodeURIComponent\("(.*?)"\)\);',r.text)[0]))['currentUser'])
        
    def getRecordList(self,name,page):
        s=self.sess
        if(not s):
            print('请先登录!')
            return
        r=s.get('https://www.luogu.com.cn/record/list?user='+name+'&page='+str(page)+'&_contentOnly=1',headers=headers)
        return (r.json()['currentData']['records'])
    
    def getNotification(self,typ,page):
        s=self.sess
        if(not s):
            print('请先登录!')
            return
        r=s.get('https://www.luogu.com.cn/user/notification?type='+str(typ)+'&page='+str(page)+'&_contentOnly=1',headers=headers)
        return (r.json()['currentData']['notifications'])
        
    def QianDao():
        s=self.sess
        if(not s):
            print('请先登录!')
            return
        r=s.get('https://www.luogu.com.cn/index/ajax_punch',headers=headers)
        return json.loads(r.text)
        
    def getLatestMessages(self):
        s=self.sess
        if(not s):
            print('请先登录!')
            return
        r=s.get('https://www.luogu.com.cn/chat',headers=headers)
        return (json.loads(unquote(re.findall('JSON.parse\(decodeURIComponent\("(.*?)"\)\);',r.text)[0]))['currentData']['latestMessages'])
    
    def getMessagesRecord(self,uid):
        s=self.sess
        if(not s):
            print('请先登录!')
            return
        r=s.get('https://www.luogu.com.cn/api/chat/record?user='+str(uid),headers=headers)
        return r.json()['messages']
    
    def sendMessage(self,uid,content):
        s=self.sess
        if(not s):
            print('请先登录!')
            return
        postData={
            'content':content,
            'user':uid,
        }
        return s.post('https://www.luogu.com.cn/api/chat/new',headers=headers,data=postData).json()
        
    def getLastCode(self,pid):
        s=self.sess
        if(not s):
            print('请先登录!')
            return
        r=s.get('https://www.luogu.com.cn/problem/'+pid,headers=headers)
        res=json.loads(unquote(re.findall('JSON.parse\(decodeURIComponent\("(.*?)"\)\);',r.text)[0]))['currentData']
        return {'lastLanguage':res['lastLanguage'],'lastCode':res['lastCode']}
    
def getUid(name):
    r=requests.get('https://www.luogu.com.cn/api/user/search?keyword='+name,headers=headers).json()
    if(r['users'][0]):
        return str(r['users'][0]['uid'])
    else:
        return '-1'
        
def searchProblem(keyword,page,diffi=-1):
    r=requests.get('https://www.luogu.com.cn/problem/list?keyword='+keyword+('&difficulty='+str(diffi) if diffi!=-1 else '')+'&page='+str(page)+'&_contentOnly=1',headers=headers)
    return r.json()['currentData']
    
def getContestList(page):
    r=requests.get('https://www.luogu.com.cn/contest/list?page='+str(page)+'&_contentOnly=1',headers=headers)
    return r.json()['currentData']['contests']
    
def loginWithCookie(client_id,uid):
    s=requests.session()
    requests.utils.add_dict_to_cookiejar(s.cookies,{'__client_id':client_id,'_uid':str(uid)})
    res=User('*','*')
    res.sess=s
    print('验证cookie有效性...')
    if(res.getUserData()):
        print('登录成功!')
        print('用户uid: '+uid)
        return res
    else:
        print('该cookie无效!')
        return None
    
def getProblemInfo(pid):
    r=requests.get('https://www.luogu.com.cn/problem/'+pid,headers=headers)
    return json.loads(unquote(re.findall('JSON.parse\(decodeURIComponent\("(.*?)"\)\);',r.text)[0]))['currentData']['problem']