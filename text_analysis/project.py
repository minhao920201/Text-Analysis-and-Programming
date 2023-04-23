import urllib.request as req #引入urllib模組中函式名稱為request的函式為req
import bs4 #引入bs4模組
from matplotlib import pyplot as plt #引入matplotlib模組，用以製作圖表

dic = {} #建立空字典，用來記錄常見標籤用的


#定義函式GetData，用來取得每篇文章的標籤(tag)。參數url為網址
def GetData(url):
    #建立一個Request物件，附加Request Headers的資訊
    request = req.Request(url,headers = {
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    })

    #打開request
    with req.urlopen(request) as reponse:
        data = reponse.read().decode("utf-8")

    root = bs4.BeautifulSoup(data,"html.parser") #讓BeautifulSoup解析HTML格式文件
    tags = root.find_all("div",class_="qa-list__tags") #以列表形式找出所有 class_=qa-list__tags 的 div 標籤
    
    #外層迴圈將tags列表中每一個元素一一分析
    for tag in tags:
        #內層迴圈利用split()將每一篇的標籤(tag)存成列表，以便檢姹每個標籤(tag)出現的次數
        for i in tag.text.split():
            dic[i] = dic.get(i,0)+1 #確認dic字典裡有沒有出現過該標籤(tag)名稱，如果沒出現過則將該標籤(tag)名稱加入並將其value+1，反之，若已出現過則將value直接+1。
    
    #抓取下一頁的連結
    nextLink = root.find("a",string = "下一頁") #找到內文是 下一頁 的標籤a
    return nextLink["href"] #回傳下一頁的網址


#定義 GetHotTagContent 函式，將第一熱門的標籤(tag)文章找出，並將文章內容寫入tagContent裡
def GetHotTagContent(url,HotTag):
    #建立一個Request物件，附加Request Headers的資訊
    request = req.Request(url,headers = {
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    })

    #打開request
    with req.urlopen(request) as reponse:
        data = reponse.read().decode("utf-8")

    root = bs4.BeautifulSoup(data,"html.parser") #讓BeautifulSoup解析HTML格式文件
    tags = root.find_all("div",class_="qa-list__tags") #以列表形式找出所有 class_=qa-list__tags 的 div 標籤
    titles = root.find_all("h3",class_="qa-list__title") #以列表形式找出所有 class_=qa-list__title 的 h3 標籤

    index = 0 #從每頁最上方開始由上而下編號 index，此 index 用以找出該篇文章是否包含最熱門的標籤(tag)
    li_index = [] #將符合條件的 index 記錄在此列表裡

    #將列表tags中的每個元素一一分析
    for tag in tags:
        #如果 HotTag 在 tag 裡，則將其 index 加入 li_index 中
        if HotTag in tag.text:
            li_index.append(index)
        index += 1 #下一篇的索引值(index)
    
    print(li_index) #在底下視窗印出每頁有包含熱門標籤(tag)的索引值

    #將有 HotTag 的文章內容寫入 tagContent 中
    with open("tagContent.txt",mode = "a", encoding = "utf-8") as ftext:
        #將li_index中的索引值(index)一一取出，以找出擁有HotTag文章
        for id in li_index:
            #ftext.write("網址:"+titles[id].a["href"]+"\n") #將網址寫入txt檔
            url2 = titles[id].a["href"] #將擁有HotTag的文章之網址存放在url2中

            #建立一個Request物件，附加Request Headers的資訊
            request2 = req.Request(url2,headers={
                "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
            })

            #打開request2
            with req.urlopen(request2) as response2:
                data2 = response2.read().decode("utf-8")
            
            root2 = bs4.BeautifulSoup(data2,"html.parser") #讓BeautifulSoup解析HTML格式文件
            contents = root2.find("div",class_="markdown__style").text #找出內文
            ftext.write(contents+"\n\n") #將內文寫入txt檔
    #抓取下一頁的連結
    nextLink = root.find("a",string = "下一頁") #找到內文是 下一頁 的標籤a
    return nextLink["href"] #回傳下一頁的網址


