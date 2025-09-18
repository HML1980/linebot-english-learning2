import sys
import os

# 添加專案路徑到 Python 路徑
path = '/home/yourusername/linebot-english-learning'
if path not in sys.path:
    sys.path.insert(0, path)

# 設定環境變數
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'production'

# 導入應用程式
from app import app as application

if __name__ == "__main__":
    application.run()
