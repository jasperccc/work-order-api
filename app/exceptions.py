class EmailAlreadyRegisteredError(Exception):
    """邮箱已经注册。"""


class InvalidCredentialsError(Exception):
    """邮箱或密码错误。"""
