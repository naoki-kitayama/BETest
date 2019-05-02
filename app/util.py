#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
util.py
共通処理を記述する
"""

import base64

def get_user_name(req):
    user_name = 'guest'

    # リクエストヘッダから認証情報を取得
    auth_code = req.headers.get('authorization')

    # 認証情報の存在を確認できたら、デコードして名前だけ取り出す
    if auth_code and auth_code[:6] == 'Basic ':
        encoded_name = base64.b64decode(auth_code[6:]).decode()
        user_name = encoded_name[:encoded_name.find(':')]

    return user_name