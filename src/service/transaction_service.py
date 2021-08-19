"""
Account service
"""
import json
from datetime import datetime
from http import HTTPStatus

import jwt
from flask_restful import reqparse

from config import key
from src.models import TransactionModel, UserModel


class TransactionService:
    """
    Account service
    """

    def __init__(self):
        self.transaction_model = TransactionModel()
        self.user_model = UserModel()

    def get(self, req):

        """
        add account of facebook
        :param req: object
        :return:
        """
        try:
            payload = jwt.decode(req.headers.get('Authorization'), key)
            transactions = self.transaction_model.find_by_user_id(payload['sub'])
            result = []
            for transaction in transactions:
                trans = {
                    "id": transaction.id,
                    "amount": transaction.amount,
                    "content": transaction.content,
                    "user_id": transaction.user_id,
                    "created_at": transaction.created_at,
                    "updated_at": transaction.updated_at,
                    "currency_type": transaction.currency_type.value,
                    "action_type": transaction.action_type.value,
                    "expenses": transaction.expenses,
                    "income": transaction.income
                }
                result.append(trans)

            return {"result": result}
        except Exception as ex:
            response_object = {
                'status': 'fail',
                'message': 'Authorization: {}'.format(ex)
            }
            return response_object, 409

    def add(self, req):

        """
        add account of facebook
        :param req: object
        :return:
        """
        balance = 0
        expenses = 0
        income = 0
        user_amount = 0
        data = json.loads(req.data)
        payload = jwt.decode(req.headers.get('Authorization'), key)
        user = self.user_model.find_by_id(payload['sub'])
        if user:
            if data['currency_type'] == 'yen':
                user_amount = user.currency_yen
            elif data['currency_type'] == 'baht':
                user_amount = user.currency_baht
            elif data['currency_type'] == 'dong':
                user_amount = user.currency_dong
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Currency only include: yen, baht, dong'
                }
                return response_object, 409

            if data['action_type'] == 'withdrawals':
                if user_amount < data['amount']:
                    balance = user_amount
                    response_object = {
                        'status': 'fail',
                        'message': "users don't have enough money"
                    }
                    return response_object, 409
                else:
                    balance = user_amount - data['amount']
                    expenses = data['amount']
            elif data['action_type'] == 'deposits':
                balance = user_amount + data['amount']
                income = data['amount']
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Action only include: deposits, withdrawals'
                }
                return response_object, 409
            data['user_id'] = payload['sub']
            data['balance'] = balance
            data['income'] = income
            data['expenses'] = expenses
            data['currency_type'] = data['currency_type']
            result = self.transaction_model.add_transaction(data, user)
            return result

        response_object = {
            'status': 'fail',
            'message': 'User not found'
        }
        return response_object, 409

    def put(self, req):

        """
        add account of facebook
        :param req: object
        :return:
        """
        data = json.loads(req.data)
        try:
            payload = jwt.decode(req.headers.get('Authorization'), key)
            transaction = self.transaction_model.find_by_id_and_name(data["id"], payload['sub'])
            if transaction:
                result, err = self.transaction_model.update_transaction(transaction, data)
                if err:
                    return err
                return result
            return "fails"
        except Exception as ex:
            response_object = {
                'status': 'fail',
                'message': 'Authorization: {}'.format(ex)
            }
            return response_object, 409

    def delete(self, req):

        """
        add account of facebook
        :param req: object
        :return:
        """
        data = json.loads(req.data)
        try:
            payload = jwt.decode(req.headers.get('Authorization'), key)
            transaction = self.transaction_model.find_by_id_and_name(data["id"], payload['sub'])
            if transaction:
                result, err = self.transaction_model.delete_transaction(transaction)
                if err:
                    return err
                return result
            return "fails"
        except Exception as ex:
            response_object = {
                'status': 'fail',
                'message': 'Authorization: {}'.format(ex)
            }
            return response_object, 409

    def filter_date(self, req):
        data = json.loads(req.data)
        payload = jwt.decode(req.headers.get('Authorization'), key)
        if payload:
            summary = self.transaction_model.summary(payload['sub'], data)
            transactions = self.transaction_model.filter_created_at(payload['sub'], data)
            user = UserModel.query.filter_by(id=payload['sub']).first()
            balance_currency_yen = user.currency_yen
            balance_currency_baht = user.currency_baht
            balance_currency_dong = user.currency_dong
            list_trans = []
            for transaction in transactions:
                trans = {
                    "id": transaction.id,
                    "amount": transaction.amount,
                    "content": transaction.content,
                    "user_id": transaction.user_id,
                    "created_at": transaction.created_at,
                    "updated_at": transaction.updated_at,
                    "currency_type": transaction.currency_type.value,
                    "action_type": transaction.action_type.value,
                    "income": transaction.income,
                    "expenses": transaction.expenses,
                    "balance": transaction.balance
                }
                list_trans.append(trans)
            return {
                "balance_currency_yen": balance_currency_yen,
                "balance_currency_baht": balance_currency_baht,
                "balance_currency_dong": balance_currency_dong,
                "total_income": float(str(summary.total_income)),
                "total_expenses": float(str(summary.total_expenses)),
                "result": list_trans
            }
        return "user not found"