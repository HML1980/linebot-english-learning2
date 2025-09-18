from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from datetime import datetime

# 導入配置
from config.settings import config
from config.line_config import init_line_bot
from config.database import init_supabase

# 導入控制器
from controllers.line_controller import LineController

def create_app():
    app = Flask(__name__)
    
    # 載入配置
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])
    
    # 啟用 CORS
    CORS(app)
    
    # 初始化服務
    init_line_bot()
    init_supabase()
    
    # 建立控制器實例
    line_controller = LineController()
    
    # === 基礎路由 ===
    @app.route('/')
    def index():
        return jsonify({
            'message': 'LINE Bot English Learning API',
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'environment': env
        })
    
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'environment': env,
            'python_version': os.sys.version
        })
    
    # === LINE Bot Webhook ===
    @app.route('/webhook', methods=['POST'])
    def webhook():
        return line_controller.handle_webhook(request)
    
    # === 錯誤處理 ===
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Route not found',
            'path': request.path,
            'method': request.method
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal server error',
            'message': str(error) if app.debug else 'Something went wrong'
        }), 500
    
    return app

# 建立應用程式實例
app = create_app()

if __name__ == '__main__':
    print("🚀 啟動 Flask 應用程式...")
    print(f"📱 環境: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🔗 健康檢查: http://localhost:5000/health")
    print(f"📨 Webhook URL: http://localhost:5000/webhook")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
