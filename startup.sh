#!/usr/bin/env bash

# nginxが自動で立ち上がらないので手動で起動する
service nginx start

# アプリケーションを実行
python /var/www/app/main.py
