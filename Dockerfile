# Pythonイメージをベースにする
FROM python:3.9-slim

# 必要なパッケージをインストール
RUN pip install pandas

# 作業ディレクトリを作成
WORKDIR /app

# スクリプトをコンテナにコピー
COPY script.py /app/script.py

# スクリプトを実行
ENTRYPOINT ["python", "/app/script.py"]
