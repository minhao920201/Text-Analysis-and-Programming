import urllib.request as req #引入urllib模組中函式名稱為request的函式為req
import bs4 #引入bs4模組
#定義函式getData，用以取得每一頁所有標題、內文網址及內文
def getData(url):
    #建立一個Request物件，附加Request Headers的資訊
    request = req.Request(url,headers = {
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"
    })
    
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    #print(data)
    #解析原始碼，取得每篇文章的標題
    
    root = bs4.BeautifulSoup(data,"html.parser") #讓BeautifulSoup協助我們解析HTML格式文件
    #print(root.title) #印出包含title標籤的內容
    #print(root.title.string) #印出title標籤內的文字
    titles = root.find("div",class_="title") #尋找class_=title的div標籤
    #print(titles) #印出包含class=title標籤的內容
    #print(titles.a) #印出包含a標籤內的部分
    #print(titles.a.string) #印出a標籤內的文字
    #title = root.find("h3",class_="qa-list__title")
    #print(title.a.string)
    #print(title.a["href"]) #印出內文網址

    all_titles = root.find_all("h3",class_="qa-list__title") #以列表形式找出所有class_=title的div標籤
    for title in all_titles:
        with open("content.txt",mode = "a",encoding = "utf-8") as ftext:

            ftext.write(title.a["href"]+"\n")
            ftext.write(title.a.string+"\n")
            #print(title.a["href"])
            #print(title.a.string)

            url2 = title.a["href"]
            request2 = req.Request(url2,headers = {
                "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"
            })
            with req.urlopen(request2) as response2:
                data2 = response2.read().decode("utf-8")
            #print(data2)

            root2 = bs4.BeautifulSoup(data2,"html.parser")
            title2 = root2.find("div",class_="markdown__style").text
            #content = title2.find("p")
            ftext.write(title2+"\n")
            print(title2)


    #抓取下一頁的連結
    nextLink = root.find("a",string="下一頁") #找到內文是 下一頁 的標籤a
    #print(nextLink)
    #print(nextLink["href"]) #印出標籤a裡屬性為href的內容
    return nextLink["href"]

pageURL = "https://ithelp.ithome.com.tw/"
count = 0
while count<3:
    pageURL = getData(pageURL)
    count += 1