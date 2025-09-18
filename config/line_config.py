from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from config.settings import Config

# LINE Bot API 初始化
line_bot_api = None
handler = None

def init_line_bot():
    global line_bot_api, handler
    
    if not Config.LINE_CHANNEL_ACCESS_TOKEN or not Config.LINE_CHANNEL_SECRET:
        print("⚠️  LINE Bot 設定未完成，請設定環境變數")
        return False
    
    try:
        line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)
        print("✅ LINE Bot 初始化成功")
        return True
    except Exception as e:
        print(f"❌ LINE Bot 初始化失敗: {e}")
        return False

def get_line_bot_api():
    return line_bot_api

def get_handler():
    return handler
