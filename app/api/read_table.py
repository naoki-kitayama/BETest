#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
read_table.py
テーブルを全行取得する
"""

# データベースへのアクセスに使用
import sqlite3
from contextlib import closing

# 日本語をレスポンスするのに必要
import json

from db import transaction_db
import util

def execute(req, resp):
    # 台帳を全行取得
    select_ledger_list = 'SELECT id, name, quantity, note, last_update FROM ledger ORDER BY id ASC'
    # 最終取得日時を更新
    update_last_access = "REPLACE INTO last_access (user_name, date) VALUES (?,datetime('now', '+9 hours'))"

    result_row = None
    result = []
    user_name = util.get_user_name(req)

    # クエリを実行する
    with closing(sqlite3.connect(transaction_db.DBNAME)) as conn:
        c = conn.cursor()
        c.execute(select_ledger_list)
        result_row = c.fetchall()

        c.execute(update_last_access, (user_name, ))
        conn.commit()

    # データを整形する
    for row in result_row:
        result.append({
            'id': row[0],
            'name': row[1],
            'quantity': row[2],
            'note': row[3],
            'last_update': row[4],
        })

    # responseをUTF-8のJSONとして返す
    resp.headers = {"Content-Type": "application/json; charset=utf-8"}
    resp.content = json.dumps( { 'success':True, 'result':result }, ensure_ascii=False)
