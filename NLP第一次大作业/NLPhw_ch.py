import requests
import re
import math
from time import sleep
from bs4 import BeautifulSoup
max_num = 50 #爬虫的广度

file = open("D:\chtxt.txt","w",encoding='utf-8')
all_url=[] #存放第一层爬虫网址
all_double_url=[] #所有爬过的网址
# header = {"User-Agent":r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62","cookie":r"_ntes_nuid=65a59082a6c88e9a002928bd2963751d; P_INFO=liujingucas@126.com|1665502468|1|mail126|00&99|CN&1665480381&mailmaster_ios#CN&null#10#0#0|&0|mailmaster_ios|liujingucas@126.com; __bid_n=183d703617dfe73dbc4207; FEID=v10-c6e50e1c4e203ff6d5777fcba0cde0cb64d60a4e; __xaf_fpstarttimer__=1672752339785; __xaf_thstime__=1672752339899; __xaf_fptokentimer__=1672752339919; _ntes_nnid=65a59082a6c88e9a002928bd2963751d,1678547671444; s_n_f_l_n3=215b1612a4b96d541680545635752; _antanalysis_s_id=1680545636195; BAIDU_SSP_lcr=https://cn.bing.com/; pver_n_f_l_n3=a; UserProvince=%u5317%u4EAC; FPTOKEN=hiHkGgOKAeZmIFvPWtonfPUEmtdP5/QqVLB0cBFOlWbJVL/Y9Vlp+T4werz/iRaSkXPVp+GHB8M4R5mL4w+BeKIsLCwznj5bxZT+gIRaRXQws4BxwILTaMMIKK9hwjN9yJSipqMXa4KJs/QaReo1/ywFO4Uwvei1ZvuhxTgCcNi6KZuI+czXihP+LRqZSDSOOnA57h32P9KRlYGeVXT6sIVwJdAeDuRwxzkxh7p1Zw2JxhZkNI4foS/RXCIAyMNNSH4J0KP2KexhVkUXLuaSf5ZcUDoFDQDBffDKumHMGbzh/5QvK+SYKrRQ0Qqmvpn3AVF5L7XGxDSjKqDG0/QrnosoUxZl7NPgRa8lnpbhWe3RbyNuKrilx0ym4pF+61mltLULL+T+8AysPGXJwy8Etg==|QAb3KGnaHrFlRMCIxLumM3XeWYgh0z0iClE7a84co68=|10|15972fa2a9dbbaedb20d7dd7746d9af6; WM_NI=s3ASpuqSZt1WUHTnYDLtvn9XKMTIZnKfg6zU5r8fHqX2O4u523NF9pR71rR7nc10hXuycF%2Fb3HB6Mry9u4KarpLg%2BeLnDLxiqhtAsoMfuZB8fUzR6fxKSrGS1udMf2CyQW4%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeabe24394bc86a7d48095b88ea3d45a869b8fadd148f2989e88fb70f2b1b7b9e12af0fea7c3b92ab1ed8fb4f37fb38d9695b45d97989c8fdc5090acba8fbc5489939caad96689baa9d7f95ff7aef887cb7b9cee81d5f83ff2ed82a7bc7c92e9ff93d13daebdffd1eb54b7a7ada7ae6af1988ed7d07abbe7bbd5ca6bb2b08488aa6f90b28cadfb63b3b8bca2f2658fbabbbbc134a68bb6b3b56ebc959d93c659f3abacaee53a81a79fb8b737e2a3; WM_TID=yrIzPbYDBDZFQARRUFORaiGR1xYi9jGe; ne_analysis_trace_id=1680549933924; vinfo_n_f_l_n3=215b1612a4b96d54.1.0.1680545635752.0.1680549945605"}
u = requests.get(r'https://news.163.com/')
u.encoding = 'utf-8'
web = u.text
soup = BeautifulSoup(web, "lxml")
for link in soup.find_all(name='a', href=re.compile(r'https?://news.163.com/+')):
    if len(all_url) > max_num:
        break
    url = link.get('href')
    if url in all_url:
        continue
    all_url.append(url)
    all_double_url.append(url)
    print(len(all_url))
    print(url)
    #req = requests.get(url=url,headers = header)
    req = requests.get(url=url)
    req.encoding = 'utf-8'
    html = req.text
    bes = BeautifulSoup(html,"lxml")
    # texts = bes.find("div", id = "container") #注意id是否是想要的
    # texts_list = texts.text.split("\xa0"*4)
    texts_list = bes.text.split("\xa0"*4)
    # file = open("D:\chtxt.txt","w",encoding='utf-8')   ##打开读写文件，逐行将列表读入文件内
    for line in texts_list:
        file.write(line+"\n")
    # sleep(2)


