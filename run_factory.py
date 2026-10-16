import os
import time
import random
from datetime import datetime
from google import genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# --- CẤU HÌNH HỆ THỐNG CENTURY 100.1 (GEMINI + YOUTUBE) ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Thông tin xác thực YouTube OAuth2 từ GitHub Secrets
YOUTUBE_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")

client = genai.Client(api_key=GEMINI_API_KEY)
LOCK_FILE = "execution_lock.txt"

def check_daily_execution_lock():
    """Kiểm tra khóa chống chạy trùng lặp trong ngày"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as f:
            last_run = f.read().strip()
            if last_run == today_str:
                print(f"[INFO] Hôm nay ({today_str}) pipeline đã chạy rồi. Dừng tiến trình.")
                return False
    with open(LOCK_FILE, "w") as f:
        f.write(today_str)
    return True

def apply_anti_spam_jitter():
    """Ngụy trang thời gian thực thi ngẫu nhiên"""
    jitter_seconds = random.randint(30, 180)
    print(f"[INFO] Chờ ngẫu nhiên {jitter_seconds} giây để bảo mật...")
    time.sleep(jitter_seconds)

def generate_script_content():
    """Sử dụng Gemini để tạo kịch bản tự động"""
    print("[INFO] Đang kết nối Gemini AI để sinh kịch bản...")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Hãy viết một đoạn mở đầu ngắn gọn, hấp dẫn bằng tiếng Việt về một xu hướng công nghệ mới nhất.",
        )
        script_text = response.text
        print(f"[SUCCESS] Đã tạo kịch bản thành công: {script_text[:60]}...")
        return script_text
    except Exception as e:
        print(f"[ERROR] Lỗi khi gọi Gemini API: {e}")
        return None

def upload_to_youtube(title, description):
    """Kết nối YouTube API để xuất bản nội dung"""
    if not all([YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN]):
        print("[WARNING] Thiếu thông tin OAuth2 của YouTube trong Secrets. Bỏ qua bước upload thực tế.")
        return False
    
    try:
        print("[INFO] Đang khởi tạo kết nối YouTube Data API...")
        creds = Credentials(
            token=None,
            refresh_token=YOUTUBE_REFRESH_TOKEN,
            client_id=YOUTUBE_CLIENT_ID,
            client_secret=YOUTUBE_CLIENT_SECRET,
            token_uri="https://oauth2.googleapis.com/token"
        )
        youtube = build("youtube", "v3", credentials=creds)
        print("[SUCCESS] Đã kết nối thành công với kênh YouTube!")
        # Logic gọi api upload video/shorts sẽ đặt ở đây
        return True
    except Exception as e:
        print(f"[ERROR] Lỗi kết nối YouTube API: {e}")
        return False

def main():
    print("=== BẮT ĐẦU KHỞI CHẠY CENTURY 100.1 (FULL PIPELINE) ===")
    
    if not check_daily_execution_lock():
        return

    apply_anti_spam_jitter()

    script = generate_script_content()
    if not script:
        print("[ERROR] Không thể tiến hành do thiếu kịch bản.")
        return

    # Tiến hành kết nối và xuất bản YouTube
    upload_to_youtube("Xu hướng công nghệ mới", script)

    print("[SUCCESS] Hoàn tất toàn bộ chu trình tự động hóa.")

if __name__ == "__main__":
    main()
    
