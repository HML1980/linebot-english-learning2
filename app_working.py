from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

app = Flask(__name__)
CORS(app)

# 基礎配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

@app.route('/')
def index():
    return jsonify({
        'message': 'LINE Bot English Learning API',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'environment': os.getenv('FLASK_ENV', 'development'),
        'note': 'LINE Bot SDK integration pending'
    })

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
        'flask_version': '3.0.0',
        'supabase_available': True
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """暫時的 webhook 端點，等待 LINE Bot SDK 整合"""
    data = request.get_json()
    return jsonify({
        'status': 'webhook received',
        'message': 'LINE Bot integration will be added after resolving aiohttp dependency',
        'received_data': bool(data)
    })

@app.route('/test-supabase')
def test_supabase():
    """測試 Supabase 連接"""
    try:
        import supabase
        return jsonify({
            'status': 'success',
            'message': 'Supabase module imported successfully',
            'ready': True
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Supabase import failed: {str(e)}',
            'ready': False
        }), 500

if __name__ == '__main__':
    print("🚀 啟動 Flask 應用程式...")
    print(f"📱 環境: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🔗 主頁: http://localhost:5000/")
    print(f"🔗 健康檢查: http://localhost:5000/health")
    print(f"🔗 Supabase 測試: http://localhost:5000/test-supabase")
    print(f"📨 Webhook URL: http://localhost:5000/webhook")
    print("⚠️  注意：LINE Bot SDK 將在解決 aiohttp 依賴問題後整合")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
