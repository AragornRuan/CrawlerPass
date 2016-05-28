#!/usr/bin/env python
#coding=utf-8
import requests
import re

loginUrl = 'http://www.heibanke.com/accounts/login'
pwdUrl = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/?page=1'
url = 'http://www.heibanke.com/lesson/crawler_ex03'
pos_re = re.compile(r'pos">(\d+)</td>')
val_re = re.compile(r'val">(\d+)</td>')

s = requests.Session()
loginResp = s.get(loginUrl)
loginToken = loginResp.cookies['csrftoken']
loginData = {'username':'aragorn',
			 'password':'123456',
			 'csrfmiddlewaretoken':loginToken}
s.post(loginUrl, data=loginData)

count = 0
marked = [0 for i in range(100)]
pwd = ['x' for i in range(100)]
while count < 100:
	pwdResp = s.get(pwdUrl)
	html = pwdResp.content
	pos = pos_re.findall(html)
	val = val_re.findall(html)
	for i in range(len(pos)):
		if marked[int(pos[i]) - 1] == 0:
			pwd[int(pos[i]) - 1] = val[i]
			marked[int(pos[i]) - 1] = 1
			count += 1
	print 'Extracting password...', count


password = ''
for key in pwd:
	password += key

print 'Logining in'
print 'password is %s' % password
response = s.get(url)
token = response.cookies['csrftoken']
data = {'username':'aragorn',
		'password':password,
		'csrfmiddlewaretoken':token}

postResp = s.post(url, data=data)
login_re = re.compile(r'<h3>(.*?)</h3>')
text = login_re.findall(postResp.content)
print text[0]