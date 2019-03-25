#x = input()
#if(0<=int(x)<100):
#	print("sssss")
#else:
#	print("nononono")
import random
list=[i for i in range(1,5)]
print(list)
print(random.choice(list))
print(random.sample(list,2))
random.shuffle(list)
print(list)
