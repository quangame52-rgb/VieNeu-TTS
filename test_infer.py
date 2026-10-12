import sys
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from vieneu import Vieneu

def main():
    print("🚀 Đang khởi tạo VieNeu-TTS v3 Turbo...")
    vieneu = Vieneu()  # CPU ONNX runtime (torch-free)

    # 1. Danh sách giọng mẫu có sẵn
    voices = vieneu.list_preset_voices()
    print(f"🎙️  Tìm thấy {len(voices)} giọng mẫu:")
    for label, voice_id in voices[:10]:
        print(f"   - {label} ({voice_id})")
    print("   ... và nhiều giọng khác.")

    # 2. Thử nghiệm đọc văn bản với tag cảm xúc
    text = "[cười] Xin chào! VieNeu-TTS đã được triển khai và hoạt động hoàn hảo trên máy của bạn."
    print(f"\n🔊 Đang tạo giọng nói cho câu:\n   \"{text}\"")

    t0 = time.time()
    audio = vieneu.infer(text, voice="Phạm Tuyên")
    elapsed = time.time() - t0

    sample_rate = 48000
    duration = len(audio) / sample_rate
    rtf = elapsed / duration if duration > 0 else 0

    output_file = "output_chao_mung.wav"
    vieneu.save(audio, output_file)

    print(f"\n✅ Đã lưu file: {output_file}")
    print(f"⏱️  Thời gian xử lý: {elapsed:.2f}s | Độ dài audio: {duration:.2f}s | RTF: {rtf:.3f}")

if __name__ == "__main__":
    main()
