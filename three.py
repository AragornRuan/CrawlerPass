#!/usr/bin/env python
#coding=utf-8
import requests
import re

loginUrl = 'http://www.heibanke.com/accounts/login'
url = 'http://www.heibanke.com/lesson/crawler_ex02'
wrong = '密码错误'

s = requests.Session()
loginResp = s.get(loginUrl)
loginToken = loginResp.cookies['csrftoken']
postdata = {'username':'aragorn',
			'password':'123456',
			'csrfmiddlewaretoken':loginToken}
s.post(loginUrl, data=postdata)

for pwd in range(31):
	resp = s.get(url)
	token = resp.cookies['csrftoken']
	data = {'username':'aragorn',
			'password':pwd,
			'csrfmiddlewaretoken':token}
	response = s.post(url, data=data)
	html = response.content
	if wrong in html:
		print 'Trying password %d' % pwd
		pwd += 1
	else:
		print 'Login password %d' % pwd
		break

login_re = re.compile(r'<h3>(.*?)</h3>')
text = login_re.findall(html)
print text[0]