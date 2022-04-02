# philtune2

## 環境構築

Pythonのバージョン: 3.7.10
### venv作成
```
python3 -m venv .venv
```

### 仮想環境に入る
```
. .venv/bin/activate
```

### 仮想環境を出る
```
deactivate
```

### 必要なライブラリをインストール
```
(仮想環境に入った状態で)
pip3 install requirements.txt
```

### データベースのセットアップ
```
(仮想環境外で)
brew install postgresql@10
```
バージョンチェック
```
psql --version
```
データベース作成
```
brew services start postgresql@10
createdb philtune
```
確認
```
psql -l
```
### Djangoによるサーバー立ち上げ
開発環境用に設定ファイルを指定して実行
```
python3 manage.py runserver --settings philtune.settings_dev
```
正常に立ち上がればhttp://127.0.0.1:8000
にサーバーが立つ
### データベースの構築(マイグレーション)
初回だけで良い
```
python3 manage.py migrate
```
### スーパーユーザーの作成
初回だけで良い
```
python3 manage.py createsuperuser
```


