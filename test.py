'''
- User should either login or register to use 
- chat can be seen by anyone but message can be sent by only users who have joined group
- join the group before to send message
'''

import requests

user=None
def login():
	global user
	print(("-"*30)+"\n"+"Login:- "+"\n"+("-"*30))
	username=input("Enter username: ")
	password=input("Enter Password: ")
	res=requests.get("http://localhost:5000/checkUser?username="+username+"&password="+password).json()
	if (res["status"]=="Success"):
		user=username
	print(res["msg"])

def register():
	global user
	print(("-"*30)+"\n"+"Register:- "+"\n"+("-"*30))
	username=input("Set username: ")
	password=input("Set Password: ")
	res=requests.get("http://localhost:5000/addUser?username="+username+"&password="+password).json()
	if (res["status"]=="Success"):
		user=username
	print(res["msg"])

def createGroup():
	print(("-"*30)+"\n"+"Creating a Group"+"\n"+("-"*30))
	name=input("Enter Group Name:  ")
	res=requests.get("http://localhost:5000/createGroup?groupname="+name+"&username="+user).json()
	print(res["msg"])
	if (res["status"]=="Success"):
		pass

def joinGroup():
	print(("-"*30)+"\n"+"Joining a group"+"\n"+("-"*30))
	name=input("Enter Group Name to join:  ")
	res=requests.get("http://localhost:5000/joinGroup?group="+name+"&username="+user).json()
	print(res["msg"])
	if (res["status"]=="Success"):
		pass

def viewInfo():
	info=int(input("Enter the information for which you need\n 1)Group 2)User\nEnter :"))
	if info==1:
		name=input("Enter the group name:  ")
		res=requests.get("http://localhost:5000/groupInfo?groupname="+name).json()
		print(res["msg"])
	elif info==2:
		name=input("Enter the user name:  ")
		res=requests.get("http://localhost:5000/userInfo?username="+name).json()
		print(res["msg"])

def viewChat():
	q="2"
	name=None
	while (q!="3"):
		if (q=="2"):
			if not name:
				name=input("Enter Group Name to chat:  ")
			res=requests.get("http://localhost:5000/viewChat?groupname="+name).json()
			if (res["status"]=="Success"):
				msg="\nMessages "+name+"\n"+("-"*30)+"\n"
				for i in res["msg"]["msgs"]:
					msg+=(i["name"]+" :    "+i["msg"]+"\n")
				qmsg="\nchoose one\n 1)send message 2)reload 3)go back \n Choose one:  "
				q=input(msg+("-"*30)+"\n"+qmsg+"\n")
		elif (q=="1"):
			msg=input("Enter msg:  ")
			res=requests.get("http://localhost:5000/sendMessage?groupname="+name+"&username="+user+"&message="+msg).json()
			print(res["msg"])
			q="2"


while True:
	if (not user):
		no=int(input(("-"*30)+"\n"+" Please login or register to continue:\n 1)Login 2)Register\n"+("-"*30)+"\n"+" Enter option (1 or 2):  "))
		if (no==1):
			login()
		elif (no==2):
			register()
	else:
		ques="\n 1)create a Group\n 2)join a Group\n 3)Chat in group \n 4)view Infos"+"\n"+("-"*30)+"\nEnter an option: "
		ops=int(input(("-"*30)+"\n hi "+user+"\n"+("-"*30)+ques+"\n"))
		if ops==1:
			createGroup()
		elif ops==2:
			joinGroup()
		elif ops==3:
			viewChat()
		elif ops==4:
			viewInfo()
	print("")
