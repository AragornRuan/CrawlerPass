#!/usr/bin/env python
#coding=utf-8
import requests
import re
import threading

loginUrl = 'http://www.heibanke.com/accounts/login'
pwdUrl = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/?page=1'
url = 'http://www.heibanke.com/lesson/crawler_ex03'
pos_re = re.compile(r'pos">(\d+)</td>')
val_re = re.compile(r'val">(\d+)</td>')
count = 0
pwd = ['x' for i in range(100)]
lock = threading.Lock()

def login_fun():
	s = requests.Session()
	loginResp = s.get(loginUrl)
	loginToken = loginResp.cookies['csrftoken']
	loginData = {'username':'aragorn',
				 'password':'123456',
				 'csrfmiddlewaretoken':loginToken}
	s.post(loginUrl, data=loginData)
	return s

class MyThread(threading.Thread):
	def __init__(self, arg):
		threading.Thread.__init__(self)
		self.s = arg

	def run(self):
		global count
		global pwd
		global lock
		while count < 100:
			pwdResp = s.get(pwdUrl)
			html = pwdResp.content
			pos = pos_re.findall(html)
			val = val_re.findall(html)
			for i in range(len(pos)):
				lock.acquire()
				if pwd[int(pos[i]) - 1] == 'x':
					pwd[int(pos[i]) - 1] = val[i]
					count += 1
				lock.release()
			print threading.current_thread().name, 'Extracting password...', count

if __name__ == '__main__':
	s = login_fun()

	thread = [MyThread(s) for i in range(2)]
	for t in thread:
		t.start()

	for t in thread:
		t.join()

	password = ''.join(pwd)

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
