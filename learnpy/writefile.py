with open('test1.txt','a') as file:
	file.write('i love python too\n')
with open('test1.txt') as file:
	contests = file.read()
	print(contests)
