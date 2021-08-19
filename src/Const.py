import re


# regex
regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex_pwd = r'[A-Za-z0-9@#$%^&+=]{8,}'

def check_email(email):
    return re.fullmatch(regex_email, email)


def check_pwd(pwd):
    return re.fullmatch(regex_pwd, pwd)


