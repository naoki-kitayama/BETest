#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
write_table.py
テーブルを1行更新する
"""

# データベースへのアクセスに使用
import sqlite3
from contextlib import closing

# 日本語をレスポンスするのに必要
import json

from db import transaction_db
import util

async def execute(req, resp):
    select_ledger = 'SELECT id, name, quantity, note, last_update FROM ledger WHERE id=?'
    get_last_access = 'SELECT user_name, date FROM last_access WHERE user_name=?'
    insert_ledger = "INSERT INTO ledger (name, quantity, note, last_update) VALUES (?,?,?,datetime('now', '+9 hours'))"
    update_ledger = "UPDATE ledger SET name=?, quantity=?, note=?, last_update=datetime('now', '+9 hours') WHERE id=?"
    add_write_history = "INSERT INTO write_history (id, name, quantity, note, success, date) VALUES (NULL,?,?,?,?,datetime('now', '+9 hours'))"
    # 最終取得日時を更新
    update_last_access = "REPLACE INTO last_access (user_name, date) VALUES (?,datetime('now', '+9 hours'))"

    user_name = util.get_user_name(req)
    success = True
    message = ''

    id = None
    name = None
    quantity = None
    note = ''

    data = await req.media()
    if data.get('id'):
        id = data.get('id')
    if data.get('name'):
        name = data.get('name')
    if data.get('quantity'):
        quantity = data.get('quantity')
    if data.get('note'):
        note = data.get('note')

    # note以外入力されていればOKとする
    if name and quantity:
        with closing(sqlite3.connect(transaction_db.DBNAME)) as conn:
            c = conn.cursor()

            # 台帳の特定の1行取得
            c.execute(select_ledger, (id, ))
            ledger_exists = c.fetchone()

            if ledger_exists:
                # 同じidのデータがある場合
                c.execute(get_last_access, (user_name, ))
                last_login = c.fetchone()

                if last_login and ledger_exists[4] <= last_login[1]:
                    # 更新可能 台帳の1行更新
                    c.execute(update_ledger, (name, quantity, note, id))
                else:
                    # このユーザーのデータ取得後に行更新があった場合はUpdateさせない
                    success = False
                    message = '他のユーザーによってデータが変更されている可能性があります'

            else:
                # 新規データ場合 台帳に1行追加
                c.execute(insert_ledger, (name, quantity, note))

            # 最後に、成否に関わらず履歴を残す
            c.execute(add_write_history, (name, quantity, note, success ))
            c.execute(update_last_access, (user_name, ))

            conn.commit()

        # バックアップファイルを上書きする
        transaction_db.save_file()
    else:
        success = False
        message = '更新データに不備があります'

    result = {}
    if success:
        result = { 'success':True, }
    else:
        result = { 'success':False, 'message':message }

    # responseをUTF-8のJSONとして返す
    resp.headers = {"Content-Type": "application/json; charset=utf-8"}
    resp.content = json.dumps(result, ensure_ascii=False)
