from datetime import datetime, timedelta

from sqlalchemy import func

from config import db
import enum

class CURRENCY_TYPE(enum.Enum):
    yen = 'yen'
    baht = 'baht'
    dong = 'dong'

class ACTION_TYPE(enum.Enum):
    deposits = 'deposits'
    withdrawals = 'withdrawals'

class TransactionModel(db.Model):
    """ User Model for storing user related details """
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float(precision=2), default=0.0)

    content = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    created_at = db.Column(db.DateTime, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at = db.Column(db.DateTime, default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    currency_type = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.yen, nullable=False)
    action_type = db.Column(db.Enum(ACTION_TYPE), default=ACTION_TYPE.deposits, nullable=False)

    balance = db.Column(db.Float(precision=2), default=0.0)
    expenses = db.Column(db.Float(precision=2), default=0.0)
    income = db.Column(db.Float(precision=2), default=0.0)


    @classmethod
    def find_by_id_and_name(self, id, user_id):
        return self.query.filter_by(id=id, user_id=user_id).first()

    @classmethod
    def find_by_user_id(self, user_id):
        return self.query.filter_by(user_id=user_id).all()

    @classmethod
    def summary(self, user_id, data):
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d') + timedelta(days=1)
        return self.query.with_entities(func.sum(TransactionModel.income).label('total_income'), func.sum(TransactionModel.expenses).label('total_expenses')).filter_by(user_id=user_id).filter(self.created_at <= end_date,
                                                            self.created_at >= start_date).first()


    @classmethod
    def filter_created_at(self, user_id ,data):
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d') + timedelta(days=1)
        return self.query.filter_by(user_id=user_id).filter(self.created_at <= end_date,
                                                            self.created_at >= start_date).all()

    @classmethod
    def add_transaction(self, data, user):
        try:
            transaction = TransactionModel(amount=data['amount'], content=data['content'], user_id=data['user_id'], currency_type=data['currency_type'], action_type=data['action_type'], balance=data['balance'], expenses=data['expenses'], income=data['income'])
            db.session.add(transaction)
            if data['currency_type'] == 'yen':
                user.currency_yen = data['balance']
            elif data['currency_type'] == 'baht':
                user.currency_baht = data['balance']
            elif data['currency_type'] == 'dong':
                user.currency_dong = data['balance']
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Add transaction success.'
            }
            return response_object, 201
        except Exception as ex:
            response_object = {
                'status': 'fail',
                'message': 'Add transaction Fail: {}'.format(ex)
            }
            return response_object, 409

    @classmethod
    def update_transaction(self, transaction, data):
        try:
            transaction.content = data['content']
            transaction.updated_at = datetime.now()
            db.session.commit()
            result = "update transaction success", ""
        except Exception as ex:
            result = "", "update transaction Fail: {}".format(ex)
        return result

    @classmethod
    def delete_transaction(self, transaction):
        try:
            db.session.delete(transaction)
            db.session.commit()
            result = "Delete success", ""
        except Exception as ex:
            result = "", "update transaction Fail: {}".format(ex)
        return result

    def __repr__(self):
        return "<Transaction '{}'>".format(self.user_id)




