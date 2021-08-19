"""
Config path for resource
"""

ROUTER_CONFIG = {
    "api": {
        "path": '/api',
        "v1": {
            "path": "/api/v1",
            "auth": {
                "path_login": "/api/v1/login",          #done
                "path_logout": "/api/v1/logout",        #done
            },
            "user": {
                "path_add_user": "/api/v1/register",    # done
            },
            "transactions": {
                "path_list_transaction": "/api/v1/transaction", #done
                "path_add_transaction": "/api/v1/transaction/add", # done
                "path_update_transaction": "/api/v1/transaction/update", #done
                "path_delete_transaction": "/api/v1/transaction/delete", #done
                "path_filter_date": "/api/v1/transaction/filter/date",
            },
            "currency": {
                "path_list_currency": "/api/v1/currency", #done
                "path_add_currency": "/api/v1/currency/add", #done
                "path_update_currency": "/api/v1/currency/update", #done
                "path_delete_currency": "/api/v1/currency/delete" #done
            },
            "action": {
                "path_list_action": "/api/v1/action", #done
                "path_add_action": "/api/v1/action/add", #done
                "path_update_action": "/api/v1/action/update", #done
                "path_delete_action": "/api/v1/action/delete" #done
            },
        }
    }
}
