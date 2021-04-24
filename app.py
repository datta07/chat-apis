from flask import Flask,request,jsonify
import sqlite3

app=Flask(__name__)

msgId=None

@app.route("/")
def home():
	return "hello args is"

@app.route("/addUser")
def addUser():
	groups=None
	UserName = request.args.get('username')
	Password = request.args.get('password')
	if 'groups' in request.args:
		groups=request.args.get('groups')
	try:
		con=sqlite3.connect("Auth.db")
		con.execute("CREATE TABLE IF NOT EXISTS AUTH (UserName TEXT PRIMARY KEY,Password TEXT,groups Text)")
		con.execute("INSERT INTO AUTH VALUES (?,?,?)",(UserName,Password,groups))
		con.commit()
		con.close()
		return jsonify({"status":"Success","msg":"User Registered succesfully"})
	except Exception:
		con.close()
		return jsonify({"status":"Fails","msg":"User Already exist"})

@app.route("/checkUser")
def checkUser():
	UserName = request.args.get('username')
	Password = request.args.get('password')
	try:
		con=sqlite3.connect("Auth.db")
		data=con.execute("SELECT Password from AUTH where UserName=(?)",(UserName,))
		for i in data:
			if (i[0]==Password):
				return jsonify({"status":"Success","msg":"Auth succesful,he can login"})
			else:
				return jsonify({"status":"Fails","msg":"Password Fails"})
		return jsonify({"status":"Fails","msg":"No User Name exist as "+UserName})
	except Exception:
		return jsonify({"status":"Fails","msg":"No User Name exist as "+UserName})

@app.route("/createGroup")
def createGroup():
	groupName = request.args.get('groupname')
	admin=request.args.get('username')
	con=sqlite3.connect("tables.db")
	con.execute("CREATE TABLE IF NOT EXISTS groupInfo (GroupName TEXT PRIMARY KEY,adminName TEXT,usersCount Number)")
	try:
		con.execute("INSERT INTO groupInfo VALUES(?,?,1)",(groupName,admin))
	except Exception:
		con.close()
		return jsonify({"status":"Fails","msg":"Group Already Exists"})
	con.execute("CREATE TABLE "+groupName+" (msgId NUMBER PRIMARY KEY,message TEXT,userName TEXT,likes NUMBER,tagsWith NUMBER)")
	con1=sqlite3.connect("Auth.db")
	group=""
	data=con1.execute("SELECT groups from AUTH where UserName=(?)",(admin,))
	flag=False
	for i in data:
		flag=True
		if (i[0]!=None):
			group+=i[0]
	if (not flag):
		con.close()
		con1.close()
		return jsonify({"status":"Fails","msg":"No such user found"})
	if (group!=""):
		group+=(","+groupName)
	else:
		group+=groupName
	con1.execute("UPDATE Auth SET groups=(?) WHERE UserName=(?)",(group,admin))
	con.commit()
	con.close()
	con1.commit()
	con1.close()
	return jsonify({"status":"Success","msg":"Successfully created the group and joined "+admin})

@app.route("/joinGroup")
def joinGroup():
	try:
		UserName = request.args.get('username')
		groupName=request.args.get("group")
		con1=sqlite3.connect("tables.db")
		data=con1.execute("SELECT usersCount from groupInfo WHERE GroupName=(?)",(groupName,))
		for i in data:
			count=i[0]
		con1.execute("UPDATE groupInfo SET usersCount=(?) WHERE GroupName=(?)",(count+1,groupName))
		con=sqlite3.connect("Auth.db")
		group=""
		data=con.execute("SELECT groups from AUTH where UserName=(?)",(UserName,))
		for i in data:
			if (i[0]!=None):
				group+=i[0]
		if (groupName in group.split(",")):
			con.close()
			con1.close()
			return jsonify({"status":"Fails","msg":"User Already exists"})
		if (group!=""):
			group+=(","+groupName)
		else:
			group+=groupName
		con.execute("UPDATE Auth SET groups=(?) WHERE UserName=(?)",(group,UserName))
		con.commit()
		con.close()
		con1.commit()
		con1.close()
		return jsonify({"status":"Success","msg":"Successfully added to group"})
	except Exception:
		con1.close()
		return jsonify({"status":"Fails","msg":"no such group"})

