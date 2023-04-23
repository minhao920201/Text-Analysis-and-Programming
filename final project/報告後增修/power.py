#將檔案中的資料作讀取
with open("TagContent.txt",mode = "r",encoding = "utf-8") as ftext:
    reading = ftext.read() #將檔案讀取到的資料傳入變數中
li = [] #取出英文字詞
#將文章中的英文做處理，當遇到中文或空白時，將中文或空白前所記錄到的英文字寫入檔案中
with open("power.txt",mode = "a",encoding = "utf-8") as ftext:
    #以空白當做區隔，避免有一長串英文字母
    for i in reading.split():
        count = 1 #用來與下面的preCount做出變化量的比較，如果兩者不同，代表出現非英文字，此時就要把出現非英文字前的英文字加入檔案中
        preCount = count #用來與上面的count做出變化量的比較，如果兩者不同，代表出現非英文字，此時就要把出現非英文字前的英文字加入檔案中
        #把空白前的一段文字一個一個取出
        for j in i:
            #如果是英文字，則加入list中
            if 64<ord(j)<91 or 96<ord(j)<123:
                li.append(j)
            #如果出現非英文字，則讓count-1
            else:
                count -= 1
            #當count與preCount不同時
            if preCount != count:
                #當非空List時
                if len(li) !=0:
                    #將List中的每一個字寫入檔案中
                    for k in li:
                        ftext.write(k)
                    ftext.write("\n") #換行以示區隔
                    li = [] #讓List清空，重新抓取英文字
                preCount = count #讓preCount=count以確保不會每次判斷"if preCount != count:"時都必須進入if裡面
        #如果List當中有英文字，讓最後出現的英文字佳入檔案中，避免最後出現的英文字與下一段出現的英文字結合在一起
        if len(li) !=0:
            #將List中的每一個字寫入檔案中
            for k in li:
                ftext.write(k)
            ftext.write("\n")#換行以示區隔
        li = [] #讓List清空，重新抓取英文字