for uurl in all_url:
    double_url=[]
    u = requests.get(url=uurl)
    u.encoding = 'utf-8'
    web = u.text
    soup = BeautifulSoup(web, "lxml")
    for link in soup.find_all(name='a', href=re.compile(r'https?://news.163.com/+')):
        if len(double_url) > max_num:
            break
        url = link.get('href')
        if url in all_double_url:
            continue
        double_url.append(url)
        all_double_url.append(url)
        print(len(double_url))
        print(url)
        #req = requests.get(url=url,headers = header)
        req = requests.get(url=url)
        req.encoding = 'utf-8'
        html = req.text
        bes = BeautifulSoup(html,"lxml")
        # texts = bes.find("div", id = "container") #注意id是否是想要的
        # texts_list = texts.text.split("\xa0"*4)
        texts_list = bes.text.split("\xa0"*4)
        # file = open("D:\chtxt.txt","w",encoding='utf-8')   ##打开读写文件，逐行将列表读入文件内
        for line in texts_list:
            file.write(line+"\n")


####################################################################################

all_url=[] #存放第一层爬虫网址
all_double_url=[] #所有爬过的网址
# header = {"User-Agent":r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62","cookie":r"_ntes_nuid=65a59082a6c88e9a002928bd2963751d; P_INFO=liujingucas@126.com|1665502468|1|mail126|00&99|CN&1665480381&mailmaster_ios#CN&null#10#0#0|&0|mailmaster_ios|liujingucas@126.com; __bid_n=183d703617dfe73dbc4207; FEID=v10-c6e50e1c4e203ff6d5777fcba0cde0cb64d60a4e; __xaf_fpstarttimer__=1672752339785; __xaf_thstime__=1672752339899; __xaf_fptokentimer__=1672752339919; _ntes_nnid=65a59082a6c88e9a002928bd2963751d,1678547671444; s_n_f_l_n3=215b1612a4b96d541680545635752; _antanalysis_s_id=1680545636195; BAIDU_SSP_lcr=https://cn.bing.com/; pver_n_f_l_n3=a; UserProvince=%u5317%u4EAC; FPTOKEN=hiHkGgOKAeZmIFvPWtonfPUEmtdP5/QqVLB0cBFOlWbJVL/Y9Vlp+T4werz/iRaSkXPVp+GHB8M4R5mL4w+BeKIsLCwznj5bxZT+gIRaRXQws4BxwILTaMMIKK9hwjN9yJSipqMXa4KJs/QaReo1/ywFO4Uwvei1ZvuhxTgCcNi6KZuI+czXihP+LRqZSDSOOnA57h32P9KRlYGeVXT6sIVwJdAeDuRwxzkxh7p1Zw2JxhZkNI4foS/RXCIAyMNNSH4J0KP2KexhVkUXLuaSf5ZcUDoFDQDBffDKumHMGbzh/5QvK+SYKrRQ0Qqmvpn3AVF5L7XGxDSjKqDG0/QrnosoUxZl7NPgRa8lnpbhWe3RbyNuKrilx0ym4pF+61mltLULL+T+8AysPGXJwy8Etg==|QAb3KGnaHrFlRMCIxLumM3XeWYgh0z0iClE7a84co68=|10|15972fa2a9dbbaedb20d7dd7746d9af6; WM_NI=s3ASpuqSZt1WUHTnYDLtvn9XKMTIZnKfg6zU5r8fHqX2O4u523NF9pR71rR7nc10hXuycF%2Fb3HB6Mry9u4KarpLg%2BeLnDLxiqhtAsoMfuZB8fUzR6fxKSrGS1udMf2CyQW4%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeabe24394bc86a7d48095b88ea3d45a869b8fadd148f2989e88fb70f2b1b7b9e12af0fea7c3b92ab1ed8fb4f37fb38d9695b45d97989c8fdc5090acba8fbc5489939caad96689baa9d7f95ff7aef887cb7b9cee81d5f83ff2ed82a7bc7c92e9ff93d13daebdffd1eb54b7a7ada7ae6af1988ed7d07abbe7bbd5ca6bb2b08488aa6f90b28cadfb63b3b8bca2f2658fbabbbbc134a68bb6b3b56ebc959d93c659f3abacaee53a81a79fb8b737e2a3; WM_TID=yrIzPbYDBDZFQARRUFORaiGR1xYi9jGe; ne_analysis_trace_id=1680549933924; vinfo_n_f_l_n3=215b1612a4b96d54.1.0.1680545635752.0.1680549945605"}
u = requests.get(r'https://baike.baidu.com/')
u.encoding = 'utf-8'
web = u.text
soup = BeautifulSoup(web, "lxml")
for link in soup.find_all(name='a', href=re.compile(r'https?://baike.baidu.com/+')):
    if len(all_url) > max_num:
        break
    url = link.get('href')
    if url in all_url:
        continue
    all_url.append(url)
    all_double_url.append(url)
    print(len(all_url))
    print(url)
    #req = requests.get(url=url,headers = header)
    req = requests.get(url=url)
    req.encoding = 'utf-8'
    html = req.text
    bes = BeautifulSoup(html,"lxml")
    texts_list = bes.text.split("\xa0"*4)
    for line in texts_list:
        file.write(line+"\n")


