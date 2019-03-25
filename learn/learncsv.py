import  csv

filename = "learnuse.csv"
#给encoding传参数，因为默认以gbk的格式解码文件#
#另外utf-8格式需要在文件开头加入一个BOM标识：'\ufeff，可以使用utf-8-sig
file = open(filename,encoding="utf-8-sig") #以读的方式打开文件
reader =csv.reader(file)    #创建一个与文件相关联的reader对象
#读阅读器对象返回文件的下一行
readline = next(reader)

for index,head in enumerate(readline):
    print(index,head)
#print(readline)   #输出
jianJie = []
for row in reader:
    jianJie.append(row[15])
print(jianJie)