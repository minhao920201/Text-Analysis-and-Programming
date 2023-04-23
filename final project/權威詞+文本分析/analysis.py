import re #引入re模組
from matplotlib import pyplot as plt #引入matplotlib模組，用以製作圖表


#定義函式 SowPlt 將圖顯式並儲存。第一個參數 x 為X軸上各標籤(tag)的名稱，第二個參數 y 為Y軸上的高度
def ShowPlt(x,y):
    plt.figure(figsize = (200,75)) #設定圖的外框大小
    plt.title("Hot-Tag") #將徒的標題訂為Hot-Tag
    plt.xlabel("TagName") #將X軸座標命名為TagName
    plt.ylabel("Frequency") #將Y軸座標命名為Frequency
    plt.bar(x,y) #將長條圖製作出來
    plt.show() #顯示分析圖


#文本分析
dic = {} #建立空字典，用來記錄標籤名稱(key)及其出現的次數(value)
#開檔進行讀取
with open("finalproject.txt",mode = "r",encoding = "utf-8") as ftext:
    reading = ftext.read() #將檔案讀取到的內容傳給reading
    target = re.compile(r"標籤:.*") #利用正規表示是找出"標籤:"及其後面的文字
    result = target.findall(reading) #找所有的target
    ch = "標籤:" #後面用來排除"標籤:"的字串變數
    #因為第20行findall得到的結果為列表，所以利用迴圈將列表中的東西一一取出
    for row in result:
        string = "".join(x for x in row if x not in ch) #排出"標籤:"
        #因為抓文本實有利用空白將標籤隔開，因此利用split()將每個標籤名稱一一取出
        for j in string.split():
            dic[j] = dic.get(j,0)+1 #確認dic字典裡有沒有出現過該標籤(tag)名稱，如果沒出現過則將該標籤(tag)名稱加入並將其value+1，反之，若已出現過則將value直接+1。


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

#將dic字典中的key寫入tag_key.txt中
with open("tag_key.txt",mode="a",encoding = "utf-8") as tagname:
    #將dic中的key取出
    for key in dic:
        CountWord = 0 #避免抓取一個字的標籤名稱
        #確認標籤名稱的字數
        for i in key:
            CountWord += 1
        #將大於1個字的標籤名稱寫入檔案中
        if CountWord != 1:
            if CountWord != 2:
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