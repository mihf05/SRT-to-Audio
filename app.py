from flask import Flask, request, jsonify, send_file
import os
import logging
from werkzeug.utils import secure_filename
from subtitle_to_audio import generate_audio

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'srt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'SRT to Audio Converter'})

@app.route('/api/convert-srt', methods=['POST'])
def convert_srt_to_audio():
    try:
        if 'srt_file' not in request.files:
            return jsonify({'error': 'No SRT file uploaded'}), 400
        
        file = request.files['srt_file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid SRT file'}), 400
        
        rate = request.form.get('rate', 150, type=int)
        voice_idx = request.form.get('voice_idx', 0, type=int)
        
        if not (50 <= rate <= 300) or voice_idx not in [0, 1]:
            return jsonify({'error': 'Invalid parameters'}), 400
        
        # Save temp file
        temp_srt = f"temp_{os.urandom(4).hex()}.srt"
        file.save(temp_srt)
        
        try:
            # Generate audio
            output_path = generate_audio(temp_srt, rate=rate, voice_idx=voice_idx)
            
            response = send_file(
                output_path,
                as_attachment=True,
                download_name=f'dubbed_{os.path.splitext(file.filename)[0]}.wav'
            )
            
            # Cleanup
            @response.call_on_close
            def cleanup():
                for f in [temp_srt, output_path]:
                    if os.path.exists(f):
                        try:
                            os.remove(f)
                        except:
                            pass
            
            return response
            
        except Exception as e:
            if os.path.exists(temp_srt):
                os.remove(temp_srt)
            raise
            
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': 'Server error'}), 500

@app.route('/api/convert-text', methods=['POST'])
def convert_text_to_audio():
    try:
        data = request.get_json()
        if not data or not data.get('text'):
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text'].strip()
        rate = data.get('rate', 150)
        voice_idx = data.get('voice_idx', 0)
        
        if not (50 <= rate <= 300) or voice_idx not in [0, 1]:
            return jsonify({'error': 'Invalid parameters'}), 400
        
        import pyttsx3
        output_file = f"text_{os.urandom(4).hex()}.wav"
        
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        voices = engine.getProperty('voices')
        if voices and len(voices) > voice_idx:
            engine.setProperty('voice', voices[voice_idx].id)
        
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        
        response = send_file(output_file, as_attachment=True, download_name='text_audio.wav')
        
        @response.call_on_close
        def cleanup():
            if os.path.exists(output_file):
                try:
                    os.remove(output_file)
                except:
                    pass
        
        return response
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
