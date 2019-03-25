class Student:
	def __init__(self):
		self.name = " "
		self.mid = 0
		#self.final =0
	def setName(self,name):
		self.name = name
	def setMid(self,mid):
		self.mid = mid
	def __str__(self):
		return self.name+"\t"+self.mid
class SonStudent(Student):
	def __init__(self,number):
		super().__init__()
		self.number = number
	def __str__(self):
		return self.name+"\t"+self.mid+"\t"+self.num
		
def main():
	list=[]
	carryOn ='Y'
	while(carryOn =='Y'):
		
		name =input()
		mid = input()
		num = input()
		st =SonStudent(num)
		st.setName(name)
		st.setMid(mid)
		#st = SonStudent(num)
		carryOn =='N'
		print(st)
main()
