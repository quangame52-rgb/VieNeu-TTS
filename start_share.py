import os
import re
import subprocess
import sys
import time
import urllib.request

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE = os.path.join(ROOT_DIR, ".venv", "Scripts", "python.exe")
CLOUDFLARED_EXE = os.path.join(ROOT_DIR, "cloudflared.exe")

def wait_for_server(url="http://127.0.0.1:7860", timeout=60):
    print("⏳ Đang chờ máy chủ Web UI khởi động...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if resp.status == 200:
                    print("✅ Web UI đã sẵn sàng tại http://127.0.0.1:7860!")
                    return True
        except Exception:
            time.sleep(1)
    return False

def main():
    print("==================================================")
    print("   KHỞI ĐỘNG VIENEU-TTS + PUBLIC SHARE LINK")
    print("==================================================")

    # 1. Khởi động Web UI
    print("🚀 Đang khởi động Gradio Web UI...")
    web_proc = subprocess.Popen(
        [PYTHON_EXE, os.path.join(ROOT_DIR, "apps", "gradio_main.py")],
        cwd=ROOT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if not wait_for_server():
        print("❌ Lỗi: Web UI không khởi động được trong 60 giây.")
        web_proc.terminate()
        sys.exit(1)

    # 2. Khởi động Cloudflare Tunnel để tạo link Public
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

        # Tự động mở trình duyệt
        try:
            import webbrowser
            webbrowser.open(public_url)
        except Exception:
            pass
    else:
        print("⚠️ Không lấy được link public tự động. Kiểm tra cloudflared.")

    try:
        while True:
            time.sleep(1)
            if web_proc.poll() is not None:
                print("Web UI đã dừng.")
                break
            if tunnel_proc.poll() is not None:
                print("Tunnel đã dừng.")
                break
    except KeyboardInterrupt:
        print("\nĐang tắt máy chủ...")
    finally:
        web_proc.terminate()
        tunnel_proc.terminate()

if __name__ == "__main__":
    main()
