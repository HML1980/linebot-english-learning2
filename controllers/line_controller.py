from flask import request, abort, jsonify
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FollowEvent, UnfollowEvent, PostbackEvent
)
import json
from datetime import datetime

from config.line_config import get_line_bot_api, get_handler
from config.settings import Config

class LineController:
    def __init__(self):
        self.line_bot_api = get_line_bot_api()
        self.handler = get_handler()
        self.setup_handlers()
    
    def setup_handlers(self):
        """設定 LINE Bot 事件處理器"""
        if not self.handler:
            return
        
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_text_message(event):
            self.handle_text_message(event)
        
        @self.handler.add(FollowEvent)
        def handle_follow(event):
            self.handle_follow_event(event)
        
        @self.handler.add(UnfollowEvent)
        def handle_unfollow(event):
            self.handle_unfollow_event(event)
        
        @self.handler.add(PostbackEvent)
        def handle_postback(event):
            self.handle_postback_event(event)
    
    def handle_webhook(self, request):
        """處理 LINE Bot Webhook 請求"""
        try:
            # 取得請求簽名
            signature = request.headers.get('X-Line-Signature', '')
            
            # 取得請求內容
            body = request.get_data(as_text=True)
            
            if not signature or not body:
                print("❌ 缺少簽名或請求內容")
                abort(400)
            
            # 驗證並處理事件
            if self.handler:
                self.handler.handle(body, signature)
            else:
                print("⚠️  LINE Bot Handler 尚未初始化")
                return jsonify({'status': 'handler not initialized'}), 200
            
            return jsonify({'status': 'success'}), 200
            
        except InvalidSignatureError:
            print("❌ 無效的簽名")
            abort(400)
        except LineBotApiError as e:
            print(f"❌ LINE Bot API 錯誤: {e}")
            return jsonify({'error': str(e)}), 500
        except Exception as e:
            print(f"❌ Webhook 處理錯誤: {e}")
            return jsonify({'error': str(e)}), 500
    
    def handle_text_message(self, event):
        """處理文字訊息"""
        try:
            user_id = event.source.user_id
            message_text = event.message.text.strip().lower()
            
            print(f"📨 收到訊息: {message_text} (來自: {user_id})")
            
            # 基本指令處理
            response_text = self.get_response_text(message_text, user_id)
            
            # 回覆訊息
            if self.line_bot_api:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=response_text)
                )
            else:
                print("⚠️  LINE Bot API 尚未初始化")
                
        except Exception as e:
            print(f"❌ 處理文字訊息錯誤: {e}")
    
    def get_response_text(self, message_text, user_id):
        """根據訊息內容產生回應"""
        
        # 基本指令對應
        responses = {
            '學習': '📚 開始學習！\n\n目前可學習：\n✅ 初級單字\n🔒 中級單字 (需訂閱)\n\n請選擇學習階段：',
            'study': '📚 開始學習！\n\n目前可學習：\n✅ 初級單字\n🔒 中級單字 (需訂閱)\n\n請選擇學習階段：',
            
            '進度': '📊 您的學習進度：\n\n📚 初級單字：0/100\n🔒 中級單字：需要訂閱\n📖 總進度：0%',
            'progress': '📊 您的學習進度：\n\n📚 初級單字：0/100\n🔒 中級單字：需要訂閱\n📖 總進度：0%',
            
            '測驗': '🎮 測驗功能！\n\n🔒 此功能需要訂閱付費版\n💎 升級後可享受：\n• 隨機20題測驗\n• 錯誤分析\n• 弱點改善建議',
            'test': '�� 測驗功能！\n\n🔒 此功能需要訂閱付費版\n💎 升級後可享受：\n• 隨機20題測驗\n• 錯誤分析\n• 弱點改善建議',
            
            '書籤': '⭐ 您的書籤單字：\n\n目前沒有書籤單字\n學習過程中可以將重要單字加入書籤！',
            'bookmark': '⭐ 您的書籤單字：\n\n目前沒有書籤單字\n學習過程中可以將重要單字加入書籤！',
            
            '訂閱': '💎 訂閱付費版解鎖全功能！\n\n🆓 免費版：\n• 初級單字學習\n• 基礎進度追蹤\n• 書籤功能\n\n💎 付費版：\n• 完整學習路徑\n• 智能測驗系統\n• 錯誤分析報告\n• 個人化推薦',
            'subscribe': '💎 訂閱付費版解鎖全功能！\n\n🆓 免費版：\n• 初級單字學習\n• 基礎進度追蹤\n• 書籤功能\n\n💎 付費版：\n• 完整學習路徑\n• 智能測驗系統\n• 錯誤分析報告\n• 個人化推薦',
            
            '說明': '❓ 使用說明\n\n這是一個英檢單字學習 LINE Bot\n\n📱 手機用戶：使用下方選單\n💻 電腦用戶：輸入文字指令\n\n開發中功能會陸續開放！',
            'help': '❓ 使用說明\n\n這是一個英檢單字學習 LINE Bot\n\n📱 手機用戶：使用下方選單\n💻 電腦用戶：輸入文字指令\n\n開發中功能會陸續開放！'
        }
        
        # 查找對應回應
        if message_text in responses:
            return responses[message_text]
        
        # 預設回應
        return ('歡迎使用英檢單字學習 Bot！\n\n'
                '🎯 可用指令：\n'
                '📚 學習 - 開始學習單字\n'
                '📊 進度 - 查看學習進度\n'
                '🎮 測驗 - 開始測驗\n'
                '⭐ 書籤 - 查看書籤單字\n'
                '💎 訂閱 - 升級到付費版\n'
                '❓ 說明 - 查看使用說明')
    
    def handle_follow_event(self, event):
        """處理加入好友事件"""
        try:
            user_id = event.source.user_id
            print(f"🎉 新用戶加入: {user_id}")
            
            welcome_text = ('🎉 歡迎加入英檢單字學習！\n\n'
                           '我是您的英語學習夥伴，可以幫助您：\n'
                           '📚 學習初級和中級單字\n'
                           '📊 追蹤學習進度\n'
                           '🎮 進行測驗練習\n'
                           '⭐ 管理重要單字書籤\n\n'
                           '輸入「說明」開始使用！')
            
            if self.line_bot_api:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=welcome_text)
                )
            
            # TODO: 將用戶資訊存入資料庫
            
        except Exception as e:
            print(f"❌ 處理加入好友事件錯誤: {e}")
    
    def handle_unfollow_event(self, event):
        """處理取消好友事件"""
        try:
            user_id = event.source.user_id
            print(f"👋 用戶取消關注: {user_id}")
            
            # TODO: 處理用戶取消關注的邏輯
            
        except Exception as e:
            print(f"❌ 處理取消好友事件錯誤: {e}")
    
    def handle_postback_event(self, event):
        """處理按鈕回調事件"""
        try:
            user_id = event.source.user_id
            postback_data = event.postback.data
            
            print(f"🔘 按鈕回調: {postback_data} (來自: {user_id})")
            
            response_text = "功能開發中，敬請期待！"
            
            if self.line_bot_api:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=response_text)
                )
            
        except Exception as e:
            print(f"❌ 處理按鈕回調事件錯誤: {e}")
