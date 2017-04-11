import requests
import bs4

try:
	r = requests.get("http://ip-check.info/?lang=en", proxies={'http' : '46.10.220.64'})
	b4 = bs4.BeautifulSoup(r.text, 'html.parser')
	print b4.getText()
except requests.exceptions.ProxyError:
	print "Error"

