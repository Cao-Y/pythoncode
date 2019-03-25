import json
numbers=[1,2,3,4,5,6,7,8]
with open('numbers.json') as file:
	#json.dump(numbers,file)
	number=json.load(file)
print(number)
