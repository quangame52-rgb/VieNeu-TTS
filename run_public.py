import os
import sys

# Đảm bảo UTF-8
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

os.environ["GRADIO_SHARE"] = "true"
os.environ["GRADIO_SERVER_NAME"] = "0.0.0.0"

from apps import gradio_main

if __name__ == "__main__":
    print("🚀 Đang khởi động VieNeu-TTS với Public Share...")
    gradio_main.main()
