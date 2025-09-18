from supabase import create_client, Client
from config.settings import Config

# Supabase 客戶端
supabase: Client = None
supabase_admin: Client = None

def init_supabase():
    global supabase, supabase_admin
    
    if not Config.SUPABASE_URL or not Config.SUPABASE_ANON_KEY:
        print("⚠️  Supabase 設定未完成，請設定環境變數")
        return False
    
    try:
        # 一般客戶端 (RLS 限制)
        supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_ANON_KEY)
        
        # 管理員客戶端 (繞過 RLS，謹慎使用)
        if Config.SUPABASE_SERVICE_KEY:
            supabase_admin = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_KEY)
        
        print("✅ Supabase 初始化成功")
        return True
    except Exception as e:
        print(f"❌ Supabase 初始化失敗: {e}")
        return False

def get_supabase():
    return supabase

def get_supabase_admin():
    return supabase_admin

# 資料庫表格名稱常數
class Tables:
    USERS = 'users'
    VOCABULARY = 'vocabulary'
    USER_PROGRESS = 'user_progress'
    BOOKMARKS = 'bookmarks'
    QUIZ_SESSIONS = 'quiz_sessions'
    QUIZ_ANSWERS = 'quiz_answers'

# 訂閱狀態常數
class SubscriptionStatus:
    FREE = 'free'
    PREMIUM = 'premium'
    EXPIRED = 'expired'

# 學習狀態常數
class LearningStatus:
    LEARNING = 'learning'
    MASTERED = 'mastered'
    REVIEWING = 'reviewing'
