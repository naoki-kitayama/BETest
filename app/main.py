#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
main.py
サーバ起動時の処理を記述する

ここではURLの割り当てのみ行い
サービスごとの処理は別ファイルに記述する
"""

# =========================================
# ライブラリとサービス、初期化処理が必要な部分のimport
# =========================================

# responderの読み込み
import responder

import base64

# 各API処理の読み込み
from api import read_table
from api import write_table

# DBの初期化処理の読み込み
from db import transaction_db


# =========================================
# 初期化処理
# =========================================

# responderの初期化
api = responder.API()

# データベースの初期化
transaction_db.init()
#transaction_db.create()

# =========================================
# それぞれの処理（サービス）にURLを割り当てる
# =========================================

# テーブルのデータ一覧を取得
@api.route("/api/read-table")
def api_read_table(req, resp):
	read_table.execute(req, resp)

# テーブルのデータを1行追加・更新
@api.route("/api/write-table")
async def api_write_table(req, resp):
	await write_table.execute(req, resp)

# UIのHTMLファイルを返す
api.add_route("/", static=True)


# responderのサーバ起動処理
if __name__ == '__main__':
	# api.run(address="0.0.0.0",port=80)
	api.run(port=8000)
