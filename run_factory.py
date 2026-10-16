import os
import time
import random
from datetime import datetime
from google import genai

# --- CẤU HÌNH HỆ THỐNG CENTURY 100.1 (GEMINI) ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Khởi tạo client Gemini chính thức
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

def main():
    print("=== BẮT ĐẦU KHỞI CHẠY CENTURY 100.1 (GEMINI EDITION) ===")
    
    if not check_daily_execution_lock():
        return

    apply_anti_spam_jitter()

    script = generate_script_content()
    if not script:
        print("[ERROR] Không thể tiến hành do thiếu kịch bản.")
        return

    print("[SUCCESS] Quy trình vận hành cốt lõi với Gemini đã sẵn sàng.")

if __name__ == "__main__":
    main()
