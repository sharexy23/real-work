from db import db
import hashlib
from models.user import *
#from models.transfers import Transfer
from flask import jsonify
from flask_restful import Resource, reqparse, inputs
#from flask_jwt import jwt_required
from flask_jwt_extended import create_access_token,jwt_required
#from flask_mail import *
#from plyer import  plyer.platforms.win.notification


class register(Resource):
    parser = reqparse.RequestParser()
    #parser.add_argument('id',
    #                    type=int,
    #                    required=True,
    #                    help="This field cannot be left blank!"
    #                    )
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('firstname',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('middlename',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('lastname',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('date_of_birth',
                        type=inputs.datetime_from_iso8601,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('pin',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def encrypt_string(hash_string):
        sha_signature = \
            hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature


    def post(self):

        data = register.parser.parse_args()
        if Ujer.find_by_phone_number(data['phone_number']):
            return  {
            'status':False,
            'message':'user exists'
            },400

        user = Ujer(data['phone_number'],data['firstname'],data['middlename'],data['lastname'],data['date_of_birth'],
        data['password'],data['email'],data['pin'],'00')

        #user.password = register.encrypt_string(user.password)
        user.pin = register.encrypt_string(user.pin)


        Ujer.save_to_db(user)



        #notification.notify(title= "notification",message="you are succesfully registered",timeout=5)
        return {
        'status': True,
        #'data info': user.jsonyo(),
        'data':user.json(),
        'message':'user created succesfully'
        },201

class login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = login.parser.parse_args()
        user = Ujer.find_by_phone_number(data['phone_number']) and Ujer.find_by_password(data['password'])
        if user:
            access_token = create_access_token(identity=user.id,fresh =True)
            #refresh_token= create_refresh_token(user.id)
            return {
                  'status': True,
                  'data': access_token,
                  'message':'you are logged in'
            },200
        return {
        'status':True,
        'status':False,
        'message':'user not found'
        },404


class account_balance(Resource):
    @jwt_required()
    def get(self, phone_number):
        user = Ujer.find_by_phone_number(phone_number)
        balance = user.account_balance
        #n =user.phone_number[x.json() for x in Received_Transfer.query.all()]
        if user:
            return {
            'status':True,
            'data': balance,
            'message':'this is your account balance'
            }
    #    return {'user': 'does not exist'}
        return {
        'status':True,
        'user': 'does not exist'
        },404


class Top__up(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('ammount',
                        type= float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('user_id',
                        type= int,
                        required=True,
                        help="This field cannot be left blank!"
                        )


    @jwt_required()
    def put(self):
        data = Top__up.parser.parse_args()
        user = Ujer.find_by_phone_number(data['phone_number'])
        #user.money_in_the_bag = float(user.money_in_the_bag)
        if user:
            user.account_balance = float(user.account_balance)
            user.account_balance = data['ammount'] + user.account_balance
            user.account_balance =str(user.account_balance)
            herky = Top_up('money transfer to your ubeus account','user.phone_number',data['ammount'],data['user_id'])
            Top_up.save_to_db(herky)
            Ujer.save_to_db(user)
            json = user.account_balance
            return{
            'status':True,
            'data': json,
            'message':'your ubeus accounthas been credited'
            },200
        return{
        'status': False,
        'message':'user does not exist'
        },404


class transfer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('source_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('destination_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('pin',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('amount',
                        type= float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('description',
                        type= str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('destination_phone_number',
                        type= str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('sender_id',
                        type= int,
                        required=True,
                        help="every transfer needs a user"
                        )
    parser.add_argument('destination_id',
                        type= int,
                        required=True,
                        help="every transfer needs a user"
                        )

    @jwt_required()
    def post(self):
        data = transfer.parser.parse_args()

        user = Ujer.find_by_phone_number(data['phone_number'])
        #user = User.find_by_pin(data['pin'])
        destination = Ujer.find_by_phone_number(data['destination_phone_number'])

        #user.money_in_the_bag = float(user.money_in_the_bag)
        #destination.money_in_the_bag = float(destination.money_in_the_bag)



        if user is not None and destination is not None:
            user.account_balance = float(user.account_balance)
            destination.account_balance = float(destination.account_balance)
            if user.account_balance < data['amount']:
                return {'message':'your account balance is less than required amount'}


            destination.account_balance = data['amount'] + destination.account_balance
            user.account_balance = user.account_balance - data['amount']
            user.account_balance = str(user.account_balance)
            destination.account_balance = str(destination.account_balance)
            transferg = Transfer(data['source_name'],data['destination_name'],data['description'],data['destination_phone_number'],data['phone_number'],data['amount'],data['sender_id'])
            transfergee = Received_Transfer(data['source_name'],data['destination_name'],data['description'],data['destination_phone_number'],data['phone_number'],data['amount'],data['destination_id'])
            Transfer.save_to_db(transferg)
            Received_Transfer.save_to_db(transfergee)
            Ujer.save_to_db(user)
            #user.transfers = user.transfers + ('j')
            acc = user.account_balance
            return {
                          'status':True,
                          'data': acc,
                          'message':'you have succesfully made your transfer'
            }
        return {'message':'either your account or the destination account doesnt exist'}



class TransferHistory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    #it seems to me that this function is cursed
    @jwt_required()
    def post(self):
        data = TransferHistory.parser.parse_args()
        user = Ujer.find_by_phone_number(data['phone_number'])
        if user:
            return {
            'status':True,
            'data':user.jsony(),
            'message':'this is your transfer logs'
            }
        return {'message':'user not found'},404


class lookup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    #it seems to me that this function is cursed
    @jwt_required()
    def post(self):
        data = TransferHistory.parser.parse_args()
        user = Ujer.find_by_phone_number(data['phone_number'])

        if user:
            uu = user.re_transfers
            return {
            'status':True,
            'data':user.jsonyo(),
            'message':'this is your info'
            }
        return {
        'status': True,
        'message':'user not found'
        },404
