#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
transaction_db.py
transaction.dbの読み込み、書き込み中継器
"""

# データベースへのアクセスに使用
import sqlite3
from contextlib import closing

# dropboxにDBバックアップを取るために使用
import dropbox

# データベース名（ファイル名）の定義
DBNAME = 'tmp/transaction.db'

# dropboxのアクセストークン
DROPBOX_TOKEN = 'WrzQhXRZ4LUAAAAAAAAAXfAR9O_ARWI0qOMea3gIsrlD5WMXxbJNKGNao0aFahYF'
DROPBOX_PATH = '/transaction.db'


# データベースの初期化
def init():
    # dropboxからバックアップを復元
    dbx = dropbox.Dropbox( DROPBOX_TOKEN )
    dbx.users_get_current_account()
    dbx.files_download_to_file(DBNAME, DROPBOX_PATH)


def in_it():
    create_table_ledger = '''
        CREATE TABLE ledger (
            id INTEGER PRIMARY KEY, 
            name VARCHAR(32), 
            quantity INTEGER, 
            note VARCHAR(64), 
            last_update DATETIME
        )
    '''
    create_table_write_history = '''
        CREATE TABLE write_history (
            id INTEGER PRIMARY KEY, 
            target_id INTEGER, 
            name VARCHAR(32), 
            quantity INTEGER, 
            note VARCHAR(64), 
            success BOOLEAN, 
            date DATETIME
        )
    '''

    insert_ledger = "INSERT INTO ledger (id, name, quantity, note, last_update) VALUES (?,?,?,?,datetime('now', '+9 hours'))"
    ledger = [
        (1, '人参', 2, '群馬県産'),
        (2, 'じゃがいも', 13, '北海道産'),
        (3, '玉ねぎ', 5, '鹿児島県産')
    ]

    with closing(sqlite3.connect(DBNAME)) as conn:
        c = conn.cursor()

        # テーブル作成の実行
        c.execute(create_table_ledger)
        c.execute(create_table_write_history)

        c.executemany(insert_ledger, ledger)
        conn.commit()

    # バックアップファイルを上書きする
    save_file()


# 台帳を全行取得
def read_all():
    result = []

    select_ledger_list = 'SELECT id, name, quantity, note, last_update FROM ledger ORDER BY id ASC'

    with closing(sqlite3.connect(DBNAME)) as conn:
        c = conn.cursor()
        c.execute(select_ledger_list)
        result = c.fetchall()

    return result


# 台帳の特定の1行取得
def read(id):
    result = None

    select_ledger = 'SELECT id, name, quantity, note, last_update FROM ledger WHERE id=?'

    with closing(sqlite3.connect(DBNAME)) as conn:
        c = conn.cursor()
        c.execute(select_ledger, (id, ))
        result = c.fetchone()

    return result


# 台帳の1行更新
def write(id, name, quantity, note):
    # REPLACE(SQLite):テーブルの主キーで判別。データがあればUPDATE、無ければINSERT
    replace_ledger = "REPLACE INTO ledger (id, name, quantity, note, last_update) VALUES (?,?,?,?,datetime('now', '+9 hours'))"

    with closing(sqlite3.connect(DBNAME)) as conn:
        c = conn.cursor()

        c.executemany(replace_ledger, (id, name, quantity, note))
        conn.commit()

# 履歴を記録
def write_history(id, name, note, success, date):
    pass

# DBファイルを外部にバックアップ
def save_file():
    dbx = dropbox.Dropbox( DROPBOX_TOKEN )
    dbx.users_get_current_account()

    with open(DBNAME, "rb") as f:
        dbx.files_upload(f.read(), DROPBOX_PATH, mode=dropbox.files.WriteMode('overwrite'))
