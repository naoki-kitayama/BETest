#!/usr/bin/env bash

# nginxの設定を変更
sed -i -e 's/$PORT/'"80"'/g' /etc/nginx/conf.d/default.conf

# アプリケーションを実行
supervisord -c /etc/supervisord.conf
