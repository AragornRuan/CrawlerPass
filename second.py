#!/usr/bin/env python
#coding=utf-8
import urllib2
import urllib
import re

url = r'http://www.heibanke.com/lesson/crawler_ex01/'
vaules = {}
vaules['username'] = 'aragorn'
html_re = re.compile(r'<h3>.*?(密码错误).*?</h3>')
for psw in range(31):
	vaules['password'] = psw
	print "Tring password %s" % vaules['password']
	data = urllib.urlencode(vaules)
	request = urllib2.Request(url, data)
	response = urllib2.urlopen(request)
	html = response.read()
	wrong = html_re.findall(html)
	if len(wrong) == 0:
		break
print 'Login!'
login_re = re.compile(r'<h3>(.*?)</h3>')
text = login_re.findall(html)
print text[0]
