import os
import time
import random
from datetime import datetime
import openai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# --- CẤU HÌNH HỆ THỐNG CENTURY 100.1 ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

LOCK_FILE = "execution_lock.txt"

def check_daily_execution_lock():
    """Kiểm tra khóa chống chạy trùng lặp trong ngày để tránh vi phạm giới hạn quota"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as f:
            last_run = f.read().strip()
            if last_run == today_str:
                print(f"[INFO] Hôm nay ({today_str}) pipeline đã chạy rồi. Dừng tiến trình để an toàn.")
                return False
    with open(LOCK_FILE, "w") as f:
        f.write(today_str)
    return True

def apply_anti_spam_jitter():
    """Ngụy trang thời gian thực thi ngẫu nhiên để tránh thuật toán phát hiện bot tự động"""
    jitter_seconds = random.randint(30, 180)
    print(f"[INFO] Ngụy trang thời gian thực: Chờ ngẫu nhiên {jitter_seconds} giây...")
    time.sleep(jitter_seconds)

def generate_script_content():
    """Sử dụng OpenAI để tạo kịch bản tự động"""
    print("[INFO] Đang kết nối OpenAI để sinh kịch bản chủ đề công nghệ/đời sống...")
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Bạn là một nhà sáng tạo nội dung YouTube tự động chuyên nghiệp."},
                {"role": "user", "content": "Hãy viết một đoạn mở đầu ngắn gọn, hấp dẫn bằng tiếng Việt về một xu hướng công nghệ mới nhất."}
            ]
        )
        script_text = response.choices[0].message.content
        print(f"[SUCCESS] Đã tạo kịch bản thành công: {script_text[:60]}...")
        return script_text
    except Exception as e:
        print(f"[ERROR] Lỗi khi gọi OpenAI API: {e}")
        return None

def main():
    print("=== BẮT ĐẦU KHỞI CHẠY CENTURY 100.1 FACTORY == ->")
    
    # 1. Kiểm tra khóa chạy trong ngày
    if not check_daily_execution_lock():
        return

    # 2. Ngụy trang chống spam
    apply_anti_spam_jitter()

    # 3. Tạo nội dung kịch bản
    script = generate_script_content()
    if not script:
        print("[ERROR] Không thể tiến hành do thiếu kịch bản.")
        return

    print("[SUCCESS] Quy trình vận hành cốt lõi đã sẵn sàng bước tiếp theo (Render/Upload).")

if __name__ == "__main__":
    main()
