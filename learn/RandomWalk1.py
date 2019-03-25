from random import choice

class RandomWalk():
    """一个生成随机漫步的类"""
    def __init__(self,num_points=50000):
        self.num_points = num_points
        self.x=[0]
        self.y=[0]
    def walk(self):
        """计算随机漫步包含的所有点"""
        while(len(self.x)<self.num_points):
            x_dir = choice([1,-1])
            x_dis = choice([0,1,2,3,4])
            x_step = x_dir * x_dis

            y_dir = choice([1, -1])
            y_dis = choice([0, 1, 2, 3, 4])
            y_step = y_dir * y_dis

            if x_step==0 and y_step ==0:
                continue
            next_x = self.x[-1] + x_step
            next_y = self.y[-1] + y_step

            self.x.append(next_x)
            self.y.append(next_y)

from datetime import datetime
import matplotlib.pyplot as plt
import time
iw =RandomWalk()
start = time.time()
iw.walk()
end = time.time()
plt.scatter(iw.x,iw.y,s=15)
end2 = time.time()
plt.show()
print(end-start)
print((end2 - start))
#print(time.strftime("%Y/%m/%d/ %H:%M:%S"))
print(time.time())
t=time.strftime("%Y/%m/%d/ %H:%M:%S")
print(t)
s = datetime.strptime(t,"%Y/%m/%d/ %H:%M:%S")
print(s)
print(type(s))
#m=time.strftime("%Y/%m/%d/",s)
#print(m)