for uurl in all_url:
    double_url=[]
    u = requests.get(url=uurl)
    u.encoding = 'utf-8'
    web = u.text
    soup = BeautifulSoup(web, "lxml")
    for link in soup.find_all(name='a', href=re.compile(r'https?://baike.baidu.com/+')):
        if len(double_url) > max_num:
            break
        url = link.get('href')
        if url in all_double_url :
            continue
        double_url.append(url)
        all_double_url.append(url)
        print(len(double_url))
        print(url)
        #req = requests.get(url=url,headers = header)
        req = requests.get(url=url)
        req.encoding = 'utf-8'
        html = req.text
        bes = BeautifulSoup(html,"lxml")
        # texts = bes.find("div", id = "container") #注意id是否是想要的
        # texts_list = texts.text.split("\xa0"*4)
        texts_list = bes.text.split("\xa0"*4)
        # file = open("D:\chtxt.txt","w",encoding='utf-8')   ##打开读写文件，逐行将列表读入文件内
        for line in texts_list:
            file.write(line+"\n")

####################################################################################

all_url=[] #存放待爬取的网址
# 由于是小说网站，由于选取的网站特性，只取第一层爬虫即可达到效果
# header = {"User-Agent":r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62"}
u = requests.get(r'http://www.xbiquge.la/10/10489/')
u.encoding = 'utf-8'
web = u.text
soup = BeautifulSoup(web, "lxml")
# regx="<dd><a href='(.*)' >"
for link in soup.find_all(name='a', href=re.compile(r'/10/10489/9+')): #href格式有所不同
    if len(all_url) > max_num:
        break
    url = link.get('href')
    url = 'https://www.ibiquge.la' + url #加上一个拼接操作
    if url in all_url:
        continue
    all_url.append(url)
    print(len(all_url))
    print(url)
    #req = requests.get(url=url,headers = header)
    req = requests.get(url=url)
    req.encoding = 'utf-8'
    html = req.text
    bes = BeautifulSoup(html,"lxml")
    texts_list = bes.text.split("\xa0"*4)
    for line in texts_list:
        file.write(line+"\n")


file.close()


##############################################################################################################
# 清洗爬虫下来的数据，计算熵并打印输出
# 打开文件
fr=open('D:\chtxt.txt','r', encoding='utf-8')
# 去掉英文字母、标点符号，只留下汉字
txt = fr.read()
# 使用正则表达式去匹配标点符号
# txt = re.sub("[0-9a-zA-Z\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）：《》「」|:·+-]", "",txt)
# txt = txt.replace(" ","")
# txt = txt.replace("\n","")
# txt = txt.replace("\t","")
# txt = txt.replace("\r","")
txt = re.sub(r'[^\u4e00-\u9fa5]+', "",txt)
fr.close()

#把清洗过的文本写回去
w = open('D:\chtxt.txt','w', encoding='utf-8')
w.write(str(txt))
w.close()

# 读取文件所有行
fr=open('D:\chtxt.txt','r', encoding='utf-8')
content=fr.readlines()
contentLines=''
 
characers=[]#存放不同字的总数
rate={}#存放每个字出现的频率

# 依次迭代所有行
for line in content:
    # 去除空格
    line=line.strip()
    #如果是空行，则跳过
    if len(line)==0:
        continue
    contentLines = contentLines + line
    # 统计每一字出现的个数
    for x in range(0,len(line)):
        # 如果字符第一次出现 加入到字符数组中
        if not line[x] in characers:
            characers.append(line[x])
        # 如果是字符第一次出现 加入到字典中
        if line[x] not in rate:
            rate[line[x]]=1
        #出现次数加一
        rate[line[x]]+=1
 

# 按出现次数排序，非必要，为了观察哪些字出现频率最高
rate=sorted(rate.items(), key=lambda e:e[1], reverse=True)
print('语料库共有%d个字'%len(contentLines))
print('其中有%d个不同的字'%len(characers))
k=0
for i in rate:
    if i[1] > 1000: #汉字过于丰富，所以只选取出现频次大于5000的字（该频次阈值可以根据max_num来调整，这里针对max_num=200选取了5000）
        print("[",i[0],"] 频次为 ", float(i[1]/len(contentLines)), "次")
        k+=1
    if k==16:
        break
# 计算汉字熵
entropy = 0
for i in rate:
    entropy += i[1] / len(contentLines) * math.log( len(contentLines) / i[1]) / math.log(2)
print('Entropy of Chinese is %f'%entropy)
fr.close()