#定義函式 SowPlt 將圖顯式並儲存。第一個參數 x 為X軸上各標籤(tag)的名稱，第二個參數 y 為Y軸上的高度
def ShowPlt(x,y):
    plt.figure(figsize = (200,75)) #設定圖的外框大小
    plt.title("Hot-Tag") #將徒的標題訂為Hot-Tag
    plt.xlabel("TagName") #將X軸座標命名為TagName
    plt.ylabel("Frequency") #將Y軸座標命名為Frequency
    plt.bar(x,y) #將長條圖製作出來
    plt.show() #顯示分析圖


#主程式碼

pageURL = "https://ithelp.ithome.com.tw/" #將起始網頁的網址存到pageURL裡
count = 0 #count用來表示想抓取幾頁
#重複抓取每頁資料
while count<500:
    pageURL = GetData(pageURL) #將 return 回來的網址覆蓋到pageURL上，以便重複利用。第二個參數 count*30 是因為每一頁有30篇
    count += 1 #執行完一次後增加1，以確保能抓到預期的頁數


pattern = {} #創立空字典，後續作圖使用
#將dic字典中每個key及value寫入tag.txt中
with open("tag.txt",mode="a",encoding = "utf-8") as ftext:
    #將dic中的key取出
    for key in dic:
        ftext.write(key+":") #寫入字典中的key
        ftext.write(str(dic[key])+"\n") #寫入字典中的value
        #只將字典value的值大於100的資料加進pattern裡
        if dic[key] > 100:
            pattern[key] = dic[key] #將pattern這個空字典加入符合條件的資料
with open("tag_key.txt",mode="a",encoding = "utf-8") as tagname:
    for key in dic:
        CountWord = 0
        for i in key:
            CountWord += 1
        if CountWord != 1:
            tagname.write(key+"\n")


#總共做成三張圖表
patternX1 = [] #第一張圖表X軸資料
patternY1 = [] #第一張圖表Y軸資料
patternX2 = [] #第二張圖表X軸資料
patternY2 = [] #第二張圖表Y軸資料
patternX3 = [] #第三張圖表X軸資料
patternY3 = [] #第三張圖表Y軸資料
div = 0 #為了分成3張圖表而使用此變數
#從 pattern 這個字典裡分成三張圖表的X和Y軸資料
for key in pattern:
    #第一章圖表資料
    if div % 3 == 0:
        patternX1.append(key)
        patternY1.append(pattern[key])
    #第二章圖表資料
    elif div %3 == 1:
        patternX2.append(key)
        patternY2.append(pattern[key])
    #第三章圖表資料
    else:
        patternX3.append(key)
        patternY3.append(pattern[key])
    div += 1 #讓每張圖表的資料盡可能平均

ShowPlt(patternX1,patternY1) #顯示第一張圖表
ShowPlt(patternX2,patternY2) #顯示第二張圖表
ShowPlt(patternX3,patternY3) #顯示第三張圖表


largest_value = 0 #將最熱門標籤(value)的值設為0
#將字典走訪一遍並比較每個 value 跟 largest_value 的大小
for key in dic:
    #如果 largest_value 比較小，則將 largest_value 設為 dic[key]
    if dic[key] > largest_value:
        largest_value = dic[key] #將 largest_value 設為 dic[key]
        largest_key = key #將比較大的 largest_value 的 key 記錄下來 
print(largest_key,largest_value) #在底下視窗印出最熱門的標籤名稱及其值


contentURL = "https://ithelp.ithome.com.tw/" #將起始網頁的網址存到pageURL裡
count2 = 0 #count2用來表示想抓取幾頁
#重複抓取每頁資料
while count2<500:
    contentURL = GetHotTagContent(contentURL,largest_key) #將 return 回來的網址覆蓋到contentURL上，以便重複利用。第二個參數將最熱門的標籤(tag)傳入函式裡
    count2 += 1 #執行完一次後增加1，以確保能抓到預期的頁數
