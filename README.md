# SRT to Audio Converter

## Overview
This system converts SRT subtitle files to audio using text-to-speech technology. It provides a REST API that accepts SRT files and returns synchronized audio files with proper timing.

## Architecture
The system consists of two main components:
1. **Core Audio Generator** (`subtitle_to_audio.py`): Handles SRT parsing, text-to-speech conversion, and audio timing synchronization
2. **Flask API Wrapper** (`app.py`): Provides RESTful endpoints for file upload, processing, and audio delivery

The system parses SRT timestamps, converts each subtitle text to audio using pyttsx3, and creates silence gaps between audio segments to maintain proper timing synchronization.

## Features
- Parse SRT subtitle files with timestamp extraction
- Convert text to speech with configurable voice and speed
- Maintain proper timing synchronization with silence gaps
- RESTful API with file upload support
- Error handling and logging
- Health check endpoint
- Support for both file upload and direct text conversion

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- Windows (for pyttsx3 voice support)

### Installation
1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Test the API:
   ```bash
   python test_simple.py
   ```

5. The API will be available at: `http://localhost:5000`

## API Endpoints

### 1. Health Check
```
GET /api/health
```
Returns service status and version information.

**Response:**
```json
{
  "status": "healthy",
  "service": "SRT to Audio Converter",
  "version": "1.0.0"
}
```

### 2. Convert SRT File to Audio
```
POST /api/convert-srt
```
Upload an SRT file and convert it to synchronized audio.

**Parameters:**
- `srt_file` (file, required): SRT subtitle file
- `rate` (form field, optional): Speech rate in WPM (50-300, default: 150)
- `voice_idx` (form field, optional): Voice selection (0 or 1, default: 0)

**Response:** WAV audio file download

**Example using curl:**
```bash
curl -X POST \
  -F "srt_file=@test/test.srt" \
  -F "rate=180" \
  -F "voice_idx=0" \
  http://localhost:5000/api/convert-srt \
  --output dubbed_audio.wav
```

### 3. Convert Text to Audio
```
POST /api/convert-text
```
Convert raw text to audio (simple TTS without timing).

**Request Body:**
```json
{
  "text": "Hello, this is a test message",
  "rate": 150,
  "voice_idx": 0
}
```

**Response:** WAV audio file download

**Example using curl:**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world", "rate":180}' \
  http://localhost:5000/api/convert-text \
  --output text_audio.wav
```

## Testing

### Using the Sample File
Test with the provided sample SRT file:
```bash
curl -X POST \
  -F "srt_file=@test/test.srt" \
  http://localhost:5000/api/convert-srt \
  --output sample_output.wav
```

### Using Postman
1. Import the collection directly from this link: [SRT to Audio Converter Collection](https://www.postman.com/navigation-engineer-74802791/srt-to-audio/collection/wawjcty/srt-to-audio-converter?action=share&creator=31974666)

2. Or import the local collection file:
  ```bash
  postman_collection.json
  ```

3. Manual setup:
  - Method: POST
  - URL: `http://localhost:5000/api/convert-srt`
  - Body: form-data
    - Key: `srt_file`, Type: File, Value: [select your SRT file]
    - Key: `rate`, Type: Text, Value: `150`
    - Key: `voice_idx`, Type: Text, Value: `0`

## Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `PORT`: Server port (default: 5000)
- `MAX_FILE_SIZE`: Maximum upload file size in bytes

### Voice Configuration
- Voice 0: Default system voice (usually female)
- Voice 1: Alternative system voice (usually male)
- Rate: 50-300 words per minute

## Error Handling
The API includes comprehensive error handling:
- File validation (SRT files only)
- Parameter validation (rate, voice index)
- File size limits (16MB maximum)
- Proper HTTP status codes
- Detailed error messages

## Challenges Faced and Solutions

### 1. Timing Synchronization
**Challenge:** Maintaining accurate timing between subtitle start times and audio playback.
**Solution:** Implemented precise millisecond calculation and silence gap insertion between audio segments.

### 2. Temporary File Management
**Challenge:** Managing temporary audio files during processing without conflicts.
**Solution:** Used Python's tempfile module with automatic cleanup to handle temporary files safely.

### 3. Cross-Platform TTS
**Challenge:** pyttsx3 behavior varies across operating systems.
**Solution:** Focused on Windows compatibility and added voice validation with fallback options.

## File Structure
```
├── app.py                 # Flask API application (simplified)
├── subtitle_to_audio.py   # Core SRT processing and TTS
├── requirements.txt       # Python dependencies (minimal)
├── test_simple.py         # Simple test script
├── README.md             # This file
├── test/
│   └── test.srt          # Sample SRT file for testing
└── Dockerfile            # Docker configuration (optional)
```

## Demo Results
- ✅ All API endpoints tested successfully
- ✅ SRT file conversion working with proper timing synchronization
- ✅ Stress test: Multiple requests handled successfully  
- ✅ File handling optimized for Windows environments
- ✅ Clean, production-ready code structure

## Docker Support (Optional)
Create a Docker container:
```bash
docker build -t srt-to-audio .
docker run -p 5000:5000 srt-to-audio
```

## Future Enhancements
- Support for additional subtitle formats (ASS, VTT)
- Multiple language TTS support
- Audio quality options (bitrate, format)
- Batch processing capabilities
- Web interface for easier testing

