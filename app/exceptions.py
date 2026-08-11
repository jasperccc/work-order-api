class EmailAlreadyRegisteredError(Exception):
    """邮箱已经注册。"""


class InvalidCredentialsError(Exception):
    """邮箱或密码错误。"""


class InvalidTokenError(Exception):
    """访问token无效。"""


class WorkOrderNotFoundError(Exception):
    """工单不存在或当前用户无权访问。"""
