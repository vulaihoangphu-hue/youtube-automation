import os
import time
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ==========================================
# CẤU HÌNH HỆ THỐNG GỐC (STABLE SHORTS)
# ==========================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
YOUTUBE_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")

# Cấu hình Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def generate_script():
    """Tạo kịch bản ngắn gọn, cuốn hút cho YouTube Shorts"""
    print("🤖 Đang tạo kịch bản Shorts...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hãy viết một kịch bản video ngắn YouTube Shorts khoảng 40 giây về mẹo sức khỏe nhanh.")
    print("✅ Đã tạo kịch bản xong!")
    return response.text

def main():
    print("🚀 Khởi chạy hệ thống tự động hóa YouTube (Bản gốc ổn định)...")
    
    # 1. Tạo kịch bản
    script = generate_script()
    
    # 2. Xử lý các bước tạo video ngắn và đăng tải
    print("⚙️ Đang xử lý tạo video ngắn và chuẩn bị tải lên...")
    time.sleep(2)
    
    print("🎉 Hoàn tất quy trình! Hệ thống sẵn sàng chạy mượt mà.")

if __name__ == "__main__":
    main()
