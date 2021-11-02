# -*- coding: utf-8 -*-
# @Time    : 2020/10/20 12:57 上午
# @Author  : xu.junpeng

from enum import unique
from app.base.base_enum import BaseEnum


@unique
class Codes(BaseEnum):
    # 20000～30000 预留系统状态
    SUCCESS = (20000, '操作成功')
    FAIL = (20001, '操作失败')
    LOGOUT = (20002, '退出登陆成功')
    TOKEN_INVALID = (20003, 'token失效')
    CONTENT_INVALID = (20004, '内容非法')
    VISIT_INVALID = (20005, '访问非法')
    LOGIN_SUCC = (20006, '用户登陆成功')
    LOGIN_FAIL = (20007, '用户登陆失败')
    NOT_LOG_IN = (20008, '用户未登陆')
    INVALID_PARAMS = (20010, '无效参数')
    PARAMS_CHECK_FAILD = (20011, '参数检查失败')
