import requests
import os

def test_api():
    base_url = "http://localhost:5000"
    print("Testing SRT to Audio Converter API...")
    
    # Health check
    print("\n1. Health check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            return
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return
    
    # Text to audio
    print("\n2. Text to audio...")
    try:
        data = {"text": "Hello, this is a test message.", "rate": 150}
        response = requests.post(f"{base_url}/api/convert-text", json=data)
        if response.status_code == 200:
            with open("test_audio.wav", "wb") as f:
                f.write(response.content)
            print("✅ Text conversion successful")
        else:
            print(f"❌ Text conversion failed: {response.text}")
    except Exception as e:
        print(f"❌ Text conversion error: {e}")
    
    # SRT file conversion
    print("\n3. SRT file conversion...")
    if os.path.exists("test/test.srt"):
        try:
            with open("test/test.srt", 'rb') as f:
                files = {'srt_file': f}
                data = {'rate': '150', 'voice_idx': '0'}
                response = requests.post(f"{base_url}/api/convert-srt", files=files, data=data)
            
            if response.status_code == 200:
                with open("test_srt_audio.wav", "wb") as f:
                    f.write(response.content)
                print("✅ SRT conversion successful")
            else:
                print(f"❌ SRT conversion failed: {response.text}")
        except Exception as e:
            print(f"❌ SRT conversion error: {e}")
    else:
        print("⚠️ SRT test file not found")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_api()
