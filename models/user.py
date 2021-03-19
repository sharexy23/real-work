from db import db

class Ujer(db.Model):
    __tablename__ = 'ujer'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(110000000))
    firstname = db.Column(db.String(80))
    middlename = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    date_of_birth = db.Column(db.String(60))
    password = db.Column(db.String(80))
    account_balance = db.Column(db.String(800))
    email = db.Column(db.String(80))
    pin = db.Column(db.String(400))

    transfers = db.relationship('Transfer', lazy='dynamic',backref='parent')
    topup = db.relationship('Top_up', lazy='dynamic')
    re_transfers = db.relationship('Received_Transfer', lazy='dynamic')



    def __init__(self, phone_number, firstname,middlename,lastname,date_of_birth, password,email,pin, account_balance):
        self.phone_number = phone_number
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.date_of_birth = date_of_birth
        self.password = password
        self.email = email
        self.pin = pin
        self.account_balance = account_balance




        #self.verification_code = verification_code

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'id':self.id,'phone_number':self.phone_number,'first_name':self.firstname,'middle_name':self.middlename,'last_name':self.lastname,'date_of_birth':self.date_of_birth,'email':self.email}
    def rectrans(self):
        return {'Received_Transfer':[transfer.json() for transfer in self.re_transfers.all()]}
    def trans(self):
        return {'transfers':[transfer.json() for transfer in self.transfers.all()]}
    def jsony(self):
        return {'Top_ups':[top_up.json() for top_up in self.topup.all()]}
    def jsonyo(self):
        return {'id':self.id,'first_name':self.firstname,'middle_name':self.middlename,'last_name':self.lastname,'email':self.email}

    @classmethod
    def find_by_password(cls, password):
        return cls.query.filter_by(password=password).first()

    @classmethod
    def find_by_passwordandpin(cls, phone_number,pin):
        return cls.query.filter_by(phone_number=phone_number ,pin=pin).first()

    @classmethod
    def find_by_phone_number(cls, phone_number):
        return cls.query.filter_by(phone_number = phone_number).first()


    @classmethod
    def find_by_pin(cls, pin):
        return cls.query.filter_by(pin=pin).first()



class Transfer(db.Model):
    __TableName__ = 'transfers'

    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(900))
    destination_name = db.Column(db.String(800))
    description = db.Column(db.String(900))
    destination_account = db.Column(db.String(800))
    source_account = db.Column(db.String(80))
    ammount = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('ujer.id'), nullable=False )
    #local = db.relationship('Company', foreign_keys=local_id)
    user = db.relationship('Ujer')#,# foreign_keys= user_id)


    def __init__(self,source_name,destination_name,description,destination_account,source_account,ammount,user_id):
        #self.id = _id
        self.source_name = source_name
        self.destination_name = destination_name
        self.description = description
        self.destination_account = destination_account
        self.source_account = source_account
        self.ammount = ammount
        self.user_id = user_id



        #self.verification_code = verification_code

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'source_name':self.source_name,'destination_name':self.destination_name,'description':self.description,'destination_account':self.destination_account,'source_account':self.source_account,'ammount':self.ammount}



class Top_up(db.Model):
    __TableName__ = 'topup'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(900))
    destination_account = db.Column(db.String(800))
    ammount = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('ujer.id'), nullable=False )
    #local = db.relationship('Company', foreign_keys=local_id)
    user = db.relationship('Ujer')#,# foreign_keys= user_id)


    def __init__(self,description,destination_account,ammount,user_id):
        #self.id = _i
        self.description = description
        self.destination_account = destination_account
        self.ammount = ammount
        self.user_id = user_id



        #self.verification_code = verification_code

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'description':self.description,'destination_account':self.destination_account,'ammount':self.ammount}


class Received_Transfer(db.Model):
    __TableName__ = 're_transfers'

    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(900))
    destination_name = db.Column(db.String(800))
    description = db.Column(db.String(900))
    destination_account = db.Column(db.String(800))
    source_account = db.Column(db.String(80))
    ammount = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('ujer.id'), nullable=False )
    #local = db.relationship('Company', foreign_keys=local_id)
    user = db.relationship('Ujer')#,# foreign_keys= user_id)


    def __init__(self,source_name,destination_name,description,destination_account,source_account,ammount,user_id):
        #self.id = _id
        self.source_name = source_name
        self.destination_name = destination_name
        self.description = description
        self.destination_account = destination_account
        self.source_account = source_account
        self.ammount = ammount
        self.user_id = user_id



        #self.verification_code = verification_code

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'source_name':self.source_name,'destination_name':self.destination_name,'description':self.description,'destination_account':self.destination_account,'source_account':self.source_account,'ammount':self.ammount}
