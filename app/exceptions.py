class EmailAlreadyRegisteredError(Exception):
    """邮箱已经注册。"""


class InvalidCredentialsError(Exception):
    """邮箱或密码错误。"""


class InvalidTokenError(Exception):
    """访问token无效。"""
