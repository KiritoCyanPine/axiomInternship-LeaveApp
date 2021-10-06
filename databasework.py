from app import db, User, Leave , generate_password_hash

db.create_all()
usrnames = ["@trash" , "@lonewolf", "@mainheroin", "@mr.x"]
fnames = ["kushida" , "suzune", "karuizawa", "ayanokoji"]
lname = ["kikyo", "horikita", "kei", "kiyotaka"]
isAdmin = [False,False,False,True]

bis = zip(usrnames ,fnames ,lname ,isAdmin )
for i,j,k,l in bis:
	a = User(username=i,first_name=j,last_name=k,isAdmin=l ,password=generate_password_hash("password", method='sha256'))
	db.session.add(a)
	db.session.commit()

#a = User(username="ayanokouji",first_name="ayanokouji",last_name="kiyotaka" )
#db.session.add(a)
#db.session.commit()
