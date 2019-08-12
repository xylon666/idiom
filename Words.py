import requests,os
from bs4 import BeautifulSoup
import concurrent.futures

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
}
url = 'http://chengyu.tqnxs.com/'
Linkfile = 'linkfile.txt'       #存放链接文件
Wordfile = 'wordfile.txt'       #存放下载的成语

def WordHtml(url):
    try:
        response = requests.get(url , headers=headers)
        if response.status_code == 200:
            return response.text
    except:
        return None

def WordLink(url):
    if not os.path.exists(Linkfile):
        for i in range(0, 26):
            t = 65 + i
            # print(chr(t))
            turl = url + chr(t) + '/'
            html = WordHtml(turl)
            if html:
                soup = BeautifulSoup(html, 'lxml')
                txt = soup.find('div', class_='yingList clearfix').text  # 获取首位拼音
                list = txt.split()  #提取字符为列表
                print(list)
                with open(Linkfile,'a') as f:
                    for i in list:
                        f.write(turl + str(i))
                        f.write('\n')

def WordRun():
    WordLink(url)
    lines = []
    with open(Linkfile,'r') as f:
        while True:
            line = f.readline()
            #print(line)
            if not line:
                break
            line = line.strip('\n')
            lines.append(line)
    print(lines)
    with concurrent.futures.ThreadPoolExecutor(len(lines)) as x:
        for i in lines:
            html = WordHtml(str(i))
            if html:
                x.submit(Download,str(i))
                soup = BeautifulSoup(html, 'lxml')
                pages = soup.find('div', class_='pages')
                if pages:
                    page = soup.find(class_='pages').find_all('a')[-2].string
                    # print(page)
                    if page:
                        for p in range(2, int(page) + 1):
                            x.submit(Download,str(i) + '/' + str(p) + '.html')

def Download(url):
    html = WordHtml(url)
    soup = BeautifulSoup(html, 'lxml')
    words = soup.find('ul', class_='ulLi120 fsc16').find_all('li')
    for item in words:
        word = item.find('a').string
        print(word)
        if len(word) > 4 or len(word) < 4:
            continue
        with open(Wordfile, 'a', encoding='utf-8') as f:
            f.write(item.find('a').string)
            f.write('\n')

WordRun()
print("----下载完成！----")
