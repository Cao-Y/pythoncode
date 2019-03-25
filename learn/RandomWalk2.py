from RandomWalk1 import RandomWalk
import  matplotlib.pyplot as plt

while(True):
    iw = RandomWalk(50000)
   # start = time.time()
    iw.walk()
    plt.figure(figsize=(10,6))
    point= list(range(iw.num_points))

    plt.scatter(iw.x,iw.y,c=point,cmap="Reds",s=15)
    plt.scatter(0, 0, c="Green", s=50)
    plt.scatter(iw.x[-1],iw.y[-1],c="black",s=50)
    plt.axes().get_xaxis().set_visible(False)
    plt.axes().get_yaxis().set_visible(False)
    #end = time.time()
    #plt.scatter(iw.x,iw.y,s=15)
    plt.show()