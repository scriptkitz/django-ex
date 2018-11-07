
import re
import ssl
import http.client as httplib
from django.http import StreamingHttpResponse

context = ssl._create_unverified_context()
def getSSR(url):
    if url.startswith("https"):
        gp = re.match("https://([^/]*)(.*)",url)
        host = gp.group(1)
        geturl = gp.group(2)
        conn = httplib.HTTPSConnection(host)
    else:
        gp = re.match("http://([^/]*)(.*)",url)
        host = gp.group(1)
        geturl = gp.group(2)
        #conn = httplib.HTTPConnection(host)
        conn = httplib.HTTPSConnection(host)
    conn.connect()
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
    conn.request("GET",geturl,headers=headers)
    resp = conn.getresponse()
    data = resp.read()
    if data:
        ssr = re.search("ssr://\w+",data).group()
    else:
        ssr = ""
    return ssr

def go():
    conn = httplib.HTTPSConnection("doub.ws",context=context)
    conn.connect()
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  }
    conn.request("GET","/sszhfx/",headers=headers)
    resp = conn.getresponse()
    data = resp.read()
    if data:
        urls = re.findall('http://doub\.pw/qr/qr\.php\?text=ssr://\w*',data)
        for url in urls:
            if not url.endswith("xxxxxx"):
                s = getSSR(url) + "\n"
                yield s

def ssr(request):
    return StreamingHttpResponse(go())
