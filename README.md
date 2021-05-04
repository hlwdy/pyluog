
A python module for using Luogu Api.
一个用于洛谷API的的Python模块。

**如何使用**

首先，你需要使用`pip install pyluog`来安装本模块，然后再进行引用：

```
import pyluog
```

你可以定义一个账号变量，需要两个字符串参数，分别是账号密码：

```
a=pyluog.User('name','password')
```

注意，以上操作并没有进行登录，登录操作需要执行：

```
a.login()
```

中途会要求输入验证码，请根据显示的图片验证码正确输入。

如果过程顺利，最后会输出 登录成功!。

除此之外，你还可以使用cookie进行登录 (两个参数，__client_id和你的uid)：

```
a=pyluog.loginWithCookie('aaabbcc1233dd344ee','12345')
```

登录操作完成后，你可以用：


- a.getUserData() 获取当前用户的信息

- a.getRecordList('name','1') 获取指定用户的评测提交记录 (两个参数分别是用户名和页数)

- a.getNotification(1,1) 获取当前用户的通知，(两个参数分别是类型和页数)
	- 类型1: @我的
	- 类型2: 回复
	- 类型3: 系统通知


- a.QianDao() 执行签到

- a.getLatestMessages() 获取私信最新消息列表

- a.getMessagesRecord('uid') 获取与指定用户的聊天记录 (注意参数是uid而不是用户名)

- a.sendMessage('uid','content') 向指定用户发送一条私信

- a.getLastCode('P1001') 获取你指定题目最后一次提交的代码

- a.getMyPastes() 获取你发布的所有云剪贴板信息

以上操作均会返回一个json对象。

无需登录账号即可执行的操作：

- pyluog.getUid('name') 根据用户名获取该用户的uid，如果不存在则返回'-1'

- pyluog.searchProblem('keyword',1,-1) 搜索题库内容 (三个参数分别是关键词，页数和题目难度，默认难度-1)
	- -1为全部难度
	- 0为暂无评定
	- 1为入门
	- 2为普及-
	- 3为普及/提高-
	- 4为普及+/提高
	- 5为提高+/省选-
	- 6为省选/NOI-
	- 7为NOI/NOI+/CTSC


- pyluog.getContestList('1') 获取比赛列表，参数为页数

- pyluog.getProblemInfo('P1001') 获取指定题目的详细内容 (包括题面，提交数，通过数，难度等)