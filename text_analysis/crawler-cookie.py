#抓取PTT八卦版的網頁原始碼(HTML)
import urllib.request as req
def getData(url):
    #建立一個Request物件，附加Request Headers的資訊
    request = req.Request(url,headers = {
        "cookie":"over18=1",
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    #print(data)
    #解析原始碼，取得每篇文章的標題
    import bs4
    root = bs4.BeautifulSoup(data,"html.parser") #讓BeautifulSoup協助我們解析HTML格式文件
    #print(root.title) #印出包含title標籤的內容
    #print(root.title.string) #印出title標籤內的文字
    titles = root.find("div",class_="title") #尋找class_=title的div標籤
    #print(titles) #印出包含class=title標籤的內容
    #print(titles.a) #印出包含a標籤內的部分
    #print(titles.a.string) #印出a標籤內的文字
    all_titles = root.find_all("div",class_="title") #以列表形式找出所有class_=title的div標籤
    for title in all_titles:
        if title.a != None: #如果標題包含a標籤(沒有被刪除)，印出來
            print(title.a.string)

    #抓取上一頁的連結
    nextLink = root.find("a",string="‹ 上頁") #找到內文是 ‹ 上頁 的a標籤
    #print(nextLink) #將整個a標籤內的內容印出
    #print(nextLink["href"]) #印出標籤a裡屬性為href的內容
    return nextLink["href"]
#主程序 : 抓取多個頁面的標題
pageURL = "https://www.ptt.cc/bbs/Gossiping/index.html"
count = 0
while count<3:
    pageURL = "http://www.ptt.cc"+getData(pageURL)
    count += 1