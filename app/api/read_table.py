#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
read_table.py
テーブルを全行取得する
"""

import json

from db import transaction_db

def execute(req, resp):

    result = []

    # データを整形する
    for row in transaction_db.read_all():
        result.append({
            'id': row[0],
            'name': row[1],
            'quantity': row[2],
            'note': row[3],
            'last_update': row[4],
        })

    # responseをUTF-8のJSONとして返す
    resp.headers = {"Content-Type": "application/json; charset=utf-8"}
    resp.content = json.dumps(result, ensure_ascii=False)
