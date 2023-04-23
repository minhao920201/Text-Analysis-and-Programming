import urllib.request as req
import bs4
url = "https://ithelp.ithome.com.tw/"
request = req.Request(url,headers={
    "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
})

with req.urlopen(request) as response:
    data = response.read().decode("utf-8")
#print(data)

root = bs4.BeautifulSoup(data,"html.parser")
tags = root.find_all("div",class_="qa-list__tags")
titles = root.find_all("h3",class_="qa-list__title")
index = 0
li_index = []
for tag in tags:
    if "python" in tag.text:
        print("yes")
        print(index)
        li_index.append(index)
    else:
        print("no")
    index += 1
    print(tag.text)

print(li_index)

with open("findTitle.txt",mode = "a", encoding = "utf-8") as ftext:
    for id in li_index:
        ftext.write("網址:"+titles[id].a["href"]+"\n")
        url2 = titles[id].a["href"]
        request2 = req.Request(url2,headers={
            "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
        })
        with req.urlopen(request2) as response2:
            data2 = response2.read().decode("utf-8")
        
        root2 = bs4.BeautifulSoup(data2,"html.parser") #讓BeautifulSoup解析HTML格式文件
        contents = root2.find("div",class_="markdown__style").text #找出內文
        ftext.write(contents+"\n")
        #print(contents)

        #print(titles[id].a["href"])

