class Restaurant():
	def __init__(self,rname,rtype):
		self.name = rname
		self.type = rtype
	def open(self):
		print(self.name+" "+self.type)
res = Restaurant("happy","no")
res.open()
class User():
	def __init__(self,first_name,last_name):
		self.fname = first_name
		self.lname = last_name
	def describe_user(self):
		print(self.fname+"  sss  "+self.lname)
user = User("wen","zhe")
user.describe_user()
 

		
