import urllib
import urllib2

url = "http://206.189.92.209/ezchallz/index.php?page=register"

user = "sherlock"
data = {"username" : user} ## post
data = urllib.urlencode(data)

print(data)
for i in range(0,100):
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	the_page = response.read()

	print(the_page)
	
"""
if the_page.find("DONE") != -1:
    return
"""