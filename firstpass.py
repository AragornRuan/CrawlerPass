#!/usr/bin/env python

import urllib2
import re

url = r'http://www.heibanke.com/lesson/crawler_ex00/'
num_re = re.compile(r'<h3>[^\d]*?(\d+)[^\d]*?</h3>')
myurl = url
while True:
	print "visiting %s" % myurl
	response = urllib2.urlopen(myurl)
	html = response.read()
	num = num_re.findall(html)
	if len(num) != 0:
		myurl = url + num[0]
	else:
		break
print 'Passed!'
