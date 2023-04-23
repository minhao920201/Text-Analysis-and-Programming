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
    all_titles = root.find_all("h3",class_="qa-list__title") #以列表形式找出所有class_=title的h3標籤


    #開啟finalproject.txt並用a模式保留原本資料並將新的資料寫入
    with open("finalproject.txt",mode = "a",encoding = "utf-8") as ftext:
        #此迴圈會找出該頁所有標題、標籤及內文
        for title in all_titles:
            ftext.write("標題:"+title.a.string+"\n標籤:") #將內文的標題寫入finalproject.txt裡

            url2 = title.a["href"] #將內文的網址存到url2裡

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


pageURL = "https://ithelp.ithome.com.tw/" #將起始網頁的網址存到pageURL裡
count = 0 #count用來表示想抓取幾頁
#重複抓取每頁資料
while count<500:
    pageURL = getData(pageURL) #將 return 回來的網址覆蓋到pageURL上，以便重複利用
    count += 1 #執行完一次後增加1，以確保能抓到預期的頁數