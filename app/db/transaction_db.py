#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
transaction_db.py
データベースの処理
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


# DBファイルを外部にバックアップ
def save_file():
    dbx = dropbox.Dropbox( DROPBOX_TOKEN )
    dbx.users_get_current_account()

    # dropboxにアップロード
    with open(DBNAME, "rb") as f:
        dbx.files_upload(f.read(), DROPBOX_PATH, mode=dropbox.files.WriteMode('overwrite'))


# データベース作成用のコード　本番では不使用
def create():
    # 物品台帳（仮）
    create_table_ledger = '''
        CREATE TABLE ledger (
            id INTEGER PRIMARY KEY, 
            name VARCHAR(32), 
            quantity INTEGER, 
            note VARCHAR(64), 
            last_update DATETIME
        )
    '''
    # データ変更履歴
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
    # 利用者ごとの最終アクセス時間
    create_table_last_access = '''
        CREATE TABLE last_access (
            user_name VARCHAR(32) PRIMARY KEY, 
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
        c.execute(create_table_last_access)

        c.executemany(insert_ledger, ledger)
        conn.commit()

    # バックアップファイルを上書きする
    save_file()
