import os
import sys

# Thêm src vào sys.path để import vieneu
root_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(root_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from apps import gradio_main

# Expose demo for Hugging Face Spaces
demo = gradio_main.demo

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    demo.queue().launch(server_name="0.0.0.0", server_port=port, share=False)
