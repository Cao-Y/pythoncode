import matplotlib.pyplot as plt
squares =[1,4,9,16,25]
plt.plot(squares)
plt.title("LearnMat",fontsize = 24)
plt.xlabel("X",fontsize = 16)
plt.ylabel("Y",fontsize = 16)


p1=plt.scatter(2,4,s=200)
p2=plt.scatter(squares,squares,s=100)
x=list(range(1,1001))
y = [i**2 for i in x]

plt.scatter(x,y,s=4,c=y,cmap="Greens")
plt.legend([p1,p2],['label1','label2'])
plt.show()