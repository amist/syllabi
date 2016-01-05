import sys
import os
import httplib2
import re

def check_link(url):
    RETRIES = 3
    http = httplib2.Http()
    print(url + ' ', end='')
    for _ in range(RETRIES):
        try:
            response, content = http.request(url, 'GET')
            if response.status == 200:
                print('OK')
                return True
            else:
                print(str(response.status) + ' FAIL')
                return False
        except ConnectionResetError:
            pass
    print('ConnectionResetError FAIL')
    return False
        
        
def get_link_from_line(line):
    m = re.search('\((http.*?)\)', line)
    if m is not None:
        return m.group(1)
    return None
        
        
def get_links_from_file(filename):
    ret = []
    with open(filename) as f:
        for line in f:
            link = get_link_from_line(line)
            if link is not None:
                ret.append(link)
    return ret
    
    
def get_filenames():
    directories = [x[0] for x in os.walk('.') if '.git' not in x[0] and '.' != x[0]]
    filenames = [[os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))] for directory in directories]
    filenames = [file for directory in filenames for file in directory]
    return filenames
    
    
def test_links():
    res = True
    filenames = get_filenames()
    for filename in filenames:
        links = get_links_from_file(filename)
        for link in links:
            res &= check_link(link)
    return res
    
    
if __name__ == '__main__':
    res = test_links()
    print('==============')
    if res == False:
        print('FAIL')
        sys.exit(1)
    print('OK')