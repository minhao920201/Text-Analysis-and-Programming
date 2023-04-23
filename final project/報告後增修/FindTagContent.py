import urllib.request as req #引入urllib模組中函式名稱為request的函式為req
import bs4 #引入bs4模組
#定義函式getData，用以取得每一頁所有標題、標籤及內文。參數為網址
def getData(url):
    #建立一個Request物件，附加Request Headers的資訊
    request = req.Request(url,headers = {
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"
    })
    
    #打開request
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    root = bs4.BeautifulSoup(data,"html.parser") #讓BeautifulSoup解析HTML格式文件
    all_titles = root.find_all("h3",class_="qa-list__title") #以列表形式找出所有class_=qa-list__title的h3標籤
    all_tags = root.find_all("div",class_="qa-list__tags") #以列表形式找出所有class_=qa-list__tags的div標籤

    index = 0 #從all_tags中先找出對應的文章之index
    li_idx = [] #將上面index記錄到此列表中
    #使每一個文章的所有標籤做檢視
    for tag in all_tags:
        #如果python這個詞有在標籤裡(以python為例，當然也可使用其他標籤名稱)
        if "python" in tag.text:
            li_idx.append(index) #將該文章的index記錄到列表中
        index += 1 #每判斷完一個文章就換下一篇

    #將標籤名稱有python的詞寫入檔案
    with open("TagContent.txt",mode = "a",encoding = "utf-8") as ftext:
        #從剛才找到的所有index值一一取出，用以取得對應的文章
        for i in li_idx:
            ftext.write("標題:"+all_titles[i].a.string+"\n標籤:") #將標題寫入檔案

            url2 = all_titles[i].a["href"] #將內文的網址存到url2裡

            #建立一個Request物件，附加Request Headers的資訊
            request2 = req.Request(url2,headers = {
                "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"
            })

            #打開request2
            with req.urlopen(request2) as response2:
                data2 = response2.read().decode("utf-8")
            
            root2 = bs4.BeautifulSoup(data2,"html.parser") #讓BeautifulSoup解析HTML格式文件
            contents = root2.find("div",class_="markdown__style").text #找出內文
            tags = root2.find("div",class_="qa-header__tagGroup") #以列表形式找出所有 class_=qa-header__tagGroup 的 div 標籤
            #將標籤寫入檔案中並讓每個標籤名稱以空格作為間隔
            for tag in tags.text.split():
                ftext.write(tag+" ")
            ftext.write("\n"+contents+"\n\n") #將內文寫入content.txt裡

    #抓取下一頁的連結
    nextLink = root.find("a",string="下一頁") #找到內文是 下一頁 的標籤a
    return nextLink["href"] #回傳下一頁的網址
pageURL = "https://ithelp.ithome.com.tw/"
count = 0 #紀錄要取幾頁
#一頁一頁找出對應的標籤文章
while count<500:
    pageURL = getData(pageURL) #將回傳的下一頁網址改寫到pageURL中
    count += 1 #+1以確保能找出所需的量