@app.route("/sendMessage")
def sendMessage():
	global msgId
	try:
		if msgId==None:
			conx=sqlite3.connect("tables.db")
			conx.execute("CREATE TABLE IF NOT EXISTS maxId(id NUMBER)")
			data=conx.execute("SELECT id FROM maxId")
			for i in data:
				msgId=i[0]
			if (msgId==None):
				msgId=0
		groupName = request.args.get('groupname')
		userName=request.args.get('username')
		message=request.args.get('message')
		tag=None
		if ("tagsWith" in request.args):
			tag=request.args.get('tagsWith')
		# check whether he belongs to the group
		con=sqlite3.connect("Auth.db")
		data=con.execute("SELECT groups from AUTH where UserName=(?)",(userName,))
		for i in data:
			groups=i[0]
		if (groupName not in groups.split(",")):
			con.close()
			return jsonify({"status":"Fails","msg":"User does not Belongs to the group"})
		con.close()
		con1=sqlite3.connect("tables.db")
		con1.execute("INSERT INTO "+groupName+" VALUES(?,?,?,?,?)",(msgId+1,message,userName,0,tag))
		if (msgId==0):
			con1.execute("INSERT INTO maxId values(?)",(msgId+1,))	
		else:
			con1.execute("UPDATE maxId SET id=(?) WHERE Id=(?)",(msgId+1,msgId))
		msgId+=1	
		con1.commit()
		con1.close()
		return jsonify({"status":"Success","msg":"Sended message"})
	except Exception:
		return jsonify({"status":"Fails","msg":"Invalid parameters check back once"})

@app.route("/viewChat")
def viewChat():
	groupName = request.args.get('groupname')
	con=sqlite3.connect("tables.db")
	data={"status":"Success","msgs":[]}
	try:
		rawData=con.execute("SELECT * FROM "+groupName)
	except Exception:
		return jsonify({"status":"Fails","msg":"No such group exists"})
	for i in rawData:
		data["msgs"].append({
			"id":i[0],
			"msg":i[1],
			"name":i[2],
			"likes":i[3],
			"tagsWith":i[4]
			})
	return jsonify({"status":"Success","msg":data})

@app.route("/giveLike")
def giveLike():
	groupName = request.args.get('groupname')
	msgId = request.args.get('msgid')
	con=sqlite3.connect("tables.db")
	try:
		data=con.execute("SELECT likes FROM "+groupName+" WHERE msgId=(?)",(msgId,))
		for i in data:
			count=i[0]
		con.execute("UPDATE "+groupName+" SET likes=(?) WHERE msgId=(?)",(count+1,msgId))
		con.commit()
		con.close()
		return jsonify({"status":"Success","msg":"No of likes are "+str(count+1)})
	except Exception:
		return jsonify({"status":"Fails","msg":"check back msgId and group name"})

@app.route("/groupInfo")
def groupInfo():
	groupName = request.args.get('groupname')
	con=sqlite3.connect("tables.db")
	rawData=con.execute("SELECT * FROM groupInfo WHERE GroupName=(?)",(groupName,))
	data={}
	for i in rawData:
		data={
		"group name":i[0],
		"admin":i[1],
		"users":i[2]}
	con.close()
	if (len(data)==0):
		return jsonify({"status":"Fails","msg":"Invalid group name"})
	return jsonify({"status":"Success","msg":data})

@app.route("/userInfo")
def userInfo():
	userName = request.args.get('username')
	con=sqlite3.connect("Auth.db")
	rawData=con.execute("SELECT * FROM AUTH WHERE UserName=(?)",(userName,))
	data={}
	for i in rawData:
		data={
		"User Name":i[0],
		"groups":i[2]}
	con.close()
	if (len(data)==0):
		return jsonify({"status":"Fails","msg":"Invalid user name"})
	return jsonify({"status":"Success","msg":data})

app.run(debug=True,host='0.0.0.0')