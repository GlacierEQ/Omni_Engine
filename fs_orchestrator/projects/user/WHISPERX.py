#!/usr/bin/env python3
# WHISPERX v1.0 - Forensic Audio/Video Transcription
import argparse, json, os
from pathlib import Path
import whisperx
from datetime import datetime

class WhisperX:
    def __init__(self):
        self.model = whisperx.load_model("large-v2", device="cpu")
        self.align_model, self.metadata = whisperx.load_align_model(language_code="en", device="cpu")
    
    def transcribe(self, audio_file):
        audio = whisperx.load_audio(str(audio_file))
        result = self.model.transcribe(audio, batch_size=16)
        result = whisperx.align(result["segments"], self.align_model, self.metadata, audio, "en", device="cpu")
        
        exhibit = {
            'exhibit_id': f"TX-{audio_file.stem}-{datetime.now().strftime('%Y%m%d')}",
            'source': str(audio_file),
            'segments': result["segments"],
            'duration': len(audio),
            'transcribed': datetime.utcnow().isoformat()
        }
        
        output_file = audio_file.parent / f"{exhibit['exhibit_id']}.json"
        with open(output_file, 'w') as f:
            json.dump(exhibit, f, indent=2)
        return exhibit

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WHISPERX - Audio Exhibit Transcription')
    parser.add_argument('audio', nargs='+')
    args = parser.parse_args()
    
    wx = WhisperX()
    for audio in args.audio:
        print(json.dumps(wx.transcribe(Path(audio)), indent=2))
