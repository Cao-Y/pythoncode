from random import randint
import pygal
class Die():
    """表示一个骰子的类"""
    def __init__(self,num_sides=6):
        self.num = num_sides  #骰子6个面
    def roll(self):
        return(randint(1,self.num))

tou =Die()
result =[]
for num in range(1000000):
    number =tou.roll()
    result.append(number)
#分析结果
frequency = []
for num in range(1,tou.num+1):
    fre = result.count(num)
    frequency.append(fre)
hist =pygal.Bar()
hist.title="RESULT"
hist.x_labels=['1','2','3','4','5','6']
hist.x_title="Result"
hist.y_title = "Frequency"
hist.add('D6',frequency)
hist.render_to_file('test.svg')
#print(result)
print(frequency)