# CHAT APIS

## API'S End-Points :
### /addUser :
    - adds user to database- params 
    - params : ( username , password )
    - http://localhost:5000/addUser?username=datta&password=guru

### /checkUser :
    - checks whether userName matchs with password
    - params : ( username , password )
    - http://localhost:5000/checkUser?username=datta&password=guru
    
### /createGroup :
    - creates a group and user becomes admin and automatcally joins the group
    - params : ( groupname , username )
    - http://localhost:5000/createGroup?groupname=room1&username=datta

### /joinGroup :
    - Joins other users into group
    - params : (username , group )
    - http://localhost:5000/joinGroup?username=datta&group=room1

### /sendMessage :
    - if user in group then message sends to all group members
    - params : ( groupname , username , message , tagswith {optional} )
    - http://localhost:5000/sendMessage?groupname=room1&username=datta&message=where%20are%20you
    
### /viewChat :
    - json that returns full chat data of the group
    - params : ( groupname )
    - http://localhost:5000/viewChat?groupname=room1
 
### /giveLike :
    - give a like to message
    - params : ( groupname , msgid )
    - http://localhost:5000/giveLike?groupname=room1&msgid=3

### /groupInfo :
    - information about a group
    - params : ( groupname )
    - http://localhost:5000/groupInfo?groupname=room1

### /userInfo :
    - information about a user (mainly groups involved by user)
    - params : ( username )
    - http://localhost:5000/userInfo?username=datta
