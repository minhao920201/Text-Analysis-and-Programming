#儲存檔案
"""
file = open("data.txt",mode = "w",encoding = "utf-8") #開啟  encoding="utf-8" 是為了要顯示中文字
file.write("Hello txt\n好棒棒") #操作
file.close() #關閉
"""

with open("data.txt",mode = "w",encoding = "utf-8") as file:
    file.write("5\n3")

#讀取檔案
"""
sum = 0
with open("data.txt",mode = "r",encoding = "utf-8") as file:
    #data = file.read() #將整個txt中的內容讀出來
    for line in file: #一行一行的讀出來
        sum += int(line)
#print(data)
print(sum)
"""

#json 讀檔+寫入
import json
#從檔案中讀取json資料，並存放到變數data中
with open("config.json",mode = "r",encoding = "utf-8") as file:
    data = json.load(file)
print(data) #data是一個字典資料
print("name",data["name"])
print("version",data["version"])
data["name"] = "New Name" #修改變數中的資料

#把最新的資料婦複寫回檔案裡
with open("config.json",mode = "w",encoding = "utf-8") as file:
    json.dump(data,file)
print(data)
print("name",data["name"])
print("version",data["version"])