"""
Segment Image Service
"""
from src.service.transaction_service import TransactionService
from src.util.decorator import token_required

try:
    from router_config import ROUTER_CONFIG
except ImportError:
    from src.controller.router_config import ROUTER_CONFIG


class TransactionController:
    """
    Account Controller
    """

    def __init__(self, app, req):
        """
        init
        :param app: object Flask
        :return:
        """
        self.transaction_service = TransactionService()
        self.addTransaction(app, req)
        self.updateTransaction(app, req)
        self.getTransaction(app, req)
        self.deleteTransaction(app, req)
        self.filterDateTransaction(app, req)


    def getTransaction(self, app, req):

        """
        add account of facebook
        :param app: object
        :param req: object
        :return:
        """

        transaction_service = self.transaction_service

        @app.route('{}'.format(ROUTER_CONFIG["api"]["v1"]["transactions"]["path_list_transaction"]), methods=['GET'])
        @token_required
        def getTransaction():
            """
            add account of facebook
            """
            return transaction_service.get(req)

    def addTransaction(self, app, req):

        """
        add account of facebook
        :param app: object
        :param req: object
        :return:
        """

        transaction_service = self.transaction_service

        @app.route('{}'.format(ROUTER_CONFIG["api"]["v1"]["transactions"]["path_add_transaction"]), methods=['POST'])
        @token_required
        def addTransaction():
            """
            add account of facebook
            """
            return transaction_service.add(req)

    def updateTransaction(self, app, req):

        """
        add account of facebook
        :param app: object
        :param req: object
        :return:
        """

        print(ROUTER_CONFIG["api"]["v1"]["transactions"]["path_update_transaction"])

        transaction_service = self.transaction_service

        @app.route('{}'.format(ROUTER_CONFIG["api"]["v1"]["transactions"]["path_update_transaction"]), methods=['PUT'])
        @token_required
        def updateTransaction():
            """
            add account of facebook
            """
            return transaction_service.put(req)

    def deleteTransaction(self, app, req):

        """
        add account of facebook
        :param app: object
        :param req: object
        :return:
        """

        print(ROUTER_CONFIG["api"]["v1"]["transactions"]["path_delete_transaction"])

        transaction_service = self.transaction_service

        @app.route('{}'.format(ROUTER_CONFIG["api"]["v1"]["transactions"]["path_delete_transaction"]), methods=['DELETE'])
        @token_required
        def deleteTransaction():
            """
            add account of facebook
            """
            return transaction_service.delete(req)

    def filterDateTransaction(self, app, req):

        """
        add account of facebook
        :param app: object
        :param req: object
        :return:
        """

        print(ROUTER_CONFIG["api"]["v1"]["transactions"]["path_filter_date"])

        transaction_service = self.transaction_service

        @app.route('{}'.format(ROUTER_CONFIG["api"]["v1"]["transactions"]["path_filter_date"]), methods=['POST'])
        def filterDateTransaction():
            """
            add account of facebook
            """
            return transaction_service.filter_date(req)