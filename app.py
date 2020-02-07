from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug, os
import pyrebase



firebaseConfig = {
    "apiKey": "AIzaSyBckkcgqyVlZtS4XiRVgopRc3oJeA_awiM",
    "authDomain": "metro-authentication.firebaseapp.com",
    "databaseURL": "https://metro-authentication.firebaseio.com",
    "projectId": "metro-authentication",
    "storageBucket": "metro-authentication.appspot.com",
    "messagingSenderId": "790217813817",
    "appId": "1:790217813817:web:d431cfc545eab3a248c2e8",
    "measurementId": "G-SD1788TX4L"
  }

app = Flask(__name__)
api = Api(app)



firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class user_balance(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('balance',type=str,required=True,help='balance cant be blank')
        parser.add_argument('user_id',type=str,required=True,help='user_id cant be blank')

        data = parser.parse_args()
        balance = data['balance']
        user_id = data['user_id']

        all_users = db.child("users").get()

        for user in all_users.each():
            if user_id == user.key():
                flag = 1
                user_data = user.val()
                curr_balance = int(user_data["balance"])
                break
            else:
                flag = 0

        if flag==0:
            return {"message":"user not found , transaction unsuccessful"}


        if flag:
            try:
                print(balance)
                new_balance = int(balance) + curr_balance
                db.child("users").child("{}".format(user_id)).update({"balance": "{}".format(new_balance)})
                return {"message":"transaction successful",
                        "status":"balance updated"}
            except:
                return {"message":"transaction unsuccessful",
                        "error":"invalid amount"}

    def get(self):
    	# parser = reqparse.RequestParser()
    	# parser.add_argument('user_id',type=str,required=True,help='user_id cant be blank')
    	# data = parser.parse_args()
    	# user_id = data['user_id']

    	user_id = "user_1"

    	all_users = db.child("users").get()

    	for user in all_users.each():
            if user_id == user.key():
                flag = 1
                user_data = user.val()
                curr_balance = int(user_data["balance"])

                return {"balance":"{}".format(curr_balance)}

            else:
                flag = 0

            if flag==0:
            	return {"message":"user not found , balance cant be updated"}

class source(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('user_id',type=str,required=True,help='user_name cant be blank')

		data = parser.parse_args()

		user_id = data['user_id']

		all_users = db.child("users").get()

		for user in all_users.each():
			if user.key() == user_id:
				db.child("users").child("{}".format(user_id)).update({"flag": "1"})
				return {"message":"flag has been to set to 1"}
		return {"message":"user not in database"}

class destination(Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('user_id',type=str,required=True,help='user_name cant be blank')

		data = parser.parse_args()

		user_id = data['user_id']

		all_users = db.child("users").get()

		for user in all_users.each():
			if user.key() == user_id:
				db.child("users").child("{}".format(user_id)).update({"flag": "0"})
				user_data = user.val()
				curr_balance = int(user_data['balance'])
				curr_balance = curr_balance - 25
				db.child("users").child("{}".format(user_id)).update({"balance": "{}".format(curr_balance)})
				return {"message":"flag has been to set to 0 and balance updated"}
		return {"message":"user not in database"}


class user_data(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name',type=str,required=True,help='user_name cant be blank')
        parser.add_argument('user_adhar_card',type=str,required=True,help='adhar cant be blank')
        parser.add_argument('user_phone',type=str,required=True,help='phone cant be blank')
        
        #generate user id and flag

        data = parser.parse_args()

        all_users = db.child("users").get()

        if all_users.each():
        	user_id = "user_{}".format(len(all_users.each())+1)
        else:
        	user_num = 1
        	user_id = "user_1"



        user_name = data['user_name']
        user_adhar_card = data['user_adhar_card']
        user_phone = data['user_phone']
        flag = "0"
        balance = "0"

        data = {
    			"user_name" : user_name,
    			"user_id"   : user_id,
    			"user_adhar_card" : user_adhar_card,
    			"user_phone" : user_phone,
    			"balance"    : balance,
    			"flag"       : flag
    			}

        try:
        	db.child("users").child("{}".format(user_id)).set(data)
        	return {"message":"new user created"}
        except:
        	return {"message":"could not create a new user"}

    def get(self):
	    parser = reqparse.RequestParser()
	    parser.add_argument('user_phone',type=str,required=True,help='user_number cant be blank')
	    data = parser.parse_args()

	    user_phone = data['user_phone']


	    all_users = db.child("users").get()

	    try:
	        for user in all_users.each():
	            user_data = user.val()
	            if user_phone == user_data["user_phone"]:
	                return {"user_data":user_data}
	        return {"message":"user number is not registered"}

	    except:
	        {"message":"something went wrong"}

		
api.add_resource(HelloWorld, '/')
api.add_resource(user_balance,'/balance')
api.add_resource(user_data,'/user_data')
api.add_resource(source,'/source')
api.add_resource(destination,'/destination')


if __name__ == '__main__':
    app.run(debug=True)




