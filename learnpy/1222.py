alien={'x':0,'y':25,'speed':'medium'}
print("origin: "+str(alien['x']))
if(alien['speed'] == 'slow') :
	x_in =1
elif (alien['speed'] =='medium') :
	x_in = 2
elif (alien['speed'] =='fast') :
	x_in = 3
alien['x'] = alien['x'] +x_in
print("now: "+str(alien['x']))
alien['speed'] = 'fast'
print("now: "+str(alien['x']))
print(alien)
for key,value in alien.items() :
	print(key)
	print(value)
age = input('please input')
print(age)
print(type(age))
for num in range(1,11):
	if(num%2==0) :
		continue
	else:
		print(num)


