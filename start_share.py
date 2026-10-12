import os
import re
import subprocess
import sys
import time
import webbrowser

# Đảm bảo UTF-8
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CLOUDFLARED_EXE = os.path.join(ROOT_DIR, "cloudflared.exe")

# Thêm src vào sys.path nếu cần
src_dir = os.path.join(ROOT_DIR, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from apps import gradio_main

def main():
    print("==================================================")
    print("   KHỞI ĐỘNG VIENEU-TTS + PUBLIC SHARE LINK")
    print("==================================================")
    print("🚀 Đang khởi động Gradio Web UI...")

    # 1. Khởi động Gradio trực tiếp (không khóa thread ngay để thiết lập tunnel)
    gradio_main.demo.queue().launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        prevent_thread_lock=True
    )
    print("✅ Web UI đã sẵn sàng tại http://127.0.0.1:7860!")

    # 2. Khởi động Cloudflare Tunnel
    print("\n🌐 Đang thiết lập đường hầm Cloudflare Tunnel (HTTPS công khai)...")
    tunnel_proc = subprocess.Popen(
        [CLOUDFLARED_EXE, "tunnel", "--protocol", "http2", "--url", "http://127.0.0.1:7860"],
        cwd=ROOT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    public_url = None
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

    for line in tunnel_proc.stdout:
        match = url_pattern.search(line)
        if match:
            public_url = match.group(0)
            break

    if public_url:
        with open(os.path.join(ROOT_DIR, "public_url.txt"), "w", encoding="utf-8") as f:
            f.write(public_url)

        print("\n" + "=" * 60)
        print("🎉 TRIỂN KHAI THÀNH CÔNG! LINK TRUY CẬP CÔNG KHAI:")
        print(f"👉 {public_url}")
        print("=" * 60)
        print("📱 Bạn có thể mở link trên từ MỌI TRÌNH DUYỆT, ĐIỆN THOẠI hoặc MÁY TÍNH KHÁC.")
        print("💻 Link nội bộ máy này: http://127.0.0.1:7860")
        print("⚠️  Nhấn Ctrl+C để dừng chương trình.\n")

        try:
            webbrowser.open(public_url)
        except Exception:
            pass
    else:
        print("⚠️ Không lấy được link public tự động. Bạn vẫn có thể truy cập http://127.0.0.1:7860")

    # Giữ server chạy vĩnh viễn cho đến khi người dùng tắt
    try:
        gradio_main.demo.block_thread()
    except (KeyboardInterrupt, SystemExit):
        print("\nĐang tắt máy chủ...")
    finally:
        tunnel_proc.terminate()

if __name__ == "__main__":
    main()
