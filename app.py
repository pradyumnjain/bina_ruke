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

class user_data(Resource):
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
    	parser = reqparse.RequestParser()
    	parser.add_argument('user_id',type=str,required=True,help='user_id cant be blank')
    	data = parser.parse_args()
    	user_id = data['user_id']

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




		










	    # data = {"name":"user1"}
	    # db.child("users").push(data)
	    # data = {"balance" : "60","user_id":"1"}
	    # db.child("users").child("user1").push(data)

	    # data = {"balance" : "60","user_id":"1"}
	    # db.child("users").child("user_1").set(data)

	   



	  
        # if balance>0:
        # user = db.child("users").get()

        #     return {
        #             'data':'',
        #             'message':'No file found',
        #             'status':'error'
        #             }
        # photo = data['file']
        # # type(photo)

        # if photo:
        #     # filename = '{}.png'.format(name)
        #     # photo.save(os.path.join(UPLOAD_FOLDER,filename))
        #     storage.child("{}.png".format(name)).put(data['file'])
        #     return {
        #             'data':'',
        #             'message':'photo uploaded',
        #             'status':'success'
        #             }
        # return {
        #         'data':'',
        #         'message':'Something whent wrong',
        #         'status':'error'
        #         }

    # def get(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('name',type=str,required=True,help='cant be blank')
    #     data = parser.parse_args()

    #     name = data['name']

    #     # url = storage.child("{}.png".format(name)).get_url(None)
    #     # storage.child("{}.png".format(name)).download("{}.png".format(name))
   


    #     try:
    #         url = storage.child("{}.png".format(name)).get_url(None)
    #         return {
    #                 'data':url,
    #                 'message':'photo recieved',
    #                 'status':'success'
    #                 }
    #     except:
    #         return {
    #                 'name':name,
    #                 'data':'',
    #                 'message':'Something whent wrong',
    #                 'status':'error'
    #                 }







api.add_resource(HelloWorld, '/')
api.add_resource(user_data,'/balance')
# api.add_resource(user_data,'/user')

if __name__ == '__main__':
    app.run(debug=True)




