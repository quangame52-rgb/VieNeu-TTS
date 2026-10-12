# 🦜 Hướng dẫn sử dụng VieNeu-TTS (Triển khai thành công)

Hệ thống **VieNeu-TTS v3 Turbo** (phiên bản mã nguồn mở mới nhất, âm thanh 48 kHz, hỗ trợ voice cloning và tag cảm xúc) đã được cài đặt và cấu hình sẵn sàng trong thư mục này.

---

## 1. Khởi động Giao diện Web (Web UI có Link Public)
Nhấp đúp chuột vào file:
👉 **[run_web.bat](file:///d:/acc%20moi%200612/vienew/run_web.bat)**

Hệ thống sẽ tự động khởi động và cung cấp 2 đường dẫn truy cập:
- 🌐 **Link công khai (Public HTTPS):** Truy cập từ mọi thiết bị (điện thoại, máy tính khác) hoặc trình duyệt mà không lo bị xung đột proxy localhost:
  🔗 Xem đường dẫn mới nhất tại file: **[public_url.txt](file:///d:/acc%20moi%200612/vienew/public_url.txt)**
- 💻 **Link nội bộ (Localhost):** `http://127.0.0.1:7860`

### Các tính năng trên Web UI:
- **Đọc truyện (Single Speaker):** Đọc văn bản đơn lẻ hoặc trích xuất từ file PDF, chọn trong 25+ giọng đọc có sẵn.
- **Hội thoại (Multi-Speaker):** Tự động quét nhân vật trong kịch bản và gán giọng cho từng nhân vật (Phương, Dũng, Hùng,...).
- **Phụ đề SRT:** Tải file `.srt` tiếng Việt để ghép thành file âm thanh theo chuẩn mốc thời gian.
- **Voice Cloning:** Tải lên file âm thanh mẫu (3–5 giây) để nhân bản giọng nói tức thì (không cần nhập văn bản mẫu đối với bản v3 Turbo) và lưu giọng vào danh sách.

---

## 2. Khởi động OpenAI-Compatible Speech API (Streaming)
Nhấp đúp chuột vào file:
👉 **[run_api.bat](file:///d:/acc%20moi%200612/vienew/run_api.bat)**

Endpoint hoạt động tại:
🔗 **http://127.0.0.1:8000/v1/audio/speech**

Có thể tích hợp ngay vào bất kỳ thư viện OpenAI SDK, Pipecat, LiveKit nào bằng cách trỏ `base_url="http://127.0.0.1:8000/v1"`.

---

## 3. Chạy qua Python SDK
Chạy script thử nghiệm nhanh:
```powershell
.venv\Scripts\python.exe test_infer.py
```

Ví dụ code Python:
```python
import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from vieneu import Vieneu

vieneu = Vieneu()

# Tạo giọng đọc với tag cảm xúc [cười], [thở dài], [hắng giọng]
audio = vieneu.infer(
    "[cười] Xin chào các bạn! Mình đang trải nghiệm giọng đọc tiếng Việt siêu tự nhiên của VieNeu-TTS.", 
    voice="Phạm Tuyên"
)

vieneu.save(audio, "output.wav")
print("Đã tạo file output.wav thành công!")
```
